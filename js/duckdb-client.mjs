import * as duckdb from "https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm@1.32.0/+esm";

let databasePromise;
let nextFileId = 0;

async function getDatabase() {
    if (!databasePromise) {
        databasePromise = (async () => {
            const bundle = await duckdb.selectBundle(duckdb.getJsDelivrBundles());
            const workerUrl = URL.createObjectURL(
                new Blob([`importScripts("${bundle.mainWorker}");`], {
                    type: "text/javascript"
                })
            );
            const worker = new Worker(workerUrl);
            const database = new duckdb.AsyncDuckDB(new duckdb.ConsoleLogger(), worker);

            try {
                await database.instantiate(bundle.mainModule, bundle.pthreadWorker);
            } catch (error) {
                worker.terminate();
                throw error;
            } finally {
                URL.revokeObjectURL(workerUrl);
            }

            return { database, connection: await database.connect() };
        })().catch(error => {
            databasePromise = null;
            throw error;
        });
    }

    return databasePromise;
}

export async function queryParquetBuffers(files) {
    if (files.length === 0) return new Map();

    const { database, connection } = await getDatabase();
    const registeredFiles = [];

    try {
        for (const { year, buffer } of files) {
            if (!Number.isInteger(year)) throw new TypeError(`Invalid Parquet year: ${year}`);
            const fileName = `year_${nextFileId++}.parquet`;
            await database.registerFileBuffer(fileName, new Uint8Array(buffer));
            registeredFiles.push({ year, fileName });
        }

        const query = registeredFiles.map(({ year, fileName }) =>
            `SELECT *, ${year} AS "__source_year" FROM read_parquet('${fileName}')`
        ).join("\nUNION ALL\n");
        const table = await connection.query(query);
        const rowsByYear = new Map();

        for (const arrowRow of table.toArray()) {
            const row = arrowRow.toJSON();
            const year = Number(row.__source_year);
            delete row.__source_year;
            if (!rowsByYear.has(year)) rowsByYear.set(year, []);
            rowsByYear.get(year).push(row);
        }

        return rowsByYear;
    } finally {
        for (const { fileName } of registeredFiles) {
            await database.dropFile(fileName);
        }
    }
}

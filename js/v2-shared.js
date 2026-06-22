/**
 * v2-shared.js
 * Shared utilities for version 2 pages with IndexedDB caching and smart per-year data loading
 * 
 * Key Features:
 * - IndexedDB caching with last_updated timestamp tracking
 * - Smart delta fetching (only fetch missing/new data since last visit)
 * - Per-ticker per-year file loading from data/tickers/${SYMBOL}/${SYMBOL}-${YEAR}.csv
 * - Uses tickers_index.json metadata for intelligent loading decisions
 * - Date deduplication to handle overlapping cached + fresh data
 */

// =============================
// Date Helper Functions
// =============================

/**
 * Format Date object as YYYY-MM-DD
 */
function formatDateToYMD(d) {
    if (!d || isNaN(d)) return null;
    const yyyy = d.getFullYear();
    const mm = String(d.getMonth() + 1).padStart(2, '0');
    const dd = String(d.getDate()).padStart(2, '0');
    return `${yyyy}-${mm}-${dd}`;
}

/**
 * Parse a date-like string into a local Date (avoid timezone shifts when parsing ISO YYYY-MM-DD)
 */
function parseDateStringAsLocal(s) {
    if (!s) return null;
    if (s instanceof Date) return s;
    const str = String(s).trim();
    
    // YYYY-MM-DD
    let m = str.match(/^(\d{4})-(\d{1,2})-(\d{1,2})$/);
    if (m) return new Date(Number(m[1]), Number(m[2]) - 1, Number(m[3]));
    
    // MM/DD/YYYY or M/D/YYYY
    m = str.match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/);
    if (m) return new Date(Number(m[3]), Number(m[1]) - 1, Number(m[2]));
    
    // Has time/timezone component - parse as UTC then extract the America/New_York calendar date
    const parsed = new Date(str.replace(' ', 'T'));
    if (isNaN(parsed)) return null;
    try {
        const etParts = new Intl.DateTimeFormat('en-US', {
            timeZone: 'America/New_York',
            year: 'numeric', month: '2-digit', day: '2-digit'
        }).formatToParts(parsed);
        const year  = Number(etParts.find(p => p.type === 'year').value);
        const month = Number(etParts.find(p => p.type === 'month').value);
        const day   = Number(etParts.find(p => p.type === 'day').value);
        return new Date(year, month - 1, day);
    } catch (_) {
        return new Date(parsed.getFullYear(), parsed.getMonth(), parsed.getDate());
    }
}

/**
 * Convert a date-like string to YYYY-MM-DD using local date parts
 */
function toYMDFromString(s) {
    const d = parseDateStringAsLocal(s);
    return d ? formatDateToYMD(d) : s;
}

/**
 * Normalize a row's date value into a stable YYYY-MM-DD string.
 * Handles Date objects, ISO strings, and values already stored in Date_add.
 */
function normalizeDateKey(row) {
    if (!row) return '';

    const rawDate = row.Date_add || row.Date || row.date || '';
    if (!rawDate) return '';

    if (rawDate instanceof Date) {
        return formatDateToYMD(rawDate);
    }

    if (typeof rawDate === 'string') {
        return toYMDFromString(rawDate);
    }

    return String(rawDate);
}

/**
 * Deduplicate rows by calendar date (keep only the latest entry per date)
 */
function dedupeRowsByDate(rows) {
    if (!rows || rows.length === 0) return [];
    
    // Group by date string
    const byDate = {};
    rows.forEach(row => {
        const dateKey = normalizeDateKey(row);
        if (!dateKey) return;
        // Keep the last occurrence (assumes rows are in chronological order or we want latest)
        byDate[dateKey] = row;
    });
    
    // Return sorted by date
    return Object.values(byDate).sort((a, b) => {
        const da = normalizeDateKey(a);
        const db = normalizeDateKey(b);
        return String(da).localeCompare(String(db));
    });
}

// =============================
// IndexedDB Helpers
// =============================

const DB_NAME = 'stockmarket-v2-cache';
const DB_VERSION = 1;
const STORE_NAME = 'ticker-data';

/**
 * Open IndexedDB connection
 */
function openDB() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open(DB_NAME, DB_VERSION);
        
        request.onerror = () => reject(request.error);
        request.onsuccess = () => resolve(request.result);
        
        request.onupgradeneeded = (event) => {
            const db = event.target.result;
            
            // Create object store if it doesn't exist
            if (!db.objectStoreNames.contains(STORE_NAME)) {
                const store = db.createObjectStore(STORE_NAME, { keyPath: 'id' });
                store.createIndex('ticker', 'ticker', { unique: false });
                store.createIndex('year', 'year', { unique: false });
                console.log('[IDB] Created object store:', STORE_NAME);
            }
        };
    });
}

/**
 * Get data from IndexedDB by key
 */
async function idbGet(key) {
    try {
        const db = await openDB();
        return new Promise((resolve, reject) => {
            const tx = db.transaction(STORE_NAME, 'readonly');
            const store = tx.objectStore(STORE_NAME);
            const request = store.get(key);
            
            request.onsuccess = () => {
                console.log(`[IDB] Get ${key}:`, request.result ? 'HIT' : 'MISS');
                resolve(request.result);
            };
            request.onerror = () => {
                console.error(`[IDB] Get ${key} error:`, request.error);
                reject(request.error);
            };
        });
    } catch (err) {
        console.error('[IDB] openDB failed:', err);
        return null;
    }
}

/**
 * Put data into IndexedDB
 */
async function idbPut(data) {
    try {
        const db = await openDB();
        return new Promise((resolve, reject) => {
            const tx = db.transaction(STORE_NAME, 'readwrite');
            const store = tx.objectStore(STORE_NAME);
            const request = store.put(data);
            
            request.onsuccess = () => {
                console.log(`[IDB] Put ${data.id}: SUCCESS (${data.rows?.length || 0} rows)`);
                resolve(request.result);
            };
            request.onerror = () => {
                console.error(`[IDB] Put ${data.id} error:`, request.error);
                reject(request.error);
            };
        });
    } catch (err) {
        console.error('[IDB] openDB failed:', err);
        throw err;
    }
}

/**
 * Delete data from IndexedDB by key
 */
async function idbDelete(key) {
    try {
        const db = await openDB();
        return new Promise((resolve, reject) => {
            const tx = db.transaction(STORE_NAME, 'readwrite');
            const store = tx.objectStore(STORE_NAME);
            const request = store.delete(key);
            
            request.onsuccess = () => {
                console.log(`[IDB] Delete ${key}: SUCCESS`);
                resolve();
            };
            request.onerror = () => {
                console.error(`[IDB] Delete ${key} error:`, request.error);
                reject(request.error);
            };
        });
    } catch (err) {
        console.error('[IDB] openDB failed:', err);
    }
}

/**
 * Get all cached tickers for a specific ticker symbol
 */
async function idbGetTickerYears(ticker) {
    try {
        const db = await openDB();
        return new Promise((resolve, reject) => {
            const tx = db.transaction(STORE_NAME, 'readonly');
            const store = tx.objectStore(STORE_NAME);
            const index = store.index('ticker');
            const request = index.getAll(ticker);
            
            request.onsuccess = () => {
                console.log(`[IDB] Get all years for ${ticker}:`, request.result.length, 'entries');
                resolve(request.result);
            };
            request.onerror = () => reject(request.error);
        });
    } catch (err) {
        console.error('[IDB] openDB failed:', err);
        return [];
    }
}

// =============================
// Tickers Index Loader
// =============================

let cachedTickersIndex = null;

/**
 * Load tickers_index.json with metadata about available files
 */
async function loadTickersIndex() {
    if (cachedTickersIndex) {
        console.log('[Index] Using cached tickers_index.json');
        return cachedTickersIndex;
    }
    
    try {
        const res = await fetch('../data/tickers/tickers_index.json');
        if (!res.ok) throw new Error(`Failed to fetch index: ${res.status}`);
        
        cachedTickersIndex = await res.json();
        console.log('[Index] Loaded tickers_index.json:', Object.keys(cachedTickersIndex).length, 'tickers');
        return cachedTickersIndex;
    } catch (err) {
        console.error('[Index] Failed to load tickers_index.json:', err);
        return null;
    }
}

/**
 * Get list of ticker symbols from index
 */
async function getTickerSymbols() {
    const index = await loadTickersIndex();
    if (!index) return [];
    return Object.keys(index).sort((a, b) => a.localeCompare(b));
}

/**
 * Get metadata for a specific ticker
 */
async function getTickerMetadata(ticker) {
    const index = await loadTickersIndex();
    return index ? index[ticker] : null;
}

// =============================
// Smart Data Loading with IDB Caching
// =============================

/**
 * Parse CSV text into row objects
 * Uses simple split-based parsing (or can integrate PapaParse if available)
 */
function parseCSV(text, headers = null) {
    const lines = text.split('\n').filter(l => l.trim());
    if (lines.length === 0) return [];
    
    const headerLine = headers || lines[0].split(',').map(h => h.trim());
    const dataLines = headers ? lines : lines.slice(1);
    
    return dataLines.map(line => {
        const values = line.split(',');
        const obj = {};
        headerLine.forEach((h, i) => {
            obj[h] = values[i]?.trim() || '';
        });
        return obj;
    });
}

/**
 * Fetch and parse a single year CSV file
 */
async function fetchYearCSV(ticker, year) {
    const path = `../data/tickers/${ticker}/${ticker}-${year}.csv`;
    console.log(`[Fetch] Requesting ${path}`);
    
    try {
        const res = await fetch(path);
        if (!res.ok) {
            console.warn(`[Fetch] ${path} not found (${res.status})`);
            return null;
        }
        
        const text = await res.text();
        
        // Use PapaParse if available, otherwise fallback to simple parser
        let rows;
        if (typeof Papa !== 'undefined') {
            const parsed = Papa.parse(text, { header: true, dynamicTyping: false, skipEmptyLines: true });
            rows = parsed.data;
        } else {
            rows = parseCSV(text);
        }
        
        // Normalize date field and essential columns
        rows = rows.map(row => {
            const rawDate = row['Date_add'] || row['Date'] || row['date'];
            const Date_add = rawDate ? toYMDFromString(rawDate) : null;
            
            return {
                Date_add: Date_add,
                Symbol: String(row['Symbol'] || row['symbol'] || ticker).trim(),
                Close: row['Close'] != null ? Number(row['Close']) : null,
                Low: row['Low'] != null ? Number(row['Low']) : null,
                Previous_Close: row['Previous_Close'] != null ? Number(row['Previous_Close']) : null,
                Open: row['Open'] != null ? Number(row['Open']) : null,
                High: row['High'] != null ? Number(row['High']) : null,
                Volume: row['Volume'] != null ? Number(row['Volume']) : null,
                // Include all other fields as-is
                ...row
            };
        }).filter(r => r.Date_add); // Filter out rows with no valid date
        
        console.log(`[Fetch] Parsed ${rows.length} rows from ${path}`);
        return rows;
    } catch (err) {
        console.error(`[Fetch] Error fetching ${path}:`, err);
        return null;
    }
}

/**
 * Load ticker data with smart caching:
 * 1. Check IDB for cached years
 * 2. Compare cached last_updated with server metadata
 * 3. Fetch only missing/stale years
 * 4. For current year, fetch delta (rows after last cached date)
 * 5. Merge and deduplicate
 * 6. Update IDB cache
 * 
 * @param {string} ticker - Ticker symbol (e.g., 'AAPL')
 * @param {Array<number>} years - Years to load (e.g., [2023, 2024, 2025])
 * @returns {Promise<Array>} - Array of row objects sorted by date
 */
async function loadTickerData(ticker, years) {
    console.log(`[Loader] Loading ${ticker} for years:`, years);
    
    // Get server metadata from tickers_index.json
    const metadata = await getTickerMetadata(ticker);
    if (!metadata) {
        console.error(`[Loader] No metadata found for ${ticker}`);
        return [];
    }
    
    const allRows = [];
    const currentYear = new Date().getFullYear();
    
    for (const year of years) {
        const cacheKey = `${ticker}::${year}`;
        const serverFileInfo = metadata.files?.[String(year)];
        
        if (!serverFileInfo) {
            console.warn(`[Loader] No server file info for ${ticker} year ${year}`);
            continue;
        }
        
        // Check cache
        const cached = await idbGet(cacheKey);
        
        // Determine if we need to fetch with smart validation
        let shouldFetch = false;
        let deltaFetch = false;
        let afterDate = null;
        let cacheIsValid = false;
        
        if (!cached) {
            // Cache miss - fetch entire year
            console.log(`[Loader] Cache MISS for ${cacheKey}`);
            shouldFetch = true;
        } else {
            // Cache exists - validate against server metadata
            // Compare last_updated timestamp
            const lastUpdatedMatch = cached.last_updated === serverFileInfo.last_updated;
            
            // Validate date ranges if metadata is available
            let dateRangeMatch = true;
            if (serverFileInfo.min_date && serverFileInfo.max_date && cached.rows && cached.rows.length > 0) {
                // Get date range from cached data
                const cachedDates = cached.rows.map(r => r.Date_add).filter(Boolean).sort();
                if (cachedDates.length > 0) {
                    const cachedMinDate = cachedDates[0];
                    const cachedMaxDate = cachedDates[cachedDates.length - 1];
                    
                    // Compare date ranges
                    dateRangeMatch = (cachedMinDate === serverFileInfo.min_date && 
                                     cachedMaxDate === serverFileInfo.max_date);
                    
                    if (!dateRangeMatch) {
                        console.log(`[Loader] Date range mismatch for ${cacheKey}`);
                        console.log(`  Index: ${serverFileInfo.min_date} to ${serverFileInfo.max_date}`);
                        console.log(`  Cache: ${cachedMinDate} to ${cachedMaxDate}`);
                    }
                }
            }
            
            // Cache is valid only if both timestamp and date ranges match
            if (lastUpdatedMatch && dateRangeMatch) {
                cacheIsValid = true;
                console.log(`✓ Cache VALID for ${cacheKey} (${cached.rows.length} rows, dates verified)`);
                allRows.push(...cached.rows);
                continue;
            } else if (!lastUpdatedMatch) {
                // Cache stale - server has newer data
                console.log(`✗ Cache STALE for ${cacheKey} (cached: ${cached.last_updated}, server: ${serverFileInfo.last_updated})`);
                
                if (year === currentYear) {
                    // For current year, fetch delta (rows after last cached date)
                    deltaFetch = true;
                    shouldFetch = true;
                    
                    // Find the max date in cached rows
                    const cachedDates = cached.rows.map(r => r.Date_add).filter(Boolean).sort();
                    afterDate = cachedDates[cachedDates.length - 1];
                    console.log(`[Loader] Delta fetch for ${cacheKey} after ${afterDate}`);
                } else {
                    // For historical years, refetch entire file (shouldn't change often)
                    shouldFetch = true;
                }
            } else {
                // Date range mismatch - invalidate cache and refetch
                console.log(`✗ Cache INVALID for ${cacheKey}: date range mismatch`);
                shouldFetch = true;
                
                // Delete stale cache
                try {
                    await idbDelete(cacheKey);
                    console.log(`[Loader] Deleted stale cache for ${cacheKey}`);
                } catch (err) {
                    console.warn(`[Loader] Failed to delete stale cache for ${cacheKey}:`, err);
                }
            }
        }
        
        // Fetch from server if needed
        if (shouldFetch) {
            const freshRows = await fetchYearCSV(ticker, year);
            
            if (!freshRows) {
                // Fetch failed, use cached data if available
                if (cached) {
                    console.warn(`[Loader] Fetch failed for ${cacheKey}, using cached data`);
                    allRows.push(...cached.rows);
                }
                continue;
            }
            
            // Merge with cached if doing delta fetch
            let finalRows = freshRows;
            if (deltaFetch && cached && afterDate) {
                // Filter fresh rows to only those after the last cached date
                const newRows = freshRows.filter(r => r.Date_add > afterDate);
                console.log(`[Loader] Delta: ${newRows.length} new rows after ${afterDate}`);
                
                // Merge cached + new rows and deduplicate
                finalRows = dedupeRowsByDate([...cached.rows, ...newRows]);
                console.log(`[Loader] Merged: ${finalRows.length} total rows after deduplication`);
            }
            
            // Update cache
            try {
                await idbPut({
                    id: cacheKey,
                    ticker: ticker,
                    year: year,
                    last_updated: serverFileInfo.last_updated,
                    rows: finalRows,
                    cached_at: new Date().toISOString()
                });
            } catch (err) {
                console.error(`[Loader] Failed to cache ${cacheKey}:`, err);
            }
            
            allRows.push(...finalRows);
        }
    }
    
    // Final deduplication and sort
    const dedupedRows = dedupeRowsByDate(allRows);
    console.log(`[Loader] Final result for ${ticker}: ${dedupedRows.length} rows`);
    
    return dedupedRows;
}

function normalizePeriod(period) {
    if (!period && period !== 0) return 'ytd';
    const raw = String(period).trim().toLowerCase();
    if (raw === 'all') return 'all';
    if (raw === 'ytd') return 'ytd';
    if (raw === '1y' || raw === '1') return '1y';
    const match = raw.match(/^(\d+)\s*y$/);
    if (match) return `${match[1]}y`;
    const digits = raw.match(/^(\d+)$/);
    if (digits) return `${digits[1]}y`;
    console.warn(`[Loader] Unknown period format "${period}". Falling back to YTD.`);
    return 'ytd';
}

/**
 * Determine which years to load based on period selection
 * @param {string} period - 'ytd', '5y', '10y', '15y', '20y', or 'all'
 * @param {Array<number>} availableYears - Years available for the ticker
 * @returns {Array<number>} - Years to load
 */
function determineYearsToLoad(period, availableYears) {
    const normalized = normalizePeriod(period);
    const currentYear = new Date().getFullYear();

    if (!Array.isArray(availableYears) || availableYears.length === 0) {
        return [];
    }

    const sortedYears = [...availableYears].sort((a, b) => a - b);

    if (normalized === 'all') {
        return sortedYears;
    }

    if (normalized === 'ytd' || normalized === '1y') {
        const targetYear = normalized === 'ytd' ? currentYear : currentYear - 1;
        const years = sortedYears.filter(y => y >= targetYear);
        if (years.length > 0) return years;
        return [sortedYears[sortedYears.length - 1]];
    }

    const match = normalized.match(/^(\d+)y$/);
    if (match) {
        const yearsBack = Number(match[1]);
        const startYear = currentYear - yearsBack;
        const years = sortedYears.filter(y => y >= startYear);
        if (years.length > 0) return years;

        // Fallback: return the most recent years available
        const fallbackCount = Math.min(yearsBack + 1, sortedYears.length);
        return sortedYears.slice(-fallbackCount);
    }

    console.warn(`[Loader] Unable to resolve period "${period}". Using latest available year.`);
    return [sortedYears[sortedYears.length - 1]];
}

/**
 * Main entry point: Load ticker data for a given period
 * @param {string} ticker - Ticker symbol
 * @param {string} period - Period selection ('ytd', '5y', '10y', etc.)
 * @returns {Promise<Array>} - Filtered rows for the period
 */
async function loadTickerDataForPeriod(ticker, period) {
    const normalizedPeriod = normalizePeriod(period);
    console.log(`[Main] Loading ${ticker} for period ${period} (normalized: ${normalizedPeriod})`);
    
    // Get available years from metadata
    const metadata = await getTickerMetadata(ticker);
    if (!metadata || !metadata.years) {
        console.error(`[Main] No years available for ${ticker}`);
        return [];
    }
    
    // Determine which years to load
    const yearsToLoad = determineYearsToLoad(normalizedPeriod, metadata.years);
    console.log(`[Main] Years to load for ${ticker} ${normalizedPeriod}:`, yearsToLoad);
    
    if (!yearsToLoad || yearsToLoad.length === 0) {
        console.warn(`[Main] No matching years for ${ticker} and period ${normalizedPeriod}`);
        return [];
    }

    // Load data with smart caching
    const rows = await loadTickerData(ticker, yearsToLoad);
    
    // Apply additional date filtering if needed
    const currentDate = new Date();
    let startDate = null;

    if (normalizedPeriod === 'ytd') {
        startDate = new Date(currentDate.getFullYear(), 0, 1);
    } else if (normalizedPeriod === '1y') {
        startDate = new Date(currentDate);
        startDate.setFullYear(currentDate.getFullYear() - 1);
    } else if (normalizedPeriod !== 'all') {
        const match = normalizedPeriod.match(/^(\d+)y$/);
        if (match) {
            startDate = new Date(currentDate);
            startDate.setFullYear(currentDate.getFullYear() - Number(match[1]));
        }
    }
    
    if (startDate) {
        const startDateStr = formatDateToYMD(startDate);
        const endDateStr = formatDateToYMD(currentDate);
        
        return rows.filter(r => {
            const rawDate = r.Date_add || r.Date || r.date;
            if (!rawDate) return false;
            const normalizedDate = toYMDFromString(rawDate);
            return normalizedDate && normalizedDate >= startDateStr && normalizedDate <= endDateStr;
        });
    }
    
    return rows;
}

// =============================
// History Slider Component
// =============================

/**
 * Initialize a history slider component
 * @param {Object} config - Configuration object
 * @param {string} config.containerId - ID of container element
 * @param {Function} config.onChange - Callback when slider changes (receives period string like 'ytd', '5y')
 * @param {Function} config.onInput - Optional callback for real-time slider input (for live updates)
 * @param {number} config.initialValue - Initial slider value (0 for YTD)
 * @param {number} config.maxYears - Maximum years on slider (default: 25)
 * @returns {Object} - Slider control object with methods
 */
function initHistorySlider(config) {
    const {
        containerId,
        onChange,
        onInput,
        initialValue = 0,
        maxYears = 25
    } = config;
    
    const container = document.getElementById(containerId);
    if (!container) {
        console.error(`[v2-shared] Container #${containerId} not found for history slider`);
        return null;
    }
    
    // Create slider HTML
    container.innerHTML = `
        <div class="history-slider-component" style="text-align:center; margin:20px 0;">
            <label for="${containerId}-slider" class="slider-label" style="font-weight:bold; color:var(--blue); font-size:1.1em;">
                History: YTD
            </label>
            <div style="display:flex; align-items:center; gap:12px; justify-content:center; margin-top:8px;">
                <input 
                    id="${containerId}-slider" 
                    type="range" 
                    min="0" 
                    max="${maxYears}" 
                    value="${initialValue}" 
                    step="1" 
                    class="history-slider-input"
                    style="width:420px; cursor:pointer;"
                />
                <div class="slider-value-display" style="min-width:80px; color:var(--gray); font-weight:bold;">
                    YTD
                </div>
            </div>
            <div class="slider-help-text" style="font-size:0.85em; color:var(--gray); margin-top:6px;">
                Use the slider to select time period (YTD = current year only)
            </div>
        </div>
    `;
    
    const slider = container.querySelector('.history-slider-input');
    const valueDisplay = container.querySelector('.slider-value-display');
    const label = container.querySelector('.slider-label');
    
    // Convert slider value to period string
    function sliderValueToPeriod(val) {
        const numVal = Number(val);
        if (numVal === 0) return 'YTD';
        if (numVal === 1) return '1Y';
        if (numVal === 5) return '5Y';
        if (numVal === 10) return '10Y';
        if (numVal === 15) return '15Y';
        if (numVal === 20) return '20Y';
        // For other values, return generic format
        return `${numVal}Y`;
    }
    
    // Update display
    function updateDisplay(val) {
        const period = sliderValueToPeriod(val);
        const numVal = Number(val);
        
        if (numVal === 0) {
            valueDisplay.textContent = 'YTD';
            label.textContent = 'History: YTD';
        } else {
            valueDisplay.textContent = `${numVal}Y`;
            label.textContent = `History: ${numVal} year${numVal > 1 ? 's' : ''}`;
        }
        
        return period;
    }
    
    // Input event (real-time feedback as user drags)
    slider.addEventListener('input', function() {
        const period = updateDisplay(this.value);
        if (onInput) {
            onInput(period, Number(this.value));
        }
    });
    
    // Change event (when user releases slider)
    slider.addEventListener('change', function() {
        const period = updateDisplay(this.value);
        if (onChange) {
            onChange(period, Number(this.value));
        }
    });
    
    // Initialize display
    updateDisplay(initialValue);
    
    // Return control object
    return {
        getValue: () => Number(slider.value),
        getPeriod: () => sliderValueToPeriod(slider.value),
        setValue: (val) => {
            slider.value = val;
            updateDisplay(val);
        },
        setMax: (max) => {
            slider.max = max;
        },
        getMax: () => Number(slider.max),
        setMin: (min) => {
            slider.min = min;
        }
    };
}

/**
 * Create period buttons (legacy support - for pages that prefer buttons over slider)
 * @param {Object} config - Configuration object
 * @param {string} config.containerId - ID of container element
 * @param {Array<string>} config.periods - Array of period strings like ['YTD', '5Y', '10Y', '15Y', '20Y']
 * @param {Function} config.onChange - Callback when button clicked (receives period string)
 * @param {string} config.initialPeriod - Initially active period (default: 'YTD')
 * @returns {Object} - Button control object
 */
function createPeriodButtons(config) {
    const {
        containerId,
        periods = ['YTD', '5Y', '10Y', '15Y', '20Y'],
        onChange,
        initialPeriod = 'YTD'
    } = config;
    
    const container = document.getElementById(containerId);
    if (!container) {
        console.error(`[v2-shared] Container #${containerId} not found for period buttons`);
        return null;
    }
    
    container.innerHTML = '';
    container.className = 'period-controls';
    container.style.cssText = 'display:flex; justify-content:center; gap:10px; margin:20px 0; flex-wrap:wrap;';
    
    const buttons = {};
    
    periods.forEach(period => {
        const btn = document.createElement('button');
        btn.className = 'period-btn';
        btn.textContent = period;
        btn.style.cssText = `
            padding: 10px 20px;
            margin: 0 5px;
            background-color: var(--light-gray);
            border: 2px solid var(--blue);
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
            color: var(--blue);
            transition: all 0.2s;
        `;
        
        if (period === initialPeriod) {
            btn.classList.add('active');
            btn.style.backgroundColor = 'var(--blue)';
            btn.style.color = 'white';
        }
        
        btn.addEventListener('click', function() {
            // Remove active from all buttons
            Object.values(buttons).forEach(b => {
                b.classList.remove('active');
                b.style.backgroundColor = 'var(--light-gray)';
                b.style.color = 'var(--blue)';
            });
            
            // Set this button active
            this.classList.add('active');
            this.style.backgroundColor = 'var(--blue)';
            this.style.color = 'white';
            
            if (onChange) {
                onChange(period);
            }
        });
        
        // Hover effect
        btn.addEventListener('mouseenter', function() {
            if (!this.classList.contains('active')) {
                this.style.backgroundColor = 'var(--light-blue)';
            }
        });
        btn.addEventListener('mouseleave', function() {
            if (!this.classList.contains('active')) {
                this.style.backgroundColor = 'var(--light-gray)';
            }
        });
        
        container.appendChild(btn);
        buttons[period] = btn;
    });
    
    return {
        setActive: (period) => {
            Object.entries(buttons).forEach(([p, btn]) => {
                if (p === period) {
                    btn.classList.add('active');
                    btn.style.backgroundColor = 'var(--blue)';
                    btn.style.color = 'white';
                } else {
                    btn.classList.remove('active');
                    btn.style.backgroundColor = 'var(--light-gray)';
                    btn.style.color = 'var(--blue)';
                }
            });
        }
    };
}

// =============================
// Export functions for use in HTML pages
// =============================

// Make functions available globally
window.V2Shared = {
    // Date helpers
    formatDateToYMD,
    parseDateStringAsLocal,
    toYMDFromString,
    dedupeRowsByDate,
    
    // IndexedDB
    openDB,
    idbGet,
    idbPut,
    idbDelete,
    idbGetTickerYears,
    
    // Tickers index
    loadTickersIndex,
    getTickerSymbols,
    getTickerMetadata,
    
    // Data loading
    loadTickerData,
    loadTickerDataForPeriod,
    determineYearsToLoad,
    normalizePeriod,
    fetchYearCSV,
    
    // UI Components
    initHistorySlider,
    createPeriodButtons
};

console.log('[v2-shared.js] Loaded successfully');

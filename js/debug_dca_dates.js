// Debug script to compare DCA date calculations

// DCA.HTML logic (10 years back, Mondays only)
const endDate = new Date('2025-09-01');
const startDate = new Date('2025-09-01');
startDate.setFullYear(endDate.getFullYear() - 10);

console.log('DCA.HTML Logic:');
console.log('Start Date:', startDate.toISOString().split('T')[0]);
console.log('End Date:', endDate.toISOString().split('T')[0]);

// DCA-STRAT.HTML logic (weekly intervals from Sept 14, 2015)
const stratStart = new Date('2015-09-14');
const stratEnd = new Date('2025-09-01');
let weeklyDates = [];

let currentDate = new Date(stratStart);
while (currentDate <= stratEnd) {
    weeklyDates.push(currentDate.toISOString().split('T')[0]);
    currentDate.setDate(currentDate.getDate() + 7);
}

console.log('\nDCA-STRAT.HTML Logic (weekly intervals):');
console.log('Start Date:', stratStart.toISOString().split('T')[0]);
console.log('End Date:', stratEnd.toISOString().split('T')[0]);
console.log('Total weekly intervals:', weeklyDates.length);
console.log('First few dates:', weeklyDates.slice(0, 5));
console.log('Last few dates:', weeklyDates.slice(-5));
console.log('Expected investment:', weeklyDates.length * 25);

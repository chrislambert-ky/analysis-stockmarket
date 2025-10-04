# Slider Migration Examples for V2 Pages

This document shows specific examples for migrating each V2 page to use the new history slider component.

## Update v2-shared.js Version

First, update the script tag version in ALL pages from `v=3` to `v=4`:

```html
<!-- OLD -->
<script src="../js/v2-shared.js?v=3"></script>

<!-- NEW -->
<script src="../js/v2-shared.js?v=4"></script>
```

---

## Example 1: dcav2.html (Single/All Ticker Analysis)

### BEFORE (Lines 125-135):

```html
<div class="period-controls">
    <h3 id="selected-ticker-display" style="color: var(--blue); margin: 0;">Selected: None</h3>
    <div>
        <button id="ytd-btn" class="period-btn">YTD</button>
        <button id="5y-btn" class="period-btn">5 Years</button>
        <button id="10y-btn" class="period-btn">10 Years</button>
        <button id="15y-btn" class="period-btn">15 Years</button>
        <button id="20y-btn" class="period-btn">20 Years</button>
    </div>
    <button id="download-analysis-btn">Download CSV</button>
</div>
```

### AFTER:

```html
<div class="period-controls">
    <h3 id="selected-ticker-display" style="color: var(--blue); margin: 0;">Selected: None</h3>
    <!-- Slider will be inserted here -->
    <div id="periodSlider"></div>
    <button id="download-analysis-btn">Download CSV</button>
</div>
```

### JavaScript Changes (After line 1200+):

REMOVE all these event listeners:

```javascript
// DELETE THESE:
document.getElementById('ytd-btn').addEventListener('click', async function() { ... });
document.getElementById('5y-btn').addEventListener('click', async function() { ... });
document.getElementById('10y-btn').addEventListener('click', async function() { ... });
document.getElementById('15y-btn').addEventListener('click', async function() { ... });
document.getElementById('20y-btn').addEventListener('click', async function() { ... });

function updatePeriodButtonStates(activeButtonId) { ... } // DELETE THIS TOO
```

ADD this initialization:

```javascript
// Initialize history slider (add after V2Shared is loaded)
let currentSlider = null;

document.addEventListener('DOMContentLoaded', function() {
    currentSlider = window.V2Shared.initHistorySlider({
        containerId: 'periodSlider',
        initialValue: 0,  // Start with YTD
        maxYears: 25,
        
        onChange: async (period, sliderValue) => {
            console.log('[DCA] Period changed to:', period);
            currentPeriod = period;
            
            if (selectedTicker === 'ALL') {
                await renderAllTickersChart(period);
            } else if (selectedTicker) {
                await calculateAndRenderDCA();
            }
        }
    });
});
```

---

## Example 2: bodv2.html (Single/All Ticker BOD Analysis)

Same pattern as dcav2.html above.

---

## Example 3: dca-tickersv2.html (Grid View)

### BEFORE (Lines 176-180):

```html
<div class="period-controls">
    <button id="ytd-btn" class="period-btn active">YTD</button>
    <button id="5y-btn" class="period-btn">5 Years</button>
    <button id="10y-btn" class="period-btn">10 Years</button>
    <button id="15y-btn" class="period-btn">15 Years</button>
    <button id="20y-btn" class="period-btn">20 Years</button>
</div>
```

### AFTER:

```html
<!-- History Slider -->
<div id="periodSlider"></div>
```

### JavaScript Changes (At end of file, before closing </script>):

REMOVE:

```javascript
// DELETE all these period button listeners:
document.getElementById('ytd-btn').addEventListener('click', function() { ... });
document.getElementById('5y-btn').addEventListener('click', function() { ... });
// etc...

function updatePeriodButtonStates(activeButtonId) { ... } // DELETE
```

ADD:

```javascript
// Initialize history slider
window.V2Shared.initHistorySlider({
    containerId: 'periodSlider',
    initialValue: 0,
    onChange: (period) => {
        console.log('[DCA-Tickers] Rendering for period:', period);
        renderAllCharts(period);
    }
});

// Initial render
renderAllCharts('YTD');
```

---

## Example 4: bod-tickersv2.html (Grid View)

Same as dca-tickersv2.html above.

---

## Example 5: dca-stratv2.html (Advanced with Custom Settings)

This page has both ticker dropdown AND period selection. The slider integration is similar but note the layout:

### BEFORE:

```html
<div class="flex-row">
    <div class="input-group">
        <label>Ticker:</label>
        <select id="tickerSelect">...</select>
    </div>
    <div class="period-selection">
        <button id="ytd-btn" class="period-btn active" onclick="setStartToYTD()">YTD</button>
        <button id="5y-btn" class="period-btn" onclick="shiftStartYears(5)">5Y</button>
        <!-- etc -->
    </div>
</div>
```

### AFTER:

```html
<div class="flex-row">
    <div class="input-group">
        <label>Ticker:</label>
        <select id="tickerSelect">...</select>
    </div>
    <!-- Slider replaces period buttons -->
    <div id="periodSlider" style="flex:1;"></div>
</div>
```

### JavaScript:

REMOVE inline onclick handlers and period button functions.

ADD:

```javascript
let strategySlider = null;

// Initialize after DOM loaded
window.addEventListener('DOMContentLoaded', function() {
    strategySlider = window.V2Shared.initHistorySlider({
        containerId: 'periodSlider',
        initialValue: 0,
        onChange: (period, years) => {
            console.log('[Strategy] Period changed:', period);
            
            // Update date inputs to match period
            const endDate = new Date();
            const startDate = new Date();
            
            if (years === 0) {
                // YTD
                startDate.setMonth(0, 1);
            } else {
                // X years back
                startDate.setFullYear(endDate.getFullYear() - years);
            }
            
            document.getElementById('startDate').value = formatDateToYMD(startDate);
            document.getElementById('endDate').value = formatDateToYMD(endDate);
            
            // Recalculate if ticker selected
            const ticker = document.getElementById('tickerSelect').value;
            if (ticker) {
                calculateStrategy();
            }
        }
    });
});
```

---

## Example 6: bod-stratv2.html (Advanced)

Same as dca-stratv2.html above.

---

## Example 7: metricsv2.html (Ticker Metrics Dashboard)

metricsv2.html already has support for the slider through the loadTickersIndex integration. Just needs the HTML and initialization.

### BEFORE:

```html
<div class="timeframe-buttons">
    <button class="timeframe-btn active" data-period="ytd">YTD</button>
    <button class="timeframe-btn" data-period="3m">3M</button>
    <button class="timeframe-btn" data-period="6m">6M</button>
    <!-- etc -->
</div>
```

### AFTER:

```html
<!-- History Slider -->
<div id="periodSlider"></div>
```

### JavaScript:

REMOVE:

```javascript
// DELETE timeframe button event listeners
document.querySelectorAll('.timeframe-btn').forEach(btn => {
    btn.addEventListener('click', function() { ... });
});
```

ADD:

```javascript
// Initialize slider
window.V2Shared.initHistorySlider({
    containerId: 'periodSlider',
    initialValue: 0,
    onChange: (period) => {
        console.log('[Metrics] Period changed:', period);
        currentPeriod = period.toLowerCase();
        
        // Reload data if ticker selected
        if (selectedTicker) {
            selectTicker(selectedTicker);
        }
    }
});
```

---

## CSS Cleanup (Optional)

After migrating, you can remove these CSS rules if no longer used:

```css
/* Can be removed if all pages use slider */
.period-btn { ... }
.period-btn:hover { ... }
.period-btn.active { ... }
.period-controls { ... }
.timeframe-buttons { ... }
.timeframe-btn { ... }
```

The slider component uses inline styles and CSS variables, so no additional CSS is needed.

---

## Testing Checklist

After migrating each page:

- [ ] Slider appears and is visually correct
- [ ] Slider label shows "History: YTD" initially
- [ ] Dragging slider updates the label (e.g., "History: 5 years")
- [ ] Releasing slider triggers data reload
- [ ] Data loads correctly for different time periods
- [ ] Page works on mobile/tablet (slider is touch-friendly)
- [ ] Console shows no errors
- [ ] Download buttons still work (if applicable)

---

## Migration Order

Suggested order for migrating pages:

1. **dca-tickersv2.html** - Simplest (grid view, no dropdown)
2. **bod-tickersv2.html** - Same as above
3. **dcav2.html** - Medium (has ticker selection)
4. **bodv2.html** - Same as above
5. **metricsv2.html** - Medium (different structure)
6. **dca-stratv2.html** - Complex (custom settings + date inputs)
7. **bod-stratv2.html** - Complex (same as above)

---

## Rollback

If you need to rollback, just:

1. Restore the HTML with the period buttons
2. Restore the event listener code
3. Change script tag back to `?v=3`

The old code will continue to work since v2-shared.js maintains backward compatibility.

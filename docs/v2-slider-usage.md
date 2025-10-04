# V2 History Slider Component

## Overview

The V2 shared module now includes a reusable history slider component that replaces the fixed period buttons. This provides a better user experience with more granular time period selection (0-25 years).

## Features

- **Smooth slider interface** from YTD to 25 years of history
- **Real-time feedback** as user drags the slider
- **Consistent styling** across all V2 pages
- **Easy integration** with just a few lines of code
- **Fallback to buttons** for pages that prefer the old style

## Basic Usage

### 1. Add Container to HTML

```html
<!-- Replace your existing period buttons with this empty container -->
<div id="periodSlider"></div>
```

### 2. Initialize Slider in JavaScript

```javascript
// After V2Shared is loaded
const sliderControl = window.V2Shared.initHistorySlider({
    containerId: 'periodSlider',
    initialValue: 0,  // 0 = YTD
    maxYears: 25,     // Maximum years on slider
    
    // Called when user releases slider (use this for data loading)
    onChange: (period, sliderValue) => {
        console.log('Selected period:', period);  // 'YTD', '5Y', '10Y', etc.
        // Reload your data here
        loadDataForPeriod(period);
    },
    
    // Optional: Called in real-time as user drags (use for live UI updates)
    onInput: (period, sliderValue) => {
        console.log('Dragging over:', period);
        // Update UI labels, estimates, etc.
    }
});
```

### 3. Control the Slider Programmatically

```javascript
// Get current value
const value = sliderControl.getValue();  // Returns number (0-25)
const period = sliderControl.getPeriod();  // Returns 'YTD', '5Y', etc.

// Set slider position
sliderControl.setValue(5);  // Set to 5 years

// Adjust max value
sliderControl.setMax(20);  // Limit to 20 years max
```

## Period Mapping

The slider automatically maps values to standard period strings:

| Slider Value | Period String | Description |
|--------------|---------------|-------------|
| 0 | YTD | Year to date (current year only) |
| 1 | 1Y | 1 year of history |
| 5 | 5Y | 5 years of history |
| 10 | 10Y | 10 years of history |
| 15 | 15Y | 15 years of history |
| 20 | 20Y | 20 years of history |
| 2-25 | {n}Y | Any value becomes "{n}Y" |

## Full Example

```html
<!DOCTYPE html>
<html>
<head>
    <title>My Analysis Page</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <h1>Stock Analysis</h1>
    
    <!-- Slider will be inserted here -->
    <div id="periodSlider"></div>
    
    <div id="results">
        <!-- Your results here -->
    </div>
    
    <!-- Load V2 Shared -->
    <script src="../js/v2-shared.js?v=4"></script>
    <script>
        // Initialize slider
        const slider = window.V2Shared.initHistorySlider({
            containerId: 'periodSlider',
            initialValue: 0,
            onChange: async (period) => {
                console.log('Loading data for period:', period);
                showLoading();
                
                // Load data using V2 loader
                const data = await window.V2Shared.loadTickerDataForPeriod('AAPL', period);
                
                // Process and display
                displayResults(data);
                hideLoading();
            }
        });
        
        // Start with initial load
        slider.onChange(slider.getPeriod());
    </script>
</body>
</html>
```

## Alternative: Period Buttons

If you prefer the old button-style interface:

```javascript
const buttons = window.V2Shared.createPeriodButtons({
    containerId: 'periodControls',
    periods: ['YTD', '5Y', '10Y', '15Y', '20Y'],
    initialPeriod: 'YTD',
    onChange: (period) => {
        console.log('Selected period:', period);
        loadDataForPeriod(period);
    }
});

// Set active button programmatically
buttons.setActive('10Y');
```

## Migration Guide

### Before (Old Button Style)

```html
<div class="period-controls">
    <button id="ytd-btn" class="period-btn active">YTD</button>
    <button id="5y-btn" class="period-btn">5 Years</button>
    <button id="10y-btn" class="period-btn">10 Years</button>
</div>

<script>
    document.getElementById('ytd-btn').addEventListener('click', function() {
        loadData('YTD');
    });
    document.getElementById('5y-btn').addEventListener('click', function() {
        loadData('5Y');
    });
    // ... more buttons
</script>
```

### After (New Slider Style)

```html
<div id="periodSlider"></div>

<script src="../js/v2-shared.js?v=4"></script>
<script>
    window.V2Shared.initHistorySlider({
        containerId: 'periodSlider',
        onChange: (period) => loadData(period)
    });
</script>
```

## Styling

The slider uses CSS variables from your style.css:
- `var(--blue)` - Label and active states
- `var(--gray)` - Help text and value display
- `var(--light-gray)` - Inactive states

You can customize by targeting these classes:
```css
.history-slider-component { /* Main container */ }
.slider-label { /* "History: YTD" label */ }
.history-slider-input { /* The actual range input */ }
.slider-value-display { /* "YTD", "5Y", etc. display */ }
.slider-help-text { /* Help text below slider */ }
```

## Benefits

1. **More granular control**: Users can select any year from 0-25, not just 5/10/15/20
2. **Less screen space**: One slider vs 5-7 buttons
3. **Better mobile experience**: Easier to use on touch devices
4. **Consistent UI**: Same slider across all V2 pages
5. **Easy maintenance**: Update slider behavior in one place (v2-shared.js)

## Browser Support

Works in all modern browsers that support:
- `<input type="range">` (HTML5)
- ES6+ JavaScript
- CSS variables

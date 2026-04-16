# Real-World Validation Experiment

## Purpose
This experiment validates the Phase 2 prescriptive optimization model using **real-world hosted webpages** instead of circular model validation.

## Validation Approach

### The Problem with Circular Validation
The original Phase 2 validation was circular:
1. Model predicts "slow" → Optimizer changes features → Model predicts "fast"
2. **The model validates itself** — not suitable for research publication

### The Solution: Real-World A/B Test
```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│  SLOW PAGE (Before) │────▶│   PHASE 2 MODEL     │────▶│  FAST PAGE (After)  │
│  - Large image      │     │   - Get metrics     │     │  - Optimized image  │
│  - 500 empty divs   │     │   - Predict "slow"  │     │  - Minimal DOM      │
│  - Blocking JS      │     │   - Prescriptions   │     │  - Async JS         │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
         │                                                        │
         ▼                                                        ▼
┌─────────────────────┐                              ┌─────────────────────┐
│  PageSpeed API      │                              │  PageSpeed API      │
│  (External Validator)│                             │  (External Validator)│
│  Expected: SLOW     │                              │  Expected: FAST     │
└─────────────────────┘                              └─────────────────────┘
```

## Files Structure

```
validation_pages/
├── slow_page/                    # BEFORE optimization
│   ├── index.html                # Intentionally slow page
│   ├── generate_large_image.py   # Creates ~6MB uncompressed BMP
│   └── large_image.bmp           # Generated large image
│
├── fast_page/                    # AFTER optimization (to be created)
│   ├── index.html                # Optimized version
│   └── optimized_image.webp      # Compressed image
│
├── pagespeed_api_collector.py    # Collects metrics from PageSpeed API
├── validation_analysis.py        # Analyzes before/after results
└── README.md                     # This file
```

## Step-by-Step Validation Process

### Step 1: Generate Large Image
```powershell
cd c:\Dissertation\validation_pages\slow_page
python generate_large_image.py
```

### Step 2: Host the Slow Page
Options:
- **GitHub Pages** (Free): Push to a GitHub repo, enable Pages
- **Netlify** (Free): Drag & drop folder
- **Vercel** (Free): Connect repo or deploy folder
- **Local + ngrok**: For quick testing

### Step 3: Collect Metrics via PageSpeed API
```powershell
python pagespeed_api_collector.py --url "https://your-slow-page-url.com" --output slow_page_metrics.json
```

### Step 4: Run Phase 2 Model
Use the collected metrics to:
1. Predict performance class (should be "slow")
2. Get prescriptive recommendations
3. Document specific changes needed

### Step 5: Create Optimized Page
Apply Phase 2 recommendations:
- Compress/optimize images (WebP format)
- Remove empty DOM elements
- Defer/async JavaScript
- Minify resources

### Step 6: Host the Fast Page
Deploy the optimized version to the same hosting platform.

### Step 7: Collect Metrics for Fast Page
```powershell
python pagespeed_api_collector.py --url "https://your-fast-page-url.com" --output fast_page_metrics.json
```

### Step 8: Validate Results
- Compare before/after metrics
- Verify model predictions match actual classifications
- Document improvement percentages

## Performance Issues in Slow Page

| Issue | Implementation | Expected Impact |
|-------|---------------|-----------------|
| Large Image | ~6MB uncompressed BMP | High transfer size, slow LCP |
| DOM Complexity | 500 empty `<div>` elements | High DOM size, parsing delay |
| Render-Blocking JS | Heavy sync computation | Poor FCP, LCP, TTI, TBT |

### Expected Metrics (Slow Page)
| Metric | Expected Range | Impact |
|--------|---------------|--------|
| FCP | >3000ms | Blocked by sync JS |
| LCP | >5000ms | Large image load |
| TTI | >7000ms | JS execution delay |
| TBT | >1000ms | Long tasks blocking |
| CLS | ~0 | No layout shift issues |
| Page Size | >6MB | Large uncompressed image |
| DOM Elements | >500 | 500 empty divs + content |

## Research Significance

This validation approach is **stronger for publication** because:

1. **Independent Validation**: Google's PageSpeed API (external) validates both states
2. **Controlled Experiment**: Same content structure, only prescribed optimizations applied
3. **Reproducible**: Anyone can host the same pages and verify results
4. **Real-World Applicable**: Demonstrates practical value of the model
5. **Eliminates Circular Bias**: Model predictions are validated by external measurement

## Citation
If using this validation approach in research, cite as part of the AI-Driven Web Performance Optimization Framework dissertation project.

---
*Last Updated: January 2026*

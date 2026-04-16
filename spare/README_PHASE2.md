# Phase 2: Dataset Augmentation - User Guide

## 📋 Overview

This guide explains how to use the Phase 2 notebook to augment your Website Performance Dataset with live webpage features extracted using Selenium and BeautifulSoup. These features will be used for prescriptive optimization in the next phase.

---

## 🎯 What Phase 2 Does

Phase 2 augments your original dataset with **actionable web performance features** by:

1. **Loading URLs** from your existing Kaggle dataset
2. **Scraping live webpages** using Selenium (headless Chrome)
3. **Extracting network metrics**: Resource sizes, request counts, compression, CDN usage
4. **Extracting structural metrics**: DOM depth, script counts, lazy loading
5. **Merging data** into a comprehensive augmented dataset
6. **Exporting** the augmented dataset for prescriptive modeling

---

## 🛠️ Prerequisites

### Required Software

1. **Python 3.8+** (same as Phase 1)
2. **Google Chrome browser** (latest version)
3. **ChromeDriver** (matching your Chrome version)

### Installing ChromeDriver

#### **Windows (Automatic - Recommended):**

```powershell
# Install using pip (will auto-download ChromeDriver)
pip install webdriver-manager
```

Then add this to your notebook (already included):
```python
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
```

#### **Windows (Manual):**

1. Check Chrome version: Open Chrome → Menu (⋮) → Help → About Google Chrome
2. Download matching ChromeDriver: https://chromedriver.chromium.org/downloads
3. Extract `chromedriver.exe` to a folder
4. Add folder to PATH or specify path in code

---

## 📦 Installation Instructions

### Step 1: Install Required Libraries

```powershell
cd D:\_MTechProject
pip install -r requirements_phase2.txt
```

### Alternative: Install individually

```powershell
pip install selenium beautifulsoup4 lxml requests tqdm webdriver-manager
```

---

## 🚀 How to Run Phase 2

### **Configuration (Important!)**

Before running, configure the settings in **Cell 2**:

```python
CONFIG = {
    'original_dataset': 'website_performance_dataset.csv',
    'output_dataset': 'augmented_website_performance_dataset.csv',
    'timeout': 30,  # seconds per page
    'max_urls': 10,  # ⚠️ SET THIS FOR TESTING!
    'headless': True,  # Run browser invisibly
    'retry_attempts': 2,
    'delay_between_requests': 2,  # seconds between URLs
}
```

**⚠️ FOR TESTING:** Set `'max_urls': 10` to test with only 10 URLs first!

**FOR FULL RUN:** Set `'max_urls': None` to process all URLs (may take hours!)

---

## 📝 Cell Execution Order

### **Cell 1: Import Libraries** ✅
- Imports Selenium, BeautifulSoup, pandas, etc.
- **Expected:** "✓ All libraries imported successfully!"
- **Time:** ~5 seconds

### **Cell 2: Configuration** ✅
- Sets up configuration parameters
- **Action:** MODIFY `max_urls` for testing!
- **Time:** Instant

### **Cell 3: Load Dataset** ✅
- Loads original Kaggle dataset
- Validates and cleans URLs
- **Expected:** Dataset overview and URL count
- **Time:** ~2 seconds

### **Cell 4: Initialize Selenium** ✅
- Starts Chrome WebDriver (headless mode)
- **Expected:** "✓ WebDriver initialized successfully"
- **Time:** ~5-10 seconds
- **⚠️ Error?** See troubleshooting below

### **Cell 5: Network Metrics Function** ✅
- Defines function to extract network performance data
- **Time:** Instant

### **Cell 6: Structural Metrics Function** ✅
- Defines function to extract DOM structure data
- **Time:** Instant

### **Cell 7: Complete Pipeline** ✅
- Combines network + structural extraction
- **Time:** Instant

### **Cell 8: Batch Processing** ✅
- Defines batch processing with progress tracking
- **Time:** Instant

### **Cell 9: Execute Extraction** ⏱️ **LONG RUNNING!**
- **This cell does the actual scraping**
- Shows progress bar with ETA
- **Time:** 
  - 10 URLs: ~5-10 minutes
  - 100 URLs: ~1 hour
  - 736 URLs (full): ~4-6 hours

**Expected Output:**
```
Processing URLs: 100%|██████████| 10/10 [05:23<00:00, 32.3s/url]

BATCH PROCESSING COMPLETE
Total processed: 10
Successful: 8 (80.0%)
Failed: 2 (20.0%)
```

### **Cell 10: Merge Datasets** ✅
- Combines original + extracted features
- **Expected:** Merged dataset shape
- **Time:** ~2 seconds

### **Cell 11: Summary** ✅
- Shows augmentation statistics
- **Expected:** Feature counts, success rates
- **Time:** ~2 seconds

### **Cell 12: Export** ✅
- Saves augmented dataset as CSV
- **Expected:** File saved confirmation
- **Time:** ~5 seconds

### **Cell 13: Cleanup** ✅
- Closes Selenium browser
- **Expected:** "✓ Selenium WebDriver closed"
- **Time:** Instant

---

## 📊 Features Extracted

### **Network Performance Metrics (from Selenium):**

| Feature | Description | Unit |
|---------|-------------|------|
| `total_requests` | Total HTTP requests | count |
| `total_transfer_size` | Total data transferred | KB |
| `js_size` | JavaScript file sizes | KB |
| `css_size` | CSS file sizes | KB |
| `image_size` | Image file sizes | KB |
| `font_size` | Font file sizes | KB |
| `js_requests` | Number of JS files | count |
| `css_requests` | Number of CSS files | count |
| `image_requests` | Number of images | count |
| `ttfb` | Time to First Byte | ms |
| `dns_lookup_time` | DNS resolution time | ms |
| `tcp_connect_time` | TCP connection time | ms |
| `server_response_time` | Server response time | ms |
| `uses_compression` | Using gzip/brotli | boolean |
| `compression_type` | gzip/br/none | string |
| `uses_cdn` | Using CDN | boolean |
| `cdn_provider` | CDN name | string |
| `total_load_time` | Complete load time | seconds |

### **Structural Metrics (from BeautifulSoup):**

| Feature | Description | Unit |
|---------|-------------|------|
| `dom_depth` | Maximum DOM tree depth | levels |
| `total_dom_nodes` | Total HTML elements | count |
| `total_images` | Image tags | count |
| `total_scripts` | Script tags | count |
| `total_css_links` | CSS link tags | count |
| `async_scripts` | Async scripts | count |
| `defer_scripts` | Defer scripts | count |
| `inline_scripts` | Inline scripts | count |
| `external_scripts` | External scripts | count |
| `inline_styles` | Style tags | count |
| `total_links` | Anchor tags | count |
| `total_forms` | Form tags | count |
| `total_iframes` | Iframe tags | count |
| `lazy_load_images` | Images with lazy loading | count |
| `srcset_images` | Images with srcset | count |

---

## ⏱️ Time Estimates

| Dataset Size | Estimated Time | Recommendation |
|--------------|----------------|----------------|
| 10 URLs | 5-10 minutes | ✅ Good for testing |
| 50 URLs | 30-45 minutes | ✅ Good for development |
| 100 URLs | 1-1.5 hours | ⚠️ Medium dataset |
| 500 URLs | 4-6 hours | ⚠️ Large dataset |
| 736 URLs (full) | 6-8 hours | ⚠️ Run overnight |

**Factors affecting time:**
- Website response speed
- Network connection
- Timeout setting (default: 30s per URL)
- Retry attempts (default: 2)
- Delay between requests (default: 2s)

---

## ⚠️ Troubleshooting

### **Error: ChromeDriver not found**

**Solution 1 (Automatic):**
```powershell
pip install webdriver-manager
```

Then modify Cell 4:
```python
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
```

**Solution 2 (Manual):**
1. Download ChromeDriver: https://chromedriver.chromium.org/
2. Place in PATH or specify location

### **Error: Timeout exceptions**

Many timeouts? Increase timeout in Cell 2:
```python
'timeout': 60,  # Increase from 30 to 60 seconds
```

### **Error: Too many failed extractions**

If >50% fail:
1. Check internet connection
2. Try non-headless mode: `'headless': False`
3. Increase retry attempts: `'retry_attempts': 3`
4. Some old URLs may be dead (expected)

### **Browser Opens Visibly**

Set headless mode in Cell 2:
```python
'headless': True,
```

### **Process Too Slow**

Speed up (with tradeoffs):
1. Reduce timeout: `'timeout': 15`
2. Remove delay: `'delay_between_requests': 0` (may get rate-limited)
3. Process subset: `'max_urls': 100`

### **Memory Issues**

If computer freezes:
1. Close other applications
2. Process in batches (modify code to save intermediate results)
3. Increase virtual memory (Windows settings)

---

## 📁 Output Files

After successful run:

```
D:\_MTechProject/
├── augmented_website_performance_dataset_20251116_143000.csv  ← Main output
├── phase2_augmentation.log                                    ← Execution log
└── phase2_dataset_augmentation.ipynb                          ← This notebook
```

### **Augmented Dataset Columns:**

- **Original columns** (9): Sr No, website_url, Category, Page Size (KB), etc.
- **Network columns** (~18): total_requests, js_size, ttfb, uses_cdn, etc.
- **Structural columns** (~15): dom_depth, total_scripts, async_scripts, etc.
- **Total columns**: ~42 columns

---

## 🎯 Expected Results

### **Success Metrics:**

✅ **Good Run:**
- Success rate: >70%
- Most features populated
- Few timeout errors

⚠️ **Acceptable Run:**
- Success rate: 50-70%
- Some old URLs failed (expected)
- Key features still usable

❌ **Poor Run:**
- Success rate: <50%
- Check troubleshooting section
- Verify ChromeDriver installation

### **Sample Output:**

```
BATCH PROCESSING COMPLETE
════════════════════════════════════════════════════════════════════════════════
Total processed: 100
Successful: 82 (82.0%)
Failed: 18 (18.0%)
════════════════════════════════════════════════════════════════════════════════

AUGMENTED DATASET SUMMARY
════════════════════════════════════════════════════════════════════════════════
Total records: 100
Total columns: 42

Average total transfer size: 2456.78 KB
Average DOM depth: 12.3
Average scripts per page: 18.7
CDN usage: 45.6%
════════════════════════════════════════════════════════════════════════════════
```

---

## 🔍 Checking Your Results

After Cell 12, inspect the augmented dataset:

```python
# Check successful extractions
df_augmented[df_augmented['extraction_successful'] == True].shape

# View new features
df_augmented[['website_url', 'total_requests', 'js_size', 'dom_depth', 'uses_cdn']].head()

# Check missing values
df_augmented.isnull().sum()

# Statistics
df_augmented[['total_requests', 'total_transfer_size', 'dom_depth']].describe()
```

---

## 💡 Best Practices

### **1. Test First**
Always run with `max_urls=10` first to verify everything works!

### **2. Run Overnight**
For full dataset (736 URLs), start before bed or before leaving for the day.

### **3. Save Intermediate Results**
For very large datasets, modify code to save every 100 URLs.

### **4. Monitor Progress**
Watch the progress bar and log file for issues.

### **5. Handle Failures**
Some URL failures are normal (dead links, redirects, timeouts).

---

## 🔮 Next Steps (Phase 3)

After augmentation is complete:

1. ✅ **Analyze augmented dataset** - Understand new features
2. ✅ **Feature selection** - Choose optimization targets
3. ✅ **Prescriptive modeling** - Use SciPy for optimization
4. ✅ **Generate recommendations** - Actionable improvements
5. ✅ **Explainability layer** - SHAP/LIME integration

---

## 📞 Common Questions

**Q: Can I pause and resume?**
A: Not built-in. Consider modifying code to save checkpoints.

**Q: Will this work on all websites?**
A: No. Some sites block automation, require login, or have CAPTCHAs.

**Q: Do I need a fast computer?**
A: Not really. Main factor is internet speed and website response times.

**Q: Can I run multiple instances in parallel?**
A: Yes, but complex. Easier to run single instance with all URLs.

**Q: What if a website blocks me?**
A: Normal. The code includes delays and user-agent headers to minimize blocking.

---

## 🎓 Technical Notes

### **Why Selenium + BeautifulSoup?**

- **Selenium**: Needed for JavaScript-heavy sites, network timing, resource sizes
- **BeautifulSoup**: Fast HTML parsing, DOM analysis, element counting

### **Performance Considerations**

- Headless mode is ~20% faster
- Each page opens a new tab (closed after scraping)
- Network logs capture all HTTP requests
- Progress bar shows real-time ETA

### **Data Quality**

- Some features may be 0 (e.g., old sites without CDN)
- Failed extractions marked with `extraction_successful=False`
- Missing values handled in prescriptive phase

---

## ✅ Quick Start Checklist

- [ ] Install requirements: `pip install -r requirements_phase2.txt`
- [ ] Install ChromeDriver (automatic or manual)
- [ ] Open `phase2_dataset_augmentation.ipynb`
- [ ] Set `max_urls=10` in Cell 2 for testing
- [ ] Run all cells sequentially
- [ ] Verify output file created
- [ ] Check success rate >70%
- [ ] If successful, set `max_urls=None` for full run
- [ ] Run full extraction (overnight recommended)
- [ ] Review augmented dataset

---

**Total Setup Time:** 10-15 minutes  
**Testing Run Time:** 5-10 minutes (10 URLs)  
**Full Run Time:** 6-8 hours (736 URLs)  
**Output:** Augmented CSV ready for prescriptive optimization

---

**Happy Augmenting! 🚀**

*Phase 2 - Dataset Augmentation*  
*Last Updated: November 16, 2025*

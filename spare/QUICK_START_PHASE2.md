# Phase 2 Quick Start - Dataset Augmentation

## 🚀 Fast Setup (< 5 minutes)

### 1. Install ChromeDriver (Automatic)
```powershell
pip install webdriver-manager
```

### 2. Install Requirements
```powershell
cd D:\_MTechProject
pip install -r requirements_phase2.txt
```

### 3. Test Run (10 URLs)
- Open `phase2_dataset_augmentation.ipynb`
- In **Cell 2**, set: `'max_urls': 10`
- Run all cells (Shift + Enter through each)
- Wait 5-10 minutes
- Check for augmented CSV file

### 4. Full Run (All URLs)
- In **Cell 2**, set: `'max_urls': None`
- Run all cells
- Wait 6-8 hours (run overnight!)
- Check for augmented CSV file

---

## 📊 What Gets Extracted

### Network Metrics (18 features):
- Resource sizes (JS, CSS, images, fonts)
- Request counts
- Network timings (TTFB, DNS, TCP)
- Compression & CDN usage

### Structural Metrics (15 features):
- DOM depth & node count
- Script/image/CSS counts
- Async/defer script usage
- Lazy loading detection

---

## ⏱️ Time Estimates

| URLs | Time |
|------|------|
| 10 | 5-10 min |
| 100 | 1-1.5 hours |
| 736 (all) | 6-8 hours |

---

## ⚠️ Quick Troubleshooting

### ChromeDriver Error?
```powershell
pip install webdriver-manager
```

### Too Many Timeouts?
Cell 2: Change `'timeout': 30` to `'timeout': 60`

### Process Too Slow?
Cell 2: Change `'delay_between_requests': 2` to `'delay_between_requests': 0`

### Want to See Browser?
Cell 2: Change `'headless': True` to `'headless': False`

---

## ✅ Expected Output

```
BATCH PROCESSING COMPLETE
Total processed: 10
Successful: 8 (80.0%)
Failed: 2 (20.0%)

Output file: augmented_website_performance_dataset_20251116_143000.csv
```

---

## 📁 Output Files

- `augmented_website_performance_dataset_[timestamp].csv` ← Main output
- `phase2_augmentation.log` ← Execution log

---

## 🎯 Success Criteria

✅ Success rate > 70%  
✅ CSV file created  
✅ ~42 columns in output  
✅ New features populated  

---

## 💡 Pro Tips

1. **Always test with 10 URLs first!**
2. **Run full dataset overnight**
3. **Check log file for errors**
4. **Some URL failures are normal (dead links)**
5. **Monitor progress bar for ETA**

---

## 🔄 Cell Execution Order

1. Import Libraries ✅
2. Configuration ✅ ← **MODIFY max_urls HERE!**
3. Load Dataset ✅
4. Initialize Selenium ✅
5-8. Define Functions ✅
9. **Execute Extraction** ⏱️ ← **LONG RUNNING!**
10. Merge Datasets ✅
11. Summary ✅
12. Export ✅
13. Cleanup ✅

---

## 📞 Need Help?

See `README_PHASE2.md` for detailed guide!

---

**Quick Start Time:** 5 minutes  
**Test Run:** 10 minutes  
**Full Run:** 6-8 hours  

**Ready to augment! 🎉**

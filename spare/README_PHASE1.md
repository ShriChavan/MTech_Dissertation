# Phase 1: Predictive Model Development - User Guide

## 📋 Overview
This guide will help you set up and run the predictive modeling phase of your **Predictive–Prescriptive–Explainable AI Framework for Web Performance Optimization** research project.

---

## 🛠️ Prerequisites

### Required Software
- **Python 3.8+** (recommended: Python 3.9 or 3.10)
- **Jupyter Notebook** or **VS Code with Jupyter extension**

### Dataset
- `website_performance_dataset.csv` (already in your project folder)

---

## 📦 Installation Instructions

### Step 1: Install Required Libraries

Open your terminal (PowerShell in Windows) and navigate to your project directory:

```powershell
cd D:\_MTechProject
```

Then install all required packages:

```powershell
pip install pandas numpy matplotlib seaborn scikit-learn xgboost joblib
```

### Alternative: Install using requirements file

You can also create a `requirements.txt` file (see below) and install all packages at once:

```powershell
pip install -r requirements.txt
```

---

## 📄 Required Libraries

Here's a breakdown of what each library does:

| Library | Version | Purpose |
|---------|---------|---------|
| `pandas` | ≥1.3.0 | Data manipulation and analysis |
| `numpy` | ≥1.21.0 | Numerical computations |
| `matplotlib` | ≥3.4.0 | Data visualization |
| `seaborn` | ≥0.11.0 | Statistical visualizations |
| `scikit-learn` | ≥1.0.0 | Machine learning models and preprocessing |
| `xgboost` | ≥1.5.0 | XGBoost classifier implementation |
| `joblib` | ≥1.1.0 | Model serialization |

### requirements.txt
```
pandas>=1.3.0
numpy>=1.21.0
matplotlib>=3.4.0
seaborn>=0.11.0
scikit-learn>=1.0.0
xgboost>=1.5.0
joblib>=1.1.0
```

---

## 🚀 How to Run the Notebook

### Option 1: Using VS Code (Recommended)

1. **Open VS Code** and navigate to your project folder
2. **Open the notebook**: `phase1_predictive_model.ipynb`
3. **Select Python kernel**: Click on the kernel selector in the top-right corner
4. **Run cells sequentially**: 
   - Click the "Run" button (▶️) next to each cell
   - Or use keyboard shortcuts:
     - `Shift + Enter`: Run cell and move to next
     - `Ctrl + Enter`: Run cell and stay
     - `Alt + Enter`: Run cell and insert new cell below

### Option 2: Using Jupyter Notebook

1. Open terminal and navigate to project directory:
   ```powershell
   cd D:\_MTechProject
   ```

2. Launch Jupyter Notebook:
   ```powershell
   jupyter notebook
   ```

3. Open `phase1_predictive_model.ipynb` in the browser

4. Run cells sequentially from top to bottom

---

## 📊 Execution Flow

### Cell-by-Cell Execution Guide

#### **Cell 1: Import Libraries**
- **Action**: Run this cell first
- **Expected Output**: "✓ All libraries imported successfully!"
- **Time**: ~2-5 seconds
- **Note**: If you see import errors, revisit installation step

#### **Cell 2: Data Loading**
- **Action**: Loads the dataset
- **Expected Output**: Dataset shape and preview of first 10 rows
- **Time**: ~1 second

#### **Cell 3: Exploratory Data Analysis**
- **Action**: Displays comprehensive data statistics
- **Expected Output**: 
  - Dataset info
  - Statistical summary
  - Missing values report
  - Target variable distributions
- **Time**: ~2-3 seconds

#### **Cell 4: Data Visualizations**
- **Action**: Creates 6 visualizations + correlation heatmap
- **Expected Output**: 
  - Distribution plots
  - Correlation heatmap
- **Time**: ~5-8 seconds
- **Note**: Visualizations will appear inline

#### **Cell 5: Data Preprocessing**
- **Action**: Handles missing values, encodes categories, creates feature sets
- **Expected Output**: Preprocessing summary with feature counts
- **Time**: ~2-3 seconds

#### **Cell 6: Feature Engineering**
- **Action**: Creates interaction and log-transformed features
- **Expected Output**: List of new features created
- **Time**: ~1-2 seconds

#### **Cell 7: Train-Test Split & Normalization**
- **Action**: Splits data (80/20) and normalizes features
- **Expected Output**: 
  - Training set size
  - Test set size
  - Class distribution
- **Time**: ~1 second

#### **Cell 8: Model Training**
- **Action**: Trains 3 models (SVM, Random Forest, XGBoost)
- **Expected Output**: Confirmation for each model trained
- **Time**: ~10-30 seconds (varies by dataset size)
- **Note**: This is the most time-consuming step

#### **Cell 9: Model Evaluation**
- **Action**: Evaluates all models with metrics
- **Expected Output**: 
  - Accuracy, Precision, Recall, F1-Score for each model
  - Classification reports
  - Model comparison table
  - Best model announcement
- **Time**: ~3-5 seconds

#### **Cell 10: Results Visualization**
- **Action**: Creates performance comparison charts and confusion matrices
- **Expected Output**: 
  - 4 bar charts (accuracy, precision, recall, F1)
  - 3 confusion matrices (one per model)
- **Time**: ~5-8 seconds

#### **Cell 11: Feature Importance Plot**
- **Action**: Displays top features for tree-based models
- **Expected Output**: Horizontal bar charts showing feature importance
- **Time**: ~3-5 seconds

#### **Cell 12: Model Export**
- **Action**: Saves the best model to disk
- **Expected Output**: 
  - Two files created (.joblib and .pkl)
  - Model metadata displayed
- **Time**: ~2-3 seconds
- **Note**: Files saved in project directory

#### **Cell 13: Model Loading Example**
- **Action**: Defines function for loading saved models
- **Expected Output**: Function definition confirmation
- **Time**: Instant

#### **Cell 14: Summary**
- **Action**: Displays project summary and next steps
- **Expected Output**: Complete summary of Phase 1
- **Time**: Instant

---

## ⏱️ Total Expected Runtime

- **Complete notebook execution**: ~1-2 minutes
- **Most time-intensive**: Model training (Cell 8)

---

## 📁 Output Files

After running the notebook, you'll have:

1. **Model files** (2 per run):
   - `best_model_[model_name]_[timestamp].joblib` (primary format)
   - `best_model_[model_name]_[timestamp].pkl` (backup format)

2. **Visualizations** (displayed inline in notebook):
   - Data distribution plots
   - Correlation heatmap
   - Model comparison charts
   - Confusion matrices
   - Feature importance plots

---

## 🎯 Key Features Implemented

### Data Preprocessing
✅ Missing value imputation (median for numeric, mode for categorical)  
✅ Label encoding for categorical variables  
✅ Robust scaling for feature normalization  
✅ Stratified train-test split (80/20)

### Feature Engineering
✅ Size-to-LoadTime ratio  
✅ Total time metric (Response + Load)  
✅ Throughput-to-ResponseTime ratio  
✅ Log transformations (Page Size, Throughput)

### Models Trained
✅ **Support Vector Machine (SVM)** - RBF kernel  
✅ **Random Forest** - 100 estimators  
✅ **XGBoost** - Gradient boosting with hyperparameters

### Evaluation Metrics
✅ Accuracy  
✅ Precision (weighted)  
✅ Recall (weighted)  
✅ F1-Score (weighted)  
✅ Classification reports  
✅ Confusion matrices

---

## 🔧 Troubleshooting

### Common Issues

#### 1. **Import Error: No module named 'X'**
**Solution**: Install the missing library
```powershell
pip install [library_name]
```

#### 2. **Kernel Selection Error**
**Solution**: 
- In VS Code: Click kernel selector → Select Python interpreter
- In Jupyter: Kernel → Change kernel → Select Python 3

#### 3. **File Not Found Error**
**Solution**: Ensure `website_performance_dataset.csv` is in the same directory as the notebook

#### 4. **Memory Error**
**Solution**: 
- Close other applications
- Reduce dataset size for testing
- Use fewer estimators in Random Forest/XGBoost

#### 5. **Slow Training**
**Solution**:
- Normal for first run (model compilation)
- Reduce `n_estimators` in Cell 8 for faster testing
- Consider using a GPU if available (for XGBoost)

---

## 📈 Understanding Results

### Target Variable
- **Performance_Label**: Predicts website performance (fast/medium/slow)

### Model Selection Criteria
The notebook automatically selects the best model based on:
1. **Primary**: Highest accuracy
2. **Secondary**: Highest F1-score (for balanced performance)

### Interpreting Metrics
- **Accuracy**: Overall correctness (higher is better)
- **Precision**: How many predicted positives are actually positive
- **Recall**: How many actual positives were caught
- **F1-Score**: Harmonic mean of precision and recall (balanced metric)

---

## 🔮 Next Steps (Future Phases)

### Phase 2: Prescriptive Optimization
- Use SciPy for optimization algorithms
- Recommend optimal configurations
- Implement constraint-based solutions

### Phase 3: Explainability Layer
- SHAP (SHapley Additive exPlanations) for global interpretability
- LIME (Local Interpretable Model-agnostic Explanations) for local explanations
- Enhanced visualizations for stakeholder communication

---

## 💾 Loading and Using Saved Models

### Load a saved model:
```python
import joblib

# Load the model package
model_package = joblib.load('best_model_random_forest_20250101_120000.joblib')

# Extract components
model = model_package['model']
scaler = model_package['scaler']
encoders = model_package['encoders']
feature_names = model_package['feature_names']

# Make predictions on new data
new_data_scaled = scaler.transform(new_data)
predictions = model.predict(new_data_scaled)

# Decode predictions
if 'target' in encoders:
    predictions = encoders['target'].inverse_transform(predictions)
```

---

## 📞 Support

If you encounter issues:
1. Check the error message carefully
2. Verify all libraries are installed correctly
3. Ensure dataset is in the correct location
4. Review the cell output for specific error details

---

## ✅ Checklist Before Running

- [ ] Python 3.8+ installed
- [ ] All required libraries installed
- [ ] Dataset (`website_performance_dataset.csv`) is in project folder
- [ ] Jupyter kernel selected in VS Code or Jupyter Notebook running
- [ ] Sufficient disk space for model files (~10-50 MB)
- [ ] Good internet connection (for initial package installation)

---

## 📊 Expected Performance

Based on the dataset structure:
- **Expected Accuracy**: 70-95% (varies by model)
- **Training Time**: 10-30 seconds
- **Dataset Size**: 736 samples (from preview)
- **Features**: ~10-15 after engineering

---

**Good luck with your research project! 🚀**

*Last Updated: November 1, 2025*

# Phase 1 - Project Structure & Architecture

## 📁 Project Files Overview

```
D:\_MTechProject/
│
├── website_performance_dataset.csv          # Your dataset (already present)
├── phase1_predictive_model.ipynb           # Main notebook (NEW)
├── requirements.txt                         # Python dependencies (NEW)
├── README_PHASE1.md                        # Detailed guide (NEW)
├── QUICK_START.md                          # Quick reference (NEW)
└── PROJECT_ARCHITECTURE.md                 # This file (NEW)
```

### Generated Files (after running notebook):
```
├── best_model_[model_name]_[timestamp].joblib    # Saved model (primary)
└── best_model_[model_name]_[timestamp].pkl       # Saved model (backup)
```

---

## 🏗️ Framework Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│    Predictive–Prescriptive–Explainable AI Framework             │
│              for Web Performance Optimization                   │
└─────────────────────────────────────────────────────────────────┘
                            ▼
        ┌───────────────────────────────────────┐
        │   PHASE 1: PREDICTIVE MODELING        │  ← YOU ARE HERE
        │   (Current Implementation)            │
        └───────────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
    ┌───────────────────────┐  ┌───────────────────────┐
    │  PHASE 2: PRESCRIPTIVE│  │ PHASE 3: EXPLAINABLE  │
    │    (Future - SciPy)   │  │   (Future - SHAP/LIME)│
    └───────────────────────┘  └───────────────────────┘
```

---

## 🔄 Phase 1 - Data Flow Pipeline

```
┌──────────────────┐
│  Raw CSV Data    │
│  (736 samples)   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Data Loading    │ ← Load CSV, check structure
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  EDA & Viz       │ ← Explore distributions, correlations
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Preprocessing   │ ← Handle missing values
│                  │   Encode categories
│                  │   Drop irrelevant columns
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Feature Eng.    │ ← Create interaction features
│                  │   Log transformations
│                  │   Ratio calculations
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Train-Test      │ ← 80/20 split (stratified)
│  Split           │   RobustScaler normalization
└────────┬─────────┘
         │
         ├────────────────┬────────────────┐
         ▼                ▼                ▼
    ┌────────┐      ┌─────────┐     ┌─────────┐
    │  SVM   │      │ Random  │     │ XGBoost │
    │ Model  │      │ Forest  │     │  Model  │
    └────┬───┘      └────┬────┘     └────┬────┘
         │               │               │
         └───────────┬───┴───────────────┘
                     ▼
         ┌─────────────────────┐
         │  Model Evaluation   │ ← Accuracy, Precision, Recall, F1
         │  & Comparison       │   Confusion Matrix
         └──────────┬──────────┘
                    ▼
         ┌─────────────────────┐
         │  Best Model Export  │ ← Save as .joblib & .pkl
         └─────────────────────┘
```

---

## 🧩 Code Structure

### Modular Design (Extensible for Phases 2 & 3)

```python
# Cell 1: Configuration & Imports
├── Core libraries (pandas, numpy)
├── Visualization (matplotlib, seaborn)
├── Preprocessing (sklearn.preprocessing)
├── Models (SVM, RandomForest, XGBoost)
├── Metrics (sklearn.metrics)
└── Persistence (joblib, pickle)

# Cell 2-4: Data Analysis Module
├── load_data()                    # Load CSV
├── perform_eda()                  # Statistical analysis
└── visualize_data()               # Create plots

# Cell 5: Preprocessing Module
└── preprocess_data()              # Clean & encode data
    ├── Drop irrelevant columns
    ├── Impute missing values
    ├── Encode categorical variables
    └── Encode target variable

# Cell 6: Feature Engineering Module
└── engineer_features()            # Create new features
    ├── Interaction features
    ├── Ratio features
    └── Log transformations

# Cell 7: Data Preparation Module
└── prepare_train_test_data()     # Split & normalize
    ├── Stratified split
    └── RobustScaler normalization

# Cell 8: Model Training Module
└── train_models()                 # Train all models
    ├── SVM (RBF kernel)
    ├── Random Forest (100 trees)
    └── XGBoost (gradient boosting)

# Cell 9: Evaluation Module
└── evaluate_models()              # Assess performance
    ├── Classification metrics
    ├── Model comparison
    └── Best model selection

# Cell 10-11: Visualization Module
├── visualize_results()            # Performance charts
└── plot_feature_importance()      # Feature rankings

# Cell 12: Export Module
└── export_model()                 # Save best model
    ├── Package model + metadata
    └── Save as joblib & pickle

# Cell 13: Deployment Module
└── load_and_predict()             # Load & use model
```

---

## 📊 Dataset Schema

### Input Features
```
┌─────────────────────────────────────────┐
│ ORIGINAL FEATURES                       │
├─────────────────────────────────────────┤
│ • Sr No              (int) - Drop       │
│ • website_url        (str) - Drop       │
│ • Category           (str) - Encode     │
│ • Page Size (KB)     (float)            │
│ • Load Time(s)       (float)            │
│ • Response Time(s)   (float)            │
│ • Throughput         (float)            │
└─────────────────────────────────────────┘
         │
         ▼ (Feature Engineering)
┌─────────────────────────────────────────┐
│ ENGINEERED FEATURES                     │
├─────────────────────────────────────────┤
│ • Size_LoadTime_Ratio                   │
│ • Total_Time                            │
│ • Throughput_ResponseTime_Ratio         │
│ • Log_Page_Size                         │
│ • Log_Throughput                        │
└─────────────────────────────────────────┘
```

### Target Variables
```
┌─────────────────────────────────────────┐
│ TARGET (Choose one)                     │
├─────────────────────────────────────────┤
│ • Performance_Label  (fast/medium/slow) │ ← Primary target
│ • User Response      (Fast/Medium/Slow) │ ← Alternative
└─────────────────────────────────────────┘
```

---

## 🤖 Model Specifications

### 1. Support Vector Machine (SVM)
```python
SVC(
    kernel='rbf',           # Radial basis function
    C=1.0,                  # Regularization
    gamma='scale',          # Kernel coefficient
    probability=True        # Enable probability estimates
)
```
**Use Case**: Non-linear decision boundaries  
**Strength**: Works well with high-dimensional data  
**Training Time**: Moderate

### 2. Random Forest
```python
RandomForestClassifier(
    n_estimators=100,       # 100 decision trees
    max_depth=None,         # Unlimited depth
    min_samples_split=2,    # Min samples to split
    n_jobs=-1               # Use all CPU cores
)
```
**Use Case**: Ensemble learning  
**Strength**: Robust to overfitting, feature importance  
**Training Time**: Fast (parallel)

### 3. XGBoost
```python
XGBClassifier(
    n_estimators=100,       # 100 boosting rounds
    max_depth=6,            # Tree depth
    learning_rate=0.1,      # Step size
    subsample=0.8,          # Sample 80% per tree
    colsample_bytree=0.8    # Use 80% features
)
```
**Use Case**: Gradient boosting  
**Strength**: High accuracy, handles missing values  
**Training Time**: Moderate

---

## 📈 Evaluation Metrics Explained

### Classification Metrics
```
┌──────────────────────────────────────────────────────┐
│ METRIC          │ FORMULA        │ INTERPRETATION    │
├──────────────────────────────────────────────────────┤
│ Accuracy        │ (TP+TN)/Total  │ Overall correct   │
│ Precision       │ TP/(TP+FP)     │ Positive accuracy │
│ Recall          │ TP/(TP+FN)     │ Coverage          │
│ F1-Score        │ 2×(P×R)/(P+R)  │ Balanced metric   │
└──────────────────────────────────────────────────────┘

TP = True Positives   FP = False Positives
TN = True Negatives   FN = False Negatives
```

### Confusion Matrix Layout
```
                Predicted
              fast  med  slow
Actual fast   [ TP   FP   FP ]
       med    [ FP   TP   FP ]
       slow   [ FP   FP   TP ]
```

---

## 🔌 Integration Points for Future Phases

### Phase 2 Extension (Prescriptive)
```python
# Add to notebook after Cell 12
def prescriptive_optimization(model, constraints):
    """
    Use SciPy to find optimal parameter configurations
    that maximize performance while meeting constraints.
    """
    from scipy.optimize import minimize
    
    # Define objective function
    def objective(params):
        prediction = model.predict(params.reshape(1, -1))
        return -prediction  # Minimize negative = maximize
    
    # Define constraints
    # ... optimization logic
    
    result = minimize(objective, x0, constraints=constraints)
    return result
```

### Phase 3 Extension (Explainability)
```python
# Add to notebook after Phase 2
def explain_predictions(model, X_test, feature_names):
    """
    Use SHAP and LIME to explain model decisions.
    """
    import shap
    from lime import lime_tabular
    
    # SHAP explanations
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)
    
    # LIME explanations
    lime_explainer = lime_tabular.LimeTabularExplainer(
        X_train, feature_names=feature_names
    )
    
    # Generate explanations
    # ... explanation logic
    
    return shap_values, lime_explanations
```

---

## 🎯 Model Output Format

### Model Package Structure
```python
{
    'model': <trained_model_object>,
    'model_name': 'Random Forest',
    'scaler': <RobustScaler_object>,
    'encoders': {
        'Category': <LabelEncoder>,
        'target': <LabelEncoder>
    },
    'feature_names': [
        'Category', 'Page Size (KB)', 'Load Time(s)',
        'Response Time(s)', 'Throughput',
        'Size_LoadTime_Ratio', 'Total_Time',
        'Throughput_ResponseTime_Ratio',
        'Log_Page_Size', 'Log_Throughput'
    ],
    'metrics': {
        'Accuracy': 0.9234,
        'Precision': 0.9145,
        'Recall': 0.9234,
        'F1-Score': 0.9187
    },
    'timestamp': '20250101_120000'
}
```

---

## 🧪 Testing & Validation

### Validation Strategy
- **Train-Test Split**: 80% training, 20% testing
- **Stratification**: Maintains class balance in split
- **Cross-Validation**: Can be added in future iterations
- **Normalization**: RobustScaler (outlier-resistant)

### Performance Benchmarks
```
Expected Performance Ranges:
├── Excellent:  Accuracy > 90%
├── Good:       Accuracy 80-90%
├── Acceptable: Accuracy 70-80%
└── Needs Work: Accuracy < 70%
```

---

## 📚 Dependencies Graph

```
scikit-learn (1.0.0+)
    ├── Used by: SVM, Random Forest
    ├── Used by: Preprocessing (LabelEncoder, StandardScaler)
    ├── Used by: Metrics (accuracy, precision, recall, F1)
    └── Used by: train_test_split, cross_val_score

xgboost (1.5.0+)
    └── Used by: XGBoost Classifier

pandas (1.3.0+)
    ├── Used by: Data loading
    ├── Used by: Data manipulation
    └── Used by: Results formatting

numpy (1.21.0+)
    ├── Used by: Numerical operations
    └── Used by: Array manipulations

matplotlib (3.4.0+) & seaborn (0.11.0+)
    ├── Used by: Data visualizations
    └── Used by: Results plotting

joblib (1.1.0+)
    └── Used by: Model serialization
```

---

## 🔐 Best Practices Implemented

✅ **Modular Code**: Each function has single responsibility  
✅ **Documentation**: Comprehensive docstrings  
✅ **Error Handling**: Robust data validation  
✅ **Reproducibility**: Fixed random seeds (42)  
✅ **Scalability**: Efficient data structures  
✅ **Maintainability**: Clear variable names  
✅ **Extensibility**: Ready for Phases 2 & 3  
✅ **Version Control**: Timestamped model exports  

---

## 🚀 Performance Optimization Tips

### For Faster Training
```python
# Reduce estimators for quick testing
n_estimators=10  # Instead of 100

# Use fewer features
X_subset = X[:, :5]  # Use only first 5 features

# Smaller dataset for testing
df_sample = df.sample(n=100)  # Use 100 samples
```

### For Better Accuracy
```python
# Hyperparameter tuning with GridSearchCV
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [5, 10, 15],
    'learning_rate': [0.01, 0.1, 0.3]
}

grid_search = GridSearchCV(xgb_model, param_grid, cv=5)
grid_search.fit(X_train, y_train)
best_model = grid_search.best_estimator_
```

---

## 📖 Research Paper Integration

### Tables for Publication
- Model comparison table (ready for LaTeX)
- Feature importance rankings
- Confusion matrices

### Figures for Publication
- Data distribution plots
- Performance comparison charts
- Feature correlation heatmap

### Metrics for Reporting
- Accuracy, Precision, Recall, F1-Score
- Training time per model
- Model complexity (parameters count)

---

## 🎓 Learning Resources

### Understanding the Models
- **SVM**: Support Vector Machines for classification
- **Random Forest**: Ensemble of decision trees
- **XGBoost**: Gradient boosting framework

### Key Concepts
- **Feature Engineering**: Creating new features from existing ones
- **Normalization**: Scaling features to similar ranges
- **Stratification**: Maintaining class balance in splits
- **Cross-Validation**: K-fold validation for robust evaluation

---

**Framework Version**: 1.0 (Phase 1)  
**Last Updated**: November 1, 2025  
**Author**: Research Project - M.Tech  
**Status**: Phase 1 Complete ✅

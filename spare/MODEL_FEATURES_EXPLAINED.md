# Model Features and Predictions Explained

## 📊 Overview

This document explains the input features used for training the predictive model and the output predictions it generates for website performance classification.

---

## 🔢 INPUT FEATURES (What the model learns from)

The model is trained on **10 features total**:

### **Original Features (5 from dataset):**

| Feature | Type | Description | Example Value |
|---------|------|-------------|---------------|
| **Category** | Categorical | Website category (Travel, Social Networking, News, etc.) | Travel |
| **Page Size (KB)** | Numeric | Size of the webpage in kilobytes | 3400.0 KB |
| **Load Time(s)** | Numeric | Time taken to fully load the page | 4.19 seconds |
| **Response Time(s)** | Numeric | Server response time | 0.523 seconds |
| **Throughput** | Numeric | Data transfer rate | 622.58 |

**Note:** Category is encoded as numbers (e.g., Travel=0, News=1) before training.

### **Engineered Features (5 additional calculated features):**

| Feature | Formula | Purpose | Description |
|---------|---------|---------|-------------|
| **Size_LoadTime_Ratio** | `Page Size / Load Time` | Efficiency metric | How much data is loaded per second |
| **Total_Time** | `Response Time + Load Time` | Total wait time | Complete time from request to full load |
| **Throughput_ResponseTime_Ratio** | `Throughput / Response Time` | Efficiency metric | Throughput efficiency relative to response time |
| **Log_Page_Size** | `log(Page Size + 1)` | Normalize large values | Reduces impact of extremely large page sizes |
| **Log_Throughput** | `log(Throughput + 1)` | Normalize large values | Reduces impact of throughput outliers |

---

## 🎯 OUTPUT (What the model predicts)

### **Target Variable: Performance_Label**

The model predicts **one single classification** with **3 possible categories:**

| Prediction | Meaning | Characteristics |
|------------|---------|-----------------|
| **"fast"** | ✅ High Performance | Low load time, high throughput, quick response |
| **"medium"** | ⚠️ Moderate Performance | Average metrics, acceptable performance |
| **"slow"** | ❌ Poor Performance | High load time, low throughput, slow response |

---

## 💡 How It Works - Example Prediction

### **Input Example:**
```
Category            = Travel (encoded as 0)
Page Size (KB)      = 3400.0
Load Time(s)        = 4.19
Response Time(s)    = 0.523
Throughput          = 622.58

Calculated Features:
Size_LoadTime_Ratio           = 3400.0 / 4.19 = 811.46
Total_Time                    = 0.523 + 4.19 = 4.713
Throughput_ResponseTime_Ratio = 622.58 / 0.523 = 1190.33
Log_Page_Size                 = log(3400.0 + 1) = 8.13
Log_Throughput                = log(622.58 + 1) = 6.44
```

### **Model Prediction:**
```
Performance_Label = "medium"
```

**Interpretation:** *"Based on these 10 features, this website has MEDIUM performance"*

---

## 📈 Model Training and Testing Process

### **1. Data Split:**
- **80% Training Data** (589 websites) - Model learns patterns
- **20% Testing Data** (147 websites) - Model makes predictions

### **2. Training Phase:**
The model learns patterns like:
- "When Load Time > 3s AND Throughput < 100 → likely 'slow'"
- "When Response Time < 0.5s AND Page Size < 2000 → likely 'fast'"
- "When Total_Time is moderate → likely 'medium'"

### **3. Testing Phase:**
For each website in the test set:

```
Input:  10 features → [0, 3400.0, 4.19, 0.523, 622.58, 811.46, 4.713, 1190.33, 8.13, 6.44]
Output: Predicted class → "medium"
Actual: True label → "medium" ✅ Correct!
```

### **4. Accuracy Calculation:**

```
Website 1: Predicted = "fast"    | Actual = "fast"    | ✅ Correct
Website 2: Predicted = "medium"  | Actual = "slow"    | ❌ Wrong
Website 3: Predicted = "slow"    | Actual = "slow"    | ✅ Correct
Website 4: Predicted = "fast"    | Actual = "fast"    | ✅ Correct
...
Website 147: Predicted = "medium" | Actual = "medium" | ✅ Correct

Accuracy = (Correct Predictions / Total Predictions) × 100
         = (136 / 147) × 100
         = 92.5%
```

---

## 🔍 Evaluation Metrics

The model is evaluated using multiple metrics:

### **Classification Metrics:**

| Metric | Description | Formula |
|--------|-------------|---------|
| **Accuracy** | Overall correctness | `(TP + TN) / Total` |
| **Precision** | Accuracy of positive predictions | `TP / (TP + FP)` |
| **Recall** | Coverage of actual positives | `TP / (TP + FN)` |
| **F1-Score** | Harmonic mean of precision & recall | `2 × (Precision × Recall) / (Precision + Recall)` |

**Legend:**
- TP = True Positives (Correctly predicted as positive)
- TN = True Negatives (Correctly predicted as negative)
- FP = False Positives (Incorrectly predicted as positive)
- FN = False Negatives (Incorrectly predicted as negative)

---

## 🤖 Models Used

Three machine learning algorithms are trained and compared:

| Model | Type | Strengths |
|-------|------|-----------|
| **SVM** (Support Vector Machine) | Non-linear classifier | Good with high-dimensional data |
| **Random Forest** | Ensemble of decision trees | Robust, provides feature importance |
| **XGBoost** | Gradient boosting | High accuracy, handles missing values |

The model with the **highest accuracy** is automatically selected and saved.

---

## 📊 Feature Importance

After training, the model identifies which features are most important for predictions:

**Example Feature Importance Rankings:**
1. **Load Time(s)** - 25% importance
2. **Throughput** - 20% importance
3. **Response Time(s)** - 18% importance
4. **Total_Time** - 15% importance
5. **Page Size (KB)** - 12% importance
6. ...and so on

This tells us that **Load Time** and **Throughput** are the most critical factors in determining website performance.

---

## 🎯 What the Model Actually Does

### **In Simple Terms:**

**Purpose:** Automatically classify website performance into categories

**Input:** 10 website performance metrics (features)

**Output:** One prediction → "fast", "medium", or "slow"

**Use Case:** 
- Identify slow-performing websites for optimization
- Monitor website performance automatically
- Predict performance before deployment
- Benchmark against industry standards

### **Real-World Application:**

```python
# Load saved model
model = joblib.load('best_model_random_forest_20251101_141600.joblib')

# New website data
new_website = [
    [0, 2500.0, 2.1, 0.35, 850.0, 1190.48, 2.45, 2428.57, 7.82, 6.75]
]

# Predict performance
prediction = model.predict(new_website)
print(f"Performance: {prediction[0]}")  # Output: "fast"
```

---

## 📝 Summary

| Aspect | Details |
|--------|---------|
| **Problem Type** | Multi-class Classification |
| **Number of Classes** | 3 (fast, medium, slow) |
| **Input Features** | 10 features (5 original + 5 engineered) |
| **Output** | 1 prediction (performance category) |
| **Dataset Size** | 736 websites |
| **Train/Test Split** | 80% / 20% |
| **Best Model** | Random Forest (expected ~92% accuracy) |
| **Evaluation** | Accuracy, Precision, Recall, F1-Score |

---

## 🔮 Key Takeaways

1. **Input:** The model uses 10 numerical features derived from website performance metrics
2. **Output:** The model predicts one of three performance categories
3. **Process:** It learns patterns from 80% of the data and tests on 20%
4. **Accuracy:** Measured by comparing predictions to actual labels
5. **Purpose:** Automated website performance classification for optimization

---

**Document Version:** 1.0  
**Last Updated:** November 16, 2025  
**Project:** Phase 1 - Predictive Model Development  
**Repository:** MTech_Dissertation

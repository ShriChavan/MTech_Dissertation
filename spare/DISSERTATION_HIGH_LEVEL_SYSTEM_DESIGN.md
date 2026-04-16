# Proposed High-Level System Design

## 1. Introduction

This document presents the high-level system design for the **Predictive-Prescriptive-Explainable AI Framework for Web Performance Optimization**. The framework is architected as a three-phase modular system that integrates machine learning, optimization algorithms, and explainable AI techniques to provide actionable insights for improving website performance.

The system follows a layered architecture approach where each phase builds upon the outputs of previous phases while maintaining loose coupling to enable independent development, testing, and deployment.

---

## 2. System Architecture Overview

### 2.1 Architectural Pattern

The system employs a **Pipeline Architecture** combined with a **Layered Architecture** pattern. This hybrid approach enables:

- **Sequential data flow** through predictive, prescriptive, and explainability stages
- **Modular separation** of concerns for data processing, model training, optimization, and explanation
- **Extensibility** for future enhancements without disrupting existing functionality
- **Maintainability** through clear component boundaries and interfaces

### 2.2 Design Principles

The architecture is guided by the following principles:

1. **Modularity**: Each phase operates as an independent module with well-defined inputs and outputs
2. **Scalability**: System can handle datasets ranging from hundreds to thousands of websites
3. **Reproducibility**: All operations are deterministic with fixed random seeds and versioned outputs
4. **Extensibility**: New models, optimization algorithms, or explanation methods can be added without redesigning the core
5. **Robustness**: Comprehensive error handling and validation at each stage
6. **Transparency**: Full audit trail of data transformations, model decisions, and recommendations

---

## 3. System Components

### 3.1 Three-Phase Architecture

The system is organized into three primary phases:

#### **Phase 1: Predictive Modeling Layer**
- **Purpose**: Build machine learning models to predict website performance classifications
- **Input**: Historical website performance dataset (Kaggle dataset)
- **Output**: Trained classification models with performance metrics
- **Status**: ✅ **Implemented**

#### **Phase 2: Data Augmentation Layer**
- **Purpose**: Enrich dataset with real-time performance metrics from live websites
- **Input**: URLs from original dataset
- **Output**: Augmented dataset with additional 16+ performance features
- **Status**: ✅ **Implemented**

#### **Phase 3: Prescriptive Optimization and Explainability Layer** *(Planned)*
- **Purpose**: Generate optimization recommendations with interpretable explanations
- **Input**: Trained models + augmented dataset
- **Output**: Actionable recommendations with explanations
- **Status**: 🔄 **In Design**

---

## 4. Detailed Component Design

### 4.1 Phase 1: Predictive Modeling Layer

#### 4.1.1 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    PREDICTIVE MODELING LAYER                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────┐      ┌──────────────┐      ┌─────────────┐ │
│  │ Data Loading  │  →   │ Exploratory  │  →   │   Data      │ │
│  │   Module      │      │     Data     │      │Preprocessing│ │
│  │               │      │   Analysis   │      │   Module    │ │
│  └───────────────┘      └──────────────┘      └─────────────┘ │
│         ↓                                            ↓          │
│  ┌───────────────┐      ┌──────────────┐      ┌─────────────┐ │
│  │   Feature     │  ←   │ Train-Test   │  ←   │   Feature   │ │
│  │ Importance    │      │    Split     │      │ Engineering │ │
│  │  Analysis     │      │              │      │             │ │
│  └───────────────┘      └──────────────┘      └─────────────┘ │
│         ↓                                            ↓          │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │              Model Training Ensemble                       │ │
│  │  ┌─────────┐  ┌──────────────┐  ┌──────────────┐        │ │
│  │  │   SVM   │  │ Random Forest│  │   XGBoost    │        │ │
│  │  │  (RBF)  │  │  (100 trees) │  │ (Gradient    │        │ │
│  │  │         │  │              │  │  Boosting)   │        │ │
│  │  └─────────┘  └──────────────┘  └──────────────┘        │ │
│  └───────────────────────────────────────────────────────────┘ │
│         ↓                      ↓                      ↓          │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │              Model Evaluation & Comparison                │ │
│  │  • Accuracy    • Precision    • Recall    • F1-Score     │ │
│  │  • Confusion Matrix    • Feature Importance              │ │
│  └───────────────────────────────────────────────────────────┘ │
│         ↓                                                       │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │         Best Model Selection & Persistence                │ │
│  │  • Model Object    • Scaler    • Encoders                │ │
│  │  • Feature Names   • Metrics   • Timestamp               │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 4.1.2 Key Components

**Data Loading Module**
- **Functionality**: Loads CSV dataset and validates schema
- **Technologies**: Pandas
- **Output**: DataFrame with 736 website records

**Exploratory Data Analysis Module**
- **Functionality**: Statistical analysis, distribution visualization, correlation analysis
- **Technologies**: Pandas, Matplotlib, Seaborn
- **Output**: Insights on data quality, distributions, and relationships

**Data Preprocessing Module**
- **Functionality**: 
  - Missing value imputation (median for numeric, mode for categorical)
  - Categorical encoding (Label Encoding)
  - Target variable encoding
  - Irrelevant column removal (Sr No, website_url)
- **Technologies**: Scikit-learn (SimpleImputer, LabelEncoder)
- **Output**: Clean, encoded feature matrix and target vector

**Feature Engineering Module**
- **Functionality**: Creates derived features
  - Ratio features: `Size_LoadTime_Ratio`, `Throughput_ResponseTime_Ratio`
  - Temporal features: `Total_Time`
  - Log transformations: `Log_Page_Size`, `Log_Throughput`
- **Technologies**: NumPy, Pandas
- **Output**: Enhanced feature set (10 features from 5 original)

**Train-Test Split Module**
- **Functionality**: 
  - Stratified 80/20 split to maintain class balance
  - RobustScaler normalization (outlier-resistant)
- **Technologies**: Scikit-learn
- **Output**: Training set (588 samples), Test set (148 samples)

**Model Training Ensemble**
- **Models**:
  1. **Support Vector Machine (SVM)**: RBF kernel for non-linear classification
  2. **Random Forest**: 100 decision trees with parallel training
  3. **XGBoost**: Gradient boosting with regularization
- **Technologies**: Scikit-learn, XGBoost
- **Training Strategy**: Train all models on identical data splits for fair comparison

**Model Evaluation Module**
- **Metrics**: Accuracy, Precision, Recall, F1-Score (weighted average)
- **Visualizations**: Confusion matrices, performance comparison charts
- **Selection Criteria**: Highest accuracy with balanced precision-recall

**Model Persistence Module**
- **Functionality**: Serializes best model with all preprocessing artifacts
- **Format**: Joblib (primary), Pickle (backup)
- **Package Contents**: Model object, scaler, encoders, feature names, metrics, timestamp

#### 4.1.3 Data Flow

```
Raw CSV (736 records × 9 features)
    ↓
Cleaned Data (736 records × 5 features)
    ↓
Engineered Features (736 records × 10 features)
    ↓
Normalized Data (588 train + 148 test × 10 features)
    ↓
3 Trained Models → Evaluation → Best Model (Random Forest/XGBoost)
    ↓
Serialized Model Package (.joblib + .pkl)
```

---

### 4.2 Phase 2: Data Augmentation Layer

#### 4.2.1 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  DATA AUGMENTATION LAYER                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────┐      ┌──────────────┐      ┌─────────────┐ │
│  │  Load URLs    │  →   │ Google       │  →   │  API        │ │
│  │  from Phase 1 │      │ PageSpeed    │      │  Request    │ │
│  │   Dataset     │      │ Insights API │      │  Manager    │ │
│  └───────────────┘      └──────────────┘      └─────────────┘ │
│         ↓                                            ↓          │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │           Feature Extraction Pipeline                    │  │
│  │                                                           │  │
│  │  ┌────────────────────┐    ┌─────────────────────────┐ │  │
│  │  │ Core Web Vitals    │    │  Resource Metrics       │ │  │
│  │  │ • LCP, FCP, CLS    │    │  • Total bytes          │ │  │
│  │  │ • TTI, TBT         │    │  • Request count        │ │  │
│  │  │ • Speed Index      │    │  • DOM size             │ │  │
│  │  └────────────────────┘    └─────────────────────────┘ │  │
│  │                                                           │  │
│  │  ┌────────────────────┐    ┌─────────────────────────┐ │  │
│  │  │ Performance Score  │    │  Optimization Checks    │ │  │
│  │  │ • Lighthouse score │    │  • Text compression     │ │  │
│  │  │ • Desktop strategy │    │  • Render blocking      │ │  │
│  │  │                    │    │  • HTTP/2, WebP, etc.   │ │  │
│  │  └────────────────────┘    └─────────────────────────┘ │  │
│  └─────────────────────────────────────────────────────────┘  │
│         ↓                                                       │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │         Batch Processing with Progress Tracking          │ │
│  │  • Rate limiting (0.5s delay)  • Timeout handling (60s)  │ │
│  │  • Retry logic                 • Error logging           │ │
│  │  • Progress visualization      • ETA calculation         │ │
│  └───────────────────────────────────────────────────────────┘ │
│         ↓                                                       │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │              Dataset Merging & Validation                 │ │
│  │  • Join on URL key        • Validate completeness        │ │
│  │  • Quality assessment     • Missing value analysis       │ │
│  └───────────────────────────────────────────────────────────┘ │
│         ↓                                                       │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │         Augmented Dataset Export                          │ │
│  │  • Original features (5) + Augmented features (16)        │ │
│  │  • Total: 21+ features per website                        │ │
│  │  • Timestamped CSV output                                 │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 4.2.2 Key Components

**URL Extraction Module**
- **Functionality**: Extracts valid URLs from Phase 1 dataset
- **Validation**: Protocol check (http/https), duplicate removal, null filtering
- **Output**: List of 736 unique URLs

**Google PageSpeed Insights API Integration**
- **API Endpoint**: `https://www.googleapis.com/pagespeedonline/v5/runPagespeed`
- **Strategy**: Desktop analysis (faster than mobile)
- **Categories**: Performance-only (optimized for speed)
- **Authentication**: API key-based

**Feature Extraction Engine**

*Core Web Vitals Extraction*
- **LCP (Largest Contentful Paint)**: Time to render largest content element
- **FCP (First Contentful Paint)**: Time to first visible content
- **CLS (Cumulative Layout Shift)**: Visual stability metric
- **TTI (Time to Interactive)**: Time until page is fully interactive
- **TBT (Total Blocking Time)**: Main thread blocking time
- **Speed Index**: Visual loading speed

*Performance Metrics*
- **Performance Score**: Lighthouse performance score (0-100)
- **Total Byte Weight**: Total page size in KB
- **Request Count**: Number of HTTP requests
- **DOM Size**: Total DOM elements

*Optimization Audits*
- **Text Compression**: Gzip/Brotli usage
- **Render Blocking Resources**: CSS/JS blocking render
- **Unused JavaScript**: Dead code detection
- **HTTP/2**: Protocol version check
- **Modern Image Formats**: WebP/AVIF usage

**Batch Processing Controller**
- **Rate Limiting**: 0.5 second delay between requests
- **Timeout Management**: 60-second timeout per request
- **Retry Logic**: Automatic retry on transient failures
- **Progress Tracking**: Real-time progress bar with ETA
- **Error Handling**: Graceful failure with detailed error messages

**Data Merging Pipeline**
- **Join Strategy**: Left join on `website_url` key
- **Validation**: Success rate calculation, missing value analysis
- **Quality Metrics**: Feature completeness assessment

**Export Module**
- **Format**: CSV with timestamp
- **Metadata**: Extraction timestamp, success flags, error messages
- **Versioning**: Automatic timestamped filename

#### 4.2.3 Data Flow

```
Original Dataset (736 URLs)
    ↓
API Requests (rate-limited, with retries)
    ↓
Raw API Responses (JSON)
    ↓
Feature Extraction (16 features per URL)
    ↓
Augmented Features DataFrame (736 × 16)
    ↓
Merge with Original (736 × 21+)
    ↓
Augmented Dataset CSV (timestamped export)
```

#### 4.2.4 Performance Optimization

- **Desktop Strategy**: ~30% faster than mobile analysis
- **Performance-Only Category**: Reduces API response time by 60%
- **Parallel Processing**: Could be implemented for faster throughput
- **Caching**: API responses could be cached to avoid redundant calls
- **Estimated Processing Time**: 
  - 10 URLs: ~5-10 minutes
  - 100 URLs: ~1 hour
  - 736 URLs: ~30-60 minutes

---

### 4.3 Phase 3: Prescriptive Optimization & Explainability Layer (Planned)

#### 4.3.1 Conceptual Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│          PRESCRIPTIVE OPTIMIZATION & EXPLAINABILITY LAYER       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────┐      ┌──────────────┐      ┌─────────────┐ │
│  │ Load Trained  │  →   │ Load         │  →   │  Define     │ │
│  │ Model from    │      │ Augmented    │      │ Optimization│ │
│  │  Phase 1      │      │  Dataset     │      │  Objectives │ │
│  └───────────────┘      └──────────────┘      └─────────────┘ │
│         ↓                                            ↓          │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │              SciPy Optimization Engine                   │  │
│  │                                                           │  │
│  │  ┌─────────────────────────────────────────────────┐   │  │
│  │  │  Objective Function                              │   │  │
│  │  │  • Maximize performance score                    │   │  │
│  │  │  • Minimize load time                            │   │  │
│  │  │  • Improve Core Web Vitals                       │   │  │
│  │  └─────────────────────────────────────────────────┘   │  │
│  │                                                           │  │
│  │  ┌─────────────────────────────────────────────────┐   │  │
│  │  │  Constraint Definitions                          │   │  │
│  │  │  • Budget constraints (max page size)            │   │  │
│  │  │  • Technical constraints (min requests)          │   │  │
│  │  │  • User experience constraints (max load time)   │   │  │
│  │  └─────────────────────────────────────────────────┘   │  │
│  │                                                           │  │
│  │  ┌─────────────────────────────────────────────────┐   │  │
│  │  │  Optimization Algorithms                         │   │  │
│  │  │  • Sequential Least Squares (SLSQP)             │   │  │
│  │  │  • Trust Region Constrained                      │   │  │
│  │  │  • Differential Evolution                        │   │  │
│  │  └─────────────────────────────────────────────────┘   │  │
│  └─────────────────────────────────────────────────────────┘  │
│         ↓                                                       │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │         Explainability Engine (SHAP + LIME)               │ │
│  │                                                           │ │
│  │  ┌────────────────────┐    ┌─────────────────────────┐ │ │
│  │  │  SHAP Analysis     │    │  LIME Analysis          │ │ │
│  │  │  • Global feature  │    │  • Local instance       │ │ │
│  │  │    importance      │    │    explanations         │ │ │
│  │  │  • Feature         │    │  • Decision boundaries  │ │ │
│  │  │    interactions    │    │  • Counterfactual       │ │ │
│  │  │  • Dependence      │    │    explanations         │ │ │
│  │  │    plots           │    │                         │ │ │
│  │  └────────────────────┘    └─────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────┘ │
│         ↓                                                       │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │         Recommendation Generation Engine                  │ │
│  │                                                           │ │
│  │  • Optimal parameter configurations                      │ │
│  │  • Prioritized action items                              │ │
│  │  • Expected performance improvements                     │ │
│  │  • Implementation difficulty scores                      │ │
│  │  • Cost-benefit analysis                                 │ │
│  └───────────────────────────────────────────────────────────┘ │
│         ↓                                                       │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │              Report Generation Module                     │ │
│  │  • PDF/HTML reports with visualizations                  │ │
│  │  • Interactive dashboards                                │ │
│  │  • API endpoints for programmatic access                 │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 4.3.2 Planned Components

**SciPy Optimization Engine**
- **Objective**: Find optimal feature values that maximize performance
- **Algorithms**: SLSQP, Trust-Region, Differential Evolution
- **Constraints**: User-defined bounds and linear/non-linear constraints
- **Output**: Optimal parameter vectors

**SHAP (SHapley Additive exPlanations) Module**
- **Functionality**: Global model interpretability
- **Visualizations**: Feature importance, dependence plots, force plots
- **Output**: Feature contribution scores

**LIME (Local Interpretable Model-agnostic Explanations) Module**
- **Functionality**: Local instance-level explanations
- **Visualizations**: Decision boundaries, feature weights
- **Output**: Human-readable explanations for individual predictions

**Recommendation Engine**
- **Functionality**: Translates optimization results into actionable recommendations
- **Prioritization**: Based on impact, effort, and cost
- **Output**: Ranked list of improvements with expected outcomes

**Report Generation Module**
- **Formats**: PDF, HTML, JSON
- **Content**: Recommendations, explanations, visualizations, metrics
- **Distribution**: Email, API, dashboard

---

## 5. Data Architecture

### 5.1 Data Flow Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                        DATA FLOW ARCHITECTURE                  │
└────────────────────────────────────────────────────────────────┘

[Raw Dataset]
    │ (website_performance_dataset.csv)
    │ 736 records × 9 features
    │
    ▼
┌─────────────────┐
│   PHASE 1:      │
│  PREDICTIVE     │
│   MODELING      │
└─────────────────┘
    │
    ├─► [Cleaned Data] → [Engineered Features] → [Normalized Data]
    │
    ├─► [Training Set: 588 samples] ──┐
    │                                  │
    ├─► [Test Set: 148 samples] ──────┼──► [Model Training]
    │                                  │      SVM, RF, XGBoost
    │                                  │
    └─► [Best Model Package] ◄────────┘
         • Model object (.joblib)
         • Scaler, Encoders
         • Feature names
         • Performance metrics
                │
                ▼
        [Model Persistence Storage]
                │
                │
[URL List] ◄────┘
    │ 736 URLs extracted
    │
    ▼
┌─────────────────┐
│   PHASE 2:      │
│     DATA        │
│  AUGMENTATION   │
└─────────────────┘
    │
    ├─► [Google PageSpeed API] → [Raw API Responses]
    │                                     │
    │                                     ▼
    │                            [Feature Extraction]
    │                              • 16 new features
    │                                     │
    │                                     ▼
    │                            [Augmented Features]
    │                                     │
    └─────────────────────────────────────┤
                                          │
                                          ▼
                                   [Dataset Merge]
                                   Original + Augmented
                                          │
                                          ▼
                              [Augmented Dataset CSV]
                              736 records × 21+ features
                                          │
                                          │
        [Best Model] ◄────────────────────┤
              │                           │
              ▼                           ▼
┌─────────────────────────────────────────────────────┐
│              PHASE 3: PRESCRIPTIVE                  │
│         OPTIMIZATION & EXPLAINABILITY               │
└─────────────────────────────────────────────────────┘
              │
              ├─► [Optimization Engine (SciPy)]
              │        │
              │        ▼
              │   [Optimal Configurations]
              │        │
              ├─► [Explainability (SHAP/LIME)]
              │        │
              │        ▼
              │   [Feature Explanations]
              │        │
              └────────┴──────► [Recommendation Engine]
                                        │
                                        ▼
                                [Final Reports]
                                • PDF/HTML
                                • Interactive dashboards
                                • API responses
```

### 5.2 Data Schema Evolution

#### **Phase 1 Input Schema**
```
website_performance_dataset.csv (736 × 9)
├── Sr No              : Integer (identifier)
├── website_url        : String (URL)
├── Category           : String (website type)
├── Page Size (KB)     : Float (page weight)
├── Load Time(s)       : Float (loading time)
├── Response Time(s)   : Float (server response)
├── Throughput         : Float (data transfer rate)
├── Performance_Label  : String (fast/medium/slow)
└── User Response      : String (Fast/Medium/Slow)
```

#### **Phase 1 Output Schema (Engineered)**
```
Engineered Features (736 × 10)
├── Category                        : Integer (encoded)
├── Page Size (KB)                  : Float (normalized)
├── Load Time(s)                    : Float (normalized)
├── Response Time(s)                : Float (normalized)
├── Throughput                      : Float (normalized)
├── Size_LoadTime_Ratio             : Float (computed)
├── Total_Time                      : Float (computed)
├── Throughput_ResponseTime_Ratio   : Float (computed)
├── Log_Page_Size                   : Float (computed)
└── Log_Throughput                  : Float (computed)
```

#### **Phase 2 Output Schema (Augmented)**
```
Augmented Dataset (736 × 21+)
├── [Original 5 features]
├── [Engineered 5 features]
└── [Augmented 16 features]
    ├── performance_score           : Float (0-100)
    ├── lcp                         : Float (milliseconds)
    ├── fcp                         : Float (milliseconds)
    ├── cls                         : Float (0-1 scale)
    ├── tti                         : Float (milliseconds)
    ├── tbt                         : Float (milliseconds)
    ├── speed_index                 : Float (milliseconds)
    ├── total_byte_weight           : Float (KB)
    ├── num_requests                : Integer (count)
    ├── dom_size                    : Integer (elements)
    ├── uses_text_compression       : Boolean (0/1)
    ├── render_blocking_resources   : Boolean (0/1)
    ├── unused_js                   : Boolean (0/1)
    ├── uses_http2                  : Boolean (0/1)
    ├── modern_image_formats        : Boolean (0/1)
    └── extraction_successful       : Boolean (0/1)
```

---

## 6. Technology Stack

### 6.1 Core Technologies

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Language** | Python | 3.8+ | Primary development language |
| **Data Processing** | Pandas | 1.5+ | Data manipulation and analysis |
| **Numerical Computing** | NumPy | 1.23+ | Array operations and mathematics |
| **Machine Learning** | Scikit-learn | 1.0+ | Model training and evaluation |
| **Gradient Boosting** | XGBoost | 1.5+ | Advanced ML models |
| **Optimization** | SciPy | 1.9+ | (Phase 3) Optimization algorithms |
| **Explainability** | SHAP | 0.41+ | (Phase 3) Model interpretability |
| **Explainability** | LIME | 0.2+ | (Phase 3) Local explanations |
| **Visualization** | Matplotlib | 3.4+ | Static plots and charts |
| **Visualization** | Seaborn | 0.11+ | Statistical visualizations |
| **API Client** | Requests | 2.28+ | HTTP requests to PageSpeed API |
| **Progress Tracking** | tqdm | 4.64+ | Progress bars |
| **Serialization** | Joblib | 1.1+ | Model persistence |
| **Development** | Jupyter | Latest | Interactive development |

### 6.2 External Services

| Service | Provider | Purpose | Phase |
|---------|----------|---------|-------|
| **PageSpeed Insights API** | Google | Performance metrics extraction | Phase 2 |
| **Cloud Storage** | (TBD) | Model and data versioning | Future |
| **Dashboard Platform** | (TBD) | Interactive reporting | Phase 3 |

---

## 7. System Integration Points

### 7.1 Inter-Phase Communication

**Phase 1 → Phase 2**
- **Data**: URL list extracted from original dataset
- **Format**: List of strings
- **Validation**: URL format validation, duplicate removal

**Phase 2 → Phase 3**
- **Data**: Augmented dataset CSV
- **Format**: CSV file with 21+ columns
- **Validation**: Feature completeness check, data type validation

**Phase 1 → Phase 3**
- **Data**: Trained model package
- **Format**: Joblib serialized dictionary
- **Contents**: Model, scaler, encoders, feature names, metrics

### 7.2 External API Integration

**Google PageSpeed Insights API**
- **Endpoint**: `https://www.googleapis.com/pagespeedonline/v5/runPagespeed`
- **Authentication**: API key (query parameter)
- **Rate Limit**: 25,000 requests/day (free tier)
- **Response Format**: JSON
- **Error Handling**: Retry logic with exponential backoff

---

## 8. Quality Assurance Strategy

### 8.1 Data Quality

**Validation Checkpoints**
1. **Input Validation**: Schema validation, null checks, data type verification
2. **Processing Validation**: Feature distribution checks, outlier detection
3. **Output Validation**: Completeness checks, range validation

**Quality Metrics**
- Data completeness rate (target: >95%)
- Feature extraction success rate (target: >80%)
- Model prediction confidence (target: >0.7 for top prediction)

### 8.2 Model Quality

**Training Validation**
- Stratified k-fold cross-validation
- Train/test split validation
- Hyperparameter tuning with grid search

**Performance Benchmarks**
- Accuracy: >85% (target for all models)
- Precision/Recall balance: F1-Score >0.85
- No significant class imbalance (<20% difference)

### 8.3 System Testing

**Unit Testing**
- Individual function testing
- Edge case handling
- Error condition testing

**Integration Testing**
- Phase-to-phase data flow
- API integration testing
- Model loading and prediction testing

**End-to-End Testing**
- Complete pipeline execution
- Performance benchmarking
- Output validation

---

## 9. Scalability Considerations

### 9.1 Data Scalability

**Current Capacity**
- Dataset size: 736 websites
- Processing time: ~1 hour (Phase 2)
- Storage: <10 MB

**Scaling Strategy**
- **Horizontal Scaling**: Parallel API requests using multiprocessing
- **Batch Processing**: Process in chunks to manage memory
- **Caching**: Redis/Memcached for API response caching
- **Database**: Migrate from CSV to PostgreSQL/MongoDB for larger datasets

**Projected Capacity**
- Target: 10,000+ websites
- Estimated time with parallelization: ~2-3 hours
- Storage: ~100 MB

### 9.2 Computational Scalability

**Model Training**
- Current: Single machine (CPU-based)
- Future: GPU-accelerated training for deep learning models
- Cloud: AWS SageMaker or Google Cloud AI Platform

**Optimization**
- Current: Sequential optimization
- Future: Parallel optimization with multiple workers
- Distributed: Apache Spark for large-scale optimization

---

## 10. Security and Privacy Considerations

### 10.1 Data Security

**Sensitive Data Handling**
- API keys stored in environment variables (not hardcoded)
- No personal user data collected
- Website URLs are public information

**Access Control**
- Model files access-controlled
- API rate limiting to prevent abuse
- Audit logs for data access

### 10.2 Privacy Compliance

**Data Collection**
- Only publicly available website performance data
- No user tracking or personal information
- Compliance with website terms of service

**Data Retention**
- Temporary storage during processing
- Configurable retention policies
- Secure deletion of intermediate files

---

## 11. Deployment Architecture (Future)

### 11.1 Deployment Options

**Option 1: Local Desktop Application**
- Jupyter Notebook-based (current)
- Suitable for: Research, development, small-scale analysis
- Limitations: Manual execution, no automation

**Option 2: Web Application**
- Flask/FastAPI backend
- React/Vue frontend
- Suitable for: Internal teams, medium-scale analysis
- Features: User authentication, scheduled jobs, reporting dashboard

**Option 3: Cloud-Native Microservices**
- Containerized services (Docker)
- Kubernetes orchestration
- Suitable for: Enterprise deployment, high scalability
- Features: Auto-scaling, high availability, distributed processing

### 11.2 Recommended Architecture (Future)

```
┌─────────────────────────────────────────────────────────────┐
│                    CLOUD DEPLOYMENT                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐      ┌──────────────┐      ┌──────────┐  │
│  │   Web UI    │ ←──→ │  API Gateway │ ←──→ │  Auth    │  │
│  │  (React)    │      │  (FastAPI)   │      │ Service  │  │
│  └─────────────┘      └──────────────┘      └──────────┘  │
│                              │                              │
│         ┌────────────────────┼────────────────────┐        │
│         ▼                    ▼                    ▼         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │ Prediction   │  │ Augmentation │  │ Optimization │    │
│  │  Service     │  │   Service    │  │   Service    │    │
│  │ (Container)  │  │ (Container)  │  │ (Container)  │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
│         │                    │                    │         │
│         └────────────────────┼────────────────────┘        │
│                              ▼                              │
│                    ┌──────────────────┐                    │
│                    │   Data Storage   │                    │
│                    │  (PostgreSQL)    │                    │
│                    └──────────────────┘                    │
│                              │                              │
│                    ┌──────────────────┐                    │
│                    │  Model Registry  │                    │
│                    │   (S3/GCS)       │                    │
│                    └──────────────────┘                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 12. Monitoring and Maintenance

### 12.1 System Monitoring

**Performance Metrics**
- API response times
- Model inference latency
- Feature extraction success rate
- System resource utilization

**Logging Strategy**
- Application logs (INFO, WARNING, ERROR levels)
- Audit logs for data operations
- Performance logs for optimization

**Alerting**
- API failure rate >20%
- Model accuracy degradation >5%
- System resource >80% utilization

### 12.2 Model Maintenance

**Retraining Strategy**
- Schedule: Quarterly or when accuracy drops >5%
- Trigger: New data availability or significant performance drift
- Validation: A/B testing before deployment

**Version Control**
- Model versioning with semantic versioning (v1.0.0)
- Dataset versioning with timestamps
- Code versioning with Git

---

## 13. Extensibility and Future Enhancements

### 13.1 Planned Extensions

**Phase 3 Enhancements**
1. **Multi-Objective Optimization**: Balance performance, cost, and user experience
2. **Sensitivity Analysis**: Understand parameter impact ranges
3. **What-If Scenarios**: Interactive exploration of optimization trade-offs

**Phase 4 (Future)**
1. **Real-Time Monitoring**: Continuous performance tracking
2. **Automated Remediation**: Auto-apply optimizations
3. **Competitive Analysis**: Compare against competitor websites
4. **Mobile Optimization**: Separate mobile performance analysis

### 13.2 Integration Opportunities

**Third-Party Tools**
- **GTmetrix API**: Additional performance metrics
- **WebPageTest API**: Advanced waterfall analysis
- **Lighthouse CI**: Continuous performance tracking
- **Sentry**: Error tracking and monitoring
- **Grafana**: Performance dashboards

**Machine Learning Enhancements**
- Deep learning models (LSTM for time-series prediction)
- Ensemble methods (stacking, blending)
- AutoML for hyperparameter optimization
- Federated learning for privacy-preserving training

---

## 14. Conclusion

The Predictive-Prescriptive-Explainable AI Framework represents a comprehensive solution for website performance optimization. The modular, three-phase architecture ensures:

1. **Scalability**: Easily handle growing datasets and increased complexity
2. **Maintainability**: Clear separation of concerns enables independent development
3. **Extensibility**: Well-defined interfaces allow seamless integration of new features
4. **Robustness**: Comprehensive error handling and validation throughout
5. **Transparency**: Full auditability and explainability of recommendations

With Phase 1 (Predictive Modeling) and Phase 2 (Data Augmentation) successfully implemented, the foundation is solid for Phase 3 (Prescriptive Optimization and Explainability), which will complete the end-to-end framework.

---

## 15. References and Documentation

### 15.1 Technical Documentation

- **Scikit-learn Documentation**: https://scikit-learn.org/
- **XGBoost Documentation**: https://xgboost.readthedocs.io/
- **SHAP Documentation**: https://shap.readthedocs.io/
- **LIME Documentation**: https://lime-ml.readthedocs.io/
- **SciPy Optimization**: https://docs.scipy.org/doc/scipy/reference/optimize.html
- **Google PageSpeed Insights API**: https://developers.google.com/speed/docs/insights/v5/get-started

### 15.2 Research Papers

- Ribeiro et al. (2016). "Why Should I Trust You?" Explaining the Predictions of Any Classifier
- Lundberg & Lee (2017). A Unified Approach to Interpreting Model Predictions
- Chen & Guestrin (2016). XGBoost: A Scalable Tree Boosting System
- Nocedal & Wright (2006). Numerical Optimization

---

**Document Version**: 1.0  
**Last Updated**: November 20, 2025  
**Author**: M.Tech Dissertation Research Project  
**Status**: Phase 1 & 2 Complete, Phase 3 In Design

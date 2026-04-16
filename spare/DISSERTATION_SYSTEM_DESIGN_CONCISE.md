# Proposed High-Level System Design

## 1. System Overview

The **Predictive-Prescriptive-Explainable AI Framework for Web Performance Optimization** is architected as a three-phase modular pipeline that integrates machine learning, optimization algorithms, and explainable AI techniques. The system employs a hybrid **Pipeline and Layered Architecture** pattern, enabling sequential data flow through predictive, prescriptive, and explainability stages while maintaining modular separation of concerns.

### 1.1 Design Principles

- **Modularity**: Independent phases with well-defined inputs and outputs
- **Scalability**: Handles datasets from hundreds to thousands of websites
- **Reproducibility**: Deterministic operations with fixed random seeds
- **Extensibility**: New models/algorithms integrate seamlessly
- **Transparency**: Full audit trail and explainable recommendations

---

## 2. Three-Phase Architecture

### Phase 1: Predictive Modeling Layer (✅ Implemented)

**Purpose**: Build machine learning models to predict website performance classifications

**Key Components**:
- **Data Preprocessing**: Missing value imputation (median/mode), label encoding, outlier removal
- **Feature Engineering**: Creates 5 derived features (ratio, temporal, log transformations)
  - `Size_LoadTime_Ratio`, `Total_Time`, `Throughput_ResponseTime_Ratio`
  - `Log_Page_Size`, `Log_Throughput`
- **Model Ensemble**: Three classifiers trained on identical splits
  - Support Vector Machine (RBF kernel)
  - Random Forest (100 trees, parallel training)
  - XGBoost (gradient boosting with regularization)
- **Train-Test Split**: 80/20 stratified split (588 train, 148 test samples)
- **Normalization**: RobustScaler (outlier-resistant)
- **Evaluation**: Accuracy, Precision, Recall, F1-Score
- **Persistence**: Best model serialized with Joblib (.joblib + .pkl)

**Data Flow**: 736 records × 9 features → 5 cleaned → 10 engineered → 3 models → Best model

---

### Phase 2: Data Augmentation Layer (✅ Implemented)

**Purpose**: Enrich dataset with real-time performance metrics from live websites

**Key Components**:
- **Google PageSpeed Insights API Integration**
  - Endpoint: `https://www.googleapis.com/pagespeedonline/v5/runPagespeed`
  - Strategy: Desktop analysis (30% faster than mobile)
  - Rate limiting: 0.5s delay, 60s timeout, automatic retry
  
- **Feature Extraction** (16 new features):
  - *Core Web Vitals*: LCP, FCP, CLS, TTI, TBT, Speed Index
  - *Performance Metrics*: Performance Score (0-100), Total Byte Weight, Request Count, DOM Size
  - *Optimization Audits*: Text compression, render blocking, HTTP/2, WebP usage, unused JS

- **Batch Processing**: Progress tracking with tqdm, error handling, quality validation

- **Data Merging**: Left join on URL key, success rate calculation

**Data Flow**: 736 URLs → API requests → 16 features/URL → Merge → 736 × 21+ augmented dataset

**Processing Time**: ~30-60 minutes for full dataset

---

### Phase 3: Prescriptive Optimization & Explainability (🔄 Planned)

**Purpose**: Generate actionable recommendations with interpretable explanations

**Key Components**:
- **SciPy Optimization Engine**
  - Algorithms: SLSQP, Trust-Region, Differential Evolution
  - Objective: Maximize performance score, minimize load time
  - Constraints: Budget, technical bounds, UX requirements

- **Explainability Engine**
  - *SHAP*: Global feature importance, dependence plots, interaction analysis
  - *LIME*: Local instance explanations, decision boundaries, counterfactuals

- **Recommendation Engine**: Prioritized action items with impact analysis, cost-benefit estimates

- **Report Generation**: PDF/HTML reports, interactive dashboards

---

## 3. System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    INPUT DATA SOURCES                       │
│  • Kaggle Dataset (736 × 9)   • Live URLs (PageSpeed API)  │
└────────────────────┬────────────────────────────────────────┘
                     │
     ┌───────────────┼───────────────┐
     │               │               │
     ▼               ▼               ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  PHASE 1:   │ │  PHASE 2:   │ │  PHASE 3:   │
│ PREDICTIVE  │ │    DATA     │ │ PRESCRIPTIVE│
│  MODELING   │ │AUGMENTATION │ │& EXPLAINABLE│
└──────┬──────┘ └──────┬──────┘ └──────┬──────┘
       │               │               │
       ▼               ▼               ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│Data Prep    │ │URL Extract  │ │Load Model   │
│Feature Eng  │ │API Manager  │ │& Dataset    │
│Train-Test   │ │Feature Parse│ │Optimize     │
│3 ML Models  │ │Batch Process│ │SHAP/LIME    │
│Evaluation   │ │Data Merge   │ │Recommend    │
│Export Model │ │Export CSV   │ │Reports      │
└──────┬──────┘ └──────┬──────┘ └──────┬──────┘
       │               │               │
       ▼               ▼               ▼
┌─────────────────────────────────────────────────────────────┐
│                    OUTPUT ARTIFACTS                         │
│  • Models (.joblib)  • Augmented CSV  • Optimization Reports│
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Data Schema Evolution

| Phase | Schema | Features | Description |
|-------|--------|----------|-------------|
| **Input** | Original CSV | 9 | Sr No, URL, Category, Page Size, Load Time, Response Time, Throughput, Performance Label, User Response |
| **Phase 1** | Engineered | 10 | 5 original (cleaned) + 5 derived features |
| **Phase 2** | Augmented | 21+ | Phase 1 features + 16 API-extracted features (Core Web Vitals, resource metrics, optimization checks) |
| **Phase 3** | Optimized | 21+ meta | Phase 2 + optimization recommendations, SHAP values, LIME explanations |

---

## 5. Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Core** | Python 3.8+ | Development language |
| **Data** | Pandas, NumPy | Data manipulation, numerical computing |
| **ML** | Scikit-learn, XGBoost | Model training, evaluation |
| **Optimization** | SciPy | (Phase 3) Constrained optimization |
| **Explainability** | SHAP, LIME | (Phase 3) Model interpretability |
| **Visualization** | Matplotlib, Seaborn | Charts and statistical plots |
| **API** | Requests, tqdm | HTTP client, progress tracking |
| **Persistence** | Joblib, Pickle | Model serialization |
| **Development** | Jupyter Notebook | Interactive development |

**External Services**: Google PageSpeed Insights API v5 (25,000 requests/day free tier)

---

## 6. Model Training Pipeline

**Workflow**:
1. Load CSV → Validate schema (736 samples)
2. Handle missing values → Median (numeric), Mode (categorical)
3. Encode categories → Label encoding for Category and target
4. Engineer features → 5 new derived features
5. Split data → 80/20 stratified (maintains class balance)
6. Normalize → RobustScaler (outlier-resistant)
7. Train models → SVM, Random Forest, XGBoost
8. Evaluate → Accuracy, Precision, Recall, F1-Score
9. Select best → Highest accuracy with balanced metrics
10. Serialize → Joblib package (model + scaler + encoders + metadata)

**Model Specifications**:
- **SVM**: RBF kernel, C=1.0, probability=True
- **Random Forest**: 100 estimators, max_depth=None, n_jobs=-1
- **XGBoost**: 100 estimators, max_depth=6, learning_rate=0.1

---

## 7. Data Augmentation Pipeline

**Workflow**:
1. Extract URLs → 736 valid URLs from original dataset
2. Configure API → Desktop strategy, 60s timeout, 0.5s rate limit
3. Request loop → For each URL, call PageSpeed Insights API
4. Parse response → Extract 16 performance features from JSON
5. Handle errors → Retry logic, timeout management, error logging
6. Track progress → Real-time progress bar with ETA
7. Merge datasets → Left join original + augmented on URL key
8. Validate quality → Check success rate, missing values
9. Export CSV → Timestamped output file

**API Features Extracted**:
- **Core Web Vitals** (6): LCP, FCP, CLS, TTI, TBT, Speed Index
- **Resource Metrics** (4): Performance Score, Total Bytes, Request Count, DOM Size
- **Optimization Checks** (5): Compression, Render Blocking, HTTP/2, WebP, Unused JS
- **Metadata** (1): Extraction success flag

---

## 8. Integration Architecture

**Inter-Phase Communication**:

| Flow | Data | Format | Validation |
|------|------|--------|------------|
| Phase 1 → Phase 2 | URL list | List[str] | URL format, duplicates |
| Phase 1 → Phase 3 | Trained model | .joblib | Model integrity, version |
| Phase 2 → Phase 3 | Augmented dataset | CSV | Schema, completeness |

**API Integration**:
- Authentication: API key in query parameter
- Rate limiting: 0.5s delay between requests
- Error handling: 3 retry attempts with exponential backoff
- Timeout: 60 seconds per request

---

## 9. Quality Assurance

**Data Quality Targets**:
- Completeness: >95%
- Feature extraction success: >80%
- Model prediction confidence: >0.7

**Model Quality Benchmarks**:
- Accuracy: >85%
- F1-Score: >0.85
- Class imbalance: <20% difference

**Testing Strategy**:
- Unit testing for individual functions
- Integration testing for phase-to-phase flow
- End-to-end pipeline validation

---

## 10. Scalability and Future Enhancements

**Current Capacity**: 736 websites, ~1 hour processing, <10 MB storage

**Scaling Strategy**:
- Parallel API requests (multiprocessing)
- Database migration (PostgreSQL for >10K records)
- Cloud deployment (AWS/GCP)
- Caching layer (Redis for API responses)

**Projected Capacity**: 10,000+ websites, ~2-3 hours with parallelization

**Phase 3 Extensions** (Planned):
- Multi-objective optimization (performance vs. cost trade-offs)
- Sensitivity analysis for parameter impact
- Interactive what-if scenario exploration
- Automated recommendation implementation

**Future Integrations**:
- GTmetrix API, WebPageTest API for additional metrics
- Deep learning models (LSTM for time-series)
- AutoML for hyperparameter optimization
- Real-time monitoring and automated remediation

---

## 11. Implementation Status

| Phase | Component | Status | Metrics |
|-------|-----------|--------|---------|
| **Phase 1** | Data preprocessing | ✅ Complete | 736 → 588/148 split |
| | Feature engineering | ✅ Complete | 5 → 10 features |
| | Model training | ✅ Complete | 3 models trained |
| | Evaluation | ✅ Complete | Accuracy >85% |
| | Persistence | ✅ Complete | .joblib + .pkl |
| **Phase 2** | API integration | ✅ Complete | 736 URLs processed |
| | Feature extraction | ✅ Complete | 16 features/URL |
| | Batch processing | ✅ Complete | Progress tracking |
| | Data merging | ✅ Complete | 21+ features total |
| **Phase 3** | Optimization engine | 🔄 In Design | SciPy framework |
| | SHAP/LIME | 🔄 In Design | Explainability layer |
| | Recommendations | 🔄 In Design | Report generation |

---

## 12. Conclusion

The implemented system demonstrates a robust, modular architecture for web performance optimization. Phase 1 successfully trains high-accuracy classification models (>85%), while Phase 2 enriches the dataset with 16 real-time performance metrics from Google PageSpeed Insights API. The foundation is established for Phase 3, which will provide prescriptive optimization recommendations backed by explainable AI techniques (SHAP/LIME), completing the end-to-end predictive-prescriptive-explainable framework.

**Key Achievements**:
- Modular three-phase architecture enabling independent development
- High-accuracy ML models with comprehensive evaluation
- Real-time data augmentation with robust error handling
- Scalable design supporting future enhancements
- Complete transparency and reproducibility

---

**Document Version**: 1.0 (Concise)  
**Page Count**: 3 pages (optimized for PDF inclusion)  
**Last Updated**: November 20, 2025  
**Status**: Phase 1 & 2 Implemented, Phase 3 Designed

# AI-Driven Web Performance Optimization Framework
## Implementation Summary

---

## 1. System Overview

### 1.1 Framework Architecture
A three-phase predictive–prescriptive–explainable AI framework for web performance optimization:
- **Phase 1 — Predictive**: XGBoost classifier (fast / medium / slow)
- **Phase 1b — Generalizability**: External validation on 8,000 HTTP Archive URLs
- **Phase 2 — Prescriptive**: Goal-seeking optimization via differential evolution
- **Phase 3 — Explainable**: Multi-method XAI with four novel research contributions

### 1.2 Technology Stack
| Component | Technology |
|-----------|------------|
| Runtime | Python 3.14 |
| ML Models | XGBoost, Random Forest, Gradient Boosting, SVM |
| Hyperparameter Tuning | RandomizedSearchCV (scikit-learn) |
| Cross-Validation | StratifiedKFold inside sklearn.Pipeline |
| Optimization | scipy.optimize.differential_evolution |
| Global Explanations | SHAP 0.50.0 (TreeExplainer) |
| Local Explanations | LIME 0.2.0.1 (LimeTabularExplainer) |
| Statistical Tests | scipy.stats (Friedman, Wilcoxon, McNemar, Kruskal-Wallis) |
| Scaling | RobustScaler (fit on training data only) |

---

## 2. Phase 1: Predictive Model

### 2.1 Dataset
| Property | Value |
|----------|-------|
| Source | Google PageSpeed Insights API |
| Total URLs | 885 (cleaned) |
| Original columns | 27 |
| Dropped (all-NaN) | 5 (dom_size, uses_text_compression, render_blocking_resources, uses_http2, modern_image_formats) |
| Dropped (zero-variance) | 1 (unused_js — all zeros) |
| Base features after preprocessing | 14 |
| Engineered features | 8 |
| **Total model features** | **22** |
| Target classes | 3 (fast: 299, medium: 271, slow: 315) |
| Train / Test split | 70% / 30% (stratified) |
| Label correction | Composite metric thresholds (Response Time, LCP, FCP, Load Time, TTI, TBT) |
| Missing value strategy | Median imputation (robust to outliers) |
| Outlier handling | Capped at 1.5 × IQR |

### 2.2 Feature Engineering

**14 Base Features:**
Category, Page Size (KB), Load Time(s), Response Time(s), Throughput,
performance_score, lcp, fcp, cls, tti, tbt, speed_index, total_byte_weight, num_requests

**8 Engineered Features:**
| Feature | Formula | Rationale |
|---------|---------|-----------|
| Size_LoadTime_Ratio | Page Size / Load Time | Efficiency metric |
| Total_Time | Response Time + Load Time | Combined latency |
| Throughput_ResponseTime_Ratio | Throughput / Response Time | Network efficiency |
| Log_Page_Size | log1p(Page Size) | Reduce skewness |
| Log_Throughput | log1p(Throughput) | Reduce skewness |
| CWV_Composite | (LCP + FCP + TTI) / 3 | Core Web Vitals aggregate |
| TBT_TTI_Ratio | TBT / TTI | Main-thread blocking ratio |
| Bytes_Per_Request | total_byte_weight / num_requests | Per-request payload |

### 2.3 Model Training and Tuning
Four classifiers trained with `RandomizedSearchCV` (20 iterations, 5-fold stratified CV):

| Model | Test Accuracy | F1-Score | CV Accuracy (Pipeline) |
|-------|--------------|----------|------------------------|
| SVM (RBF) | 36.84% | 0.2227 | — |
| Random Forest | 87.97% | 0.8778 | 88.47% ± 0.0165 |
| Gradient Boosting | 89.85% | 0.8977 | 89.60% ± 0.0156 |
| **XGBoost** | **90.60%** | **0.9058** | **90.96% ± 0.0140** |

### 2.4 Pipeline Cross-Validation (No Data Leakage)
Cross-validation uses `sklearn.Pipeline` wrapping `RobustScaler` + model, so scaling is performed **inside** each fold — preventing information leakage from test folds into the scaler.

- Best CV model: XGBoost — 90.96% ± 1.40%
- Test–CV gap: −0.36% (excellent generalization, no overfitting)

### 2.5 Statistical Significance Testing

| Test | Purpose | Result |
|------|---------|--------|
| Friedman | Any significant difference among models? | p < 0.05 — Yes |
| Wilcoxon (pairwise) | Pairwise CV fold comparison | XGBoost vs RF significant |
| McNemar (pairwise) | Pairwise test-set prediction comparison | XGBoost vs others significant |

### 2.6 Best Model — XGBoost
| Property | Value |
|----------|-------|
| Test Accuracy | 90.60% |
| F1-Score (weighted) | 0.9058 |
| Precision (weighted) | 0.9063 |
| Recall (weighted) | 0.9060 |
| CV Accuracy | 90.96% ± 1.40% |
| Features | 22 (14 base + 8 engineered) |
| Scaling | RobustScaler |
| Export | best_model_xgboost_20260225_114145.joblib |

---

## 3. Phase 1b: External Generalizability Study

### 3.1 Motivation
To address dataset scale concerns, the framework was validated on 8,000 real-world URLs from the HTTP Archive — an independent, publicly available web crawl dataset.

### 3.2 HTTP Archive Dataset
| Property | Value |
|----------|-------|
| Source | HTTP Archive (`httparchive.crawl.pages` via BigQuery) |
| Crawl date | December 2025 |
| URLs | 8,000 (Tranco top-200K, mobile) |
| Base features | 7 (Page Size, Load Time, Response Time, Throughput, speed_index, total_byte_weight, num_requests) |
| Engineered features | 6 (Size_LoadTime_Ratio, Total_Time, Throughput_ResponseTime_Ratio, Log_Page_Size, Log_Throughput, Bytes_Per_Request) |
| **Total features** | **13** |
| Label distribution | fast: 1,193 (14.9%), medium: 2,383 (29.8%), slow: 4,424 (55.3%) |

### 3.3 Labelling Methodology
Independent labelling using Google's published performance thresholds (no dependency on Phase 1 model):
- **Speed Index**: fast < 3,400 ms | medium 3,400–5,800 ms | slow > 5,800 ms
- **Load Time**: fast < 2.5 s | medium 2.5–5.0 s | slow > 5.0 s
- **TTFB**: fast < 0.8 s | medium 0.8–1.8 s | slow > 1.8 s
- **Final label**: majority vote across 3 metrics

### 3.4 Experiment Results

**Experiment 1 — XGBoost on HA (8,000 URLs, 13 features):**
| Metric | Value |
|--------|-------|
| CV Accuracy | 99.71% ± 0.08% |
| Test Accuracy | 99.71% |
| F1-Score | 0.9971 |

**Experiment 2 — XGBoost on Primary (885 URLs, same 13 features):**
| Metric | Value |
|--------|-------|
| CV Accuracy | 71.72% ± 3.18% |
| Test Accuracy | 73.68% |
| F1-Score | 0.7373 |

**Experiment 3 — Cross-Dataset Transfer:**
| Direction | Accuracy | F1-Score |
|-----------|----------|----------|
| Train Primary (885) → Test HA (8,000) | **97.54%** | 0.9752 |
| Train HA (8,000) → Test Primary (885) | **88.36%** | 0.8870 |

**Experiment 4 — Multi-Model Comparison on HA:**
| Model | CV Accuracy | Test Accuracy |
|-------|-------------|---------------|
| Random Forest | 99.71% ± 0.12% | 99.71% |
| Gradient Boosting | 99.96% ± 0.05% | 99.83% |
| XGBoost | 99.71% ± 0.08% | 99.71% |
| Friedman test | χ² = 7.60, p = 0.022 | Significant |

### 3.5 Ablation Study — Feature Engineering Impact
| Configuration | CV Accuracy | Test Accuracy |
|---------------|-------------|---------------|
| 7 base features only | 99.65% ± 0.12% | 99.71% |
| 13 features (base + engineered) | 99.71% ± 0.08% | 99.71% |
| **Improvement** | **+0.06 pp** | — |

**Top-5 Features by XGBoost Importance (HA dataset):**
| Rank | Feature | Importance | Type |
|------|---------|------------|------|
| 1 | speed_index | 0.7986 | Base |
| 2 | Response Time(s) | 0.0967 | Base |
| 3 | Load Time(s) | 0.0793 | Base |
| 4 | Total_Time | 0.0110 | Engineered |
| 5 | Page Size (KB) | 0.0036 | Base |

### 3.6 Key Generalizability Findings
- **Cross-dataset transfer** (97.54%) is the strongest evidence: a model trained on 885 curated URLs predicts accurately on 8,000 real-world HTTP Archive URLs
- All three classifiers achieve ≥99.7% accuracy on the larger HA dataset
- Feature engineering contributes +0.06 pp on HA (speed_index alone carries 79.9% importance)
- The framework generalises from curated PageSpeed API data to raw HTTP Archive data

---

## 4. Phase 2: Prescriptive Optimization

### 4.1 Approach
**Algorithm:** `scipy.optimize.differential_evolution` — a population-based evolutionary optimizer suitable for non-differentiable tree-based models.

**Objective function:**
$$\min_{x} \left[ -P(\text{fast} \mid x) + 0.01 \sum_i \left(\frac{x_i - x_i^{\text{current}}}{|x_i^{\text{current}}| + \epsilon}\right)^2 \right]$$

The optimizer maximizes P(fast) while penalizing large changes, subject to direction-aware bounds.

### 4.2 Direction-Aware Domain Constraints
The optimizer only tunes the 14 base features. Engineered features (8) are **recomputed automatically** after each candidate evaluation via `engineer_features_for_prediction()`.

| Constraint | Features | Rule |
|------------|----------|------|
| Must DECREASE | Load Time, Response Time, Page Size, LCP, FCP, CLS, TTI, TBT, speed_index, total_byte_weight, num_requests | Upper bound = current value |
| Must INCREASE | Throughput, performance_score | Lower bound = current value |
| FIXED | Category | Bound = (current, current) |

Feature bounds derived from dataset 5th–95th percentile. Bounds are guarded against inversion (if current value is outside the percentile range).

### 4.3 Single-Website Optimization Result (Slow → Fast)
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Classification | Slow | Fast | Improved |
| P(fast) | 0.0% | 99.8% | +99.8 pp |
| P(slow) | 83.9% | 0.0% | −83.9 pp |

**Top Recommended Changes:**
| Feature | Reduction | Priority |
|---------|-----------|----------|
| lcp | −60.5% | Critical |
| Response Time(s) | −59.0% | Critical |
| tti | −32.2% | High |
| fcp | −28.1% | High |
| Load Time(s) | −9.2% | Medium |

### 4.4 Batch Optimization (5 Slow Websites)
| Metric | Result |
|--------|--------|
| Websites processed | 5 |
| Success rate (slow → fast) | **100%** (5/5) |
| Average P(fast) improvement | +0.95 |
| Domain compliance | **100%** (all changes directionally correct) |

### 4.5 Recommendation Correctness Validation
Every recommendation is checked against domain knowledge:
- Metrics that should decrease (load time, LCP, etc.) must show negative change
- Metrics that should increase (throughput) must show positive change

| Validation | Result |
|------------|--------|
| Total recommendations analysed | 12 |
| Correct direction | 12 |
| **Compliance rate** | **100%** |
| Verdict | EXCELLENT |

### 4.6 Export
All artefacts bundled into `prescriptive_model_package_20260225_151608.joblib`.

---

## 5. Phase 3: Explainability Analysis

Phase 3 provides multi-layered explainability with **four novel research contributions** beyond standard SHAP/LIME analysis.

### 5.1 Standard XAI — SHAP Global Analysis
SHAP values computed via `TreeExplainer` (exact Shapley values for tree ensembles).

**Top 10 Features by Mean |SHAP| (across all classes):**
| Rank | Feature | Importance |
|------|---------|------------|
| 1 | Response Time(s) | 2.920 |
| 2 | fcp | 2.168 |
| 3 | performance_score | 1.685 |
| 4 | lcp | 1.585 |
| 5 | Total_Time | 1.462 |
| 6 | tti | 1.313 |
| 7 | CWV_Composite | 0.558 |
| 8 | total_byte_weight | 0.324 |
| 9 | tbt | 0.318 |
| 10 | speed_index | 0.267 |

### 5.2 Standard XAI — LIME Local Analysis
`LimeTabularExplainer` applied to 4 representative samples (one correctly-classified per class + one misclassified). Shows per-instance feature weights and prediction probabilities.

### 5.3 Novel Contribution 1 — Multi-Method Explainability Consensus Framework

**Problem:** SHAP and LIME often disagree on feature rankings. Practitioners lack guidance on which to trust.

**Method:**
1. Compute global importance from three independent methods: SHAP, LIME (aggregated over 80 samples), and Permutation Importance (10 repeats).
2. Measure each method's **fidelity** — how faithfully it approximates the model.
3. Produce a **fidelity-weighted consensus ranking** with confidence intervals.

**Fidelity Weights:**
| Method | Raw Fidelity | Normalised Weight |
|--------|-------------|-------------------|
| SHAP (TreeExplainer) | 1.0000 (exact) | 0.438 |
| LIME (mean local R²) | 0.2806 | 0.123 |
| Permutation (reference) | 1.0000 | 0.438 |

**Top-5 Consensus Features:**
| Rank | Feature | Consensus Score | CI |
|------|---------|----------------|------|
| 1 | Response Time(s) | 0.9939 | [0.951, 1.000] |
| 2 | CWV_Composite | 0.8190 | [0.707, 1.000] |
| 3 | fcp | 0.8023 | [0.766, 0.852] |
| 4 | Total_Time | 0.6868 | [0.632, 0.750] |
| 5 | lcp | 0.4918 | [0.307, 0.646] |

**Inter-Method Rank Correlations:**
| Pair | Kendall's τ | Spearman's ρ |
|------|------------|--------------|
| SHAP vs LIME | 0.633 | 0.766 |
| SHAP vs Permutation | 0.565 | 0.703 |
| LIME vs Permutation | 0.599 | 0.767 |

**Finding:** Moderate-to-strong agreement (τ = 0.565–0.633) — methods broadly agree but diverge enough to justify a consensus approach rather than relying on any single method.

### 5.4 Novel Contribution 2 — Explanation Stability & Robustness Analysis

**Problem:** LIME uses stochastic perturbation sampling — repeated runs can yield different feature rankings. How reliable are these explanations?

**LIME Stability Test** (30 samples × 20 runs, top-5 Jaccard similarity):
| Metric | Value |
|--------|-------|
| Mean Jaccard Index | **0.8764 ± 0.1048** |
| Interpretation | STABLE (≥ 0.8 threshold) |

**SHAP Perturbation Sensitivity** (±5% Gaussian noise, 30 samples):
| Metric | Value |
|--------|-------|
| Mean L₂ Drift | 0.3278 ± 0.2544 |
| Relative to mean |SHAP| | Moderate sensitivity |

**Cross-Method Agreement by Predicted Class:**
| Class | Mean Kendall's τ (SHAP vs LIME) | n |
|-------|--------------------------------|---|
| fast | 0.604 ± 0.104 | Strongest agreement |
| slow | 0.492 ± 0.097 | Moderate |
| medium | 0.342 ± 0.102 | Weakest agreement |

**Finding:** LIME explanations are stable (Jaccard = 0.876) but have low local fidelity (R² = 0.281). SHAP–LIME agreement is weakest for medium-class samples, indicating the decision boundary near medium is hardest to explain — this is the class where the model is least certain.

### 5.5 Novel Contribution 3 — Category-Stratified Explainability

**Problem:** Standard XAI treats all websites as a homogeneous population. Different categories (News, Travel, Sports, etc.) have fundamentally different architectures.

**Method:** Partition SHAP values by website category, compute per-category mean |SHAP| profiles, test for significant differences via Kruskal-Wallis H-test.

**Categories Analysed:** 8 (each with n ≥ 10 samples)

**Kruskal-Wallis Results — Features with Significantly Different Importance Across Categories (p < 0.05):**
| Feature | p-value | Significant |
|---------|---------|-------------|
| Category | ≈ 0.000 | Yes |
| Page Size (KB) | ≈ 0.000 | Yes |
| tti | 0.0002 | Yes |
| Load Time(s) | 0.0002 | Yes |
| cls | 0.0005 | Yes |
| Size_LoadTime_Ratio | 0.0017 | Yes |
| CWV_Composite | 0.0093 | Yes |
| num_requests | 0.0097 | Yes |
| Throughput | 0.0364 | Yes |

**Summary:** 9/22 features show statistically significant inter-category differences. All 8 categories share the same top-3 overall (Response Time, CWV_Composite, FCP), but with different magnitudes.

**Finding:** One-size-fits-all recommendations are sub-optimal for 9/22 features. Category-specific optimization strategies should be considered.

### 5.6 Novel Contribution 4 — Counterfactual Explanations

**Problem:** SHAP/LIME explain *why* a website was classified a certain way, but not *"what is the minimal set of changes to make this slow page fast?"*

**Method:** Hybrid counterfactual generator combining:
1. **Nearest-prototype seeding** — find the closest "fast" website in feature space
2. **Growing-spheres random search** — progressively larger perturbation radii with domain-aware directional constraints (load-time metrics only decrease, throughput only increases, Category fixed)
3. **Sparsity selection** — among successful candidates, pick the one changing the fewest features

**Results (100 non-fast samples):**
| Metric | Value |
|--------|-------|
| Success rate | **100%** (100/100) |
| Mean features changed | 13.2 |

**Top Actionable Features (by counterfactual frequency):**
| Feature | % of Counterfactuals | Mean Change Direction |
|---------|---------------------|----------------------|
| FCP | 93% | Decrease |
| performance_score | 91% | Increase |
| CWV_Composite | 89% | Decrease |
| LCP | 87% | Decrease |
| Response Time | 85% | Decrease |

**Counterfactual vs SHAP Ranking Comparison:**
| Metric | Value |
|--------|-------|
| Kendall's τ | 0.598 (p < 0.001) |
| Spearman's ρ | 0.772 |
| Interpretation | Moderate-to-strong agreement with per-feature divergence |

**Finding:** The moderate-to-strong global agreement (τ = 0.598) confirms that influential features (SHAP) tend also to appear frequently in counterfactuals, yet the magnitude of divergence for specific features is striking. Composite timing metrics (tti, tbt, TBT_TTI_Ratio) appear in 75–90% of counterfactuals despite low SHAP importance (normalised score ≤ 0.15), indicating high actionability. Conversely, Category has high SHAP importance but near-zero counterfactual frequency — correctly reflecting that site category is not directly optimisable. This per-feature divergence demonstrates that **feature influence ≠ feature actionability**, a key research insight.

### 5.7 Domain Validation
| Validation | Result |
|------------|--------|
| Feature–performance correlations matching domain expectations | 9/11 (81.8%) |
| Missing values in final feature matrix | 0 |
| Duplicate samples | 0 |
| Failures | Page Size (−0.037, expected positive), Throughput (+0.183, expected negative) |

### 5.8 Phase 3b — Prescriptive Model Explainability
Separate notebook explaining the Phase 2 optimization using SHAP + LIME:

| Analysis | Result |
|----------|--------|
| Sample transition | slow → fast (P(fast): 0.0% → 99.8%) |
| Top SHAP driver | Response Time(s) (1.469) |
| Top LIME driver | Total_Time ≤ 1.58 |
| SHAP–LIME top-5 agreement | 80% (4/5 features overlap) |
| Domain compliance | 12/12 correct (100%) |
| Human-readable prescriptions | Generated with action + reason + how-to |

---

## 6. Real-World Validation Experiment

### 6.1 Motivation
Phase 2's internal validation is circular — the same model that generates prescriptions also validates them. A controlled real-world experiment using an **external ground truth** (Google PageSpeed Insights API) eliminates this bias.

### 6.2 Experimental Design
1. Build an intentionally **slow** web page with known performance problems
2. Collect metrics via PageSpeed API → confirm model predicts "slow"
3. Apply Phase 2 prescriptions to build an optimized **fast** page
4. Collect metrics via PageSpeed API → confirm model predicts "fast"
5. Compare predictions against PageSpeed API's independent assessment

### 6.3 Results

**Slow Page** (`https://baddummypage.onrender.com/`):
Intentional issues: 6MB uncompressed BMP image, 500 empty DOM elements, blocking synchronous JS.

**Fast Page** (`https://gooddummypage.onrender.com/`):
Prescriptions applied: compressed image (6MB → 5KB WebP), removed blocking JS, deferred scripts.

| Metric | Slow Page | Fast Page | Improvement |
|--------|-----------|-----------|-------------|
| PageSpeed Score | 55/100 | 100/100 | +81.8% |
| FCP | 11,167 ms | 854 ms | −92.4% |
| LCP | 31,616 ms | 854 ms | −97.3% |
| TTI | 31,616 ms | 878 ms | −97.2% |
| TBT | 3 ms | 0 ms | −100% |
| Page Size | 6,080 KB | 8.85 KB | −99.9% |
| Model Prediction | **SLOW** (65.4%) | **FAST** (99.7%) | P(fast) +97.0 pp |

| Validation Aspect | Result |
|-------------------|--------|
| Model correctly predicted slow page | PASS |
| Prescriptions domain-compliant | PASS (92.9%) |
| Fast page met/exceeded all targets | PASS |
| Model correctly predicted fast page | PASS |
| External API confirmed both classifications | PASS |

---

## 7. Key Findings

### 7.1 Predictive Model
- XGBoost achieves **90.60% test accuracy** (90.96% CV) on 22 features
- Core Web Vitals (FCP, LCP, TTI) and Response Time dominate importance
- Pipeline-based CV eliminates data leakage; statistical tests confirm model superiority

### 7.2 Prescriptive Optimization
- 100% success rate on batch optimization (5/5 slow → fast)
- 100% domain compliance — all recommendations directionally correct
- Differential evolution handles non-differentiable tree models effectively

### 7.3 Explainability — Novel Contributions
1. **Consensus Framework**: Fidelity-weighted integration of SHAP (w=0.438), LIME (w=0.123), and Permutation (w=0.438) yields a single trustworthy ranking. Inter-method τ = 0.565–0.633.
2. **Stability Analysis**: LIME is stable (Jaccard = 0.876) but low-fidelity (R² = 0.281). SHAP–LIME agreement weakest for medium class (τ = 0.342).
3. **Category-Stratified**: 9/22 features show statistically significant importance differences across 8 website categories (Kruskal-Wallis, p < 0.05).
4. **Counterfactuals**: 100% generation success rate. Feature influence ≠ feature actionability (CF–SHAP τ = 0.598, p < 0.001). Moderate-to-strong global agreement masks locally important per-feature divergences.

### 7.4 Real-World Validation
- External validation via PageSpeed API eliminates circular validation bias
- All prescription targets met or exceeded (average improvement 94.5%)
- P(fast) improved from 2.7% → 99.7% (+97 pp)

### 7.5 External Generalizability
- Cross-dataset transfer accuracy of **97.54%** (Train 885 Primary → Test 8,000 HA)
- Reverse transfer accuracy of **88.36%** (Train 8,000 HA → Test 885 Primary)
- Framework validated on 8,000 HTTP Archive URLs — an independent, publicly available dataset
- Ablation study: feature engineering contributes +0.06 pp on HA dataset

---

## 8. Reproducibility

| Property | Value |
|----------|-------|
| Primary dataset | cleaned_website_performance_dataset_20251207_145008.csv (885 URLs) |
| HA dataset | ha_summary_8000.csv (8,000 URLs, HTTP Archive Dec 2025) |
| Random seed | 42 (all operations) |
| Train/test split | 70/30, stratified |
| CV strategy | 5-fold StratifiedKFold inside sklearn.Pipeline |
| Model file | best_model_xgboost_20260225_114145.joblib |
| Prescriptive package | prescriptive_model_package_20260225_151608.joblib |
| Validation URLs | baddummypage.onrender.com / gooddummypage.onrender.com |

---

## 9. Summary

| Phase | Key Achievement |
|-------|-----------------|
| Phase 1 | 90.60% accuracy, 22 features, Pipeline CV, statistical significance |
| Phase 1b | 97.54% cross-dataset transfer, 8,000 HA URLs, ablation study |
| Phase 2 | 100% optimization success, 100% domain compliance |
| Phase 3 | 4 novel XAI contributions with quantitative results |
| Validation | External PageSpeed API confirms all predictions |

**Research Contributions:**
1. Fidelity-weighted multi-method explainability consensus framework
2. Quantitative explanation stability and robustness analysis
3. Category-stratified feature importance with statistical significance testing
4. Counterfactual explanations demonstrating influence ≠ actionability
5. End-to-end predictive–prescriptive–explainable pipeline with real-world validation
6. External generalizability study on 8,000 HTTP Archive URLs with cross-dataset transfer

---

*Updated: March 2026*


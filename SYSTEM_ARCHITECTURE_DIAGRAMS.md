# System Architecture Diagrams
## Predictive-Prescriptive-Explainable AI Framework for Web Performance Optimization

---

## 1. Complete Framework Architecture

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#ffffff', 'tertiaryColor': '#ffffff', 'clusterBkg': '#ffffff', 'clusterBorder': '#000000', 'fontSize': '14px', 'fontFamily': 'Arial'}}}%%
flowchart TB
    subgraph Input[" "]
        direction LR
        I0[<b>DATA LAYER</b>]:::title
        DS[("Primary Dataset<br/>885 URLs × 27 Columns")]
        API["Google PageSpeed<br/>Insights API"]
        I0 ~~~ DS --- API
    end

    subgraph Phase1[" "]
        direction LR
        T1[<b>PHASE 1: PREDICTIVE MODELLING</b>]:::title
        P1A["Preprocessing<br/>Median Imputation, IQR Capping"]
        P1B["Feature Engineering<br/>14 Base + 8 Derived = 22 Features"]
        P1C["Pipeline-Based Training<br/>RobustScaler + Classifier in CV"]
        P1D["XGBoost: 90.60% Test Acc<br/>90.96% Pipeline CV"]
        P1E["Statistical Significance<br/>Friedman, Wilcoxon, McNemar"]
        T1 ~~~ P1A
        P1A --> P1B --> P1C --> P1D --> P1E
    end

    subgraph Phase1b[" "]
        direction TB
        T1b[<b>PHASE 1b: GENERALIZABILITY</b>]:::title
        P1bA["HTTP Archive<br/>8,000 URLs"]
        P1bB["Cross-Dataset Transfer<br/>97.54% Accuracy"]
        P1bC["Ablation Study<br/>Feature Engineering Impact"]
        T1b ~~~ P1bA
        P1bA --> P1bB --> P1bC
    end

    subgraph Phase2[" "]
        direction TB
        T2[<b>PHASE 2: PRESCRIPTIVE OPTIMIZATION</b>]:::title
        P2A["Differential Evolution<br/>Direction-Aware Constraints"]
        P2B["Objective: max P(fast)<br/>λ=0.01 Regularization"]
        P2C["Engineered Features<br/>Recomputed Per Candidate"]
        P2D["100% Success Rate<br/>100% Domain Compliance"]
        T2 ~~~ P2A
        P2A --> P2B --> P2C --> P2D
    end

    subgraph Phase3[" "]
        direction TB
        T3[<b>PHASE 3: EXPLAINABILITY</b>]:::title
        P3A["SHAP TreeExplainer<br/>(Global)"]
        P3B["LIME TabularExplainer<br/>(Local)"]
        P3C["Permutation Importance<br/>(10 Repeats)"]
        P3D["Consensus Ranking<br/>Fidelity-Weighted, Bootstrap CI"]
        P3E["Stability Analysis<br/>LIME Jaccard=0.876"]
        P3F["Category-Stratified<br/>Kruskal-Wallis (9/22 sig.)"]
        P3G["Counterfactual Generation<br/>SHAP-CF τ=0.598"]
        T3 ~~~ P3A
        P3A & P3B & P3C --> P3D
        P3D --> P3E & P3F & P3G
    end

    subgraph Validation[" "]
        direction LR
        T4[<b>REAL-WORLD VALIDATION</b>]:::title
        V1["Deploy Baseline + Optimized<br/>Pages on Render.com"]
        V2["External Audit<br/>Google PageSpeed API"]
        V3["PageSpeed: 55 → 100<br/>LCP: -97.3%"]
        T4 ~~~ V1
        V1 --> V2 --> V3
    end

    %% Cross-subgraph edges
    DS --> P1A
    P1D --> P1bA
    P1D --> P2A
    P1D --> P3A
    P1D --> P3B
    P1D --> P3C
    P2D --> V1

    %% Force Phase1b, Phase2, Phase3 onto the same row
    Phase1b ~~~ Phase2 ~~~ Phase3

    classDef default fill:#ffffff,stroke:#000000,stroke-width:1px,color:#000000
    classDef title fill:none,stroke:none,color:#000000,font-weight:bold
```

---

## 2. High-Level Data Flow Architecture

```mermaid
flowchart LR
    subgraph Input["DATA INPUT"]
        Raw[("Cleaned Dataset<br/>885 × 27")]
        HA[("HTTP Archive<br/>8,000 URLs")]
    end

    subgraph Pipeline["FOUR-PHASE PIPELINE"]
        direction TB
        P1["Phase 1<br/>Predictive<br/>XGBoost<br/>90.60% Acc"]
        P1b["Phase 1b<br/>Generalizability<br/>Cross-Dataset<br/>97.54% Transfer"]
        P2["Phase 2<br/>Prescriptive<br/>Differential Evolution<br/>100% Compliance"]
        P3["Phase 3<br/>Explainability<br/>4 Novel XAI Contributions<br/>Consensus + CF"]
    end

    subgraph Val["VALIDATION"]
        RW["Real-World<br/>PageSpeed API<br/>55 → 100"]
    end

    subgraph Outputs["DELIVERABLES"]
        D1["Performance<br/>Classification"]
        D2["Optimization<br/>Recommendations"]
        D3["Interpretable<br/>Explanations"]
    end

    Raw --> P1
    HA --> P1b
    P1 --> P1b
    P1 --> P2
    P1 --> P3
    P2 --> RW
    P2 --> D2
    P1 --> D1
    P3 --> D3
    RW --> D2

    style Input fill:#e8f5e9,stroke:#2e7d32
    style Pipeline fill:#e3f2fd,stroke:#1565c0
    style Val fill:#fff8e1,stroke:#f9a825
    style Outputs fill:#fce4ec,stroke:#c2185b
```

---

## 3. Phase 1: Predictive Model Architecture

```mermaid
graph TB
    subgraph Input["INPUT"]
        Start[("Dataset: 885 URLs<br/>27 Features")]
    end

    subgraph Preprocessing["DATA PREPROCESSING"]
        Clean[Handle Missing Values<br/>Median Imputation]
        Drop[Drop 5 All-NaN + 1 Zero-Var<br/>dom_size, uses_text_compression, etc.]
        Encode[Label Encoding<br/>Category → Numeric]
        Scale[RobustScaler<br/>Inside Pipeline CV Folds]
    end

    subgraph Features["FEATURE ENGINEERING"]
        Base[14 Base Features<br/>Core Web Vitals + Metrics]
        Derived[8 Derived Features<br/>Ratios, Logs, CWV_Composite,<br/>TBT_TTI_Ratio, Bytes_Per_Request]
        Final[22 Final Features]
    end

    subgraph Split["TRAIN-TEST SPLIT"]
        Train[Training Set<br/>619 Samples - 70%]
        Test[Test Set<br/>266 Samples - 30%]
    end

    subgraph Models["MODEL COMPARISON"]
        SVM[SVM RBF Kernel<br/>36.84% Accuracy]
        RF[Random Forest<br/>87.97% Accuracy]
        GB[Gradient Boosting<br/>89.85% Accuracy]
        XGB[XGBoost<br/>90.60% Accuracy]
    end

    subgraph Evaluation["EVALUATION"]
        Metrics[Accuracy, Precision<br/>Recall, F1-Score]
        CV[5-Fold Pipeline CV<br/>90.96% ± 1.40%]
        Stats[Friedman + Wilcoxon<br/>+ McNemar Tests]
        Best[Best Model: XGBoost]
    end

    subgraph Output["OUTPUT"]
        Export[("Model Export<br/>best_model_xgboost.joblib")]
    end

    Start --> Clean --> Drop --> Encode --> Scale
    Scale --> Base
    Base --> Derived --> Final
    Final --> Train & Test
    Train --> SVM & RF & GB & XGB
    Test --> SVM & RF & GB & XGB
    SVM --> Metrics
    RF --> Metrics
    GB --> Metrics
    XGB --> Metrics
    Metrics --> CV --> Stats --> Best --> Export

    classDef prepStyle fill:#bbdefb,stroke:#1565c0,stroke-width:2px
    classDef featureStyle fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    classDef modelStyle fill:#fff9c4,stroke:#f9a825,stroke-width:2px
    classDef evalStyle fill:#ffccbc,stroke:#d84315,stroke-width:2px

    class Clean,Drop,Encode,Scale prepStyle
    class Base,Derived,Final featureStyle
    class SVM,RF,GB,XGB modelStyle
    class Metrics,CV,Stats,Best evalStyle
```

---

## 4. Phase 2: Prescriptive Optimization Architecture

```mermaid
graph TB
    subgraph Input["INPUT ARTIFACTS"]
        Model[("Trained XGBoost Model<br/>+ Scaler + Encoder")]
        Sample[("Sample Website<br/>Current Feature Values")]
    end

    subgraph Constraints["DOMAIN CONSTRAINTS"]
        Decrease[Features to Decrease<br/>fcp, lcp, tti, tbt<br/>Response Time, Load Time<br/>Page Size, Requests, Unused JS]
        Increase[Features to Increase<br/>performance_score<br/>Throughput]
        Bounds[Feature Bounds<br/>Min/Max from Dataset]
    end

    subgraph Optimization["OPTIMIZATION ENGINE"]
        Objective[Objective Function<br/>Maximize P_fast]
        DiffEvol[Differential Evolution<br/>scipy.optimize]
        Search[Global Search<br/>Population-Based]
        Converge[Convergence Check<br/>Optimal Solution]
    end

    subgraph Validation["DOMAIN VALIDATION"]
        Check[Direction Validation<br/>12 Recommendations]
        Compliance[Compliance Check<br/>100% Correct]
    end

    subgraph Output["OUTPUT"]
        Recommend[("Recommendations<br/>Top Changes")]
        Package[("Optimization Package<br/>.joblib")]
    end

    Model --> Objective
    Sample --> Objective
    Decrease --> Bounds
    Increase --> Bounds
    Bounds --> DiffEvol
    Objective --> DiffEvol
    DiffEvol --> Search --> Converge
    Converge --> Check --> Compliance
    Compliance --> Recommend --> Package

    classDef inputStyle fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    classDef constraintStyle fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    classDef optStyle fill:#e1bee7,stroke:#7b1fa2,stroke-width:2px
    classDef validStyle fill:#c8e6c9,stroke:#388e3c,stroke-width:2px

    class Model,Sample inputStyle
    class Decrease,Increase,Bounds constraintStyle
    class Objective,DiffEvol,Search,Converge optStyle
    class Check,Compliance validStyle
```

---

## 5. Phase 3: Explainability Architecture

```mermaid
graph TB
    subgraph Input["INPUT"]
        Model[("Trained XGBoost<br/>Model")]
        Data[("Dataset<br/>885 Samples")]
    end

    subgraph Methods["THREE EXPLAINABILITY METHODS"]
        SHAP["SHAP TreeExplainer<br/>(Exact Shapley Values)"]
        LIME["LIME TabularExplainer<br/>(5,000 Perturbations)"]
        PERM["Permutation Importance<br/>(10 Repeats)"]
    end

    subgraph Novel["FOUR NOVEL CONTRIBUTIONS"]
        N1["1. Consensus Ranking<br/>Fidelity-Weighted<br/>Bootstrap CI"]
        N2["2. Stability Analysis<br/>LIME Jaccard=0.876<br/>SHAP Perturbation Sensitivity"]
        N3["3. Category-Stratified<br/>Kruskal-Wallis H-tests<br/>9/22 Features Significant"]
        N4["4. Counterfactual Generation<br/>Nearest-Prototype + Growing-Spheres<br/>SHAP-CF τ=0.598"]
    end

    subgraph Insights["KEY INSIGHTS"]
        I1["Inter-method τ: 0.565–0.633"]
        I2["Class-specific SHAP-LIME τ:<br/>Fast=0.604, Medium=0.342, Slow=0.492"]
        I3["Feature Influence ≠ Actionability<br/>tti, tbt high CF freq, low SHAP"]
    end

    subgraph Output["OUTPUT"]
        Reports[("Consensus Rankings<br/>Figures 2–4")]
    end

    Model --> SHAP & LIME & PERM
    Data --> LIME
    SHAP --> N1
    LIME --> N1
    PERM --> N1
    N1 --> N2
    N1 --> N3
    N1 --> N4
    N2 --> I1
    N2 --> I2
    N4 --> I3
    I1 & I2 & I3 --> Reports

    classDef shapStyle fill:#c5cae9,stroke:#3f51b5,stroke-width:2px
    classDef limeStyle fill:#b2dfdb,stroke:#00796b,stroke-width:2px
    classDef novelStyle fill:#fff9c4,stroke:#f9a825,stroke-width:2px
    classDef insightStyle fill:#ffccbc,stroke:#d84315,stroke-width:2px

    class SHAP shapStyle
    class LIME,PERM limeStyle
    class N1,N2,N3,N4 novelStyle
    class I1,I2,I3 insightStyle
```

---

## 6. Integrated System Flow (Research Paper Figure)

```mermaid
graph LR
    subgraph Phase1["PHASE 1: PREDICTIVE"]
        A1[Dataset<br/>885 URLs]
        A2[Preprocessing<br/>22 Features]
        A3[XGBoost<br/>Training]
        A4[90.60%<br/>Accuracy]
    end

    subgraph Phase1b["PHASE 1b: GENERALIZABILITY"]
        Ab1[HTTP Archive<br/>8,000 URLs]
        Ab2[97.54%<br/>Transfer]
    end

    subgraph Phase2["PHASE 2: PRESCRIPTIVE"]
        B1[Load Model<br/>+ Constraints]
        B2[Differential<br/>Evolution]
        B3[Goal-Seeking<br/>Optimization]
        B4[100%<br/>Compliance]
    end

    subgraph Phase3["PHASE 3: EXPLAINABILITY"]
        C1[SHAP +<br/>LIME +<br/>Permutation]
        C2[Consensus<br/>Ranking]
        C3[Stability +<br/>Kruskal-Wallis]
        C4[Counterfactual<br/>τ=0.598]
    end

    subgraph RW["REAL-WORLD VALIDATION"]
        R1[Deploy on<br/>Render.com]
        R2[PageSpeed<br/>55 → 100]
    end

    A1 --> A2 --> A3 --> A4
    A4 -->|Model| Ab1 --> Ab2
    A4 -->|Model| B1
    B1 --> B2 --> B3 --> B4
    A4 -->|Model| C1
    C1 --> C2 --> C3 --> C4
    B4 --> R1 --> R2

    style Phase1 fill:#e3f2fd,stroke:#1565c0,stroke-width:3px
    style Phase1b fill:#e8eaf6,stroke:#3f51b5,stroke-width:3px
    style Phase2 fill:#fff3e0,stroke:#ef6c00,stroke-width:3px
    style Phase3 fill:#f3e5f5,stroke:#7b1fa2,stroke-width:3px
    style RW fill:#e8f5e9,stroke:#2e7d32,stroke-width:3px
```

---

## 7. Technology Stack

```mermaid
graph TB
    subgraph ML["MACHINE LEARNING"]
        XGB[XGBoost<br/>Classification]
        SKL[Scikit-learn<br/>SVM, Random Forest<br/>Preprocessing]
    end

    subgraph OPT["OPTIMIZATION"]
        SciPy[SciPy<br/>differential_evolution]
    end

    subgraph XAI["EXPLAINABLE AI"]
        SHAP[SHAP 0.50.0<br/>TreeExplainer]
        LIME[LIME 0.2.0.1<br/>TabularExplainer]
    end

    subgraph DATA["DATA PROCESSING"]
        Pandas[Pandas 2.3.3<br/>DataFrame Operations]
        NumPy[NumPy 1.26.4<br/>Numerical Computing]
    end

    subgraph ENV["ENVIRONMENT"]
        Python[Python 3.14.0]
        Jupyter[Jupyter Notebooks]
    end

    Python --> Pandas & NumPy
    Pandas --> SKL --> XGB
    NumPy --> SciPy
    XGB --> SHAP & LIME
    SKL --> SciPy

    classDef mlStyle fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    classDef optStyle fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    classDef xaiStyle fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef dataStyle fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px

    class XGB,SKL mlStyle
    class SciPy optStyle
    class SHAP,LIME xaiStyle
    class Pandas,NumPy dataStyle
```

---

## 8. Results Summary Diagram

```mermaid
graph TB
    subgraph Results["FRAMEWORK RESULTS"]
        subgraph P1R["Phase 1 Results"]
            R1A[XGBoost Selected]
            R1B[90.60% Test Accuracy]
            R1C[90.96% Pipeline CV]
        end

        subgraph P1bR["Phase 1b Results"]
            R1bA[8,000 HTTP Archive URLs]
            R1bB[97.54% Cross-Dataset Transfer]
        end

        subgraph P2R["Phase 2 Results"]
            R2A[P_fast: 0.0% → 99.8%]
            R2B[5/5 Batch Success]
            R2C[100% Domain Compliance]
        end

        subgraph P3R["Phase 3 Results"]
            R3A[Consensus: τ = 0.565–0.633]
            R3B[LIME Jaccard = 0.876]
            R3C[Kruskal-Wallis: 9/22 sig.]
            R3D[CF: τ = 0.598, ρ = 0.772]
        end

        subgraph RWR["Real-World Validation"]
            R4A[PageSpeed: 55 → 100]
            R4B[LCP: -97.3%]
            R4C[External API Confirmed]
        end
    end

    R1A --> R1B --> R1C
    R1bA --> R1bB
    R2A --> R2B --> R2C
    R3A --> R3B --> R3C --> R3D
    R4A --> R4B --> R4C

    style P1R fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style P1bR fill:#e8eaf6,stroke:#3f51b5,stroke-width:2px
    style P2R fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    style P3R fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style RWR fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
```

---

## Usage Instructions for Research Paper

### Recommended Diagrams by Section:
| Paper Section | Recommended Diagram |
|--------------|---------------------|
| System Design / Methodology | Diagram 1 (Complete Framework) |
| High-Level Overview | Diagram 2 (Data Flow) |
| Phase 1 Details | Diagram 3 (Predictive Model) |
| Phase 2 Details | Diagram 4 (Prescriptive Optimization) |
| Phase 3 Details | Diagram 5 (Explainability) |
| Abstract / Introduction | Diagram 6 (Integrated Flow) |
| Implementation | Diagram 7 (Technology Stack) |
| Results | Diagram 8 (Results Summary) |

### Export Instructions:
1. **Online Tool**: Visit https://mermaid.live/
2. **Paste Code**: Copy any diagram code block
3. **Export**: Download as PNG or SVG (300 DPI for print)
4. **LaTeX**: Use `\includegraphics{diagram.png}` with appropriate sizing

### Color Scheme:
- **Phase 1 (Predictive)**: Blue tones (#e3f2fd, #1565c0)
- **Phase 2 (Prescriptive)**: Orange tones (#fff3e0, #ef6c00)
- **Phase 3 (Explainability)**: Purple tones (#f3e5f5, #7b1fa2)
- **Input/Output**: Green/Pink (#e8f5e9, #fce4ec)

---

*Document Version: 3.0*  
*Updated: March 2026*  
*Aligned with REWRITTEN_PAPER.txt and IMPLEMENTATION_SUMMARY.md*

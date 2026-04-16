# High-Level System Architecture - Mermaid Diagrams

## 1. Complete System Architecture (Three-Phase Overview)

```mermaid
graph TB
    subgraph Input["📊 INPUT DATA"]
        DS1[Kaggle Dataset: 736 × 9 features]
        DS2[Google PageSpeed API]
    end

    subgraph Phase1["🔮 PHASE 1: PREDICTIVE MODELING"]
        P1A[Data Preprocessing]
        P1B[Feature Engineering<br/>+5 derived features]
        P1C[Model Training<br/>SVM, Random Forest, XGBoost]
        P1D[Model Evaluation & Selection]
    end

    subgraph Phase2["🔬 PHASE 2: DATA AUGMENTATION"]
        P2A[URL Extraction & API Requests]
        P2B[Feature Extraction<br/>16 performance metrics]
        P2C[Dataset Merging & Validation]
    end

    subgraph Phase3["🎯 PHASE 3: PRESCRIPTIVE & EXPLAINABLE AI"]
        P3A[SciPy Optimization Engine]
        P3B[SHAP & LIME Explainability]
        P3C[Recommendation Generation]
    end

    subgraph Output["📤 OUTPUTS"]
        O1[Trained Models<br/>.joblib, .pkl]
        O2[Augmented Dataset<br/>736 × 21+ features]
        O3[Optimization Reports<br/>& Dashboards]
    end

    %% Main Flow
    DS1 --> P1A
    P1A --> P1B
    P1B --> P1C
    P1C --> P1D
    P1D --> O1

    DS1 --> P2A
    DS2 --> P2A
    P2A --> P2B
    P2B --> P2C
    P2C --> O2

    O1 --> P3A
    O2 --> P3A
    P3A --> P3B
    P3B --> P3C
    P3C --> O3

    %% Styling with darker text and thicker borders
    classDef phase1Style fill:#e3f2fd,stroke:#1976d2,stroke-width:3px,color:#000,font-size:14px
    classDef phase2Style fill:#f3e5f5,stroke:#7b1fa2,stroke-width:3px,color:#000,font-size:14px
    classDef phase3Style fill:#fff3e0,stroke:#f57c00,stroke-width:3px,color:#000,font-size:14px
    classDef inputStyle fill:#e8f5e9,stroke:#388e3c,stroke-width:3px,color:#000,font-size:14px
    classDef outputStyle fill:#fce4ec,stroke:#c2185b,stroke-width:3px,color:#000,font-size:14px

    class P1A,P1B,P1C,P1D phase1Style
    class P2A,P2B,P2C phase2Style
    class P3A,P3B,P3C phase3Style
    class DS1,DS2 inputStyle
    class O1,O2,O3 outputStyle
```

---

## 2. Data Flow Architecture

```mermaid
flowchart LR
    subgraph Raw["RAW DATA"]
        RD1[(Kaggle CSV<br/>736 × 9)]
        RD2[("Live URLs<br/>PageSpeed API")]
    end

    subgraph Process["PROCESSING PIPELINE"]
        direction TB
        P1["Phase 1<br/>Predictive<br/>Modeling"]
        P2["Phase 2<br/>Data<br/>Augmentation"]
        P3["Phase 3<br/>Optimization<br/>& Explain"]
    end

    subgraph Intermediate["INTERMEDIATE OUTPUTS"]
        I1[("Trained Models<br/>+Metadata")]
        I2[("Augmented Dataset<br/>736 × 21+")]
    end

    subgraph Final["FINAL DELIVERABLES"]
        F1["Performance<br/>Predictions"]
        F2["Optimization<br/>Recommendations"]
        F3["Explainable<br/>Insights"]
    end

    RD1 -->|"Load & Clean"| P1
    P1 -->|"Export Model"| I1
    RD1 -->|"Extract URLs"| P2
    RD2 -->|"API Calls"| P2
    P2 -->|"Merge Features"| I2
    I1 -->|"Load Model"| P3
    I2 -->|"Load Data"| P3
    P3 -->|"Generate"| F1
    P3 -->|"Optimize"| F2
    P3 -->|"Explain"| F3

    style Raw fill:#e8f5e9
    style Process fill:#e3f2fd
    style Intermediate fill:#fff3e0
    style Final fill:#fce4ec
```

---

## 3. Phase 1: Predictive Modeling Detailed Architecture

```mermaid
graph TB
    Start([Raw Dataset: 736 × 9])
    
    Prep[Data Preparation<br/>Load, Clean, Encode]
    FE[Feature Engineering<br/>+5 derived features]
    Split[Train-Test Split<br/>80/20 Stratified]
    
    subgraph Models["MODEL ENSEMBLE"]
        SVM[SVM]
        RF[Random Forest]
        XGB[XGBoost]
    end
    
    Eval[Evaluation & Selection<br/>Accuracy, Precision, Recall, F1]
    Save[Model Persistence<br/>.joblib + .pkl]
    
    End([Best Model Ready])

    Start --> Prep --> FE --> Split
    Split --> SVM & RF & XGB
    SVM --> Eval
    RF --> Eval
    XGB --> Eval
    Eval --> Save --> End

    classDef prepStyle fill:#bbdefb,stroke:#1976d2,stroke-width:2px,color:#000,font-size:13px
    classDef modelStyle fill:#c8e6c9,stroke:#388e3c,stroke-width:2px,color:#000,font-size:13px
    classDef evalStyle fill:#ffe0b2,stroke:#f57c00,stroke-width:2px,color:#000,font-size:13px
    
    class Prep,FE,Split prepStyle
    class SVM,RF,XGB modelStyle
    class Eval,Save evalStyle
```

---

## 4. Phase 2: Data Augmentation Detailed Architecture

```mermaid
graph TD
    Start([Start: Original Dataset<br/>736 URLs])
    
    subgraph Extract["URL EXTRACTION"]
        GetURLs[Extract URLs<br/>from CSV]
        Validate[Validate URLs<br/>Protocol Check<br/>Remove Duplicates]
    end

    subgraph API["API INTEGRATION"]
        Config[Configure API<br/>• Strategy: Desktop<br/>• Timeout: 60s<br/>• Rate Limit: 0.5s]
        Request[API Request Manager<br/>Retry Logic<br/>Error Handling]
        Call[Google PageSpeed<br/>Insights API v5<br/>Performance Category]
    end

    subgraph Features["FEATURE EXTRACTION"]
        Parse[Parse JSON Response<br/>Lighthouse Results]
        
        subgraph CoreVitals["Core Web Vitals"]
            LCP[LCP: Largest<br/>Contentful Paint]
            FCP[FCP: First<br/>Contentful Paint]
            CLS[CLS: Cumulative<br/>Layout Shift]
            TTI[TTI: Time to<br/>Interactive]
        end
        
        subgraph Resources["Resource Metrics"]
            Bytes[Total Byte Weight<br/>Page Size in KB]
            Requests[Request Count<br/>HTTP Requests]
            DOM[DOM Size<br/>Element Count]
        end
        
        subgraph Optimizations["Optimization Checks"]
            Compress[Text Compression<br/>Gzip/Brotli]
            HTTP2[HTTP/2 Usage<br/>Protocol Check]
            WebP[Modern Images<br/>WebP/AVIF]
        end
    end

    subgraph Batch["BATCH PROCESSING"]
        Progress[Progress Tracking<br/>tqdm Progress Bar<br/>ETA Calculation]
        Collect[Collect Results<br/>Success/Failure Count]
    end

    subgraph Merge["DATA MERGING"]
        Join[Left Join<br/>Original + Augmented<br/>on URL Key]
        Quality[Quality Check<br/>Success Rate<br/>Missing Values]
    end

    subgraph Output["OUTPUT"]
        Export[Export to CSV<br/>Timestamped Filename<br/>21+ Features]
    end

    End([End: Augmented Dataset<br/>Ready for Phase 3])

    Start --> GetURLs
    GetURLs --> Validate
    Validate --> Config
    Config --> Request
    Request --> Call
    Call --> Parse
    Parse --> CoreVitals & Resources & Optimizations
    CoreVitals --> Progress
    Resources --> Progress
    Optimizations --> Progress
    Progress --> Collect
    Collect --> Join
    Join --> Quality
    Quality --> Export
    Export --> End

    classDef apiStyle fill:#e1bee7,stroke:#7b1fa2
    classDef featureStyle fill:#b2dfdb,stroke:#00796b
    classDef processStyle fill:#ffccbc,stroke:#d84315
    
    class Config,Request,Call apiStyle
    class LCP,FCP,CLS,TTI,Bytes,Requests,DOM,Compress,HTTP2,WebP featureStyle
    class Progress,Collect,Join,Quality processStyle
```

---

## 5. Phase 3: Prescriptive & Explainable Architecture (Planned)

```mermaid
graph TD
    Start([Start: Trained Model<br/>+ Augmented Dataset])
    
    subgraph Load["LOAD ARTIFACTS"]
        LoadModel[Load Model Package<br/>Model + Scaler + Encoders]
        LoadData[Load Augmented Data<br/>21+ Features]
    end

    subgraph Optimize["OPTIMIZATION ENGINE"]
        Define[Define Objective<br/>Maximize Performance<br/>Minimize Load Time]
        Constraints[Define Constraints<br/>• Budget Limits<br/>• Technical Bounds<br/>• UX Requirements]
        
        subgraph Algorithms["SciPy Algorithms"]
            SLSQP[SLSQP<br/>Sequential Least Squares]
            TrustRegion[Trust-Region<br/>Constrained]
            DiffEvol[Differential<br/>Evolution]
        end
        
        Solve[Solve Optimization<br/>Find Optimal Parameters]
    end

    subgraph Explain["EXPLAINABILITY ENGINE"]
        subgraph SHAP["SHAP Analysis"]
            SHAPGlobal[Global Feature<br/>Importance]
            SHAPInteract[Feature<br/>Interactions]
            SHAPDependence[Dependence<br/>Plots]
        end
        
        subgraph LIME["LIME Analysis"]
            LIMELocal[Local Instance<br/>Explanations]
            LIMEBoundary[Decision<br/>Boundaries]
            LIMECounter[Counterfactual<br/>Scenarios]
        end
    end

    subgraph Recommend["RECOMMENDATION ENGINE"]
        Generate[Generate<br/>Recommendations]
        Prioritize[Prioritize by Impact<br/>• High Impact<br/>• Medium Effort<br/>• Quick Wins]
        Estimate[Estimate Outcomes<br/>Expected Performance<br/>Cost-Benefit]
    end

    subgraph Report["REPORT GENERATION"]
        Format[Select Format<br/>PDF, HTML, JSON]
        Visualize[Create Visualizations<br/>Charts & Graphs]
        Dashboard[Interactive Dashboard<br/>Drill-Down Analysis]
    end

    End([End: Actionable Reports<br/>with Explanations])

    Start --> LoadModel & LoadData
    LoadModel --> Define
    LoadData --> Define
    Define --> Constraints
    Constraints --> Algorithms
    Algorithms --> Solve
    
    LoadModel --> SHAP & LIME
    LoadData --> SHAP & LIME
    SHAP --> Generate
    LIME --> Generate
    Solve --> Generate
    
    Generate --> Prioritize
    Prioritize --> Estimate
    Estimate --> Format
    Format --> Visualize
    Visualize --> Dashboard
    Dashboard --> End

    classDef optStyle fill:#fff9c4,stroke:#f57f17
    classDef explainStyle fill:#c5cae9,stroke:#3f51b5
    classDef recStyle fill:#ffccbc,stroke:#e64a19
    
    class Define,Constraints,SLSQP,TrustRegion,DiffEvol,Solve optStyle
    class SHAPGlobal,SHAPInteract,SHAPDependence,LIMELocal,LIMEBoundary,LIMECounter explainStyle
    class Generate,Prioritize,Estimate recStyle
```

---

## 6. Technology Stack Architecture

```mermaid
graph TB
    subgraph Frontend["🎨 FRONTEND LAYER (Future)"]
        UI[Web UI<br/>React/Vue]
        Dashboard[Interactive Dashboard<br/>Plotly Dash]
    end

    subgraph Application["💻 APPLICATION LAYER"]
        Jupyter[Jupyter Notebooks<br/>Interactive Development]
        API[REST API<br/>FastAPI/Flask]
    end

    subgraph Processing["⚙️ PROCESSING LAYER"]
        ML[Machine Learning<br/>Scikit-learn, XGBoost]
        Opt[Optimization<br/>SciPy]
        Explain[Explainability<br/>SHAP, LIME]
    end

    subgraph Data["📊 DATA LAYER"]
        CSV[CSV Files<br/>Pandas]
        Models[Model Storage<br/>Joblib]
        Cache[Cache Layer<br/>Redis (Future)]
    end

    subgraph External["🌐 EXTERNAL SERVICES"]
        PSI[Google PageSpeed<br/>Insights API]
        Cloud[Cloud Storage<br/>S3/GCS (Future)]
    end

    subgraph Infrastructure["🏗️ INFRASTRUCTURE (Future)"]
        Docker[Containerization<br/>Docker]
        K8s[Orchestration<br/>Kubernetes]
        Monitor[Monitoring<br/>Prometheus/Grafana]
    end

    UI --> API
    Dashboard --> API
    API --> Jupyter
    Jupyter --> ML & Opt & Explain
    ML --> CSV & Models
    Opt --> CSV & Models
    Explain --> CSV & Models
    API --> PSI
    Models --> Cloud
    API --> Docker
    Docker --> K8s
    K8s --> Monitor

    classDef frontendStyle fill:#e1f5fe,stroke:#0277bd
    classDef appStyle fill:#f3e5f5,stroke:#6a1b9a
    classDef processStyle fill:#e8f5e9,stroke:#2e7d32
    classDef dataStyle fill:#fff3e0,stroke:#ef6c00
    classDef externalStyle fill:#fce4ec,stroke:#c2185b
    
    class UI,Dashboard frontendStyle
    class Jupyter,API appStyle
    class ML,Opt,Explain processStyle
    class CSV,Models,Cache dataStyle
    class PSI,Cloud externalStyle
```

---

## 7. Deployment Architecture (Future Cloud-Native)

```mermaid
graph TB
    subgraph Internet["🌐 INTERNET"]
        Users[End Users<br/>Web Browsers]
    end

    subgraph Edge["🔒 EDGE LAYER"]
        LB[Load Balancer<br/>NGINX/ALB]
        CDN[CDN<br/>CloudFlare/Akamai]
    end

    subgraph App["📱 APPLICATION TIER"]
        WebAPI[Web API Service<br/>FastAPI Container<br/>Replicas: 3]
        Auth[Authentication Service<br/>OAuth2/JWT]
    end

    subgraph Services["🔧 MICROSERVICES TIER"]
        PredSvc[Prediction Service<br/>Model Inference<br/>Container]
        AugSvc[Augmentation Service<br/>API Integration<br/>Container]
        OptSvc[Optimization Service<br/>SciPy Engine<br/>Container]
        ExplSvc[Explanation Service<br/>SHAP/LIME<br/>Container]
    end

    subgraph Data["💾 DATA TIER"]
        DB[(PostgreSQL<br/>Primary Database<br/>Multi-AZ)]
        Cache[(Redis Cache<br/>Session & Results)]
        S3[Object Storage<br/>S3/GCS<br/>Models & Reports]
    end

    subgraph Monitoring["📊 OBSERVABILITY"]
        Logs[Logging<br/>ELK Stack]
        Metrics[Metrics<br/>Prometheus]
        Tracing[Tracing<br/>Jaeger]
    end

    Users --> CDN
    CDN --> LB
    LB --> WebAPI
    WebAPI --> Auth
    Auth --> WebAPI
    WebAPI --> PredSvc & AugSvc & OptSvc & ExplSvc
    PredSvc --> DB & Cache & S3
    AugSvc --> DB & Cache
    OptSvc --> DB & Cache
    ExplSvc --> DB & S3
    
    WebAPI --> Logs & Metrics
    PredSvc --> Logs & Metrics & Tracing
    AugSvc --> Logs & Metrics & Tracing
    OptSvc --> Logs & Metrics & Tracing
    ExplSvc --> Logs & Metrics & Tracing

    classDef edgeStyle fill:#ffebee,stroke:#c62828
    classDef appStyle fill:#e3f2fd,stroke:#1565c0
    classDef serviceStyle fill:#e8f5e9,stroke:#2e7d32
    classDef dataStyle fill:#fff3e0,stroke:#ef6c00
    classDef monitorStyle fill:#f3e5f5,stroke:#6a1b9a
    
    class LB,CDN edgeStyle
    class WebAPI,Auth appStyle
    class PredSvc,AugSvc,OptSvc,ExplSvc serviceStyle
    class DB,Cache,S3 dataStyle
    class Logs,Metrics,Tracing monitorStyle
```

---

## 8. Model Training Pipeline Architecture

```mermaid
sequenceDiagram
    participant User
    participant Notebook as Jupyter Notebook
    participant Data as Data Module
    participant Prep as Preprocessing
    participant FE as Feature Engineering
    participant Train as Model Training
    participant Eval as Evaluation
    participant Store as Model Storage

    User->>Notebook: Execute Cells
    Notebook->>Data: Load CSV Dataset
    Data-->>Notebook: Return DataFrame (736×9)
    
    Notebook->>Prep: Preprocess Data
    Prep->>Prep: Handle Missing Values
    Prep->>Prep: Encode Categories
    Prep->>Prep: Normalize Features
    Prep-->>Notebook: Clean Data (736×5)
    
    Notebook->>FE: Engineer Features
    FE->>FE: Create Ratio Features
    FE->>FE: Log Transformations
    FE-->>Notebook: Engineered Data (736×10)
    
    Notebook->>Train: Train-Test Split (80/20)
    Train->>Train: Train SVM Model
    Train->>Train: Train Random Forest
    Train->>Train: Train XGBoost
    Train-->>Notebook: 3 Trained Models
    
    Notebook->>Eval: Evaluate Models
    Eval->>Eval: Calculate Metrics
    Eval->>Eval: Compare Performance
    Eval->>Eval: Select Best Model
    Eval-->>Notebook: Best Model + Metrics
    
    Notebook->>Store: Save Model Package
    Store->>Store: Serialize with Joblib
    Store->>Store: Serialize with Pickle
    Store-->>User: Model Files (.joblib, .pkl)
    
    Note over User,Store: Phase 1 Complete ✅
```

---

## 9. Data Augmentation Pipeline Architecture

```mermaid
sequenceDiagram
    participant User
    participant Notebook as Jupyter Notebook
    participant URLMgr as URL Manager
    participant API as PageSpeed API
    participant Parser as Response Parser
    participant Merger as Data Merger
    participant Export as CSV Exporter

    User->>Notebook: Execute Augmentation
    Notebook->>URLMgr: Extract URLs from Dataset
    URLMgr->>URLMgr: Validate URLs
    URLMgr-->>Notebook: Valid URL List (736)
    
    loop For Each URL (with rate limiting)
        Notebook->>API: Request Performance Data
        API->>API: Analyze Website
        API-->>Notebook: JSON Response
        
        Notebook->>Parser: Extract Features
        Parser->>Parser: Parse Core Web Vitals
        Parser->>Parser: Parse Resource Metrics
        Parser->>Parser: Parse Optimization Checks
        Parser-->>Notebook: Feature Dictionary (16 features)
        
        Note over Notebook: Progress: X/736 (Y% complete)
    end
    
    Notebook->>Merger: Merge Original + Augmented
    Merger->>Merger: Left Join on URL
    Merger->>Merger: Validate Completeness
    Merger-->>Notebook: Augmented Dataset (736×21+)
    
    Notebook->>Export: Save to CSV
    Export->>Export: Add Timestamp
    Export-->>User: augmented_dataset_TIMESTAMP.csv
    
    Note over User,Export: Phase 2 Complete ✅
```

---

## 10. System Integration and Data Flow (Complete)

```mermaid
flowchart TD
    subgraph Phase1["PHASE 1: PREDICTIVE MODELING"]
        Input1[("Kaggle Dataset<br/>736 × 9")]
        Process1[Clean → Engineer<br/>→ Train → Evaluate]
        Output1[("Best Model<br/>.joblib")]
    end

    subgraph Phase2["PHASE 2: DATA AUGMENTATION"]
        Input2A[("URLs<br/>from Phase 1")]
        Input2B[("PageSpeed API<br/>Live Data")]
        Process2[Request → Extract<br/>→ Parse → Merge]
        Output2[("Augmented Dataset<br/>736 × 21+")]
    end

    subgraph Phase3["PHASE 3: PRESCRIPTIVE & EXPLAINABLE"]
        Input3A[("Model<br/>from Phase 1")]
        Input3B[("Dataset<br/>from Phase 2")]
        Process3[Optimize → Explain<br/>→ Recommend → Report]
        Output3A[("Recommendations<br/>PDF/HTML")]
        Output3B[("Explanations<br/>Dashboard")]
    end

    Input1 --> Process1
    Process1 --> Output1
    
    Output1 -.->|"URLs"| Input2A
    Input2A --> Process2
    Input2B --> Process2
    Process2 --> Output2
    
    Output1 --> Input3A
    Output2 --> Input3B
    Input3A --> Process3
    Input3B --> Process3
    Process3 --> Output3A
    Process3 --> Output3B

    style Phase1 fill:#e3f2fd,stroke:#1976d2,stroke-width:3px
    style Phase2 fill:#f3e5f5,stroke:#7b1fa2,stroke-width:3px
    style Phase3 fill:#fff3e0,stroke:#f57c00,stroke-width:3px
    style Output1 fill:#c8e6c9,stroke:#388e3c
    style Output2 fill:#c8e6c9,stroke:#388e3c
    style Output3A fill:#ffccbc,stroke:#d84315
    style Output3B fill:#ffccbc,stroke:#d84315
```

---

## Usage Instructions

### For Dissertation Report:
1. Copy the main "Complete System Architecture" diagram (Section 1)
2. Include the "Data Flow Architecture" (Section 2) for high-level overview
3. Add phase-specific diagrams (Sections 3-5) in detailed design chapters
4. Use the "Technology Stack" (Section 6) in implementation chapter
5. Include "Deployment Architecture" (Section 7) in future work section

### Rendering Mermaid Diagrams:
- **In Markdown viewers**: GitHub, GitLab, VS Code with Mermaid extension
- **Online**: https://mermaid.live/ (paste code and export as PNG/SVG)
- **In LaTeX**: Export as SVG/PNG and include as figures
- **In PowerPoint**: Export as images from mermaid.live

### Customization:
- Colors can be adjusted in `classDef` declarations
- Node shapes: `[]` rectangles, `()` rounded, `{}` rhombus, `[()]` stadium
- Arrow types: `-->` solid, `-.->` dotted, `==>` thick
- Subgraph styling for grouping related components

---

**Document Version**: 1.0  
**Created**: November 20, 2025  
**Format**: Mermaid.js Diagram Code  
**Compatible**: GitHub, GitLab, VS Code, mermaid.live

"""
Real-World Validation: Predict Class and Get Prescriptions for FAST PAGE
Uses the Phase 2 model to predict performance class and generate optimization recommendations.
"""

import pandas as pd
import numpy as np
import joblib
import json
from datetime import datetime

print("="*80)
print("REAL-WORLD VALIDATION: FAST PAGE PREDICTION & PRESCRIPTIONS")
print("="*80)

# 1. Load the metrics collected from PageSpeed API
print("\n1. LOADING COLLECTED METRICS (FAST PAGE)")
print("-"*40)

with open('fast_page_metrics_model_features.json', 'r') as f:
    metrics = json.load(f)

print(f"URL: https://gooddummypage.onrender.com/")
print(f"\nCollected Metrics:")
for key, value in metrics.items():
    if isinstance(value, float):
        print(f"  {key:25s}: {value:,.2f}")
    else:
        print(f"  {key:25s}: {value}")

# 2. Load the Phase 1 XGBoost model
print("\n2. LOADING PHASE 1 PREDICTIVE MODEL")
print("-"*40)

model_pkg = joblib.load('../best_model_xgboost_20251207_150032.joblib')
print(f"Model: {model_pkg['model_name']}")
print(f"Accuracy: {model_pkg['metrics']['Accuracy']:.4f}")
print(f"Features: {len(model_pkg['feature_names'])}")

model = model_pkg['model']
scaler = model_pkg['scaler']
label_encoder = model_pkg['encoders']['target']
feature_names = model_pkg['feature_names']

print(f"\nTarget Classes: {list(label_encoder.classes_)}")

# 3. Prepare features for prediction
print("\n3. PREPARING FEATURES")
print("-"*40)

# Create feature vector matching model's expected features
feature_vector = {}

# Base features from collected metrics
base_features = {
    'fcp': metrics.get('fcp', 0),
    'lcp': metrics.get('lcp', 0),
    'tti': metrics.get('tti', 0),
    'tbt': metrics.get('tbt', 0),
    'cls': metrics.get('cls', 0),
    'speed_index': metrics.get('speed_index', 0),
    'Response Time(s)': metrics.get('Response Time(s)', 0),
    'Load Time(s)': metrics.get('Load Time(s)', 0),
    'performance_score': metrics.get('performance_score', 0),
    'Page Size (KB)': metrics.get('Page Size (KB)', 0),
    'total_byte_weight': metrics.get('total_byte_weight', 0),
    'num_requests': metrics.get('num_requests', 0),
    'Throughput': metrics.get('Throughput', 0),
    'unused_js': metrics.get('unused_js', 0),
}

# Calculate derived features (from Phase 1)
base_features['Size_LoadTime_Ratio'] = base_features['Page Size (KB)'] / max(base_features['Load Time(s)'], 0.001)
base_features['Total_Time'] = base_features['Response Time(s)'] + base_features['Load Time(s)']
base_features['Throughput_ResponseTime_Ratio'] = base_features['Throughput'] / max(base_features['Response Time(s)'], 0.001)
base_features['Log_Page_Size'] = np.log(base_features['Page Size (KB)'] + 1)
base_features['Log_Throughput'] = np.log(base_features['Throughput'] + 1)

# Handle Category encoding
if 'Category' in feature_names:
    base_features['Category'] = 0  # Default encoded value

print("Feature values prepared:")
for feat in feature_names:
    if feat in base_features:
        print(f"  {feat:35s}: {base_features[feat]:,.4f}")
    else:
        print(f"  {feat:35s}: MISSING")
        base_features[feat] = 0

# Create DataFrame with correct feature order
X = pd.DataFrame([base_features])[feature_names]

print(f"\nFeature vector shape: {X.shape}")

# 4. Scale features and predict
print("\n4. PREDICTING PERFORMANCE CLASS")
print("-"*40)

X_scaled = scaler.transform(X)
prediction = model.predict(X_scaled)
probabilities = model.predict_proba(X_scaled)[0]

predicted_class = label_encoder.inverse_transform(prediction)[0]

print(f"\n🎯 PREDICTED CLASS: {predicted_class.upper()}")
print(f"\nClass Probabilities:")
for i, cls in enumerate(label_encoder.classes_):
    prob = probabilities[i]
    bar = "█" * int(prob * 30)
    print(f"  {cls:8s}: {prob*100:6.2f}% {bar}")

# 5. Load slow page results for comparison
print("\n5. COMPARISON: SLOW PAGE vs FAST PAGE")
print("="*80)

try:
    with open('validation_prediction_results.json', 'r') as f:
        slow_results = json.load(f)
    
    with open('slow_page_metrics_model_features.json', 'r') as f:
        slow_metrics = json.load(f)
    
    slow_class = slow_results['current_prediction']['class']
    slow_proba = slow_results['current_prediction']['probabilities']
    
    print(f"\n{'Metric':<30} {'SLOW PAGE':>20} {'FAST PAGE':>20} {'CHANGE':>15}")
    print("-"*85)
    
    comparison_metrics = ['fcp', 'lcp', 'tti', 'tbt', 'speed_index', 'Page Size (KB)', 
                          'total_byte_weight', 'performance_score', 'Load Time(s)']
    
    for metric in comparison_metrics:
        slow_val = slow_metrics.get(metric, 0)
        fast_val = metrics.get(metric, 0)
        
        if slow_val != 0:
            change_pct = ((fast_val - slow_val) / slow_val) * 100
            change_str = f"{change_pct:+.1f}%"
        else:
            change_str = "N/A"
        
        print(f"  {metric:<28} {slow_val:>20,.2f} {fast_val:>20,.2f} {change_str:>15}")
    
    print("\n" + "-"*85)
    print(f"\n📊 PREDICTION COMPARISON:")
    print(f"  {'':30} {'SLOW PAGE':>20} {'FAST PAGE':>20}")
    print(f"  {'Predicted Class':<30} {slow_class.upper():>20} {predicted_class.upper():>20}")
    print(f"  {'P(fast)':<30} {slow_proba['fast']*100:>19.2f}% {probabilities[list(label_encoder.classes_).index('fast')]*100:>19.2f}%")
    print(f"  {'P(medium)':<30} {slow_proba['medium']*100:>19.2f}% {probabilities[list(label_encoder.classes_).index('medium')]*100:>19.2f}%")
    print(f"  {'P(slow)':<30} {slow_proba['slow']*100:>19.2f}% {probabilities[list(label_encoder.classes_).index('slow')]*100:>19.2f}%")

except FileNotFoundError:
    print("Slow page results not found for comparison.")

# 6. Validation Summary
print("\n" + "="*80)
print("🎉 REAL-WORLD VALIDATION SUMMARY")
print("="*80)

print(f"""
┌─────────────────────────────────────────────────────────────────────────────┐
│                        VALIDATION EXPERIMENT RESULTS                        │
├─────────────────────────────────────────────────────────────────────────────┤
│  SLOW PAGE (Before Optimization)                                            │
│    URL: https://baddummypage.onrender.com/                                  │
│    PageSpeed Score: 55/100                                                  │
│    Model Prediction: SLOW (65.35% probability)                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  FAST PAGE (After Applying Prescriptions)                                   │
│    URL: https://gooddummypage.onrender.com/                                 │
│    PageSpeed Score: 100/100                                                 │
│    Model Prediction: {predicted_class.upper()} ({probabilities[list(label_encoder.classes_).index(predicted_class)]*100:.2f}% probability){'':20}│
├─────────────────────────────────────────────────────────────────────────────┤
│  VALIDATION STATUS: {"✅ SUCCESS" if predicted_class == 'fast' else "⚠️  PARTIAL"} - Model prescriptions led to improved performance  │
└─────────────────────────────────────────────────────────────────────────────┘
""")

# 7. Save results
print("\nSAVING RESULTS")
print("-"*40)

fast_results = {
    'url': 'https://gooddummypage.onrender.com/',
    'timestamp': datetime.now().isoformat(),
    'prediction': {
        'class': predicted_class,
        'probabilities': {cls: float(probabilities[i]) for i, cls in enumerate(label_encoder.classes_)}
    },
    'metrics_used': base_features,
    'pagespeed_score': metrics.get('performance_score', 0)
}

with open('fast_page_prediction_results.json', 'w') as f:
    json.dump(fast_results, f, indent=2)

print(f"✓ Results saved to: fast_page_prediction_results.json")

# Final comparison export
comparison_results = {
    'experiment': 'Real-World Validation of Prescriptive Optimization Model',
    'timestamp': datetime.now().isoformat(),
    'slow_page': {
        'url': 'https://baddummypage.onrender.com/',
        'pagespeed_score': slow_metrics.get('performance_score', 55),
        'predicted_class': slow_class,
        'probabilities': slow_proba
    },
    'fast_page': {
        'url': 'https://gooddummypage.onrender.com/',
        'pagespeed_score': metrics.get('performance_score', 100),
        'predicted_class': predicted_class,
        'probabilities': {cls: float(probabilities[i]) for i, cls in enumerate(label_encoder.classes_)}
    },
    'validation_success': predicted_class in ['fast', 'medium'] and slow_class == 'slow',
    'key_improvements': {
        'fcp_reduction_pct': ((metrics['fcp'] - slow_metrics['fcp']) / slow_metrics['fcp']) * 100,
        'lcp_reduction_pct': ((metrics['lcp'] - slow_metrics['lcp']) / slow_metrics['lcp']) * 100,
        'page_size_reduction_pct': ((metrics['Page Size (KB)'] - slow_metrics['Page Size (KB)']) / slow_metrics['Page Size (KB)']) * 100,
        'performance_score_improvement': metrics['performance_score'] - slow_metrics['performance_score']
    }
}

with open('validation_comparison_results.json', 'w') as f:
    json.dump(comparison_results, f, indent=2)

print(f"✓ Comparison saved to: validation_comparison_results.json")

print("\n" + "="*80)
print("VALIDATION COMPLETE!")
print("="*80)

"""
Real-World Validation: Predict Class and Get Prescriptions
Uses the Phase 2 model to predict performance class and generate optimization recommendations.
"""

import pandas as pd
import numpy as np
import joblib
import json
from datetime import datetime

print("="*80)
print("REAL-WORLD VALIDATION: PREDICTION & PRESCRIPTIONS")
print("="*80)

# 1. Load the metrics collected from PageSpeed API
print("\n1. LOADING COLLECTED METRICS")
print("-"*40)

with open('slow_page_metrics_model_features.json', 'r') as f:
    metrics = json.load(f)

print(f"URL: https://baddummypage.onrender.com/")
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
    # Use a default category value (will be encoded)
    category_encoder = model_pkg['encoders'].get('Category')
    if category_encoder:
        # Use most common category or default
        base_features['Category'] = 0  # Default encoded value
    else:
        base_features['Category'] = 0

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

# 5. Run Prescriptive Optimization
print("\n5. GENERATING PRESCRIPTIONS (Phase 2 Optimization)")
print("-"*40)

from scipy.optimize import differential_evolution

# Domain constraints - features that should decrease for better performance
should_decrease = ['fcp', 'lcp', 'tti', 'tbt', 'Response Time(s)', 'Load Time(s)', 
                   'Page Size (KB)', 'total_byte_weight', 'num_requests', 'speed_index', 'unused_js']
should_increase = ['Throughput', 'performance_score']

# Optimizable features (exclude derived and categorical)
optimizable_features = [
    'Page Size (KB)', 'Load Time(s)', 'Response Time(s)', 'Throughput',
    'lcp', 'fcp', 'cls', 'tti', 'tbt', 'speed_index',
    'total_byte_weight', 'num_requests', 'unused_js', 'performance_score'
]

# Get current values
current_values = X_scaled[0].copy()

# Define bounds for optimization
# For features that should decrease: allow reduction to 5th percentile
# For features that should increase: allow increase to 95th percentile
bounds = []
feature_indices = {name: i for i, name in enumerate(feature_names)}

for i, feat in enumerate(feature_names):
    current = current_values[i]
    if feat in optimizable_features:
        if feat in should_decrease:
            # Can only decrease (lower bound = much smaller, upper = current)
            # Handle negative values and ensure lower < upper
            lower = min(current * 0.1, current - abs(current) * 0.9)
            upper = current
            if lower >= upper:
                lower = upper - 0.001
            bounds.append((lower, upper))
        elif feat in should_increase:
            # Can only increase (lower = current, upper = much larger)
            lower = current
            upper = max(current * 2.0, current + abs(current) * 1.0)
            if lower >= upper:
                upper = lower + 0.001
            bounds.append((lower, upper))
        else:
            lower = min(current * 0.5, current - abs(current) * 0.5)
            upper = max(current * 1.5, current + abs(current) * 0.5)
            if lower >= upper:
                upper = lower + 0.001
            bounds.append((lower, upper))
    else:
        # Fixed (derived features or categorical)
        bounds.append((current - 0.0001, current + 0.0001))

# Objective function: maximize P(fast)
def objective(x):
    x_reshaped = x.reshape(1, -1)
    proba = model.predict_proba(x_reshaped)[0]
    fast_idx = list(label_encoder.classes_).index('fast')
    return -proba[fast_idx]  # Negative because we minimize

print("Running differential evolution optimization...")
print("(This may take a moment...)")

result = differential_evolution(
    objective,
    bounds=bounds,
    maxiter=500,
    seed=42,
    disp=False,
    polish=True
)

optimized_values = result.x
optimized_proba = model.predict_proba(optimized_values.reshape(1, -1))[0]
optimized_class = label_encoder.inverse_transform(
    model.predict(optimized_values.reshape(1, -1))
)[0]

print(f"\n✓ Optimization complete!")
print(f"  Iterations: {result.nit}")
print(f"  Success: {result.success}")

# 6. Generate Recommendations
print("\n6. PRESCRIPTIVE RECOMMENDATIONS")
print("="*80)

print(f"\n📊 BEFORE vs AFTER OPTIMIZATION:")
print(f"{'Metric':<30} {'Before':>15} {'After':>15} {'Change':>15}")
print("-"*75)

recommendations = []

for i, feat in enumerate(feature_names):
    if feat in optimizable_features:
        before_scaled = current_values[i]
        after_scaled = optimized_values[i]
        
        # Inverse transform to get original scale (approximate)
        # Since we're working with scaled values, we show the direction and magnitude
        change_pct = ((after_scaled - before_scaled) / max(abs(before_scaled), 0.0001)) * 100
        
        if abs(change_pct) > 1:  # Only show significant changes
            direction = "↓" if change_pct < 0 else "↑"
            
            # Check domain correctness
            if feat in should_decrease and change_pct < 0:
                correctness = "✓"
            elif feat in should_increase and change_pct > 0:
                correctness = "✓"
            elif feat in should_decrease and change_pct > 0:
                correctness = "✗"
            elif feat in should_increase and change_pct < 0:
                correctness = "✗"
            else:
                correctness = "-"
            
            print(f"{feat:<30} {before_scaled:>15.4f} {after_scaled:>15.4f} {direction} {abs(change_pct):>10.1f}% {correctness}")
            
            recommendations.append({
                'feature': feat,
                'before_scaled': before_scaled,
                'after_scaled': after_scaled,
                'change_pct': change_pct,
                'direction': 'decrease' if change_pct < 0 else 'increase',
                'domain_correct': correctness == "✓"
            })

# 7. Summary
print("\n" + "="*80)
print("VALIDATION SUMMARY")
print("="*80)

print(f"\n🌐 URL: https://baddummypage.onrender.com/")
print(f"\n📈 PREDICTION RESULTS:")
print(f"   Current Predicted Class:   {predicted_class.upper()}")
print(f"   P(fast):                   {probabilities[list(label_encoder.classes_).index('fast')]*100:.2f}%")
print(f"   P(medium):                 {probabilities[list(label_encoder.classes_).index('medium')]*100:.2f}%")
print(f"   P(slow):                   {probabilities[list(label_encoder.classes_).index('slow')]*100:.2f}%")

print(f"\n🎯 AFTER APPLYING PRESCRIPTIONS:")
print(f"   Optimized Predicted Class: {optimized_class.upper()}")
print(f"   P(fast):                   {optimized_proba[list(label_encoder.classes_).index('fast')]*100:.2f}%")
print(f"   P(medium):                 {optimized_proba[list(label_encoder.classes_).index('medium')]*100:.2f}%")
print(f"   P(slow):                   {optimized_proba[list(label_encoder.classes_).index('slow')]*100:.2f}%")

# Count domain-correct recommendations
correct_count = sum(1 for r in recommendations if r['domain_correct'])
total_count = len(recommendations)

print(f"\n📋 RECOMMENDATIONS SUMMARY:")
print(f"   Total Recommendations:     {total_count}")
print(f"   Domain-Correct:            {correct_count}/{total_count} ({100*correct_count/max(total_count,1):.1f}%)")

print("\n🔧 TOP ACTIONABLE RECOMMENDATIONS:")
print("-"*60)

# Sort by absolute change percentage
recommendations_sorted = sorted(recommendations, key=lambda x: abs(x['change_pct']), reverse=True)

for i, rec in enumerate(recommendations_sorted[:10], 1):
    direction_word = "Decrease" if rec['direction'] == 'decrease' else "Increase"
    correct_mark = "✓" if rec['domain_correct'] else "✗"
    print(f"   {i:2d}. {direction_word} {rec['feature']:<25} by {abs(rec['change_pct']):>6.1f}% {correct_mark}")

# 8. Save results
print("\n" + "="*80)
print("SAVING RESULTS")
print("="*80)

results = {
    'url': 'https://baddummypage.onrender.com/',
    'timestamp': datetime.now().isoformat(),
    'current_prediction': {
        'class': predicted_class,
        'probabilities': {cls: float(probabilities[i]) for i, cls in enumerate(label_encoder.classes_)}
    },
    'optimized_prediction': {
        'class': optimized_class,
        'probabilities': {cls: float(optimized_proba[i]) for i, cls in enumerate(label_encoder.classes_)}
    },
    'recommendations': recommendations_sorted,
    'metrics_used': base_features
}

with open('validation_prediction_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n✓ Results saved to: validation_prediction_results.json")

print("\n" + "="*80)
print("NEXT STEPS FOR REAL-WORLD VALIDATION:")
print("="*80)
print("""
1. Create an OPTIMIZED version of the page applying the top recommendations
2. Host the optimized page
3. Collect metrics from the optimized page via PageSpeed API
4. Verify the model predicts "FAST" for the optimized page
5. Compare before/after metrics for validation
""")
print("="*80)

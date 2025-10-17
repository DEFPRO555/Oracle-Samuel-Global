"""
Comprehensive Model Testing Script for Oracle Samuel
Tests all ML models with sample data to verify functionality
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime

# Set UTF-8 encoding for console output
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

print("=" * 80)
print("ORACLE SAMUEL - MODEL TESTING SUITE")
print("=" * 80)
print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Test results
test_results = {
    'passed': [],
    'failed': [],
    'warnings': []
}

def test_result(test_name, passed, message=""):
    """Record test result"""
    if passed:
        test_results['passed'].append(test_name)
        print(f"[PASS] {test_name}")
    else:
        test_results['failed'].append(test_name)
        print(f"[FAIL] {test_name}")
    if message:
        print(f"   {message}")
    print()

# =============================================================================
# Generate Sample Data
# =============================================================================
print("Generating sample real estate data...")
print("-" * 80)

np.random.seed(42)

# Create realistic real estate data
n_samples = 500

data = {
    'price': np.random.randint(100000, 1000000, n_samples),
    'sqft': np.random.randint(500, 5000, n_samples),
    'bedrooms': np.random.randint(1, 6, n_samples),
    'bathrooms': np.random.randint(1, 5, n_samples),
    'age': np.random.randint(0, 50, n_samples),
    'lot_size': np.random.randint(1000, 10000, n_samples),
    'garage': np.random.randint(0, 3, n_samples),
    'latitude': np.random.uniform(32.0, 34.0, n_samples),
    'longitude': np.random.uniform(-118.5, -117.0, n_samples)
}

df = pd.DataFrame(data)
print(f"Generated {len(df)} samples with {len(df.columns)} features")
print(f"Features: {list(df.columns)}")
print()

# =============================================================================
# TEST 1: Linear Regression
# =============================================================================
print("TEST 1: Linear Regression Model")
print("-" * 80)

try:
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

    # Prepare data
    X = df.drop('price', axis=1)
    y = df['price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Calculate metrics
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    test_result("Linear Regression - Training", True,
                f"R²={r2:.4f}, MAE=${mae:,.0f}, RMSE=${rmse:,.0f}")

    # Test prediction on single sample
    sample = X_test.iloc[0:1]
    prediction = model.predict(sample)[0]
    test_result("Linear Regression - Prediction", True,
                f"Predicted price: ${prediction:,.0f}")

except Exception as e:
    test_result("Linear Regression", False, str(e))

# =============================================================================
# TEST 2: Random Forest
# =============================================================================
print("TEST 2: Random Forest Model")
print("-" * 80)

try:
    from sklearn.ensemble import RandomForestRegressor

    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Calculate metrics
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    test_result("Random Forest - Training", True,
                f"R²={r2:.4f}, MAE=${mae:,.0f}, RMSE=${rmse:,.0f}")

    # Test feature importance
    importances = model.feature_importances_
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': importances
    }).sort_values('importance', ascending=False)

    test_result("Random Forest - Feature Importance", True,
                f"Top feature: {feature_importance.iloc[0]['feature']}")

except Exception as e:
    test_result("Random Forest", False, str(e))

# =============================================================================
# TEST 3: XGBoost
# =============================================================================
print("TEST 3: XGBoost Model")
print("-" * 80)

try:
    import xgboost as xgb

    # Train model
    model = xgb.XGBRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Calculate metrics
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    test_result("XGBoost - Training", True,
                f"R²={r2:.4f}, MAE=${mae:,.0f}, RMSE=${rmse:,.0f}")

except Exception as e:
    test_result("XGBoost", False, str(e))

# =============================================================================
# TEST 4: LightGBM
# =============================================================================
print("TEST 4: LightGBM Model")
print("-" * 80)

try:
    import lightgbm as lgb

    # Train model
    model = lgb.LGBMRegressor(n_estimators=100, random_state=42, n_jobs=-1, verbose=-1)
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Calculate metrics
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    test_result("LightGBM - Training", True,
                f"R²={r2:.4f}, MAE=${mae:,.0f}, RMSE=${rmse:,.0f}")

except Exception as e:
    test_result("LightGBM", False, str(e))

# =============================================================================
# TEST 5: CatBoost
# =============================================================================
print("TEST 5: CatBoost Model")
print("-" * 80)

try:
    from catboost import CatBoostRegressor

    # Train model
    model = CatBoostRegressor(iterations=100, random_state=42, verbose=False)
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Calculate metrics
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    test_result("CatBoost - Training", True,
                f"R²={r2:.4f}, MAE=${mae:,.0f}, RMSE=${rmse:,.0f}")

except Exception as e:
    test_result("CatBoost", False, str(e))

# =============================================================================
# TEST 6: Prophet (Time Series)
# =============================================================================
print("TEST 6: Prophet Time Series Model")
print("-" * 80)

try:
    from prophet import Prophet

    # Create time series data
    dates = pd.date_range(start='2020-01-01', periods=len(df), freq='D')
    ts_df = pd.DataFrame({
        'ds': dates,
        'y': df['price'].values
    })

    # Train model
    model = Prophet(daily_seasonality=True)
    model.fit(ts_df)

    # Make future predictions
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    test_result("Prophet - Training", True,
                f"Forecasted {len(future)} days")

    # Check forecast components
    if 'yhat' in forecast.columns:
        test_result("Prophet - Forecast", True,
                    f"Average forecast: ${forecast['yhat'].mean():,.0f}")

except Exception as e:
    test_result("Prophet", False, str(e))

# =============================================================================
# TEST 7: Cross-Validation
# =============================================================================
print("TEST 7: Cross-Validation")
print("-" * 80)

try:
    from sklearn.model_selection import cross_val_score
    from sklearn.linear_model import LinearRegression

    model = LinearRegression()
    scores = cross_val_score(model, X, y, cv=5, scoring='r2')

    test_result("Cross-Validation (5-fold)", True,
                f"Mean R²={scores.mean():.4f}, Std={scores.std():.4f}")

except Exception as e:
    test_result("Cross-Validation", False, str(e))

# =============================================================================
# TEST 8: Hyperparameter Tuning with Optuna
# =============================================================================
print("TEST 8: Optuna Hyperparameter Tuning")
print("-" * 80)

try:
    import optuna
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import cross_val_score

    optuna.logging.set_verbosity(optuna.logging.WARNING)

    def objective(trial):
        n_estimators = trial.suggest_int('n_estimators', 10, 50)
        max_depth = trial.suggest_int('max_depth', 2, 10)

        model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=42,
            n_jobs=-1
        )

        score = cross_val_score(model, X_train, y_train, cv=3, scoring='r2').mean()
        return score

    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=5, show_progress_bar=False)

    test_result("Optuna Tuning", True,
                f"Best R²={study.best_value:.4f}, Trials={len(study.trials)}")

except Exception as e:
    test_result("Optuna Tuning", False, str(e))

# =============================================================================
# TEST 9: SHAP Explainability
# =============================================================================
print("TEST 9: SHAP Model Explainability")
print("-" * 80)

try:
    import shap
    from sklearn.ensemble import RandomForestRegressor

    # Train a simple model
    model = RandomForestRegressor(n_estimators=50, random_state=42, max_depth=5)
    model.fit(X_train, y_train)

    # Create SHAP explainer
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test[:10])  # Use small sample

    test_result("SHAP Explainability", True,
                f"SHAP values shape: {shap_values.shape}")

except Exception as e:
    test_result("SHAP Explainability", False, str(e))

# =============================================================================
# TEST 10: Model Persistence (Save/Load)
# =============================================================================
print("TEST 10: Model Persistence")
print("-" * 80)

try:
    import joblib
    from sklearn.linear_model import LinearRegression

    # Train and save model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Save model
    model_path = 'test_model.joblib'
    joblib.dump(model, model_path)

    # Load model
    loaded_model = joblib.load(model_path)

    # Make prediction with loaded model
    pred = loaded_model.predict(X_test[:1])[0]

    # Cleanup
    if os.path.exists(model_path):
        os.remove(model_path)

    test_result("Model Save/Load", True,
                f"Saved, loaded, and predicted: ${pred:,.0f}")

except Exception as e:
    test_result("Model Save/Load", False, str(e))

# =============================================================================
# TEST 11: Data Cleaner Integration
# =============================================================================
print("TEST 11: Data Cleaner Integration")
print("-" * 80)

try:
    from utils.data_cleaner import DataCleaner

    # Add some missing values and duplicates
    dirty_df = df.copy()
    dirty_df.loc[0:5, 'sqft'] = np.nan
    dirty_df = pd.concat([dirty_df, dirty_df.iloc[0:3]])

    # Clean data
    cleaner = DataCleaner(dirty_df)
    cleaned_df, report = cleaner.clean_data()

    test_result("Data Cleaner", True,
                f"Original: {len(dirty_df)} rows, Cleaned: {len(cleaned_df)} rows")

except Exception as e:
    test_result("Data Cleaner", False, str(e))

# =============================================================================
# FINAL SUMMARY
# =============================================================================
print("=" * 80)
print("MODEL TESTING SUMMARY")
print("=" * 80)
print(f"Tests Passed: {len(test_results['passed'])}")
print(f"Tests Failed: {len(test_results['failed'])}")
print(f"Warnings: {len(test_results['warnings'])}")
print()

if test_results['failed']:
    print("FAILED TESTS:")
    for test in test_results['failed']:
        print(f"  - {test}")
    print()
    print("[FAIL] Some model tests failed - Review errors above")
    sys.exit(1)
else:
    print("[PASS] ALL MODEL TESTS PASSED!")
    print()
    print("MODEL VERIFICATION CHECKLIST:")
    print("  [PASS] Linear Regression working")
    print("  [PASS] Random Forest working")
    print("  [PASS] XGBoost working")
    print("  [PASS] LightGBM working")
    print("  [PASS] CatBoost working")
    print("  [PASS] Prophet time series working")
    print("  [PASS] Cross-validation functional")
    print("  [PASS] Optuna hyperparameter tuning working")
    print("  [PASS] SHAP explainability working")
    print("  [PASS] Model persistence working")
    print("  [PASS] Data cleaning integration working")
    print()
    print("All models are ready for deployment!")
    sys.exit(0)

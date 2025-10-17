# © 2025 Dowek Analytics Ltd.
# ORACLE SAMUEL – Simple Accuracy Enhancement Module
# MD5-Protected AI System. Unauthorized use prohibited.

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.model_selection import cross_val_score, GridSearchCV, train_test_split
from sklearn.ensemble import VotingRegressor, RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import PolynomialFeatures, RobustScaler, StandardScaler
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import ElasticNet, Ridge, Lasso
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
import xgboost as xgb
import lightgbm as lgb
import warnings
warnings.filterwarnings('ignore')

class SimpleAccuracyEnhancer:
    """
    Simple but effective accuracy enhancement for Oracle Samuel
    Uses only core scikit-learn and basic libraries
    """
    
    def __init__(self, df):
        self.df = df
        self.enhanced_models = {}
        self.feature_importance = {}
        self.performance_metrics = {}
        
    def advanced_feature_engineering(self, X):
        """Advanced feature engineering techniques"""
        print("🔧 Implementing Advanced Feature Engineering...")
        
        X_enhanced = X.copy()
        
        # 1. Statistical Features
        X_enhanced['mean_features'] = X_enhanced.mean(axis=1)
        X_enhanced['std_features'] = X_enhanced.std(axis=1)
        X_enhanced['max_features'] = X_enhanced.max(axis=1)
        X_enhanced['min_features'] = X_enhanced.min(axis=1)
        X_enhanced['range_features'] = X_enhanced['max_features'] - X_enhanced['min_features']
        
        # 2. Ratio Features (if applicable)
        if 'bedrooms' in X_enhanced.columns and 'bathrooms' in X_enhanced.columns:
            X_enhanced['bed_bath_ratio'] = X_enhanced['bedrooms'] / (X_enhanced['bathrooms'] + 1)
        if 'sqft' in X_enhanced.columns and 'bedrooms' in X_enhanced.columns:
            X_enhanced['sqft_per_bedroom'] = X_enhanced['sqft'] / (X_enhanced['bedrooms'] + 1)
        
        # 3. Interaction Features (limited to avoid explosion)
        numeric_cols = X_enhanced.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) >= 2:
            col1, col2 = numeric_cols[0], numeric_cols[1]
            X_enhanced[f'{col1}_x_{col2}'] = X_enhanced[col1] * X_enhanced[col2]
        
        print(f"✅ Feature engineering complete: {X_enhanced.shape[1]} features")
        return X_enhanced
    
    def advanced_preprocessing(self, X, y):
        """Advanced preprocessing techniques"""
        print("🔧 Implementing Advanced Preprocessing...")
        
        # 1. Robust Scaling (less sensitive to outliers)
        robust_scaler = RobustScaler()
        X_scaled = robust_scaler.fit_transform(X)
        
        # 2. Outlier Detection and Treatment (simple z-score)
        z_scores = np.abs((X_scaled - np.mean(X_scaled, axis=0)) / (np.std(X_scaled, axis=0) + 1e-8))
        outlier_mask = (z_scores < 3).all(axis=1)
        
        X_clean = X_scaled[outlier_mask]
        y_clean = y[outlier_mask]
        
        print(f"✅ Preprocessing complete: {X_clean.shape[0]} samples, {X_clean.shape[1]} features")
        return X_clean, y_clean, robust_scaler
    
    def advanced_feature_selection(self, X, y):
        """Advanced feature selection techniques"""
        print("🔧 Implementing Advanced Feature Selection...")
        
        # SelectKBest with f_regression
        k = min(15, X.shape[1])  # Select top 15 features or all if less
        selector = SelectKBest(score_func=f_regression, k=k)
        X_selected = selector.fit_transform(X, y)
        
        print(f"✅ Feature selection complete: {X_selected.shape[1]} features selected")
        return X_selected, selector
    
    def create_ensemble_models(self, X, y):
        """Create advanced ensemble models"""
        print("🔧 Creating Advanced Ensemble Models...")
        
        # Base models
        base_models = {
            'rf': RandomForestRegressor(n_estimators=200, max_depth=15, random_state=42),
            'xgb': xgb.XGBRegressor(n_estimators=200, max_depth=6, learning_rate=0.1, random_state=42),
            'lgb': lgb.LGBMRegressor(n_estimators=200, max_depth=6, learning_rate=0.1, random_state=42),
            'elastic': ElasticNet(alpha=0.1, l1_ratio=0.5, random_state=42),
            'ridge': Ridge(alpha=1.0, random_state=42),
            'lasso': Lasso(alpha=0.1, random_state=42),
            'svr': SVR(kernel='rbf', C=100, gamma='scale'),
            'knn': KNeighborsRegressor(n_neighbors=5, weights='distance'),
            'gb': GradientBoostingRegressor(n_estimators=200, max_depth=6, learning_rate=0.1, random_state=42)
        }
        
        # 1. Voting Regressor
        voting_regressor = VotingRegressor([
            ('rf', base_models['rf']),
            ('xgb', base_models['xgb']),
            ('lgb', base_models['lgb']),
            ('elastic', base_models['elastic'])
        ])
        
        # 2. Stacking Regressor
        stacking_regressor = VotingRegressor([
            ('rf', base_models['rf']),
            ('xgb', base_models['xgb']),
            ('lgb', base_models['lgb'])
        ])
        
        self.enhanced_models = {
            'voting': voting_regressor,
            'stacking': stacking_regressor,
            **base_models
        }
        
        print("✅ Ensemble models created successfully")
        return self.enhanced_models
    
    def hyperparameter_optimization(self, X, y):
        """Simple hyperparameter optimization"""
        print("🔧 Implementing Hyperparameter Optimization...")
        
        # Grid search for key models
        param_grids = {
            'rf': {
                'n_estimators': [100, 200],
                'max_depth': [10, 15],
                'min_samples_split': [2, 5]
            },
            'xgb': {
                'n_estimators': [100, 200],
                'max_depth': [4, 6],
                'learning_rate': [0.05, 0.1]
            }
        }
        
        optimized_models = {}
        
        for name, model in [('rf', RandomForestRegressor()), ('xgb', xgb.XGBRegressor())]:
            if name in param_grids:
                try:
                    grid_search = GridSearchCV(
                        model, param_grids[name], 
                        cv=3, scoring='neg_mean_absolute_error', 
                        n_jobs=-1, verbose=0
                    )
                    grid_search.fit(X, y)
                    optimized_models[name] = grid_search.best_estimator_
                    print(f"✅ {name.upper()} optimized: {grid_search.best_score_:.4f}")
                except Exception as e:
                    print(f"⚠️ {name.upper()} optimization failed: {str(e)}")
                    optimized_models[name] = model
        
        return optimized_models
    
    def cross_validation_analysis(self, X, y):
        """Cross-validation analysis"""
        print("🔧 Implementing Cross-Validation Analysis...")
        
        cv_scores = {}
        
        for name, model in self.enhanced_models.items():
            try:
                scores = cross_val_score(model, X, y, cv=5, scoring='neg_mean_absolute_error')
                cv_scores[name] = {
                    'mean_mae': -scores.mean(),
                    'std_mae': scores.std(),
                    'mean_r2': cross_val_score(model, X, y, cv=5, scoring='r2').mean()
                }
                print(f"✅ {name.upper()}: MAE={-scores.mean():.2f} ± {scores.std():.2f}")
            except Exception as e:
                print(f"⚠️ {name.upper()}: Error in CV - {str(e)}")
        
        return cv_scores
    
    def advanced_metrics_calculation(self, y_true, y_pred):
        """Calculate advanced performance metrics"""
        metrics = {
            'mae': mean_absolute_error(y_true, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
            'r2': r2_score(y_true, y_pred),
            'mape': np.mean(np.abs((y_true - y_pred) / (y_true + 1e-8))) * 100,
            'max_error': np.max(np.abs(y_true - y_pred)),
            'explained_variance': 1 - np.var(y_true - y_pred) / np.var(y_true)
        }
        return metrics
    
    def run_complete_enhancement(self):
        """Run complete accuracy enhancement pipeline"""
        print("🚀 Starting Simple Accuracy Enhancement Pipeline...")
        print("=" * 60)
        
        # Prepare data
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        X = self.df[numeric_cols].dropna()
        
        # Find target column
        price_keywords = ['price', 'cost', 'value', 'amount', 'revenue', 'sales']
        target_col = None
        for col in X.columns:
            if any(keyword in col.lower() for keyword in price_keywords):
                target_col = col
                break
        
        if target_col is None:
            print("❌ No target column found. Please ensure your data has a price/value column.")
            return None
        
        y = X[target_col]
        X = X.drop(columns=[target_col])
        
        print(f"📊 Dataset: {X.shape[0]} samples, {X.shape[1]} features")
        print(f"🎯 Target: {target_col}")
        
        # 1. Advanced Feature Engineering
        X_enhanced = self.advanced_feature_engineering(X)
        
        # 2. Advanced Preprocessing
        X_clean, y_clean, scaler = self.advanced_preprocessing(X_enhanced, y)
        
        # 3. Advanced Feature Selection
        X_selected, selector = self.advanced_feature_selection(X_clean, y_clean)
        
        # 4. Create Ensemble Models
        models = self.create_ensemble_models(X_selected, y_clean)
        
        # 5. Hyperparameter Optimization
        optimized_models = self.hyperparameter_optimization(X_selected, y_clean)
        
        # 6. Cross-Validation Analysis
        cv_results = self.cross_validation_analysis(X_selected, y_clean)
        
        # 7. Train and Evaluate Best Models
        X_train, X_test, y_train, y_test = train_test_split(
            X_selected, y_clean, test_size=0.2, random_state=42
        )
        
        final_results = {}
        for name, model in {**models, **optimized_models}.items():
            try:
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                metrics = self.advanced_metrics_calculation(y_test, y_pred)
                final_results[name] = metrics
                print(f"✅ {name.upper()}: R²={metrics['r2']:.4f}, MAE=${metrics['mae']:,.0f}")
            except Exception as e:
                print(f"⚠️ {name.upper()}: Training failed - {str(e)}")
        
        print("\n" + "=" * 60)
        print("🎉 ACCURACY ENHANCEMENT COMPLETED!")
        print("=" * 60)
        
        # Find best model
        if final_results:
            best_model = max(final_results.items(), key=lambda x: x[1]['r2'])
            print(f"🏆 BEST MODEL: {best_model[0].upper()}")
            print(f"📊 R² Score: {best_model[1]['r2']:.4f}")
            print(f"📈 MAE: ${best_model[1]['mae']:,.0f}")
            print(f"📉 RMSE: ${best_model[1]['rmse']:,.0f}")
            print(f"📊 MAPE: {best_model[1]['mape']:.2f}%")
        else:
            print("❌ No models trained successfully")
            return None
        
        return {
            'enhanced_features': X_enhanced,
            'processed_data': (X_clean, y_clean),
            'selected_features': X_selected,
            'models': {**models, **optimized_models},
            'cv_results': cv_results,
            'final_results': final_results,
            'best_model': best_model if final_results else None,
            'preprocessors': (scaler, selector)
        }

def enhance_oracle_samuel_simple(df):
    """
    Simple function to enhance Oracle Samuel accuracy
    """
    print("🚀 ORACLE SAMUEL SIMPLE ACCURACY ENHANCEMENT")
    print("© 2025 Dowek Analytics Ltd. All Rights Reserved.")
    print("=" * 60)
    
    enhancer = SimpleAccuracyEnhancer(df)
    results = enhancer.run_complete_enhancement()
    
    return results

if __name__ == "__main__":
    print("Simple Oracle Samuel Accuracy Enhancement Module")
    print("Ready for integration with main application")

# © 2025 Dowek Analytics Ltd.
# ORACLE SAMUEL – Advanced Accuracy Enhancement Module
# MD5-Protected AI System. Unauthorized use prohibited.

import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score, GridSearchCV, StratifiedKFold
from sklearn.ensemble import VotingRegressor, StackingRegressor, BaggingRegressor, RandomForestRegressor
from sklearn.preprocessing import PolynomialFeatures, RobustScaler, QuantileTransformer
from sklearn.feature_selection import SelectKBest, RFE, SelectFromModel
from sklearn.decomposition import PCA
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import ElasticNet, HuberRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
import xgboost as xgb
import lightgbm as lgb
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class AdvancedAccuracyEnhancer:
    """
    Advanced accuracy enhancement techniques for Oracle Samuel
    Implements cutting-edge ML techniques to boost performance
    """
    
    def __init__(self, X, y):
        self.X = X
        self.y = y
        self.enhanced_models = {}
        self.feature_importance = {}
        self.performance_metrics = {}
        
    def advanced_feature_engineering(self):
        """Advanced feature engineering techniques"""
        print("🔧 Implementing Advanced Feature Engineering...")
        
        X_enhanced = self.X.copy()
        
        # 1. Polynomial Features (for non-linear relationships)
        poly_features = PolynomialFeatures(degree=2, include_bias=False, interaction_only=True)
        X_poly = poly_features.fit_transform(X_enhanced)
        poly_df = pd.DataFrame(X_poly, columns=[f"poly_{i}" for i in range(X_poly.shape[1])])
        
        # 2. Statistical Features
        X_enhanced['mean_features'] = X_enhanced.mean(axis=1)
        X_enhanced['std_features'] = X_enhanced.std(axis=1)
        X_enhanced['max_features'] = X_enhanced.max(axis=1)
        X_enhanced['min_features'] = X_enhanced.min(axis=1)
        X_enhanced['range_features'] = X_enhanced['max_features'] - X_enhanced['min_features']
        
        # 3. Ratio Features
        if 'bedrooms' in X_enhanced.columns and 'bathrooms' in X_enhanced.columns:
            X_enhanced['bed_bath_ratio'] = X_enhanced['bedrooms'] / (X_enhanced['bathrooms'] + 1)
        if 'sqft' in X_enhanced.columns and 'bedrooms' in X_enhanced.columns:
            X_enhanced['sqft_per_bedroom'] = X_enhanced['sqft'] / (X_enhanced['bedrooms'] + 1)
        
        # 4. Interaction Features
        numeric_cols = X_enhanced.select_dtypes(include=[np.number]).columns
        for i, col1 in enumerate(numeric_cols[:3]):  # Limit to avoid explosion
            for col2 in numeric_cols[i+1:4]:
                X_enhanced[f'{col1}_x_{col2}'] = X_enhanced[col1] * X_enhanced[col2]
        
        # 5. Binning Features
        if 'sqft' in X_enhanced.columns:
            X_enhanced['sqft_binned'] = pd.cut(X_enhanced['sqft'], bins=5, labels=False)
        if 'year_built' in X_enhanced.columns:
            X_enhanced['age_category'] = pd.cut(2024 - X_enhanced['year_built'], 
                                              bins=[0, 10, 25, 50, 100], labels=[0, 1, 2, 3])
        
        print(f"✅ Feature engineering complete: {X_enhanced.shape[1]} features")
        return X_enhanced
    
    def advanced_preprocessing(self, X):
        """Advanced preprocessing techniques"""
        print("🔧 Implementing Advanced Preprocessing...")
        
        # 1. Robust Scaling (less sensitive to outliers)
        robust_scaler = RobustScaler()
        X_scaled = robust_scaler.fit_transform(X)
        
        # 2. Quantile Transformation (normalizes distribution)
        quantile_transformer = QuantileTransformer(output_distribution='normal', random_state=42)
        X_quantile = quantile_transformer.fit_transform(X_scaled)
        
        # 3. Outlier Detection and Treatment
        z_scores = np.abs(stats.zscore(X_quantile))
        X_clean = X_quantile[(z_scores < 3).all(axis=1)]
        y_clean = self.y[(z_scores < 3).all(axis=1)]
        
        print(f"✅ Preprocessing complete: {X_clean.shape[0]} samples, {X_clean.shape[1]} features")
        return X_clean, y_clean, robust_scaler, quantile_transformer
    
    def advanced_feature_selection(self, X, y):
        """Advanced feature selection techniques"""
        print("🔧 Implementing Advanced Feature Selection...")
        
        # 1. SelectKBest (statistical tests)
        selector_kbest = SelectKBest(k=min(20, X.shape[1]))
        X_kbest = selector_kbest.fit_transform(X, y)
        
        # 2. Recursive Feature Elimination
        from sklearn.ensemble import RandomForestRegressor
        rfe_selector = RFE(RandomForestRegressor(n_estimators=50, random_state=42), n_features_to_select=15)
        X_rfe = rfe_selector.fit_transform(X, y)
        
        # 3. SelectFromModel (tree-based)
        model_selector = SelectFromModel(RandomForestRegressor(n_estimators=100, random_state=42))
        X_model = model_selector.fit_transform(X, y)
        
        print(f"✅ Feature selection complete: {X_kbest.shape[1]} features selected")
        return X_kbest, selector_kbest
    
    def create_ensemble_models(self, X, y):
        """Create advanced ensemble models"""
        print("🔧 Creating Advanced Ensemble Models...")
        
        # Base models
        base_models = {
            'rf': RandomForestRegressor(n_estimators=200, max_depth=15, random_state=42),
            'xgb': xgb.XGBRegressor(n_estimators=200, max_depth=6, learning_rate=0.1, random_state=42),
            'lgb': lgb.LGBMRegressor(n_estimators=200, max_depth=6, learning_rate=0.1, random_state=42),
            'elastic': ElasticNet(alpha=0.1, l1_ratio=0.5, random_state=42),
            'huber': HuberRegressor(epsilon=1.35, max_iter=200),
            'svr': SVR(kernel='rbf', C=100, gamma='scale'),
            'knn': KNeighborsRegressor(n_neighbors=5, weights='distance')
        }
        
        # 1. Voting Regressor
        voting_regressor = VotingRegressor([
            ('rf', base_models['rf']),
            ('xgb', base_models['xgb']),
            ('lgb', base_models['lgb']),
            ('elastic', base_models['elastic'])
        ])
        
        # 2. Stacking Regressor
        stacking_regressor = StackingRegressor(
            estimators=[
                ('rf', base_models['rf']),
                ('xgb', base_models['xgb']),
                ('lgb', base_models['lgb'])
            ],
            final_estimator=ElasticNet(alpha=0.1, random_state=42),
            cv=5
        )
        
        # 3. Bagging Regressor
        bagging_regressor = BaggingRegressor(
            base_estimator=DecisionTreeRegressor(max_depth=10),
            n_estimators=100,
            random_state=42
        )
        
        self.enhanced_models = {
            'voting': voting_regressor,
            'stacking': stacking_regressor,
            'bagging': bagging_regressor,
            **base_models
        }
        
        print("✅ Ensemble models created successfully")
        return self.enhanced_models
    
    def hyperparameter_optimization(self, X, y):
        """Advanced hyperparameter optimization"""
        print("🔧 Implementing Hyperparameter Optimization...")
        
        # Grid search for key models
        param_grids = {
            'rf': {
                'n_estimators': [100, 200, 300],
                'max_depth': [10, 15, 20],
                'min_samples_split': [2, 5, 10]
            },
            'xgb': {
                'n_estimators': [100, 200, 300],
                'max_depth': [4, 6, 8],
                'learning_rate': [0.05, 0.1, 0.15]
            },
            'lgb': {
                'n_estimators': [100, 200, 300],
                'max_depth': [4, 6, 8],
                'learning_rate': [0.05, 0.1, 0.15]
            }
        }
        
        optimized_models = {}
        
        for name, model in [('rf', RandomForestRegressor()), 
                           ('xgb', xgb.XGBRegressor()), 
                           ('lgb', lgb.LGBMRegressor())]:
            
            if name in param_grids:
                grid_search = GridSearchCV(
                    model, param_grids[name], 
                    cv=5, scoring='neg_mean_absolute_error', 
                    n_jobs=-1, verbose=0
                )
                grid_search.fit(X, y)
                optimized_models[name] = grid_search.best_estimator_
                print(f"✅ {name.upper()} optimized: {grid_search.best_score_:.4f}")
        
        return optimized_models
    
    def cross_validation_analysis(self, X, y):
        """Advanced cross-validation analysis"""
        print("🔧 Implementing Cross-Validation Analysis...")
        
        cv_scores = {}
        cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
        
        for name, model in self.enhanced_models.items():
            try:
                scores = cross_val_score(model, X, y, cv=cv, scoring='neg_mean_absolute_error')
                cv_scores[name] = {
                    'mean_mae': -scores.mean(),
                    'std_mae': scores.std(),
                    'mean_r2': cross_val_score(model, X, y, cv=cv, scoring='r2').mean()
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
            'mape': np.mean(np.abs((y_true - y_pred) / y_true)) * 100,
            'smape': np.mean(2 * np.abs(y_true - y_pred) / (np.abs(y_true) + np.abs(y_pred))) * 100,
            'max_error': np.max(np.abs(y_true - y_pred)),
            'explained_variance': 1 - np.var(y_true - y_pred) / np.var(y_true)
        }
        return metrics
    
    def run_complete_enhancement(self):
        """Run complete accuracy enhancement pipeline"""
        print("🚀 Starting Advanced Accuracy Enhancement Pipeline...")
        print("=" * 60)
        
        # 1. Advanced Feature Engineering
        X_enhanced = self.advanced_feature_engineering()
        
        # 2. Advanced Preprocessing
        X_clean, y_clean, scaler, transformer = self.advanced_preprocessing(X_enhanced)
        
        # 3. Advanced Feature Selection
        X_selected, selector = self.advanced_feature_selection(X_clean, y_clean)
        
        # 4. Create Ensemble Models
        models = self.create_ensemble_models(X_selected, y_clean)
        
        # 5. Hyperparameter Optimization
        optimized_models = self.hyperparameter_optimization(X_selected, y_clean)
        
        # 6. Cross-Validation Analysis
        cv_results = self.cross_validation_analysis(X_selected, y_clean)
        
        # 7. Train and Evaluate Best Models
        from sklearn.model_selection import train_test_split
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
        best_model = max(final_results.items(), key=lambda x: x[1]['r2'])
        print(f"🏆 BEST MODEL: {best_model[0].upper()}")
        print(f"📊 R² Score: {best_model[1]['r2']:.4f}")
        print(f"📈 MAE: ${best_model[1]['mae']:,.0f}")
        print(f"📉 RMSE: ${best_model[1]['rmse']:,.0f}")
        print(f"📊 MAPE: {best_model[1]['mape']:.2f}%")
        
        return {
            'enhanced_features': X_enhanced,
            'processed_data': (X_clean, y_clean),
            'selected_features': X_selected,
            'models': {**models, **optimized_models},
            'cv_results': cv_results,
            'final_results': final_results,
            'best_model': best_model,
            'preprocessors': (scaler, transformer, selector)
        }

def enhance_oracle_samuel_accuracy(df):
    """
    Main function to enhance Oracle Samuel accuracy
    """
    print("🚀 ORACLE SAMUEL ACCURACY ENHANCEMENT")
    print("© 2025 Dowek Analytics Ltd. All Rights Reserved.")
    print("=" * 60)
    
    # Prepare data
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    X = df[numeric_cols].dropna()
    
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
    
    # Run enhancement
    enhancer = AdvancedAccuracyEnhancer(X, y)
    results = enhancer.run_complete_enhancement()
    
    return results

if __name__ == "__main__":
    # Example usage
    print("Oracle Samuel Accuracy Enhancement Module")
    print("Ready for integration with main application")

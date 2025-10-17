# © 2025 Dowek Analytics Ltd.
# ORACLE SAMUEL – Advanced ML Features Module
# MD5-Protected AI System. Unauthorized use prohibited.

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import DBSCAN, AgglomerativeClustering
from sklearn.decomposition import PCA, FastICA
from sklearn.manifold import TSNE
from sklearn.neural_network import MLPRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel
import xgboost as xgb
import lightgbm as lgb
from catboost import CatBoostRegressor
import optuna
import shap
import lime
import lime.lime_tabular
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class AdvancedMLFeatures:
    """
    Advanced Machine Learning features for Oracle Samuel
    Implements cutting-edge ML techniques and visualizations
    """
    
    def __init__(self, df):
        self.df = df
        self.models = {}
        self.explanations = {}
        self.visualizations = {}
        
    def neural_network_regression(self, X, y):
        """Advanced Neural Network Regression"""
        print("🧠 Implementing Neural Network Regression...")
        
        # Multiple neural network architectures
        architectures = [
            {'hidden_layer_sizes': (100,), 'activation': 'relu', 'solver': 'adam'},
            {'hidden_layer_sizes': (100, 50), 'activation': 'relu', 'solver': 'adam'},
            {'hidden_layer_sizes': (200, 100, 50), 'activation': 'relu', 'solver': 'adam'},
            {'hidden_layer_sizes': (100,), 'activation': 'tanh', 'solver': 'lbfgs'},
            {'hidden_layer_sizes': (100, 50), 'activation': 'logistic', 'solver': 'adam'}
        ]
        
        nn_models = {}
        for i, arch in enumerate(architectures):
            try:
                model = MLPRegressor(
                    **arch,
                    max_iter=1000,
                    random_state=42,
                    early_stopping=True,
                    validation_fraction=0.1
                )
                model.fit(X, y)
                nn_models[f'NN_Arch_{i+1}'] = model
                print(f"✅ Neural Network {i+1}: {arch['hidden_layer_sizes']} layers")
            except Exception as e:
                print(f"⚠️ Neural Network {i+1}: Failed - {str(e)}")
        
        return nn_models
    
    def gaussian_process_regression(self, X, y):
        """Gaussian Process Regression with different kernels"""
        print("🌊 Implementing Gaussian Process Regression...")
        
        kernels = [
            RBF(length_scale=1.0),
            RBF(length_scale=1.0) + WhiteKernel(noise_level=0.1),
            RBF(length_scale=0.5) + WhiteKernel(noise_level=0.05),
        ]
        
        gp_models = {}
        for i, kernel in enumerate(kernels):
            try:
                model = GaussianProcessRegressor(
                    kernel=kernel,
                    random_state=42,
                    n_restarts_optimizer=10
                )
                model.fit(X, y)
                gp_models[f'GP_Kernel_{i+1}'] = model
                print(f"✅ Gaussian Process {i+1}: Kernel optimized")
            except Exception as e:
                print(f"⚠️ Gaussian Process {i+1}: Failed - {str(e)}")
        
        return gp_models
    
    def advanced_clustering(self, X):
        """Advanced clustering algorithms"""
        print("🎯 Implementing Advanced Clustering...")
        
        # DBSCAN clustering
        dbscan = DBSCAN(eps=0.5, min_samples=5)
        dbscan_labels = dbscan.fit_predict(X)
        
        # Agglomerative clustering
        agg_clustering = AgglomerativeClustering(n_clusters=3, linkage='ward')
        agg_labels = agg_clustering.fit_predict(X)
        
        # Hierarchical clustering with different linkages
        linkages = ['ward', 'complete', 'average', 'single']
        hierarchical_models = {}
        
        for linkage in linkages:
            try:
                model = AgglomerativeClustering(n_clusters=3, linkage=linkage)
                labels = model.fit_predict(X)
                hierarchical_models[f'Hierarchical_{linkage}'] = labels
                print(f"✅ Hierarchical Clustering: {linkage} linkage")
            except Exception as e:
                print(f"⚠️ Hierarchical {linkage}: Failed - {str(e)}")
        
        return {
            'dbscan': dbscan_labels,
            'agglomerative': agg_labels,
            'hierarchical': hierarchical_models
        }
    
    def dimensionality_reduction(self, X):
        """Advanced dimensionality reduction techniques"""
        print("📐 Implementing Dimensionality Reduction...")
        
        # PCA
        pca = PCA(n_components=min(10, X.shape[1]))
        X_pca = pca.fit_transform(X)
        
        # FastICA
        ica = FastICA(n_components=min(10, X.shape[1]), random_state=42)
        X_ica = ica.fit_transform(X)
        
        # t-SNE
        if X.shape[0] < 1000:  # t-SNE is computationally expensive
            tsne = TSNE(n_components=2, random_state=42, perplexity=min(30, X.shape[0]//4))
            X_tsne = tsne.fit_transform(X)
        else:
            X_tsne = None
            print("⚠️ t-SNE skipped: Dataset too large")
        
        return {
            'pca': (X_pca, pca),
            'ica': (X_ica, ica),
            'tsne': (X_tsne, tsne if X_tsne is not None else None)
        }
    
    def catboost_regression(self, X, y):
        """CatBoost regression for categorical features"""
        print("🐱 Implementing CatBoost Regression...")
        
        try:
            model = CatBoostRegressor(
                iterations=1000,
                learning_rate=0.1,
                depth=6,
                random_seed=42,
                verbose=False
            )
            model.fit(X, y)
            print("✅ CatBoost Regression: Trained successfully")
            return {'catboost': model}
        except Exception as e:
            print(f"⚠️ CatBoost: Failed - {str(e)}")
            return {}
    
    def hyperparameter_optimization_optuna(self, X, y):
        """Advanced hyperparameter optimization with Optuna"""
        print("🔍 Implementing Optuna Hyperparameter Optimization...")
        
        def objective(trial):
            model_type = trial.suggest_categorical('model_type', ['xgb', 'lgb', 'rf'])
            
            if model_type == 'xgb':
                model = xgb.XGBRegressor(
                    n_estimators=trial.suggest_int('n_estimators', 100, 1000),
                    max_depth=trial.suggest_int('max_depth', 3, 10),
                    learning_rate=trial.suggest_float('learning_rate', 0.01, 0.3),
                    subsample=trial.suggest_float('subsample', 0.6, 1.0),
                    colsample_bytree=trial.suggest_float('colsample_bytree', 0.6, 1.0),
                    random_state=42
                )
            elif model_type == 'lgb':
                model = lgb.LGBMRegressor(
                    n_estimators=trial.suggest_int('n_estimators', 100, 1000),
                    max_depth=trial.suggest_int('max_depth', 3, 10),
                    learning_rate=trial.suggest_float('learning_rate', 0.01, 0.3),
                    subsample=trial.suggest_float('subsample', 0.6, 1.0),
                    colsample_bytree=trial.suggest_float('colsample_bytree', 0.6, 1.0),
                    random_state=42,
                    verbose=-1
                )
            else:  # rf
                from sklearn.ensemble import RandomForestRegressor
                model = RandomForestRegressor(
                    n_estimators=trial.suggest_int('n_estimators', 100, 1000),
                    max_depth=trial.suggest_int('max_depth', 3, 20),
                    min_samples_split=trial.suggest_int('min_samples_split', 2, 20),
                    min_samples_leaf=trial.suggest_int('min_samples_leaf', 1, 10),
                    random_state=42
                )
            
            scores = cross_val_score(model, X, y, cv=5, scoring='neg_mean_absolute_error')
            return scores.mean()
        
        try:
            study = optuna.create_study(direction='maximize')
            study.optimize(objective, n_trials=50)
            
            best_params = study.best_params
            print(f"✅ Optuna Optimization: Best score = {study.best_value:.4f}")
            print(f"📊 Best parameters: {best_params}")
            
            return study.best_params, study.best_value
        except Exception as e:
            print(f"⚠️ Optuna Optimization: Failed - {str(e)}")
            return None, None
    
    def model_explainability(self, model, X, feature_names):
        """Advanced model explainability with SHAP and LIME"""
        print("🔍 Implementing Model Explainability...")
        
        explanations = {}
        
        # SHAP explanations
        try:
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X)
            explanations['shap'] = {
                'values': shap_values,
                'explainer': explainer
            }
            print("✅ SHAP explanations generated")
        except Exception as e:
            print(f"⚠️ SHAP: Failed - {str(e)}")
        
        # LIME explanations
        try:
            explainer = lime.lime_tabular.LimeTabularExplainer(
                X, 
                feature_names=feature_names,
                mode='regression',
                random_state=42
            )
            explanations['lime'] = explainer
            print("✅ LIME explanations generated")
        except Exception as e:
            print(f"⚠️ LIME: Failed - {str(e)}")
        
        return explanations
    
    def time_series_analysis(self, df, date_col, value_col):
        """Time series analysis for temporal data"""
        print("📈 Implementing Time Series Analysis...")
        
        if date_col not in df.columns or value_col not in df.columns:
            print("⚠️ Time series analysis skipped: Date or value column not found")
            return None
        
        # Convert to time series
        ts_data = df.set_index(date_col)[value_col].sort_index()
        
        # Time series features
        ts_features = pd.DataFrame(index=ts_data.index)
        ts_features['value'] = ts_data
        ts_features['lag_1'] = ts_data.shift(1)
        ts_features['lag_7'] = ts_data.shift(7)
        ts_features['lag_30'] = ts_data.shift(30)
        ts_features['rolling_mean_7'] = ts_data.rolling(window=7).mean()
        ts_features['rolling_std_7'] = ts_data.rolling(window=7).std()
        ts_features['rolling_mean_30'] = ts_data.rolling(window=30).mean()
        ts_features['trend'] = range(len(ts_data))
        
        # Seasonal decomposition
        from statsmodels.tsa.seasonal import seasonal_decompose
        try:
            decomposition = seasonal_decompose(ts_data.dropna(), model='additive', period=12)
            ts_features['trend_component'] = decomposition.trend
            ts_features['seasonal_component'] = decomposition.seasonal
            ts_features['residual_component'] = decomposition.resid
            print("✅ Seasonal decomposition completed")
        except Exception as e:
            print(f"⚠️ Seasonal decomposition: Failed - {str(e)}")
        
        return ts_features.dropna()
    
    def anomaly_detection(self, X):
        """Advanced anomaly detection techniques"""
        print("🚨 Implementing Anomaly Detection...")
        
        from sklearn.ensemble import IsolationForest
        from sklearn.covariance import EllipticEnvelope
        from sklearn.neighbors import LocalOutlierFactor
        
        anomaly_models = {}
        
        # Isolation Forest
        iso_forest = IsolationForest(contamination=0.1, random_state=42)
        iso_anomalies = iso_forest.fit_predict(X)
        anomaly_models['isolation_forest'] = iso_anomalies
        
        # Elliptic Envelope
        elliptic_envelope = EllipticEnvelope(contamination=0.1, random_state=42)
        elliptic_anomalies = elliptic_envelope.fit_predict(X)
        anomaly_models['elliptic_envelope'] = elliptic_anomalies
        
        # Local Outlier Factor
        lof = LocalOutlierFactor(n_neighbors=20, contamination=0.1)
        lof_anomalies = lof.fit_predict(X)
        anomaly_models['local_outlier_factor'] = lof_anomalies
        
        print("✅ Anomaly detection completed")
        return anomaly_models
    
    def create_advanced_visualizations(self, results):
        """Create advanced visualizations for all features"""
        print("📊 Creating Advanced Visualizations...")
        
        visualizations = {}
        
        # 1. Model Performance Comparison
        if 'final_results' in results:
            models = list(results['final_results'].keys())
            r2_scores = [results['final_results'][model]['r2'] for model in models]
            mae_scores = [results['final_results'][model]['mae'] for model in models]
            
            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=('R² Score Comparison', 'MAE Comparison'),
                specs=[[{"secondary_y": False}, {"secondary_y": False}]]
            )
            
            fig.add_trace(
                go.Bar(x=models, y=r2_scores, name='R² Score', marker_color='lightblue'),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Bar(x=models, y=mae_scores, name='MAE', marker_color='lightcoral'),
                row=1, col=2
            )
            
            fig.update_layout(
                title_text="Advanced Model Performance Comparison",
                showlegend=False,
                height=500
            )
            
            visualizations['model_comparison'] = fig
        
        # 2. Feature Importance Heatmap
        if 'feature_importance' in results:
            importance_data = results['feature_importance']
            fig = px.imshow(
                importance_data,
                title="Feature Importance Heatmap",
                color_continuous_scale='Viridis'
            )
            visualizations['feature_importance_heatmap'] = fig
        
        # 3. Clustering Visualization
        if 'clustering_results' in results:
            clustering_data = results['clustering_results']
            fig = px.scatter(
                x=clustering_data['x'],
                y=clustering_data['y'],
                color=clustering_data['cluster'],
                title="Advanced Clustering Results",
                color_discrete_sequence=px.colors.qualitative.Set1
            )
            visualizations['clustering_plot'] = fig
        
        print(f"✅ Created {len(visualizations)} advanced visualizations")
        return visualizations
    
    def run_complete_advanced_analysis(self):
        """Run complete advanced ML analysis"""
        print("🚀 Starting Advanced ML Analysis...")
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
            print("❌ No target column found")
            return None
        
        y = X[target_col]
        X = X.drop(columns=[target_col])
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        results = {}
        
        # 1. Neural Networks
        results['neural_networks'] = self.neural_network_regression(X_scaled, y)
        
        # 2. Gaussian Processes
        results['gaussian_processes'] = self.gaussian_process_regression(X_scaled, y)
        
        # 3. Advanced Clustering
        results['clustering'] = self.advanced_clustering(X_scaled)
        
        # 4. Dimensionality Reduction
        results['dimensionality_reduction'] = self.dimensionality_reduction(X_scaled)
        
        # 5. CatBoost
        results['catboost'] = self.catboost_regression(X_scaled, y)
        
        # 6. Hyperparameter Optimization
        results['optuna_optimization'] = self.hyperparameter_optimization_optuna(X_scaled, y)
        
        # 7. Anomaly Detection
        results['anomaly_detection'] = self.anomaly_detection(X_scaled)
        
        # 8. Time Series Analysis (if applicable)
        date_cols = [col for col in self.df.columns if 'date' in col.lower() or 'time' in col.lower()]
        if date_cols:
            results['time_series'] = self.time_series_analysis(self.df, date_cols[0], target_col)
        
        # 9. Create Visualizations
        results['visualizations'] = self.create_advanced_visualizations(results)
        
        print("\n" + "=" * 60)
        print("🎉 ADVANCED ML ANALYSIS COMPLETED!")
        print("=" * 60)
        
        return results

def add_advanced_ml_features_to_app():
    """Add advanced ML features to Streamlit app"""
    
    # Advanced ML Features Section
    st.markdown("---")
    st.subheader("🧠 Advanced ML Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🧠 Neural Networks", key="neural_btn"):
            st.info("Neural Networks: Advanced deep learning models with multiple architectures")
    
    with col2:
        if st.button("🌊 Gaussian Processes", key="gp_btn"):
            st.info("Gaussian Processes: Probabilistic regression with uncertainty quantification")
    
    with col3:
        if st.button("🔍 Hyperparameter Optimization", key="optuna_btn"):
            st.info("Optuna: Advanced hyperparameter optimization with Bayesian methods")
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        if st.button("🎯 Advanced Clustering", key="advanced_clustering_btn"):
            st.info("Advanced Clustering: DBSCAN, Hierarchical, and Agglomerative clustering")
    
    with col5:
        if st.button("📐 Dimensionality Reduction", key="dim_reduction_btn"):
            st.info("Dimensionality Reduction: PCA, ICA, and t-SNE for feature analysis")
    
    with col6:
        if st.button("🚨 Anomaly Detection", key="anomaly_btn"):
            st.info("Anomaly Detection: Isolation Forest, Elliptic Envelope, and LOF")
    
    col7, col8, col9 = st.columns(3)
    
    with col7:
        if st.button("🐱 CatBoost", key="catboost_btn"):
            st.info("CatBoost: Advanced gradient boosting with categorical feature support")
    
    with col8:
        if st.button("🔍 Model Explainability", key="explainability_btn"):
            st.info("SHAP & LIME: Advanced model interpretability and feature explanations")
    
    with col9:
        if st.button("📈 Time Series Analysis", key="timeseries_btn"):
            st.info("Time Series: Temporal analysis with seasonal decomposition and forecasting")

if __name__ == "__main__":
    print("Advanced ML Features Module for Oracle Samuel")
    print("Ready for integration with main application")

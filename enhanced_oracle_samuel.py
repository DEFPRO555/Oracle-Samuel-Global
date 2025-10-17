# © 2025 Dowek Analytics Ltd.
# ORACLE SAMUEL – Enhanced AI Model with Advanced Algorithms
# MD5-Protected AI System. Unauthorized use prohibited.

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge, Lasso
from sklearn.cluster import KMeans
from sklearn.metrics import (
    mean_absolute_error, r2_score, mean_squared_error, 
    confusion_matrix, classification_report, accuracy_score,
    silhouette_score, adjusted_rand_score
)
from sklearn.preprocessing import StandardScaler, LabelEncoder, MinMaxScaler
from sklearn.decomposition import PCA
import xgboost as xgb
import lightgbm as lgb
import joblib
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

class EnhancedOracleSamuel:
    """
    Enhanced Oracle Samuel with K-means clustering, confusion matrix analysis,
    and logistic regression for improved accuracy
    """
    
    def __init__(self, df):
        self.df = df.copy()
        self.models = {}
        self.clusters = None
        self.cluster_centers = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = []
        self.target_column = None
        self.best_model = None
        self.best_model_name = None
        self.confusion_matrices = {}
        self.cluster_analysis = {}
        self.performance_metrics = {}
        
    def prepare_data(self, target_col=None):
        """Enhanced data preparation with scaling and feature engineering"""
        print("🔧 Preparing enhanced data for training...")
        
        # Auto-detect target column
        if target_col is None:
            price_keywords = ['price', 'cost', 'value', 'amount']
            for col in self.df.columns:
                if any(keyword in col.lower() for keyword in price_keywords):
                    target_col = col
                    break
        
        if target_col is None or target_col not in self.df.columns:
            return None, None, "Could not find price column"
        
        self.target_column = target_col
        
        # Separate features and target
        X = self.df.drop(columns=[target_col])
        y = self.df[target_col]
        
        # Handle categorical variables
        categorical_cols = X.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
            X[col] = self.label_encoders[col].fit_transform(X[col].astype(str))
        
        # Feature engineering
        X = self._engineer_features(X)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        X_scaled = pd.DataFrame(X_scaled, columns=X.columns)
        
        self.feature_columns = X_scaled.columns.tolist()
        
        print(f"✓ Enhanced data prepared: {len(X_scaled)} samples, {len(self.feature_columns)} features")
        return X_scaled, y, None
    
    def _engineer_features(self, X):
        """Advanced feature engineering"""
        X_eng = X.copy()
        
        # Create price categories for logistic regression
        if self.target_column in self.df.columns:
            price_quartiles = self.df[self.target_column].quantile([0.25, 0.5, 0.75])
            self.price_quartiles = price_quartiles
        
        # Add polynomial features for key numeric columns
        numeric_cols = X_eng.select_dtypes(include=[np.number]).columns
        for col in numeric_cols[:3]:  # Limit to top 3 to avoid overfitting
            if col in X_eng.columns:
                X_eng[f'{col}_squared'] = X_eng[col] ** 2
                X_eng[f'{col}_log'] = np.log1p(X_eng[col])
        
        # Add interaction features
        if len(numeric_cols) >= 2:
            X_eng['bed_bath_interaction'] = X_eng.get('bedrooms', 0) * X_eng.get('bathrooms', 0)
            X_eng['size_price_ratio'] = X_eng.get('sqft_living', 0) / (X_eng.get('price', 1) + 1)
        
        return X_eng
    
    def perform_kmeans_clustering(self, X, n_clusters=5):
        """Perform K-means clustering for market segmentation"""
        print(f"🎯 Performing K-means clustering with {n_clusters} clusters...")
        
        # Determine optimal number of clusters using elbow method
        inertias = []
        silhouette_scores = []
        K_range = range(2, min(11, len(X)//2))
        
        for k in K_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(X)
            inertias.append(kmeans.inertia_)
            silhouette_scores.append(silhouette_score(X, kmeans.labels_))
        
        # Find optimal k using silhouette score
        optimal_k = K_range[np.argmax(silhouette_scores)]
        print(f"✓ Optimal clusters: {optimal_k} (silhouette score: {max(silhouette_scores):.3f})")
        
        # Perform final clustering
        self.kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
        self.clusters = self.kmeans.fit_predict(X)
        self.cluster_centers = self.kmeans.cluster_centers_
        
        # Analyze clusters
        self._analyze_clusters(X, self.clusters)
        
        return self.clusters, optimal_k
    
    def _analyze_clusters(self, X, clusters):
        """Analyze cluster characteristics"""
        cluster_df = X.copy()
        cluster_df['cluster'] = clusters
        cluster_df['price'] = self.df[self.target_column]
        
        self.cluster_analysis = {}
        for cluster_id in np.unique(clusters):
            cluster_data = cluster_df[cluster_df['cluster'] == cluster_id]
            
            self.cluster_analysis[cluster_id] = {
                'size': len(cluster_data),
                'avg_price': cluster_data['price'].mean(),
                'price_std': cluster_data['price'].std(),
                'characteristics': cluster_data.describe()
            }
        
        print("✓ Cluster analysis completed")
    
    def create_price_categories(self, y):
        """Create price categories for logistic regression"""
        # Create price categories based on quartiles
        price_quartiles = np.percentile(y, [25, 50, 75])
        
        def categorize_price(price):
            if price <= price_quartiles[0]:
                return 'Low'
            elif price <= price_quartiles[1]:
                return 'Medium-Low'
            elif price <= price_quartiles[2]:
                return 'Medium-High'
            else:
                return 'High'
        
        y_categories = y.apply(categorize_price)
        return y_categories, price_quartiles
    
    def train_logistic_regression(self, X, y):
        """Train logistic regression for price category classification"""
        print("📊 Training logistic regression for price categories...")
        
        # Create price categories
        y_categories, quartiles = self.create_price_categories(y)
        self.price_quartiles = quartiles
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_categories, test_size=0.2, random_state=42, stratify=y_categories
        )
        
        # Train logistic regression
        log_reg = LogisticRegression(random_state=42, max_iter=1000)
        log_reg.fit(X_train, y_train)
        
        # Predictions
        y_pred = log_reg.predict(X_test)
        y_pred_proba = log_reg.predict_proba(X_test)
        
        # Calculate confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        accuracy = accuracy_score(y_test, y_pred)
        
        self.confusion_matrices['logistic_regression'] = {
            'matrix': cm,
            'accuracy': accuracy,
            'classification_report': classification_report(y_test, y_pred),
            'classes': log_reg.classes_
        }
        
        print(f"✓ Logistic regression accuracy: {accuracy:.3f}")
        
        return log_reg, cm, accuracy
    
    def train_enhanced_models(self, df, target_col=None):
        """Train enhanced models with all advanced techniques"""
        print("\n🧠 ENHANCED ORACLE SAMUEL - ADVANCED AI MODE ACTIVATED\n")
        
        # Prepare data
        X, y, error = self.prepare_data(target_col)
        if error:
            return None, error
        
        # Perform K-means clustering
        clusters, optimal_k = self.perform_kmeans_clustering(X)
        
        # Train logistic regression for price categories
        log_reg, cm, log_accuracy = self.train_logistic_regression(X, y)
        
        # Split data for regression models
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        print(f"Training set: {len(X_train)} samples")
        print(f"Test set: {len(X_test)} samples\n")
        
        # Enhanced model configurations
        models_config = {
            'Random Forest': RandomForestRegressor(
                n_estimators=300, max_depth=20, min_samples_split=5,
                min_samples_leaf=2, random_state=42, n_jobs=-1
            ),
            'XGBoost': xgb.XGBRegressor(
                n_estimators=300, max_depth=10, learning_rate=0.05,
                subsample=0.8, colsample_bytree=0.8, random_state=42
            ),
            'LightGBM': lgb.LGBMRegressor(
                n_estimators=300, max_depth=10, learning_rate=0.05,
                subsample=0.8, colsample_bytree=0.8, random_state=42, verbose=-1
            ),
            'Gradient Boosting': GradientBoostingRegressor(
                n_estimators=200, max_depth=8, learning_rate=0.1,
                subsample=0.8, random_state=42
            ),
            'Ridge Regression': Ridge(alpha=1.0, random_state=42),
            'Lasso Regression': Lasso(alpha=0.1, random_state=42, max_iter=2000)
        }
        
        results = {}
        
        for name, model in models_config.items():
            print(f"\n⚙️  Training {name}...")
            
            try:
                # Train model
                model.fit(X_train, y_train)
                
                # Predictions
                y_pred = model.predict(X_test)
                
                # Calculate metrics
                mae = mean_absolute_error(y_test, y_pred)
                rmse = np.sqrt(mean_squared_error(y_test, y_pred))
                r2 = r2_score(y_test, y_pred)
                
                # Cross-validation score
                cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
                cv_mean = cv_scores.mean()
                cv_std = cv_scores.std()
                
                results[name] = {
                    'model': model,
                    'mae': mae,
                    'rmse': rmse,
                    'r2': r2,
                    'cv_mean': cv_mean,
                    'cv_std': cv_std,
                    'y_test': y_test,
                    'y_pred': y_pred
                }
                
                print(f"✓ {name}: MAE={mae:.2f}, RMSE={rmse:.2f}, R²={r2:.4f}, CV={cv_mean:.4f}±{cv_std:.4f}")
                
            except Exception as e:
                print(f"✗ {name} failed: {str(e)}")
        
        # Select best model (highest R² with good CV score)
        best_name = max(results, key=lambda k: results[k]['r2'] + results[k]['cv_mean'])
        self.best_model = results[best_name]['model']
        self.best_model_name = best_name
        
        print(f"\n🏆 BEST MODEL: {best_name}")
        print(f"   R² Score: {results[best_name]['r2']:.4f}")
        print(f"   CV Score: {results[best_name]['cv_mean']:.4f}±{results[best_name]['cv_std']:.4f}")
        
        # Store all results
        self.performance_metrics = {
            'regression_models': results,
            'logistic_regression': {
                'model': log_reg,
                'accuracy': log_accuracy,
                'confusion_matrix': cm
            },
            'clustering': {
                'clusters': clusters,
                'optimal_k': optimal_k,
                'cluster_analysis': self.cluster_analysis
            }
        }
        
        return self.performance_metrics, None
    
    def generate_confusion_matrix_analysis(self):
        """Generate detailed confusion matrix analysis"""
        if 'logistic_regression' not in self.confusion_matrices:
            return "No confusion matrix available"
        
        cm_data = self.confusion_matrices['logistic_regression']
        cm = cm_data['matrix']
        classes = cm_data['classes']
        
        analysis = f"""
        📊 CONFUSION MATRIX ANALYSIS
        ============================
        
        Accuracy: {cm_data['accuracy']:.3f}
        
        Confusion Matrix:
        {cm}
        
        Classes: {classes}
        
        Classification Report:
        {cm_data['classification_report']}
        """
        
        return analysis
    
    def generate_cluster_analysis_report(self):
        """Generate detailed cluster analysis report"""
        if not self.cluster_analysis:
            return "No cluster analysis available"
        
        report = "🎯 CLUSTER ANALYSIS REPORT\n"
        report += "========================\n\n"
        
        for cluster_id, data in self.cluster_analysis.items():
            report += f"Cluster {cluster_id}:\n"
            report += f"  Size: {data['size']} properties\n"
            report += f"  Average Price: ${data['avg_price']:,.0f}\n"
            report += f"  Price Std Dev: ${data['price_std']:,.0f}\n"
            report += f"  Price Range: ${data['avg_price'] - data['price_std']:,.0f} - ${data['avg_price'] + data['price_std']:,.0f}\n\n"
        
        return report
    
    def create_visualizations(self):
        """Create comprehensive visualizations"""
        if not self.performance_metrics:
            return None
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Model Performance Comparison', 'Confusion Matrix', 
                          'Cluster Analysis', 'Residuals Plot'),
            specs=[[{"type": "bar"}, {"type": "heatmap"}],
                   [{"type": "scatter"}, {"type": "scatter"}]]
        )
        
        # Model performance comparison
        models = list(self.performance_metrics['regression_models'].keys())
        r2_scores = [self.performance_metrics['regression_models'][m]['r2'] for m in models]
        
        fig.add_trace(
            go.Bar(x=models, y=r2_scores, name='R² Scores'),
            row=1, col=1
        )
        
        # Confusion matrix heatmap
        if 'logistic_regression' in self.performance_metrics:
            cm = self.performance_metrics['logistic_regression']['confusion_matrix']
            classes = self.performance_metrics['logistic_regression']['model'].classes_
            
            fig.add_trace(
                go.Heatmap(z=cm, x=classes, y=classes, name='Confusion Matrix'),
                row=1, col=2
            )
        
        # Cluster analysis
        if 'clustering' in self.performance_metrics:
            clusters = self.performance_metrics['clustering']['clusters']
            prices = self.df[self.target_column]
            
            fig.add_trace(
                go.Scatter(x=clusters, y=prices, mode='markers', name='Clusters'),
                row=2, col=1
            )
        
        # Residuals plot
        best_model_name = self.best_model_name
        if best_model_name in self.performance_metrics['regression_models']:
            y_test = self.performance_metrics['regression_models'][best_model_name]['y_test']
            y_pred = self.performance_metrics['regression_models'][best_model_name]['y_pred']
            residuals = y_test - y_pred
            
            fig.add_trace(
                go.Scatter(x=y_pred, y=residuals, mode='markers', name='Residuals'),
                row=2, col=2
            )
        
        fig.update_layout(height=800, showlegend=False, title_text="Enhanced Oracle Samuel Analysis")
        return fig
    
    def save_enhanced_model(self, filename='enhanced_oracle_samuel_model.pkl'):
        """Save enhanced model with all components"""
        if self.best_model is None:
            return False, "No model trained yet"
        
        try:
            model_data = {
                'best_model': self.best_model,
                'best_model_name': self.best_model_name,
                'scaler': self.scaler,
                'label_encoders': self.label_encoders,
                'feature_columns': self.feature_columns,
                'target_column': self.target_column,
                'performance_metrics': self.performance_metrics,
                'kmeans': self.kmeans,
                'clusters': self.clusters,
                'cluster_centers': self.cluster_centers,
                'price_quartiles': self.price_quartiles,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            joblib.dump(model_data, filename)
            print(f"✓ Enhanced model saved: {filename}")
            return True, filename
        except Exception as e:
            return False, str(e)
    
    def predict_enhanced(self, input_data):
        """Enhanced prediction with clustering and category information"""
        if self.best_model is None:
            return None, "No model trained yet"
        
        try:
            # Prepare input
            X = pd.DataFrame([input_data])
            
            # Apply label encoding
            for col, encoder in self.label_encoders.items():
                if col in X.columns:
                    X[col] = encoder.transform(X[col].astype(str))
            
            # Feature engineering
            X = self._engineer_features(X)
            
            # Scale features
            X_scaled = self.scaler.transform(X)
            X_scaled = pd.DataFrame(X_scaled, columns=self.feature_columns)
            
            # Ensure all feature columns exist
            for col in self.feature_columns:
                if col not in X_scaled.columns:
                    X_scaled[col] = 0
            
            X_scaled = X_scaled[self.feature_columns]
            
            # Make prediction
            prediction = self.best_model.predict(X_scaled)[0]
            
            # Get cluster assignment
            cluster = self.kmeans.predict(X_scaled)[0]
            
            # Get price category
            if hasattr(self, 'price_quartiles'):
                if prediction <= self.price_quartiles[0]:
                    category = 'Low'
                elif prediction <= self.price_quartiles[1]:
                    category = 'Medium-Low'
                elif prediction <= self.price_quartiles[2]:
                    category = 'Medium-High'
                else:
                    category = 'High'
            else:
                category = 'Unknown'
            
            result = {
                'predicted_price': round(prediction, 2),
                'cluster': int(cluster),
                'price_category': category,
                'confidence': 'High' if hasattr(self.best_model, 'predict_proba') else 'Medium'
            }
            
            return result, None
        except Exception as e:
            return None, f"Prediction error: {str(e)}"

# Example usage and testing
def test_enhanced_oracle_samuel():
    """Test the enhanced Oracle Samuel model"""
    print("🚀 Testing Enhanced Oracle Samuel...")
    
    # Create sample data
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'bedrooms': np.random.randint(1, 6, n_samples),
        'bathrooms': np.random.randint(1, 4, n_samples),
        'sqft_living': np.random.randint(800, 4000, n_samples),
        'sqft_lot': np.random.randint(2000, 20000, n_samples),
        'floors': np.random.choice([1, 1.5, 2, 2.5, 3], n_samples),
        'waterfront': np.random.choice([0, 1], n_samples, p=[0.9, 0.1]),
        'view': np.random.randint(0, 5, n_samples),
        'condition': np.random.randint(1, 6, n_samples),
        'grade': np.random.randint(6, 14, n_samples),
        'yr_built': np.random.randint(1900, 2020, n_samples),
        'price': np.random.randint(200000, 2000000, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Initialize enhanced model
    enhanced_model = EnhancedOracleSamuel(df)
    
    # Train enhanced models
    results, error = enhanced_model.train_enhanced_models(df)
    
    if error:
        print(f"❌ Error: {error}")
        return
    
    print("\n✅ Enhanced Oracle Samuel training completed!")
    
    # Generate reports
    print("\n" + "="*50)
    print(enhanced_model.generate_confusion_matrix_analysis())
    print("\n" + "="*50)
    print(enhanced_model.generate_cluster_analysis_report())
    
    # Test prediction
    test_input = {
        'bedrooms': 3,
        'bathrooms': 2,
        'sqft_living': 2000,
        'sqft_lot': 8000,
        'floors': 2,
        'waterfront': 0,
        'view': 2,
        'condition': 4,
        'grade': 8,
        'yr_built': 2010
    }
    
    prediction, error = enhanced_model.predict_enhanced(test_input)
    if prediction:
        print(f"\n🎯 Enhanced Prediction Result:")
        print(f"   Predicted Price: ${prediction['predicted_price']:,.0f}")
        print(f"   Market Cluster: {prediction['cluster']}")
        print(f"   Price Category: {prediction['price_category']}")
        print(f"   Confidence: {prediction['confidence']}")
    
    # Save model
    success, filename = enhanced_model.save_enhanced_model()
    if success:
        print(f"\n💾 Enhanced model saved as: {filename}")
    
    return enhanced_model

if __name__ == "__main__":
    # Run the test
    model = test_enhanced_oracle_samuel()

# © 2025 Dowek Analytics Ltd.
# ORACLE SAMUEL – The Real Estate Market Prophet
# MD5-Protected AI System. Unauthorized use prohibited.

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
from sklearn.preprocessing import LabelEncoder
from datetime import datetime
import pickle


class RealEstatePredictor:
    def __init__(self, df):
        self.df = df.copy()
        self.model = None
        self.feature_importance = None
        self.metrics = {}
        self.label_encoders = {}
        self.feature_columns = []
        self.target_column = None
    
    def prepare_data(self, target_col=None):
        """Prepare data for ML training"""
        # Auto-detect target column (price-related)
        if target_col is None:
            price_keywords = ['price', 'cost', 'value', 'amount']
            for col in self.df.columns:
                if any(keyword in col.lower() for keyword in price_keywords):
                    target_col = col
                    break
        
        if target_col is None or target_col not in self.df.columns:
            return False, "Could not find price column in dataset"
        
        self.target_column = target_col
        
        # Separate features and target
        X = self.df.drop(columns=[target_col])
        y = self.df[target_col]
        
        # Handle categorical variables
        categorical_cols = X.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            self.label_encoders[col] = le
        
        # Store feature columns
        self.feature_columns = X.columns.tolist()
        
        return X, y
    
    def train_model(self, model_type='random_forest'):
        """Train ML model"""
        X, y = self.prepare_data()
        
        if isinstance(X, bool):
            return False, y  # Error message
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        if model_type == 'random_forest':
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
        else:
            self.model = LinearRegression()
        
        self.model.fit(X_train, y_train)
        
        # Predictions
        y_pred = self.model.predict(X_test)
        
        # Calculate metrics
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        
        self.metrics = {
            'model_type': model_type,
            'mae': round(mae, 2),
            'rmse': round(rmse, 2),
            'r2_score': round(r2, 4),
            'training_samples': len(X_train),
            'test_samples': len(X_test),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Feature importance (for Random Forest)
        if model_type == 'random_forest':
            self.feature_importance = pd.DataFrame({
                'feature': self.feature_columns,
                'importance': self.model.feature_importances_
            }).sort_values('importance', ascending=False)
        
        return True, self.metrics, y_test, y_pred
    
    def predict_price(self, input_data):
        """Predict price for new data"""
        if self.model is None:
            return None, "Model not trained yet"
        
        try:
            # Prepare input
            X = pd.DataFrame([input_data])
            
            # Apply label encoding
            for col, le in self.label_encoders.items():
                if col in X.columns:
                    X[col] = le.transform(X[col].astype(str))
            
            # Ensure all feature columns exist
            for col in self.feature_columns:
                if col not in X.columns:
                    X[col] = 0
            
            X = X[self.feature_columns]
            
            prediction = self.model.predict(X)[0]
            return round(prediction, 2), None
        except Exception as e:
            return None, f"Prediction error: {str(e)}"
    
    def get_top_features(self, top_n=5):
        """Get top N most important features"""
        if self.feature_importance is None:
            return None
        return self.feature_importance.head(top_n)
    
    def analyze_correlation(self):
        """Analyze feature correlations with target"""
        if self.target_column is None:
            return None
        
        # Get numeric columns only
        numeric_df = self.df.select_dtypes(include=[np.number])
        
        if self.target_column in numeric_df.columns:
            correlations = numeric_df.corr()[self.target_column].sort_values(ascending=False)
            return correlations
        return None


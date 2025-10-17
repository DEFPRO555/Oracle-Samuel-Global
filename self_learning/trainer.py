# © 2025 Dowek Analytics Ltd.
# ORACLE SAMUEL – Self-Learning AI Engine
# MD5-Protected AI System. Unauthorized use prohibited.

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
import lightgbm as lgb
import joblib
from datetime import datetime
from tqdm import tqdm
from rich.console import Console
from rich.progress import Progress
import hashlib
import os

console = Console()


class SelfLearningTrainer:
    """
    Advanced self-learning trainer for Oracle Samuel
    Supports multiple ML algorithms with auto-selection
    """
    
    def __init__(self):
        self.models = {}
        self.label_encoders = {}
        self.feature_columns = []
        self.target_column = None
        self.best_model = None
        self.best_model_name = None
        self.training_history = []
    
    def prepare_data(self, df, target_col=None):
        """Prepare data for ML training"""
        console.print("[bold cyan]🔧 Preparing data for training...[/bold cyan]")
        
        # Auto-detect target column
        if target_col is None:
            price_keywords = ['price', 'cost', 'value', 'amount']
            for col in df.columns:
                if any(keyword in col.lower() for keyword in price_keywords):
                    target_col = col
                    break
        
        if target_col is None or target_col not in df.columns:
            return None, None, "Could not find price column"
        
        self.target_column = target_col
        
        # Separate features and target
        X = df.drop(columns=[target_col])
        y = df[target_col]
        
        # Handle categorical variables
        categorical_cols = X.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
            X[col] = self.label_encoders[col].fit_transform(X[col].astype(str))
        
        self.feature_columns = X.columns.tolist()
        
        console.print(f"[green]✓[/green] Data prepared: {len(X)} samples, {len(self.feature_columns)} features")
        return X, y, None
    
    def train_multiple_models(self, df, target_col=None):
        """Train multiple models and select the best one"""
        console.print("\n[bold magenta]🧠 ORACLE SAMUEL - SELF-LEARNING MODE ACTIVATED[/bold magenta]\n")
        
        X, y, error = self.prepare_data(df, target_col)
        if error:
            return None, error
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        console.print(f"[cyan]Training set:[/cyan] {len(X_train)} samples")
        console.print(f"[cyan]Test set:[/cyan] {len(X_test)} samples\n")
        
        # Define models to train
        models_config = {
            'Random Forest': RandomForestRegressor(n_estimators=200, max_depth=15, random_state=42, n_jobs=-1),
            'XGBoost': xgb.XGBRegressor(n_estimators=200, max_depth=8, learning_rate=0.1, random_state=42),
            'LightGBM': lgb.LGBMRegressor(n_estimators=200, max_depth=8, learning_rate=0.1, random_state=42, verbose=-1),
            'Linear Regression': LinearRegression()
        }
        
        results = {}
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Training models...", total=len(models_config))
            
            for name, model in models_config.items():
                console.print(f"\n[yellow]⚙️  Training {name}...[/yellow]")
                
                try:
                    # Train model
                    model.fit(X_train, y_train)
                    
                    # Predictions
                    y_pred = model.predict(X_test)
                    
                    # Calculate metrics
                    mae = mean_absolute_error(y_test, y_pred)
                    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
                    r2 = r2_score(y_test, y_pred)
                    
                    results[name] = {
                        'model': model,
                        'mae': mae,
                        'rmse': rmse,
                        'r2': r2,
                        'y_test': y_test,
                        'y_pred': y_pred
                    }
                    
                    console.print(f"[green]✓ {name}:[/green] MAE={mae:.2f}, RMSE={rmse:.2f}, R²={r2:.4f}")
                    
                except Exception as e:
                    console.print(f"[red]✗ {name} failed:[/red] {str(e)}")
                
                progress.update(task, advance=1)
        
        # Select best model (highest R²)
        best_name = max(results, key=lambda k: results[k]['r2'])
        self.best_model = results[best_name]['model']
        self.best_model_name = best_name
        
        console.print(f"\n[bold green]🏆 BEST MODEL: {best_name}[/bold green]")
        console.print(f"[bold green]   R² Score: {results[best_name]['r2']:.4f}[/bold green]\n")
        
        # Save best model
        self.save_model()
        
        # Store training history
        training_record = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'best_model': best_name,
            'mae': results[best_name]['mae'],
            'rmse': results[best_name]['rmse'],
            'r2': results[best_name]['r2'],
            'all_results': results
        }
        self.training_history.append(training_record)
        
        return training_record, None
    
    def save_model(self, filename='oracle_samuel_model.pkl'):
        """Save the best model to disk"""
        if self.best_model is None:
            return False, "No model trained yet"
        
        try:
            model_data = {
                'model': self.best_model,
                'model_name': self.best_model_name,
                'label_encoders': self.label_encoders,
                'feature_columns': self.feature_columns,
                'target_column': self.target_column,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            joblib.dump(model_data, filename)
            
            # Calculate MD5
            with open(filename, 'rb') as f:
                md5_hash = hashlib.md5(f.read()).hexdigest()
            
            console.print(f"[green]✓ Model saved:[/green] {filename}")
            console.print(f"[green]  MD5:[/green] {md5_hash}")
            
            return True, md5_hash
        except Exception as e:
            return False, str(e)
    
    def load_model(self, filename='oracle_samuel_model.pkl'):
        """Load a saved model"""
        if not os.path.exists(filename):
            return False, "Model file not found"
        
        try:
            model_data = joblib.load(filename)
            self.best_model = model_data['model']
            self.best_model_name = model_data['model_name']
            self.label_encoders = model_data['label_encoders']
            self.feature_columns = model_data['feature_columns']
            self.target_column = model_data['target_column']
            
            console.print(f"[green]✓ Model loaded:[/green] {self.best_model_name}")
            return True, None
        except Exception as e:
            return False, str(e)
    
    def predict(self, input_data):
        """Make predictions with loaded model"""
        if self.best_model is None:
            return None, "No model loaded"
        
        try:
            X = pd.DataFrame([input_data])
            
            # Apply label encoding
            for col, encoder in self.label_encoders.items():
                if col in X.columns:
                    X[col] = encoder.transform(X[col].astype(str))
            
            # Ensure all feature columns exist
            for col in self.feature_columns:
                if col not in X.columns:
                    X[col] = 0
            
            X = X[self.feature_columns]
            prediction = self.best_model.predict(X)[0]
            
            return round(prediction, 2), None
        except Exception as e:
            return None, f"Prediction error: {str(e)}"


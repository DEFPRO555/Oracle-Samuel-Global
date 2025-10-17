# © 2025 Dowek Analytics Ltd.
# ORACLE SAMUEL – Self-Learning AI Engine
# MD5-Protected AI System. Unauthorized use prohibited.

import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime
import hashlib
from rich.console import Console
from rich.table import Table

console = Console()


class ModelEvaluator:
    """
    Tracks and logs model performance over time
    Maintains evaluation history in SQL database
    """
    
    def __init__(self, db_name='oracle_samuel_real_estate.db'):
        self.db_name = db_name
        self.engine = create_engine(f'sqlite:///{db_name}')
        self._initialize_tables()
    
    def _initialize_tables(self):
        """Create evaluation tables if they don't exist"""
        try:
            with self.engine.connect() as conn:
                # Model evaluation log
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS model_evaluation_log (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT,
                        model_name TEXT,
                        mae REAL,
                        rmse REAL,
                        r2 REAL,
                        md5_hash TEXT,
                        training_samples INTEGER,
                        test_samples INTEGER
                    )
                """))
                
                # Model comparison history
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS model_comparison (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT,
                        models_compared TEXT,
                        best_model TEXT,
                        improvement_percentage REAL
                    )
                """))
                
                conn.commit()
                
        except Exception as e:
            console.print(f"[red]Error initializing tables:[/red] {str(e)}")
    
    def log_evaluation(self, model_name, mae, rmse, r2, md5_hash=None, 
                      training_samples=0, test_samples=0):
        """Log model evaluation results"""
        try:
            df = pd.DataFrame([{
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'model_name': model_name,
                'mae': mae,
                'rmse': rmse,
                'r2': r2,
                'md5_hash': md5_hash or 'N/A',
                'training_samples': training_samples,
                'test_samples': test_samples
            }])
            
            df.to_sql('model_evaluation_log', self.engine, if_exists='append', index=False)
            
            console.print(f"[green]✓ Evaluation logged:[/green] {model_name} - R²={r2:.4f}")
            return True
            
        except Exception as e:
            console.print(f"[red]Error logging evaluation:[/red] {str(e)}")
            return False
    
    def get_evaluation_history(self, limit=10):
        """Retrieve evaluation history"""
        try:
            query = f"""
                SELECT * FROM model_evaluation_log 
                ORDER BY timestamp DESC 
                LIMIT {limit}
            """
            df = pd.read_sql(query, self.engine)
            return df
        except Exception as e:
            console.print(f"[red]Error retrieving history:[/red] {str(e)}")
            return pd.DataFrame()
    
    def get_best_model(self):
        """Get the best performing model from history"""
        try:
            query = """
                SELECT * FROM model_evaluation_log 
                ORDER BY r2 DESC 
                LIMIT 1
            """
            df = pd.read_sql(query, self.engine)
            if not df.empty:
                return df.iloc[0].to_dict()
            return None
        except Exception as e:
            console.print(f"[red]Error getting best model:[/red] {str(e)}")
            return None
    
    def compare_models(self, results_dict):
        """Compare multiple model results and log"""
        try:
            models_compared = ', '.join(results_dict.keys())
            best_model = max(results_dict, key=lambda k: results_dict[k]['r2'])
            
            # Calculate improvement over baseline (Linear Regression)
            if 'Linear Regression' in results_dict:
                baseline_r2 = results_dict['Linear Regression']['r2']
                best_r2 = results_dict[best_model]['r2']
                improvement = ((best_r2 - baseline_r2) / baseline_r2) * 100
            else:
                improvement = 0.0
            
            df = pd.DataFrame([{
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'models_compared': models_compared,
                'best_model': best_model,
                'improvement_percentage': improvement
            }])
            
            df.to_sql('model_comparison', self.engine, if_exists='append', index=False)
            
            return True
        except Exception as e:
            console.print(f"[red]Error comparing models:[/red] {str(e)}")
            return False
    
    def display_performance_table(self):
        """Display a rich table of model performance"""
        try:
            df = self.get_evaluation_history(5)
            
            if df.empty:
                console.print("[yellow]No evaluation history available[/yellow]")
                return
            
            table = Table(title="📊 Model Performance History (Top 5)")
            
            table.add_column("Timestamp", style="cyan")
            table.add_column("Model", style="magenta")
            table.add_column("MAE", style="green")
            table.add_column("RMSE", style="green")
            table.add_column("R²", style="bold green")
            
            for _, row in df.iterrows():
                table.add_row(
                    row['timestamp'],
                    row['model_name'],
                    f"${row['mae']:.2f}",
                    f"${row['rmse']:.2f}",
                    f"{row['r2']:.4f}"
                )
            
            console.print(table)
            
        except Exception as e:
            console.print(f"[red]Error displaying table:[/red] {str(e)}")
    
    def get_performance_trends(self):
        """Analyze performance trends over time"""
        try:
            df = self.get_evaluation_history(100)
            
            if len(df) < 2:
                return {
                    'trend': 'insufficient_data',
                    'improvement': 0,
                    'average_r2': 0
                }
            
            recent_r2 = df.head(5)['r2'].mean()
            older_r2 = df.tail(5)['r2'].mean()
            
            improvement = ((recent_r2 - older_r2) / older_r2 * 100) if older_r2 > 0 else 0
            
            return {
                'trend': 'improving' if improvement > 0 else 'declining',
                'improvement': improvement,
                'average_r2': df['r2'].mean(),
                'best_r2': df['r2'].max(),
                'latest_r2': df.iloc[0]['r2'] if not df.empty else 0
            }
            
        except Exception as e:
            console.print(f"[red]Error analyzing trends:[/red] {str(e)}")
            return {}


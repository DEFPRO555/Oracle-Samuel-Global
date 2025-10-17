# © 2025 Dowek Analytics Ltd.
# ORACLE SAMUEL – Self-Learning AI Engine
# MD5-Protected AI System. Unauthorized use prohibited.

import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from .trainer import SelfLearningTrainer
from .evaluator import ModelEvaluator

console = Console()


class RetrainManager:
    """
    Manages automatic retraining on new datasets
    Detects uploaded data and triggers model updates
    """
    
    def __init__(self, db_name='oracle_samuel_real_estate.db'):
        self.db_name = db_name
        self.engine = create_engine(f'sqlite:///{db_name}')
        self.trainer = SelfLearningTrainer()
        self.evaluator = ModelEvaluator(db_name)
        self._initialize_retrain_log()
    
    def _initialize_retrain_log(self):
        """Create retrain log table"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS retrain_log (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT,
                        dataset_name TEXT,
                        records_count INTEGER,
                        model_trained TEXT,
                        mae REAL,
                        r2 REAL,
                        status TEXT
                    )
                """))
                conn.commit()
        except Exception as e:
            console.print(f"[red]Error initializing retrain log:[/red] {str(e)}")
    
    def check_for_new_data(self):
        """Check for uploaded datasets in database"""
        try:
            query = "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'uploaded_%';"
            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                tables = [row[0] for row in result]
            return tables
        except Exception as e:
            console.print(f"[red]Error checking for new data:[/red] {str(e)}")
            return []
    
    def get_latest_dataset(self):
        """Get the most recently uploaded dataset"""
        try:
            # Check for main uploaded_properties table
            query = "SELECT * FROM uploaded_properties"
            df = pd.read_sql(query, self.engine)
            
            if not df.empty:
                return df, 'uploaded_properties'
            
            return None, None
            
        except Exception as e:
            console.print(f"[yellow]No dataset found or error:[/yellow] {str(e)}")
            return None, None
    
    def retrain_on_dataset(self, df, dataset_name='current_data'):
        """Retrain model on specific dataset"""
        console.print(f"\n[bold cyan]🔁 Retraining on dataset:[/bold cyan] {dataset_name}")
        console.print(f"[cyan]   Records:[/cyan] {len(df)}\n")
        
        try:
            # Train multiple models
            result, error = self.trainer.train_multiple_models(df)
            
            if error:
                console.print(f"[red]✗ Training failed:[/red] {error}")
                self._log_retrain(dataset_name, len(df), 'N/A', 0, 0, 'FAILED')
                return False, error
            
            # Log evaluation
            self.evaluator.log_evaluation(
                model_name=result['best_model'],
                mae=result['mae'],
                rmse=result['rmse'],
                r2=result['r2'],
                training_samples=len(df),
                test_samples=int(len(df) * 0.2)
            )
            
            # Log retrain
            self._log_retrain(
                dataset_name=dataset_name,
                records=len(df),
                model=result['best_model'],
                mae=result['mae'],
                r2=result['r2'],
                status='SUCCESS'
            )
            
            console.print(f"\n[bold green]✓ Retraining completed successfully![/bold green]")
            
            return True, result
            
        except Exception as e:
            console.print(f"[red]✗ Retrain error:[/red] {str(e)}")
            self._log_retrain(dataset_name, len(df), 'N/A', 0, 0, 'ERROR')
            return False, str(e)
    
    def retrain_all(self):
        """Retrain on all available datasets"""
        console.print("\n[bold magenta]🔄 STARTING COMPREHENSIVE RETRAINING[/bold magenta]\n")
        
        # Get latest dataset
        df, dataset_name = self.get_latest_dataset()
        
        if df is None:
            console.print("[yellow]⚠️  No datasets found for retraining[/yellow]")
            return False, "No data available"
        
        # Retrain on dataset
        success, result = self.retrain_on_dataset(df, dataset_name)
        
        if success:
            console.print("\n[bold green]🎉 ALL RETRAINING COMPLETE![/bold green]\n")
            self.evaluator.display_performance_table()
        
        return success, result
    
    def _log_retrain(self, dataset_name, records, model, mae, r2, status):
        """Log retraining activity"""
        try:
            df = pd.DataFrame([{
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'dataset_name': dataset_name,
                'records_count': records,
                'model_trained': model,
                'mae': mae,
                'r2': r2,
                'status': status
            }])
            
            df.to_sql('retrain_log', self.engine, if_exists='append', index=False)
            
        except Exception as e:
            console.print(f"[red]Error logging retrain:[/red] {str(e)}")
    
    def get_retrain_history(self, limit=10):
        """Get retraining history"""
        try:
            query = f"""
                SELECT * FROM retrain_log 
                ORDER BY timestamp DESC 
                LIMIT {limit}
            """
            df = pd.read_sql(query, self.engine)
            return df
        except Exception as e:
            console.print(f"[red]Error getting retrain history:[/red] {str(e)}")
            return pd.DataFrame()
    
    def auto_retrain_if_needed(self, threshold_samples=100):
        """Auto retrain if dataset size exceeds threshold"""
        df, dataset_name = self.get_latest_dataset()
        
        if df is not None and len(df) >= threshold_samples:
            console.print(f"[cyan]🔔 Auto-retrain triggered: {len(df)} samples detected[/cyan]")
            return self.retrain_on_dataset(df, dataset_name)
        
        return False, "Threshold not met"


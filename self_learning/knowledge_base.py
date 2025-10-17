# © 2025 Dowek Analytics Ltd.
# ORACLE SAMUEL – Self-Learning AI Engine
# MD5-Protected AI System. Unauthorized use prohibited.

import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from datetime import datetime
from rich.console import Console

console = Console()


class KnowledgeBase:
    """
    Maintains cumulative insights across all datasets
    Stores global market intelligence
    """
    
    def __init__(self, db_name='oracle_samuel_real_estate.db'):
        self.db_name = db_name
        self.engine = create_engine(f'sqlite:///{db_name}')
        self._initialize_knowledge_tables()
    
    def _initialize_knowledge_tables(self):
        """Create knowledge base tables"""
        try:
            with self.engine.connect() as conn:
                # Feature correlations
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS feature_correlations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT,
                        feature_name TEXT,
                        correlation_with_price REAL,
                        dataset_name TEXT
                    )
                """))
                
                # Market insights
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS market_insights (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT,
                        insight_type TEXT,
                        insight_value TEXT,
                        confidence_score REAL
                    )
                """))
                
                # Feature importance trends
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS feature_importance_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT,
                        feature_name TEXT,
                        importance_score REAL,
                        model_name TEXT
                    )
                """))
                
                conn.commit()
                
        except Exception as e:
            console.print(f"[red]Error initializing knowledge tables:[/red] {str(e)}")
    
    def store_feature_correlations(self, df, dataset_name='current'):
        """Store feature correlations with price"""
        try:
            # Find price column
            price_col = None
            for col in df.columns:
                if 'price' in col.lower():
                    price_col = col
                    break
            
            if price_col is None:
                return False, "Price column not found"
            
            # Calculate correlations
            numeric_df = df.select_dtypes(include=[np.number])
            correlations = numeric_df.corr()[price_col].drop(price_col)
            
            # Store top correlations
            records = []
            for feature, corr in correlations.items():
                records.append({
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'feature_name': feature,
                    'correlation_with_price': corr,
                    'dataset_name': dataset_name
                })
            
            df_correlations = pd.DataFrame(records)
            df_correlations.to_sql('feature_correlations', self.engine, 
                                  if_exists='append', index=False)
            
            console.print(f"[green]✓ Stored {len(records)} feature correlations[/green]")
            return True, None
            
        except Exception as e:
            console.print(f"[red]Error storing correlations:[/red] {str(e)}")
            return False, str(e)
    
    def store_feature_importance(self, feature_importance_df, model_name):
        """Store feature importance from trained models"""
        try:
            records = []
            for _, row in feature_importance_df.iterrows():
                records.append({
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'feature_name': row['feature'],
                    'importance_score': row['importance'],
                    'model_name': model_name
                })
            
            df_importance = pd.DataFrame(records)
            df_importance.to_sql('feature_importance_history', self.engine,
                                if_exists='append', index=False)
            
            console.print(f"[green]✓ Stored feature importance for {model_name}[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]Error storing feature importance:[/red] {str(e)}")
            return False
    
    def get_top_correlated_features(self, top_n=5):
        """Get most correlated features across all datasets"""
        try:
            query = """
                SELECT feature_name, AVG(correlation_with_price) as avg_correlation
                FROM feature_correlations
                GROUP BY feature_name
                ORDER BY ABS(avg_correlation) DESC
                LIMIT ?
            """
            df = pd.read_sql(query, self.engine, params=(top_n,))
            return df
        except Exception as e:
            console.print(f"[red]Error getting top features:[/red] {str(e)}")
            return pd.DataFrame()
    
    def get_feature_importance_trends(self, feature_name):
        """Get importance trend for a specific feature over time"""
        try:
            query = """
                SELECT timestamp, importance_score, model_name
                FROM feature_importance_history
                WHERE feature_name = ?
                ORDER BY timestamp DESC
            """
            df = pd.read_sql(query, self.engine, params=(feature_name,))
            return df
        except Exception as e:
            console.print(f"[red]Error getting importance trends:[/red] {str(e)}")
            return pd.DataFrame()
    
    def generate_market_insight(self, insight_type, insight_value, confidence=0.85):
        """Generate and store a market insight"""
        try:
            df = pd.DataFrame([{
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'insight_type': insight_type,
                'insight_value': insight_value,
                'confidence_score': confidence
            }])
            
            df.to_sql('market_insights', self.engine, if_exists='append', index=False)
            
            console.print(f"[green]✓ Market insight generated:[/green] {insight_type}")
            return True
            
        except Exception as e:
            console.print(f"[red]Error generating insight:[/red] {str(e)}")
            return False
    
    def get_all_insights(self, limit=20):
        """Get all market insights"""
        try:
            query = f"""
                SELECT * FROM market_insights
                ORDER BY timestamp DESC
                LIMIT {limit}
            """
            df = pd.read_sql(query, self.engine)
            return df
        except Exception as e:
            console.print(f"[red]Error retrieving insights:[/red] {str(e)}")
            return pd.DataFrame()
    
    def analyze_dataset_and_generate_insights(self, df):
        """Analyze dataset and automatically generate insights"""
        insights_generated = []
        
        try:
            # Store correlations
            success, error = self.store_feature_correlations(df)
            if success:
                insights_generated.append("Feature correlations stored")
            
            # Find price column
            price_col = None
            for col in df.columns:
                if 'price' in col.lower():
                    price_col = col
                    break
            
            if price_col:
                # Average price insight
                avg_price = df[price_col].mean()
                self.generate_market_insight(
                    'average_price',
                    f"Average property price: ${avg_price:,.2f}",
                    confidence=0.95
                )
                insights_generated.append("Average price calculated")
                
                # Price range insight
                price_range = df[price_col].max() - df[price_col].min()
                self.generate_market_insight(
                    'price_range',
                    f"Price range: ${price_range:,.2f}",
                    confidence=0.95
                )
                insights_generated.append("Price range analyzed")
                
                # Volatility insight
                price_std = df[price_col].std()
                volatility_pct = (price_std / avg_price) * 100
                volatility_level = "High" if volatility_pct > 30 else "Moderate" if volatility_pct > 15 else "Low"
                self.generate_market_insight(
                    'price_volatility',
                    f"Market volatility: {volatility_level} ({volatility_pct:.1f}%)",
                    confidence=0.90
                )
                insights_generated.append("Volatility assessed")
            
            console.print(f"[bold green]✓ Generated {len(insights_generated)} insights[/bold green]")
            return insights_generated
            
        except Exception as e:
            console.print(f"[red]Error analyzing dataset:[/red] {str(e)}")
            return insights_generated


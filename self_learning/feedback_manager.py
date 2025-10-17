# © 2025 Dowek Analytics Ltd.
# ORACLE SAMUEL – Self-Learning AI Engine
# MD5-Protected AI System. Unauthorized use prohibited.

import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime
from rich.console import Console
from rich.table import Table

console = Console()


class FeedbackManager:
    """
    Manages user feedback and ratings
    Tracks satisfaction and prediction accuracy feedback
    """
    
    def __init__(self, db_name='oracle_samuel_real_estate.db'):
        self.db_name = db_name
        self.engine = create_engine(f'sqlite:///{db_name}')
        self._initialize_feedback_tables()
    
    def _initialize_feedback_tables(self):
        """Create feedback tables"""
        try:
            with self.engine.connect() as conn:
                # User feedback table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS user_feedback (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT,
                        rating INTEGER,
                        comment TEXT,
                        feedback_type TEXT,
                        model_version TEXT
                    )
                """))
                
                # Prediction feedback table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS prediction_feedback (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT,
                        predicted_value REAL,
                        actual_value REAL,
                        accuracy_rating INTEGER,
                        notes TEXT
                    )
                """))
                
                conn.commit()
                
        except Exception as e:
            console.print(f"[red]Error initializing feedback tables:[/red] {str(e)}")
    
    def log_user_feedback(self, rating, comment, feedback_type='general', model_version='current'):
        """Log user feedback and rating"""
        try:
            if not 1 <= rating <= 5:
                return False, "Rating must be between 1 and 5"
            
            df = pd.DataFrame([{
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'rating': rating,
                'comment': comment,
                'feedback_type': feedback_type,
                'model_version': model_version
            }])
            
            df.to_sql('user_feedback', self.engine, if_exists='append', index=False)
            
            console.print(f"[green]✓ Feedback logged:[/green] {rating}⭐ - {comment[:50]}...")
            return True, "Feedback saved successfully"
            
        except Exception as e:
            console.print(f"[red]Error logging feedback:[/red] {str(e)}")
            return False, str(e)
    
    def log_prediction_feedback(self, predicted, actual, accuracy_rating, notes=''):
        """Log prediction accuracy feedback"""
        try:
            df = pd.DataFrame([{
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'predicted_value': predicted,
                'actual_value': actual,
                'accuracy_rating': accuracy_rating,
                'notes': notes
            }])
            
            df.to_sql('prediction_feedback', self.engine, if_exists='append', index=False)
            
            console.print(f"[green]✓ Prediction feedback logged[/green]")
            return True, "Prediction feedback saved"
            
        except Exception as e:
            console.print(f"[red]Error logging prediction feedback:[/red] {str(e)}")
            return False, str(e)
    
    def get_feedback_summary(self):
        """Get summary statistics of feedback"""
        try:
            query = "SELECT * FROM user_feedback"
            df = pd.read_sql(query, self.engine)
            
            if df.empty:
                return {
                    'total_feedback': 0,
                    'average_rating': 0.0,
                    'rating_distribution': {},
                    'recent_comments': []
                }
            
            summary = {
                'total_feedback': len(df),
                'average_rating': df['rating'].mean(),
                'rating_distribution': df['rating'].value_counts().to_dict(),
                'recent_comments': df.tail(5)[['timestamp', 'rating', 'comment']].to_dict('records')
            }
            
            return summary
            
        except Exception as e:
            console.print(f"[red]Error getting feedback summary:[/red] {str(e)}")
            return {
                'total_feedback': 0,
                'average_rating': 0.0,
                'rating_distribution': {},
                'recent_comments': []
            }
    
    def get_all_feedback(self, limit=50):
        """Get all feedback entries"""
        try:
            query = f"""
                SELECT * FROM user_feedback 
                ORDER BY timestamp DESC 
                LIMIT {limit}
            """
            df = pd.read_sql(query, self.engine)
            return df
        except Exception as e:
            console.print(f"[red]Error retrieving feedback:[/red] {str(e)}")
            return pd.DataFrame()
    
    def display_feedback_table(self, limit=10):
        """Display feedback in a rich table"""
        try:
            df = self.get_all_feedback(limit)
            
            if df.empty:
                console.print("[yellow]No feedback available yet[/yellow]")
                return
            
            table = Table(title=f"⭐ User Feedback (Last {limit})")
            
            table.add_column("Date", style="cyan")
            table.add_column("Rating", style="yellow")
            table.add_column("Comment", style="white")
            table.add_column("Type", style="magenta")
            
            for _, row in df.iterrows():
                stars = "⭐" * row['rating']
                comment = row['comment'][:50] + "..." if len(row['comment']) > 50 else row['comment']
                
                table.add_row(
                    row['timestamp'],
                    stars,
                    comment,
                    row['feedback_type']
                )
            
            console.print(table)
            
        except Exception as e:
            console.print(f"[red]Error displaying feedback table:[/red] {str(e)}")
    
    def get_satisfaction_score(self):
        """Calculate overall satisfaction score"""
        try:
            summary = self.get_feedback_summary()
            
            if summary['total_feedback'] == 0:
                return 0.0, "No feedback available"
            
            avg_rating = summary['average_rating']
            satisfaction_percentage = (avg_rating / 5.0) * 100
            
            return satisfaction_percentage, f"Based on {summary['total_feedback']} reviews"
            
        except Exception as e:
            return 0.0, str(e)
    
    def identify_improvement_areas(self):
        """Identify areas needing improvement based on low ratings"""
        try:
            df = self.get_all_feedback(100)
            
            if df.empty:
                return []
            
            # Find low-rated feedback (1-2 stars)
            low_rated = df[df['rating'] <= 2]
            
            if low_rated.empty:
                return ["No major issues identified - all feedback is positive!"]
            
            # Extract common themes from low-rated comments
            issues = low_rated['comment'].tolist()
            
            return issues[:5]  # Return top 5 issues
            
        except Exception as e:
            console.print(f"[red]Error identifying improvement areas:[/red] {str(e)}")
            return []


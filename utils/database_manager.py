# © 2025 Dowek Analytics Ltd.
# ORACLE SAMUEL – The Real Estate Market Prophet
# MD5-Protected AI System. Unauthorized use prohibited.

from sqlalchemy import create_engine, text
import pandas as pd
import os


class DatabaseManager:
    def __init__(self, db_name='oracle_samuel_real_estate.db'):
        self.db_path = db_name
        self.engine = create_engine(f'sqlite:///{db_name}')
    
    def save_uploaded_data(self, df, table_name='uploaded_properties'):
        """Save uploaded DataFrame to SQL database"""
        try:
            df.to_sql(table_name, self.engine, if_exists='replace', index=False)
            return True, f"Data saved successfully to {table_name}"
        except Exception as e:
            return False, f"Error saving data: {str(e)}"
    
    def get_saved_data(self, table_name='uploaded_properties'):
        """Retrieve data from SQL database"""
        try:
            query = f'SELECT * FROM {table_name}'
            df = pd.read_sql(query, self.engine)
            return df
        except Exception as e:
            return pd.DataFrame()
    
    def save_signature(self, signature_record):
        """Save MD5 signature record"""
        try:
            df = pd.DataFrame([signature_record])
            df.to_sql('md5_signatures', self.engine, if_exists='append', index=False)
            return True
        except Exception as e:
            return False
    
    def get_all_signatures(self):
        """Get all MD5 signature records"""
        try:
            query = 'SELECT * FROM md5_signatures'
            return pd.read_sql(query, self.engine)
        except Exception as e:
            return pd.DataFrame()
    
    def save_model_metrics(self, metrics_dict):
        """Save ML model performance metrics"""
        try:
            df = pd.DataFrame([metrics_dict])
            df.to_sql('model_metrics', self.engine, if_exists='append', index=False)
            return True
        except Exception as e:
            return False
    
    def get_model_metrics(self):
        """Get all model metrics"""
        try:
            query = 'SELECT * FROM model_metrics'
            return pd.read_sql(query, self.engine)
        except Exception as e:
            return pd.DataFrame()
    
    def table_exists(self, table_name):
        """Check if table exists"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(
                    f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
                ))
                return result.fetchone() is not None
        except Exception as e:
            return False


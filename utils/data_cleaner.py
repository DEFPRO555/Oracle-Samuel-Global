# © 2025 Dowek Analytics Ltd.
# ORACLE SAMUEL – The Real Estate Market Prophet
# MD5-Protected AI System. Unauthorized use prohibited.

import pandas as pd
import numpy as np
from datetime import datetime


class DataCleaner:
    def __init__(self, df):
        self.df = df.copy()
        self.cleaning_report = []
    
    def clean_data(self):
        """Main cleaning pipeline"""
        self._standardize_column_names()
        self._handle_missing_values()
        self._remove_duplicates()
        self._validate_data_types()
        self._remove_outliers()
        return self.df, self.cleaning_report
    
    def _standardize_column_names(self):
        """Standardize column names to lowercase with underscores"""
        original_cols = self.df.columns.tolist()
        self.df.columns = self.df.columns.str.lower().str.replace(' ', '_').str.replace('[^a-z0-9_]', '', regex=True)
        self.cleaning_report.append(f"✓ Standardized {len(original_cols)} column names")
    
    def _handle_missing_values(self):
        """Handle missing values intelligently"""
        missing_before = self.df.isnull().sum().sum()
        
        # Fill numeric columns with median
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if self.df[col].isnull().any():
                median_val = self.df[col].median()
                self.df[col].fillna(median_val, inplace=True)
        
        # Fill categorical columns with mode
        cat_cols = self.df.select_dtypes(include=['object']).columns
        for col in cat_cols:
            if self.df[col].isnull().any():
                mode_val = self.df[col].mode()[0] if not self.df[col].mode().empty else 'Unknown'
                self.df[col].fillna(mode_val, inplace=True)
        
        missing_after = self.df.isnull().sum().sum()
        self.cleaning_report.append(f"✓ Handled {missing_before} missing values")
    
    def _remove_duplicates(self):
        """Remove duplicate rows"""
        duplicates = self.df.duplicated().sum()
        if duplicates > 0:
            self.df.drop_duplicates(inplace=True)
            self.cleaning_report.append(f"✓ Removed {duplicates} duplicate rows")
        else:
            self.cleaning_report.append("✓ No duplicate rows found")
    
    def _validate_data_types(self):
        """Validate and convert data types"""
        # Try to identify price columns and ensure they're numeric
        price_keywords = ['price', 'cost', 'value', 'amount']
        for col in self.df.columns:
            if any(keyword in col.lower() for keyword in price_keywords):
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        self.cleaning_report.append("✓ Validated data types")
    
    def _remove_outliers(self):
        """Remove extreme outliers using IQR method"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        outliers_removed = 0
        
        for col in numeric_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 3 * IQR
            upper_bound = Q3 + 3 * IQR
            
            before_count = len(self.df)
            self.df = self.df[(self.df[col] >= lower_bound) & (self.df[col] <= upper_bound)]
            outliers_removed += (before_count - len(self.df))
        
        if outliers_removed > 0:
            self.cleaning_report.append(f"✓ Removed {outliers_removed} outlier records")
        else:
            self.cleaning_report.append("✓ No significant outliers detected")
    
    def get_summary_stats(self):
        """Generate summary statistics"""
        stats = {
            'total_records': len(self.df),
            'total_columns': len(self.df.columns),
            'numeric_columns': len(self.df.select_dtypes(include=[np.number]).columns),
            'categorical_columns': len(self.df.select_dtypes(include=['object']).columns),
            'memory_usage_mb': self.df.memory_usage(deep=True).sum() / 1024**2
        }
        return stats


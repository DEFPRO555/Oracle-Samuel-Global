# © 2025 Dowek Analytics Ltd.
# ORACLE SAMUEL – The Real Estate Market Prophet
# MD5-Protected AI System. Unauthorized use prohibited.

import hashlib
import pandas as pd
from datetime import datetime


def generate_md5_signature(file_path):
    """Generate MD5 hash for a file"""
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return hashlib.md5(data).hexdigest()
    except Exception as e:
        return f"Error generating MD5: {str(e)}"


def generate_md5_from_dataframe(df):
    """Generate MD5 hash from DataFrame content"""
    try:
        data_string = df.to_json(orient='records')
        return hashlib.md5(data_string.encode()).hexdigest()
    except Exception as e:
        return f"Error generating MD5: {str(e)}"


def verify_data_integrity(df, stored_hash):
    """Verify if DataFrame matches stored MD5 hash"""
    current_hash = generate_md5_from_dataframe(df)
    return current_hash == stored_hash


def create_signature_record(file_name, md5_hash):
    """Create a signature record for tracking"""
    return {
        'file_name': file_name,
        'md5_hash': md5_hash,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'verified'
    }


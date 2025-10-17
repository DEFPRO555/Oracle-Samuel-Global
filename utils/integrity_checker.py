# © 2025 Dowek Analytics Ltd.
# ORACLE SAMUEL – Voice & Vision Intelligence
# MD5-Protected AI System. Unauthorized use prohibited.

import hashlib
import os
from sqlalchemy import create_engine, text
import pandas as pd
from datetime import datetime


class ProjectIntegrityChecker:
    """
    Verifies project integrity using MD5 hashing
    Protects against unauthorized copying or modification
    """
    
    def __init__(self, db_name='oracle_samuel_real_estate.db'):
        self.db_name = db_name
        self.engine = create_engine(f'sqlite:///{db_name}')
        self._initialize_integrity_table()
        self.critical_files = [
            'app.py',
            'agent.py',
            'utils/predictor.py',
            'utils/visualizer.py',
            'self_learning/trainer.py',
            'voice_agent/voice_handler.py',
            'vision/image_analyzer.py',
            'geo/map_visualizer.py'
        ]
    
    def _initialize_integrity_table(self):
        """Create integrity tracking table"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS project_hashes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        file_path TEXT UNIQUE,
                        md5_hash TEXT,
                        file_size INTEGER,
                        last_verified TEXT,
                        status TEXT
                    )
                """))
                conn.commit()
        except Exception as e:
            print(f"Error initializing integrity table: {str(e)}")
    
    def calculate_file_hash(self, file_path):
        """Calculate MD5 hash of a file"""
        try:
            if not os.path.exists(file_path):
                return None, "File not found"
            
            with open(file_path, 'rb') as f:
                file_data = f.read()
                md5_hash = hashlib.md5(file_data).hexdigest()
                file_size = len(file_data)
            
            return md5_hash, file_size
            
        except Exception as e:
            return None, f"Error: {str(e)}"
    
    def register_file(self, file_path):
        """Register a file and store its hash"""
        try:
            md5_hash, file_size_or_error = self.calculate_file_hash(file_path)
            
            if md5_hash is None:
                return False, file_size_or_error
            
            # Store in database
            with self.engine.connect() as conn:
                conn.execute(text("""
                    INSERT OR REPLACE INTO project_hashes 
                    (file_path, md5_hash, file_size, last_verified, status)
                    VALUES (:file_path, :md5_hash, :file_size, :timestamp, :status)
                """), {
                    'file_path': file_path,
                    'md5_hash': md5_hash,
                    'file_size': file_size_or_error,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'status': 'VERIFIED'
                })
                conn.commit()
            
            return True, md5_hash
            
        except Exception as e:
            return False, f"Registration error: {str(e)}"
    
    def verify_file(self, file_path):
        """Verify file integrity against stored hash"""
        try:
            # Get current hash
            current_hash, _ = self.calculate_file_hash(file_path)
            
            if current_hash is None:
                return False, "File not found or cannot be read"
            
            # Get stored hash
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT md5_hash FROM project_hashes 
                    WHERE file_path = :file_path
                """), {'file_path': file_path})
                row = result.fetchone()
            
            if row is None:
                return None, "File not registered"
            
            stored_hash = row[0]
            
            if current_hash == stored_hash:
                return True, "Integrity verified"
            else:
                return False, "File has been modified"
                
        except Exception as e:
            return None, f"Verification error: {str(e)}"
    
    def verify_project_integrity(self):
        """Verify integrity of all critical project files"""
        results = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'files_checked': 0,
            'files_verified': 0,
            'files_modified': 0,
            'files_missing': 0,
            'details': []
        }
        
        for file_path in self.critical_files:
            results['files_checked'] += 1
            
            status, message = self.verify_file(file_path)
            
            if status is True:
                results['files_verified'] += 1
                status_text = "✅ VERIFIED"
            elif status is False:
                results['files_modified'] += 1
                status_text = "⚠️ MODIFIED"
            else:
                results['files_missing'] += 1
                status_text = "❌ NOT REGISTERED"
            
            results['details'].append({
                'file': file_path,
                'status': status_text,
                'message': message
            })
        
        return results
    
    def register_all_critical_files(self):
        """Register all critical project files"""
        registered = []
        failed = []
        
        for file_path in self.critical_files:
            success, result = self.register_file(file_path)
            
            if success:
                registered.append(file_path)
            else:
                failed.append({'file': file_path, 'error': result})
        
        return {
            'registered': len(registered),
            'failed': len(failed),
            'registered_files': registered,
            'failed_files': failed
        }
    
    def get_integrity_log(self, limit=50):
        """Get integrity verification history"""
        try:
            query = f"""
                SELECT * FROM project_hashes 
                ORDER BY last_verified DESC 
                LIMIT {limit}
            """
            df = pd.read_sql(query, self.engine)
            return df
        except Exception as e:
            print(f"Error retrieving integrity log: {str(e)}")
            return pd.DataFrame()
    
    def generate_integrity_report(self):
        """Generate comprehensive integrity report"""
        verification_results = self.verify_project_integrity()
        
        report = f"""
# 🔐 PROJECT INTEGRITY REPORT
**Generated:** {verification_results['timestamp']}

## Summary
- **Files Checked:** {verification_results['files_checked']}
- **Verified:** {verification_results['files_verified']} ✅
- **Modified:** {verification_results['files_modified']} ⚠️
- **Missing/Not Registered:** {verification_results['files_missing']} ❌

## File Details
"""
        
        for detail in verification_results['details']:
            report += f"\n**{detail['file']}**\n"
            report += f"Status: {detail['status']}\n"
            report += f"Message: {detail['message']}\n"
        
        # Calculate overall integrity score
        total = verification_results['files_checked']
        verified = verification_results['files_verified']
        integrity_score = (verified / total * 100) if total > 0 else 0
        
        report += f"\n\n## Overall Integrity Score: {integrity_score:.1f}%\n"
        
        if integrity_score == 100:
            report += "\n✅ **Status: EXCELLENT** - All files verified and secure."
        elif integrity_score >= 80:
            report += "\n⚠️ **Status: GOOD** - Most files verified with minor issues."
        elif integrity_score >= 60:
            report += "\n⚠️ **Status: MODERATE** - Some files modified or missing."
        else:
            report += "\n❌ **Status: CRITICAL** - Major integrity issues detected."
        
        return report


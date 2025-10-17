# © 2025 Dowek Analytics Ltd.
# ORACLE SAMUEL – Automated Backup Script
# MD5-Protected AI System. Unauthorized use prohibited.

import os
import shutil
import sqlite3
import datetime
import zipfile
import hashlib
import json
from pathlib import Path

class OracleSamuelBackup:
    """
    Automated backup system for Oracle Samuel
    Creates comprehensive backups for deployment and recovery
    """
    
    def __init__(self, source_dir=".", backup_dir="backups"):
        self.source_dir = Path(source_dir)
        self.backup_dir = Path(backup_dir)
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_name = f"oracle_samuel_backup_{self.timestamp}"
        
    def create_backup_directory(self):
        """Create backup directory structure"""
        self.current_backup = self.backup_dir / self.backup_name
        self.current_backup.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (self.current_backup / "code").mkdir(exist_ok=True)
        (self.current_backup / "data").mkdir(exist_ok=True)
        (self.current_backup / "models").mkdir(exist_ok=True)
        (self.current_backup / "config").mkdir(exist_ok=True)
        (self.current_backup / "docs").mkdir(exist_ok=True)
        
        print(f"✅ Created backup directory: {self.current_backup}")
    
    def backup_code_files(self):
        """Backup all Python code files"""
        code_files = [
            "app.py",
            "enhanced_oracle_samuel.py",
            "oracle_samuel_enhancement.py",
            "test_enhanced_features.py",
            "integrate_enhancements.py",
            "agent.py",
            "requirements.txt",
            "setup.py"
        ]
        
        code_dir = self.current_backup / "code"
        backed_up_files = []
        
        for file in code_files:
            source_file = self.source_dir / file
            if source_file.exists():
                dest_file = code_dir / file
                shutil.copy2(source_file, dest_file)
                backed_up_files.append(file)
                print(f"✅ Backed up: {file}")
        
        # Backup utils directory
        utils_dir = self.source_dir / "utils"
        if utils_dir.exists():
            dest_utils = code_dir / "utils"
            shutil.copytree(utils_dir, dest_utils, dirs_exist_ok=True)
            backed_up_files.append("utils/")
            print(f"✅ Backed up: utils/")
        
        # Backup self_learning directory
        self_learning_dir = self.source_dir / "self_learning"
        if self_learning_dir.exists():
            dest_self_learning = code_dir / "self_learning"
            shutil.copytree(self_learning_dir, dest_self_learning, dirs_exist_ok=True)
            backed_up_files.append("self_learning/")
            print(f"✅ Backed up: self_learning/")
        
        return backed_up_files
    
    def backup_data_files(self):
        """Backup database and data files"""
        data_dir = self.current_backup / "data"
        backed_up_files = []
        
        # Backup SQLite database
        db_file = self.source_dir / "oracle_samuel_real_estate.db"
        if db_file.exists():
            dest_db = data_dir / "oracle_samuel_real_estate.db"
            shutil.copy2(db_file, dest_db)
            backed_up_files.append("oracle_samuel_real_estate.db")
            print(f"✅ Backed up database: oracle_samuel_real_estate.db")
            
            # Create SQL dump
            sql_dump = data_dir / "database_dump.sql"
            with sqlite3.connect(db_file) as conn:
                with open(sql_dump, 'w') as f:
                    for line in conn.iterdump():
                        f.write(f"{line}\n")
            backed_up_files.append("database_dump.sql")
            print(f"✅ Created SQL dump: database_dump.sql")
        
        # Backup sample data
        sample_files = ["sample_data.csv", "imagined_houses.xlsx"]
        for file in sample_files:
            source_file = self.source_dir / file
            if source_file.exists():
                dest_file = data_dir / file
                shutil.copy2(source_file, dest_file)
                backed_up_files.append(file)
                print(f"✅ Backed up sample data: {file}")
        
        return backed_up_files
    
    def backup_models(self):
        """Backup trained models"""
        models_dir = self.current_backup / "models"
        backed_up_files = []
        
        model_files = [
            "oracle_samuel_model.pkl",
            "enhanced_oracle_samuel_model.pkl"
        ]
        
        for file in model_files:
            source_file = self.source_dir / file
            if source_file.exists():
                dest_file = models_dir / file
                shutil.copy2(source_file, dest_file)
                backed_up_files.append(file)
                print(f"✅ Backed up model: {file}")
        
        return backed_up_files
    
    def backup_config_files(self):
        """Backup configuration files"""
        config_dir = self.current_backup / "config"
        backed_up_files = []
        
        config_files = [
            "docker-compose.yml",
            "Dockerfile",
            "env.template",
            "run.bat",
            "run.sh",
            "setup.bat",
            "setup.sh"
        ]
        
        for file in config_files:
            source_file = self.source_dir / file
            if source_file.exists():
                dest_file = config_dir / file
                shutil.copy2(source_file, dest_file)
                backed_up_files.append(file)
                print(f"✅ Backed up config: {file}")
        
        # Backup k8s directory
        k8s_dir = self.source_dir / "k8s"
        if k8s_dir.exists():
            dest_k8s = config_dir / "k8s"
            shutil.copytree(k8s_dir, dest_k8s, dirs_exist_ok=True)
            backed_up_files.append("k8s/")
            print(f"✅ Backed up: k8s/")
        
        return backed_up_files
    
    def backup_documentation(self):
        """Backup documentation files"""
        docs_dir = self.current_backup / "docs"
        backed_up_files = []
        
        doc_files = [
            "README.md",
            "ORACLE_SAMUEL_UNIVERSAL_GUIDE.md",
            "BACKUP_AND_DEPLOYMENT_GUIDE.md",
            "INTEGRATION_INSTRUCTIONS.md",
            "ENHANCED_ORACLE_SAMUEL_SUMMARY.md",
            "LUXURY_DESIGN_GUIDE.md",
            "PREMIUM_DESIGN_IMPLEMENTATION.md",
            "SECURITY.md",
            "DEPLOYMENT.md",
            "RUNBOOK.md"
        ]
        
        for file in doc_files:
            source_file = self.source_dir / file
            if source_file.exists():
                dest_file = docs_dir / file
                shutil.copy2(source_file, dest_file)
                backed_up_files.append(file)
                print(f"✅ Backed up documentation: {file}")
        
        return backed_up_files
    
    def create_backup_manifest(self, all_files):
        """Create backup manifest with file information"""
        manifest = {
            "backup_info": {
                "name": self.backup_name,
                "timestamp": self.timestamp,
                "created": datetime.datetime.now().isoformat(),
                "source_directory": str(self.source_dir.absolute()),
                "backup_directory": str(self.current_backup.absolute())
            },
            "files": {},
            "statistics": {
                "total_files": len(all_files),
                "total_size": 0
            }
        }
        
        total_size = 0
        for file_path in all_files:
            full_path = self.current_backup / file_path
            if full_path.exists():
                file_size = full_path.stat().st_size
                total_size += file_size
                
                # Calculate MD5 hash
                with open(full_path, 'rb') as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()
                
                manifest["files"][file_path] = {
                    "size": file_size,
                    "md5_hash": file_hash,
                    "modified": datetime.datetime.fromtimestamp(full_path.stat().st_mtime).isoformat()
                }
        
        manifest["statistics"]["total_size"] = total_size
        
        # Save manifest
        manifest_file = self.current_backup / "backup_manifest.json"
        with open(manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"✅ Created backup manifest: backup_manifest.json")
        return manifest
    
    def create_compressed_backup(self):
        """Create compressed backup archive"""
        zip_file = self.backup_dir / f"{self.backup_name}.zip"
        
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.current_backup):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(self.current_backup)
                    zipf.write(file_path, arcname)
        
        zip_size = zip_file.stat().st_size
        print(f"✅ Created compressed backup: {zip_file.name} ({zip_size / (1024*1024):.2f} MB)")
        
        return zip_file
    
    def create_deployment_package(self):
        """Create deployment-ready package"""
        deploy_dir = self.current_backup / "deployment"
        deploy_dir.mkdir(exist_ok=True)
        
        # Copy essential files for deployment
        essential_files = [
            "app.py",
            "requirements.txt",
            "README.md",
            "ORACLE_SAMUEL_UNIVERSAL_GUIDE.md",
            "BACKUP_AND_DEPLOYMENT_GUIDE.md"
        ]
        
        for file in essential_files:
            source_file = self.source_dir / file
            if source_file.exists():
                dest_file = deploy_dir / file
                shutil.copy2(source_file, dest_file)
        
        # Copy directories
        dirs_to_copy = ["utils", "self_learning", "assets"]
        for dir_name in dirs_to_copy:
            source_dir = self.source_dir / dir_name
            if source_dir.exists():
                dest_dir = deploy_dir / dir_name
                shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True)
        
        # Create deployment instructions
        deploy_instructions = """
# Oracle Samuel Deployment Package

## Quick Start:
1. Install dependencies: pip install -r requirements.txt
2. Run application: streamlit run app.py
3. Access at: http://localhost:8501

## For Production:
1. Follow BACKUP_AND_DEPLOYMENT_GUIDE.md
2. Configure environment variables
3. Set up database
4. Deploy using Docker or cloud platform

## Support:
- Documentation: ORACLE_SAMUEL_UNIVERSAL_GUIDE.md
- Backup Guide: BACKUP_AND_DEPLOYMENT_GUIDE.md
- Integration: INTEGRATION_INSTRUCTIONS.md

© 2025 Dowek Analytics Ltd. All Rights Reserved.
        """
        
        with open(deploy_dir / "DEPLOYMENT_INSTRUCTIONS.txt", 'w', encoding='utf-8') as f:
            f.write(deploy_instructions)
        
        print(f"✅ Created deployment package in: {deploy_dir}")
    
    def run_complete_backup(self):
        """Run complete backup process"""
        print("🚀 Starting Oracle Samuel Backup Process...")
        print("=" * 50)
        
        # Create backup directory
        self.create_backup_directory()
        
        # Backup all components
        all_files = []
        all_files.extend(self.backup_code_files())
        all_files.extend(self.backup_data_files())
        all_files.extend(self.backup_models())
        all_files.extend(self.backup_config_files())
        all_files.extend(self.backup_documentation())
        
        # Create manifest
        manifest = self.create_backup_manifest(all_files)
        
        # Create compressed backup
        zip_file = self.create_compressed_backup()
        
        # Create deployment package
        self.create_deployment_package()
        
        # Summary
        print("\n" + "=" * 50)
        print("🎉 BACKUP COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print(f"📁 Backup Location: {self.current_backup}")
        print(f"📦 Compressed File: {zip_file}")
        print(f"📊 Total Files: {manifest['statistics']['total_files']}")
        print(f"💾 Total Size: {manifest['statistics']['total_size'] / (1024*1024):.2f} MB")
        print(f"🗜️  Compressed Size: {zip_file.stat().st_size / (1024*1024):.2f} MB")
        print("\n🚀 Ready for deployment to any platform!")
        print("📖 See BACKUP_AND_DEPLOYMENT_GUIDE.md for deployment instructions")
        
        return {
            "backup_dir": self.current_backup,
            "zip_file": zip_file,
            "manifest": manifest
        }

def main():
    """Main backup function"""
    backup = OracleSamuelBackup()
    result = backup.run_complete_backup()
    return result

if __name__ == "__main__":
    main()

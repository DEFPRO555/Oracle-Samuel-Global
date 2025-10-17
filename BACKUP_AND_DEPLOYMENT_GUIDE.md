# 🔄 ORACLE SAMUEL - Backup & Deployment Guide
## © 2025 Dowek Analytics Ltd. All Rights Reserved.

### Complete Backup and Deployment Instructions

---

## 📦 **Backup Strategy**

### **1. Complete System Backup**
```bash
# Create backup directory
mkdir oracle_samuel_backup_$(date +%Y%m%d)
cd oracle_samuel_backup_$(date +%Y%m%d)

# Copy all essential files
cp -r ../Linear_regression\ APP/* .

# Create compressed backup
tar -czf oracle_samuel_complete_backup_$(date +%Y%m%d).tar.gz *
```

### **2. Database Backup**
```bash
# Backup SQLite database
cp oracle_samuel_real_estate.db oracle_samuel_backup_$(date +%Y%m%d).db

# Export data to CSV
sqlite3 oracle_samuel_real_estate.db ".mode csv" ".output backup_data.csv" "SELECT * FROM uploaded_data;"
```

### **3. Model Backup**
```bash
# Backup trained models
cp oracle_samuel_model.pkl oracle_samuel_model_backup_$(date +%Y%m%d).pkl
cp enhanced_oracle_samuel_model.pkl enhanced_oracle_samuel_model_backup_$(date +%Y%m%d).pkl
```

---

## 🚀 **Deployment Options**

### **Option 1: Local Development**
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py

# Access at: http://localhost:8501
```

### **Option 2: Docker Deployment**
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
# Build and run Docker container
docker build -t oracle-samuel .
docker run -p 8501:8501 oracle-samuel
```

### **Option 3: Cloud Deployment**

#### **Heroku Deployment**
```bash
# Install Heroku CLI
# Create Procfile
echo "web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0" > Procfile

# Deploy to Heroku
heroku create oracle-samuel-app
git add .
git commit -m "Deploy Oracle Samuel"
git push heroku main
```

#### **AWS Deployment**
```bash
# Using AWS Elastic Beanstalk
eb init oracle-samuel
eb create oracle-samuel-env
eb deploy
```

#### **Google Cloud Deployment**
```bash
# Using Google Cloud Run
gcloud run deploy oracle-samuel --source . --platform managed --region us-central1
```

---

## 🔧 **Configuration Management**

### **Environment Variables**
```bash
# Create .env file
cat > .env << EOF
# Database Configuration
DATABASE_URL=sqlite:///oracle_samuel_real_estate.db

# Security
SECRET_KEY=your_secret_key_here
MD5_SALT=your_md5_salt_here

# API Keys (if needed)
OPENAI_API_KEY=your_openai_key
GOOGLE_MAPS_API_KEY=your_google_maps_key

# Deployment
ENVIRONMENT=production
DEBUG=False
EOF
```

### **Configuration File**
```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///oracle_samuel_real_estate.db')
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    MD5_SALT = os.getenv('MD5_SALT', 'default_salt')
    
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
    
    # Deployment
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
```

---

## 📊 **Database Migration**

### **SQLite to PostgreSQL**
```python
# migration_script.py
import sqlite3
import psycopg2
import pandas as pd

def migrate_to_postgresql():
    # Connect to SQLite
    sqlite_conn = sqlite3.connect('oracle_samuel_real_estate.db')
    
    # Connect to PostgreSQL
    pg_conn = psycopg2.connect(
        host="your_host",
        database="oracle_samuel",
        user="your_user",
        password="your_password"
    )
    
    # Migrate tables
    tables = ['uploaded_data', 'model_metrics', 'signatures', 'feedback']
    
    for table in tables:
        df = pd.read_sql_query(f"SELECT * FROM {table}", sqlite_conn)
        df.to_sql(table, pg_conn, if_exists='replace', index=False)
    
    sqlite_conn.close()
    pg_conn.close()
```

### **Database Schema**
```sql
-- PostgreSQL Schema
CREATE TABLE uploaded_data (
    id SERIAL PRIMARY KEY,
    data TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    md5_hash VARCHAR(32)
);

CREATE TABLE model_metrics (
    id SERIAL PRIMARY KEY,
    model_type VARCHAR(50),
    mae DECIMAL(10,2),
    rmse DECIMAL(10,2),
    r2_score DECIMAL(5,4),
    training_samples INTEGER,
    test_samples INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE signatures (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255),
    md5_hash VARCHAR(32),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    rating INTEGER,
    comment TEXT,
    feedback_type VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔐 **Security Configuration**

### **SSL/TLS Setup**
```bash
# Generate SSL certificates
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Update Streamlit config
echo "[server]
sslCertFile = \"cert.pem\"
sslKeyFile = \"key.pem\"
" >> ~/.streamlit/config.toml
```

### **Authentication Setup**
```python
# auth.py
import streamlit as st
import hashlib
import secrets

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password():
    """Returns `True` if the user had the correct password."""
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated successfully.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False
```

---

## 📈 **Monitoring & Logging**

### **Application Monitoring**
```python
# monitoring.py
import logging
import time
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('oracle_samuel.log'),
        logging.StreamHandler()
    ]
)

def monitor_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        logging.info(f"{func.__name__} executed in {end_time - start_time:.2f} seconds")
        return result
    return wrapper
```

### **Health Check Endpoint**
```python
# health_check.py
import streamlit as st
import psutil
import os

def health_check():
    """System health check"""
    health_status = {
        "status": "healthy",
        "timestamp": time.time(),
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent,
        "database_connected": check_database_connection(),
        "models_loaded": check_models_loaded()
    }
    
    return health_status
```

---

## 🔄 **Automated Backup Script**

```python
# backup_script.py
import os
import shutil
import sqlite3
import datetime
import schedule
import time

def create_backup():
    """Create automated backup"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backups/backup_{timestamp}"
    
    # Create backup directory
    os.makedirs(backup_dir, exist_ok=True)
    
    # Backup files
    files_to_backup = [
        "app.py",
        "enhanced_oracle_samuel.py",
        "oracle_samuel_enhancement.py",
        "requirements.txt",
        "oracle_samuel_real_estate.db",
        "oracle_samuel_model.pkl"
    ]
    
    for file in files_to_backup:
        if os.path.exists(file):
            shutil.copy2(file, backup_dir)
    
    # Backup database
    db_backup = f"{backup_dir}/database_backup.sql"
    with sqlite3.connect('oracle_samuel_real_estate.db') as conn:
        with open(db_backup, 'w') as f:
            for line in conn.iterdump():
                f.write(f"{line}\n")
    
    print(f"Backup created: {backup_dir}")

# Schedule daily backups
schedule.every().day.at("02:00").do(create_backup)

# Run scheduler
while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## 🚀 **Production Deployment Checklist**

### **Pre-deployment:**
- [ ] All tests passing
- [ ] Security scan completed
- [ ] Performance testing done
- [ ] Backup created
- [ ] Environment variables configured
- [ ] SSL certificates installed
- [ ] Database migrated (if needed)
- [ ] Monitoring configured

### **Deployment:**
- [ ] Deploy to staging environment
- [ ] Run smoke tests
- [ ] Deploy to production
- [ ] Verify all features working
- [ ] Monitor system health
- [ ] Update documentation

### **Post-deployment:**
- [ ] Monitor logs for errors
- [ ] Check performance metrics
- [ ] Verify backup systems
- [ ] Update team on deployment
- [ ] Schedule maintenance windows

---

## 📞 **Support & Maintenance**

### **Regular Maintenance Tasks:**
- **Daily**: Monitor system health, check logs
- **Weekly**: Review performance metrics, update dependencies
- **Monthly**: Security updates, backup verification
- **Quarterly**: Full system audit, capacity planning

### **Emergency Procedures:**
- **System Down**: Check logs, restart services, contact support
- **Data Loss**: Restore from backup, investigate cause
- **Security Breach**: Isolate system, investigate, patch vulnerabilities
- **Performance Issues**: Scale resources, optimize code

---

## 🎯 **Success Metrics**

### **Deployment Success:**
- **Uptime** > 99.9%
- **Response Time** < 2 seconds
- **Error Rate** < 0.1%
- **User Satisfaction** > 4.5/5

### **Business Impact:**
- **User Adoption** - Number of active users
- **Data Processing** - Volume of data analyzed
- **Insights Generated** - Number of reports created
- **Decision Support** - Business decisions influenced

---

**© 2025 Dowek Analytics Ltd. All Rights Reserved.**
**MD5-Protected Universal AI System. Unauthorized use prohibited.**

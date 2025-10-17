# Oracle Samuel - Security Guide
© 2025 Dowek Analytics Ltd.

## 🔒 Security Overview

Oracle Samuel implements defense-in-depth security with multiple layers of protection:

1. **Network Security**: TLS encryption, WAF, DDoS protection
2. **Authentication & Authorization**: JWT tokens, API keys, RBAC
3. **Data Security**: Encryption at rest and in transit
4. **Application Security**: Input validation, rate limiting, security headers
5. **Infrastructure Security**: Network isolation, least privilege IAM
6. **Monitoring & Incident Response**: Real-time threat detection, audit logging

---

## 🔐 Authentication & Authorization

### API Key Management

**Creating API Keys**:
```python
import secrets
import hashlib

# Generate secure API key
api_key = secrets.token_urlsafe(32)

# Hash for storage (never store plaintext)
api_key_hash = hashlib.sha256(api_key.encode()).hexdigest()

# Store in database with metadata
{
  "key_hash": api_key_hash,
  "customer_id": "cust_123",
  "rate_limit": 1000,
  "scopes": ["predict", "upload"],
  "expires_at": "2026-01-01T00:00:00Z"
}
```

**Validating API Keys**:
```python
# backend/main.py already implements this
async def verify_api_key(credentials: HTTPAuthorizationCredentials):
    incoming_key_hash = hashlib.sha256(credentials.credentials.encode()).hexdigest()
    # Check against database
    # Verify not expired
    # Check rate limit
    return api_key_data
```

### JWT Tokens (for user sessions)

**Implementation**:
```python
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### Role-Based Access Control (RBAC)

**Roles**:
- `admin`: Full access to all resources
- `analyst`: Read/write predictions, models
- `viewer`: Read-only access
- `api_user`: Programmatic access via API

**Implementation**:
```python
from enum import Enum

class Role(str, Enum):
    ADMIN = "admin"
    ANALYST = "analyst"
    VIEWER = "viewer"
    API_USER = "api_user"

def require_role(required_role: Role):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            user = get_current_user()  # From JWT or API key
            if user.role not in [required_role, Role.ADMIN]:
                raise HTTPException(status_code=403, detail="Insufficient permissions")
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Usage
@app.post("/api/v1/admin/users")
@require_role(Role.ADMIN)
async def create_user():
    pass
```

---

## 🔗 Network Security

### TLS/SSL Configuration

**Kubernetes (cert-manager)**:
```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: oracle-tls-cert
spec:
  secretName: oracle-tls-cert
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  dnsNames:
    - oracle-samuel.com
    - api.oracle-samuel.com
  privateKey:
    algorithm: RSA
    size: 4096
```

**NGINX Configuration**:
```nginx
server {
    listen 443 ssl http2;
    server_name oracle-samuel.com;

    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;
    
    # Strong SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
    ssl_prefer_server_ciphers on;
    ssl_session_timeout 10m;
    ssl_session_cache shared:SSL:10m;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Security headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;
}
```

### Web Application Firewall (WAF)

**GCP Cloud Armor**:
```bash
# Create security policy
gcloud compute security-policies create oracle-waf-policy \
    --description "WAF for Oracle Samuel"

# Block known bad actors
gcloud compute security-policies rules create 1000 \
    --security-policy oracle-waf-policy \
    --expression "origin.region_code == 'CN' || origin.region_code == 'RU'" \
    --action "deny-403"

# Rate limiting
gcloud compute security-policies rules create 2000 \
    --security-policy oracle-waf-policy \
    --expression "true" \
    --action "rate-based-ban" \
    --rate-limit-threshold-count 100 \
    --rate-limit-threshold-interval-sec 60

# Apply to backend
gcloud compute backend-services update oracle-backend \
    --security-policy oracle-waf-policy
```

**AWS WAF**:
```bash
# Create WAF WebACL
aws wafv2 create-web-acl \
  --name oracle-waf \
  --scope REGIONAL \
  --default-action Block={} \
  --rules file://waf-rules.json

# Associate with ALB
aws wafv2 associate-web-acl \
  --web-acl-arn arn:aws:wafv2:... \
  --resource-arn arn:aws:elasticloadbalancing:...
```

---

## 🔒 Data Security

### Encryption at Rest

**Database Encryption**:
```bash
# GCP Cloud SQL
gcloud sql instances create oracle-db \
  --database-version=POSTGRES_15 \
  --disk-encryption-key=projects/PROJECT/locations/REGION/keyRings/KEYRING/cryptoKeys/KEY

# AWS RDS
aws rds create-db-instance \
  --db-instance-identifier oracle-db \
  --storage-encrypted \
  --kms-key-id arn:aws:kms:...
```

**Object Storage Encryption**:
```bash
# GCS
gsutil kms encryption \
  -k projects/PROJECT/locations/REGION/keyRings/KEYRING/cryptoKeys/KEY \
  gs://oracle-samuel-models

# S3
aws s3api put-bucket-encryption \
  --bucket oracle-samuel-models \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "aws:kms",
        "KMSMasterKeyID": "arn:aws:kms:..."
      }
    }]
  }'
```

### Encryption in Transit

**All communication uses TLS 1.2+**:
- Client ↔ Load Balancer: HTTPS
- Load Balancer ↔ Backend: HTTPS (internal)
- Backend ↔ Database: SSL/TLS
- Backend ↔ Redis: TLS (if enabled)
- Backend ↔ Object Storage: HTTPS

**Database SSL Enforcement**:
```sql
-- PostgreSQL
ALTER SYSTEM SET ssl = on;
ALTER SYSTEM SET ssl_min_protocol_version = 'TLSv1.2';

-- Require SSL for all connections
ALTER USER oracle WITH PASSWORD 'xxx' REQUIRE SSL;
```

### Sensitive Data Handling

**PII Redaction**:
```python
import re

def redact_pii(text: str) -> str:
    # Email
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
    
    # Phone
    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', text)
    
    # Credit card (basic)
    text = re.sub(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b', '[CC]', text)
    
    return text

# Use in logging
logger.info(f"User query: {redact_pii(user_input)}")
```

**Field-Level Encryption**:
```python
from cryptography.fernet import Fernet

class EncryptedField:
    def __init__(self, key: bytes):
        self.cipher = Fernet(key)
    
    def encrypt(self, plaintext: str) -> str:
        return self.cipher.encrypt(plaintext.encode()).decode()
    
    def decrypt(self, ciphertext: str) -> str:
        return self.cipher.decrypt(ciphertext.encode()).decode()

# Usage
encryptor = EncryptedField(os.getenv("FIELD_ENCRYPTION_KEY").encode())
user.email_encrypted = encryptor.encrypt(user.email)
```

---

## 🛡️ Application Security

### Input Validation

**Pydantic Models** (already implemented):
```python
from pydantic import BaseModel, Field, validator

class PredictionRequest(BaseModel):
    area: float = Field(..., gt=0, lt=10000)
    rooms: int = Field(..., ge=1, le=20)
    city: str = Field(..., min_length=2, max_length=100)
    
    @validator('city')
    def validate_city(cls, v):
        # Prevent SQL injection
        if re.search(r"[;'\"]", v):
            raise ValueError("Invalid characters in city name")
        return v.strip()
```

### SQL Injection Prevention

**Use ORM/Parameterized Queries**:
```python
# ❌ BAD - Vulnerable to SQL injection
query = f"SELECT * FROM users WHERE email = '{user_email}'"

# ✅ GOOD - Parameterized query
query = "SELECT * FROM users WHERE email = %s"
cursor.execute(query, (user_email,))

# ✅ GOOD - SQLAlchemy ORM
session.query(User).filter(User.email == user_email).first()
```

### XSS Prevention

**Output Escaping**:
```python
import html

def safe_output(user_input: str) -> str:
    return html.escape(user_input)

# In Streamlit
st.write(safe_output(user_input))
```

**Content Security Policy**:
```python
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline';"
    )
    return response
```

### Rate Limiting

**Implementation**:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/v1/predict")
@limiter.limit("100/minute")
async def predict(request: Request):
    pass
```

**Redis-based Rate Limiting**:
```python
def check_rate_limit(api_key: str, limit: int = 1000, window: int = 3600):
    key = f"ratelimit:{api_key}"
    current = redis_client.get(key)
    
    if current and int(current) >= limit:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    pipe = redis_client.pipeline()
    pipe.incr(key)
    pipe.expire(key, window)
    pipe.execute()
```

---

## 📊 Audit Logging

### Security Events to Log

1. **Authentication Events**:
   - Login success/failure
   - API key creation/deletion
   - Token refresh
   - Password changes

2. **Authorization Events**:
   - Permission denied (403)
   - Unauthorized access attempts (401)

3. **Data Access Events**:
   - Model downloads
   - Dataset uploads
   - Prediction requests (with metadata)

4. **Administrative Events**:
   - User creation/deletion
   - Role changes
   - Configuration changes

### Implementation

```python
import logging
import json

def audit_log(event_type: str, user_id: str, details: dict):
    audit_logger = logging.getLogger("audit")
    audit_logger.info(json.dumps({
        "event_type": event_type,
        "user_id": user_id,
        "timestamp": datetime.utcnow().isoformat(),
        "ip_address": request.client.host,
        "user_agent": request.headers.get("user-agent"),
        "details": details
    }))

# Usage
@app.post("/api/v1/predict")
async def predict(request: PredictionRequest, user=Depends(get_current_user)):
    prediction = make_prediction(request)
    
    audit_log(
        event_type="prediction",
        user_id=user.id,
        details={"prediction_id": prediction.id, "model_version": "1.0.0"}
    )
    
    return prediction
```

### Log Storage

- **Retention**: 90 days hot storage, 1 year cold storage
- **Destination**: Cloud Logging (GCP) or CloudWatch (AWS)
- **SIEM Integration**: Export to Splunk/ELK for security analysis

---

## 🚨 Incident Response

### Detection

**Automated Alerts**:
1. **Brute Force Attack**: >10 failed logins in 5 minutes
2. **SQL Injection Attempt**: Detected via WAF or input validation
3. **Unusual Data Access**: Large batch downloads
4. **Credential Stuffing**: Multiple users from same IP

### Response Procedure

1. **Immediate Containment**:
```bash
# Block suspicious IP
kubectl exec -it deployment/nginx -n oracle-samuel -- \
  nginx -s reload -c /etc/nginx/conf.d/blocked_ips.conf

# Revoke API key
psql $DATABASE_URL -c "UPDATE api_keys SET revoked = true WHERE key_hash = 'xxx';"

# Disable user account
psql $DATABASE_URL -c "UPDATE users SET disabled = true WHERE id = 'xxx';"
```

2. **Investigation**:
```bash
# Review access logs
kubectl logs deployment/oracle-backend -n oracle-samuel --since=1h | grep "suspicious_ip"

# Check audit logs
gsutil cat gs://oracle-samuel-logs/audit/$(date +%Y-%m-%d)/* | grep "event_type.*unauthorized"
```

3. **Remediation**:
- Patch vulnerability
- Rotate credentials
- Update WAF rules
- Notify affected users

4. **Post-Incident**:
- Write postmortem
- Update security policies
- Implement preventive measures

---

## 🔑 Secrets Management

### Secret Rotation Policy

| Secret Type | Rotation Frequency | Automated |
|-------------|-------------------|-----------|
| API Keys | 90 days | No |
| Database Passwords | 90 days | No |
| JWT Secret | 180 days | No |
| TLS Certificates | Auto (30 days before expiry) | Yes |
| Service Account Keys | 90 days | No |

### Rotation Procedure

```bash
# 1. Generate new secret
NEW_SECRET=$(openssl rand -base64 32)

# 2. Store in secret manager
gcloud secrets versions add api-secret-key --data-file=<(echo -n "$NEW_SECRET")

# 3. Update application
gcloud run services update oracle-backend \
  --update-secrets=API_SECRET_KEY=api-secret-key:latest

# 4. Verify new secret works
curl https://api.oracle-samuel.com/health -H "Authorization: Bearer $NEW_SECRET"

# 5. Disable old secret version
gcloud secrets versions disable OLD_VERSION --secret=api-secret-key
```

---

## 🔒 Compliance

### GDPR Compliance

**Data Subject Rights**:
```python
@app.post("/api/v1/gdpr/export")
async def export_user_data(user_id: str):
    """Export all user data (GDPR Article 20)"""
    user_data = {
        "personal_info": get_user_info(user_id),
        "predictions": get_user_predictions(user_id),
        "uploads": get_user_uploads(user_id)
    }
    return user_data

@app.delete("/api/v1/gdpr/delete")
async def delete_user_data(user_id: str):
    """Delete all user data (GDPR Article 17)"""
    delete_user(user_id)
    delete_predictions(user_id)
    delete_uploads(user_id)
    audit_log("gdpr_deletion", user_id, {})
```

### SOC 2 Compliance

**Key Controls**:
- ✅ Access controls (RBAC)
- ✅ Encryption at rest and in transit
- ✅ Audit logging
- ✅ Vulnerability scanning
- ✅ Incident response plan
- ✅ Business continuity plan

---

## 📋 Security Checklist

### Pre-Deployment
- [ ] All secrets stored in secret manager (not in code)
- [ ] TLS certificates valid and auto-renewing
- [ ] WAF rules updated
- [ ] Rate limits configured
- [ ] Security headers enabled
- [ ] Vulnerability scan passed
- [ ] Dependencies updated
- [ ] Audit logging enabled

### Monthly Review
- [ ] Review access logs for anomalies
- [ ] Update dependencies
- [ ] Rotate credentials
- [ ] Review IAM permissions
- [ ] Scan for CVEs
- [ ] Test backup restoration
- [ ] Review firewall rules

### Quarterly Audit
- [ ] Penetration testing
- [ ] Security training for team
- [ ] Review and update policies
- [ ] Compliance audit (GDPR/SOC2)
- [ ] Incident response drill

---

## 📞 Security Contacts

- **Security Team**: security@dowekanalytics.com
- **CISO**: ciso@dowekanalytics.com
- **Security Incidents**: security-incidents@dowekanalytics.com (24/7)
- **Bug Bounty**: https://hackerone.com/dowek-analytics

---

**Last Updated**: 2025-01-14
**Next Review**: 2025-04-14
**Owner**: Security Team


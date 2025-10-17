# Oracle Samuel - Deployment Guide
© 2025 Dowek Analytics Ltd.

## 📋 Table of Contents
1. [Quick Start](#quick-start)
2. [Local Development](#local-development)
3. [Cloud Deployment](#cloud-deployment)
   - [GCP (Cloud Run)](#gcp-deployment)
   - [AWS (ECS)](#aws-deployment)
   - [Kubernetes](#kubernetes-deployment)
4. [Configuration](#configuration)
5. [Secrets Management](#secrets-management)
6. [Monitoring & Observability](#monitoring)
7. [Backup & Disaster Recovery](#backup-dr)
8. [Scaling](#scaling)
9. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Git
- Python 3.11+
- Cloud provider account (GCP/AWS) OR Kubernetes cluster

### Clone Repository
```bash
git clone https://github.com/dowek-analytics/oracle-samuel.git
cd oracle-samuel
```

---

## 💻 Local Development

### 1. Setup Environment
```bash
# Copy environment template
cp env.template .env

# Edit .env with your configuration
nano .env
```

### 2. Start with Docker Compose
```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Access services:
# - Frontend: http://localhost:8501
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/api/docs
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3000 (admin/admin)
```

### 3. Initialize Database
```bash
docker-compose exec backend python -c "
from utils.database_manager import DatabaseManager
db = DatabaseManager()
db.initialize_schema()
"
```

### 4. Run Tests
```bash
docker-compose exec backend pytest tests/ -v
```

### 5. Stop Services
```bash
docker-compose down
# Keep data:
docker-compose down --volumes  # Remove volumes
```

---

## ☁️ Cloud Deployment

## GCP Deployment (Cloud Run + Cloud SQL + GCS)

### Prerequisites
- GCP Account with billing enabled
- `gcloud` CLI installed
- Terraform installed

### 1. Setup GCP Project
```bash
# Login
gcloud auth login
gcloud auth application-default login

# Set project
export GCP_PROJECT_ID="your-project-id"
gcloud config set project $GCP_PROJECT_ID

# Enable required APIs
gcloud services enable \
  run.googleapis.com \
  sqladmin.googleapis.com \
  storage-api.googleapis.com \
  secretmanager.googleapis.com \
  redis.googleapis.com \
  cloudscheduler.googleapis.com
```

### 2. Deploy Infrastructure with Terraform
```bash
cd terraform/gcp

# Initialize Terraform
terraform init

# Create terraform.tfvars
cat > terraform.tfvars <<EOF
project_id    = "$GCP_PROJECT_ID"
region        = "us-central1"
environment   = "production"
db_password   = "CHANGE_ME_SECURE_PASSWORD"
EOF

# Plan deployment
terraform plan

# Apply (deploy)
terraform apply
```

### 3. Store Secrets
```bash
# API Secret Key
echo -n "your-super-secret-api-key-min-32-chars" | \
  gcloud secrets create api-secret-key --data-file=-

# OpenAI API Key
echo -n "sk-your-openai-key" | \
  gcloud secrets create openai-api-key --data-file=-
```

### 4. Build & Deploy
```bash
# Build images
gcloud builds submit --tag gcr.io/$GCP_PROJECT_ID/oracle-backend ./backend
gcloud builds submit --tag gcr.io/$GCP_PROJECT_ID/oracle-frontend ./frontend

# Deploy via Terraform (already done in step 2)
# OR deploy manually:
gcloud run deploy oracle-backend \
  --image gcr.io/$GCP_PROJECT_ID/oracle-backend:latest \
  --region us-central1 \
  --platform managed \
  --min-instances 2 \
  --max-instances 10
```

### 5. Configure Custom Domain
```bash
gcloud run domain-mappings create \
  --service oracle-frontend \
  --domain oracle-samuel.com \
  --region us-central1
```

### 6. Verify Deployment
```bash
# Get URLs
gcloud run services describe oracle-backend --region us-central1 --format='value(status.url)'
gcloud run services describe oracle-frontend --region us-central1 --format='value(status.url)'

# Test health
curl $(gcloud run services describe oracle-backend --region us-central1 --format='value(status.url)')/health
```

---

## AWS Deployment (ECS Fargate + RDS + S3)

### Prerequisites
- AWS Account
- AWS CLI configured
- Terraform installed

### 1. Configure AWS CLI
```bash
aws configure
# Enter: Access Key ID, Secret Access Key, Region (us-east-1), Output format (json)
```

### 2. Create S3 Bucket for Terraform State
```bash
aws s3 mb s3://oracle-samuel-terraform-state
aws s3api put-bucket-versioning \
  --bucket oracle-samuel-terraform-state \
  --versioning-configuration Status=Enabled
```

### 3. Deploy Infrastructure
```bash
cd terraform/aws

# Initialize Terraform
terraform init

# Create terraform.tfvars
cat > terraform.tfvars <<EOF
region       = "us-east-1"
environment  = "production"
db_password  = "CHANGE_ME_SECURE_PASSWORD"
certificate_arn = "arn:aws:acm:us-east-1:ACCOUNT:certificate/CERT_ID"
EOF

# Deploy
terraform plan
terraform apply
```

### 4. Build & Push Images
```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

# Build and push
docker build -t ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/oracle-backend:latest ./backend
docker build -t ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/oracle-frontend:latest ./frontend

docker push ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/oracle-backend:latest
docker push ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/oracle-frontend:latest
```

### 5. Update ECS Services
```bash
aws ecs update-service \
  --cluster oracle-samuel-cluster-production \
  --service oracle-backend-service \
  --force-new-deployment
```

### 6. Get Load Balancer URL
```bash
terraform output alb_dns_name
```

---

## Kubernetes Deployment (GKE/EKS/AKS)

### 1. Setup Kubernetes Cluster
```bash
# GKE
gcloud container clusters create oracle-cluster \
  --region us-central1 \
  --num-nodes 3 \
  --machine-type n1-standard-2

# Get credentials
gcloud container clusters get-credentials oracle-cluster --region us-central1

# OR EKS
eksctl create cluster \
  --name oracle-cluster \
  --region us-east-1 \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 3
```

### 2. Install Required Tools
```bash
# Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Install cert-manager (for SSL)
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Install NGINX Ingress
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/cloud/deploy.yaml
```

### 3. Create Namespace & Secrets
```bash
kubectl create namespace oracle-samuel

# Create secrets
kubectl create secret generic oracle-secrets \
  --from-literal=DB_PASSWORD='your-password' \
  --from-literal=API_SECRET_KEY='your-api-key' \
  --from-literal=OPENAI_API_KEY='sk-your-key' \
  -n oracle-samuel
```

### 4. Deploy with Kubectl
```bash
# Apply all manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/postgres.yaml
kubectl apply -f k8s/redis.yaml
kubectl apply -f k8s/backend.yaml
kubectl apply -f k8s/frontend.yaml
kubectl apply -f k8s/ingress.yaml

# Verify
kubectl get pods -n oracle-samuel
kubectl get services -n oracle-samuel
kubectl get ingress -n oracle-samuel
```

### 5. OR Deploy with Helm
```bash
cd helm/oracle-samuel

# Edit values.yaml with your configuration
nano values.yaml

# Install
helm install oracle-samuel . -n oracle-samuel

# Upgrade
helm upgrade oracle-samuel . -n oracle-samuel

# Uninstall
helm uninstall oracle-samuel -n oracle-samuel
```

---

## 🔐 Secrets Management

### GCP Secret Manager
```bash
# Create secret
gcloud secrets create SECRET_NAME --data-file=/path/to/secret

# Grant access to service account
gcloud secrets add-iam-policy-binding SECRET_NAME \
  --member='serviceAccount:SERVICE_ACCOUNT@PROJECT.iam.gserviceaccount.com' \
  --role='roles/secretmanager.secretAccessor'

# Use in Cloud Run
gcloud run services update SERVICE_NAME \
  --update-secrets=ENV_VAR=SECRET_NAME:latest
```

### AWS Secrets Manager
```bash
# Create secret
aws secretsmanager create-secret \
  --name oracle/api-key \
  --secret-string "your-secret-value"

# Reference in ECS task definition (use secretsmanager ARN)
```

### Kubernetes Secrets
```bash
# From literal
kubectl create secret generic my-secret \
  --from-literal=key=value \
  -n oracle-samuel

# From file
kubectl create secret generic my-secret \
  --from-file=./secret-file.txt \
  -n oracle-samuel

# Use sealed-secrets for GitOps
kubeseal --format=yaml < secret.yaml > sealed-secret.yaml
kubectl apply -f sealed-secret.yaml
```

---

## 📊 Monitoring & Observability

### Access Dashboards
- **Grafana**: http://your-domain:3000 (admin/admin)
- **Prometheus**: http://your-domain:9090

### Key Metrics to Monitor
1. **API Performance**
   - Request rate
   - Error rate (target: <1%)
   - P99 latency (target: <500ms)

2. **Model Performance**
   - MAE (Mean Absolute Error)
   - R² Score
   - Prediction count

3. **Infrastructure**
   - CPU usage (alert at >80%)
   - Memory usage (alert at >85%)
   - Disk usage (alert at >80%)

4. **Business Metrics**
   - Predictions per hour
   - User satisfaction score
   - API usage by customer

### Setup Alerts
```bash
# Configure Alertmanager
kubectl apply -f monitoring/alertmanager-config.yaml

# Alerts go to:
# - Slack: #oracle-alerts
# - Email: alerts@dowekanalytics.com
# - PagerDuty (P1 only)
```

---

## 💾 Backup & Disaster Recovery

### Database Backups
**GCP Cloud SQL**
```bash
# Automated backups enabled in Terraform
# Manual backup:
gcloud sql backups create \
  --instance=oracle-samuel-postgres-production

# Restore from backup:
gcloud sql backups restore BACKUP_ID \
  --backup-instance=SOURCE_INSTANCE \
  --backup-instance=TARGET_INSTANCE
```

**AWS RDS**
```bash
# Create snapshot
aws rds create-db-snapshot \
  --db-instance-identifier oracle-samuel-postgres-production \
  --db-snapshot-identifier manual-snapshot-$(date +%Y%m%d)

# Restore from snapshot
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier oracle-restored \
  --db-snapshot-identifier SNAPSHOT_ID
```

### Model & Data Backups
```bash
# GCS
gsutil -m cp -r gs://oracle-models/* ./backup/

# S3
aws s3 sync s3://oracle-samuel-models ./backup/
```

### Disaster Recovery Plan
1. **RTO**: 1 hour (Recovery Time Objective)
2. **RPO**: 15 minutes (Recovery Point Objective)
3. **Steps**:
   - Restore DB from latest snapshot
   - Deploy last known good container version
   - Restore models from object storage
   - Verify all health checks pass
   - Switch DNS to new deployment

---

## 📈 Scaling

### Auto-Scaling Configuration

**GCP Cloud Run**
- Automatically scales 0-10 instances based on load
- Min instances: 2 (always warm)
- Max instances: 10
- Concurrency: 80 requests/instance

**AWS ECS**
```bash
# CPU-based scaling
aws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --scalable-dimension ecs:service:DesiredCount \
  --resource-id service/oracle-samuel-cluster/oracle-backend-service \
  --min-capacity 2 \
  --max-capacity 10
```

**Kubernetes HPA**
```yaml
# Already configured in k8s/backend.yaml
# Scales on CPU (70%) and Memory (80%)
minReplicas: 2
maxReplicas: 10
```

### Manual Scaling
```bash
# GCP
gcloud run services update oracle-backend \
  --min-instances=5 --max-instances=20

# AWS
aws ecs update-service \
  --cluster oracle-samuel-cluster-production \
  --service oracle-backend-service \
  --desired-count 5

# K8s
kubectl scale deployment oracle-backend --replicas=5 -n oracle-samuel
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Service Not Starting
```bash
# Check logs
docker-compose logs backend
kubectl logs -f deployment/oracle-backend -n oracle-samuel
gcloud run services logs read oracle-backend --limit=50

# Common causes:
# - Missing environment variables
# - Database connection failure
# - Insufficient resources
```

#### 2. High Error Rate
```bash
# Check error logs
kubectl logs -f deployment/oracle-backend -n oracle-samuel | grep ERROR

# Check Prometheus metrics
curl http://prometheus:9090/api/v1/query?query=rate(http_requests_total{status=~"5.."}[5m])

# Rollback deployment
kubectl rollout undo deployment/oracle-backend -n oracle-samuel
```

#### 3. Database Connection Issues
```bash
# Test connection
kubectl exec -it deployment/oracle-backend -n oracle-samuel -- \
  psql $DATABASE_URL -c "SELECT 1"

# Check connection pool
SELECT count(*) FROM pg_stat_activity;

# Kill idle connections
SELECT pg_terminate_backend(pid) 
FROM pg_stat_activity 
WHERE state = 'idle' AND state_change < NOW() - INTERVAL '10 minutes';
```

#### 4. Model Performance Degradation
```bash
# Trigger manual retraining
curl -X POST https://api.oracle-samuel.com/api/v1/retrain \
  -H "Authorization: Bearer $API_KEY"

# Check model metrics
curl https://api.oracle-samuel.com/api/v1/models | jq
```

### Debug Mode
```bash
# Enable debug logging
kubectl set env deployment/oracle-backend LOG_LEVEL=DEBUG -n oracle-samuel

# Exec into container
kubectl exec -it deployment/oracle-backend -n oracle-samuel -- /bin/bash

# Check Python environment
python -c "import sys; print(sys.path)"
pip list
```

### Health Checks
```bash
# Backend
curl https://api.oracle-samuel.com/health
curl https://api.oracle-samuel.com/ready

# Frontend
curl https://oracle-samuel.com/_stcore/health

# Database
kubectl exec -it statefulset/postgres -n oracle-samuel -- pg_isready

# Redis
kubectl exec -it deployment/redis -n oracle-samuel -- redis-cli ping
```

---

## 📞 Support

For deployment issues:
- **Email**: devops@dowekanalytics.com
- **Slack**: #oracle-deployment
- **PagerDuty**: P1 incidents auto-escalate
- **Documentation**: https://docs.oracle-samuel.com

---

## 📄 License
© 2025 Dowek Analytics Ltd. All Rights Reserved.


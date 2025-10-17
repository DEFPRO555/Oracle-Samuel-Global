# Oracle Samuel - Part 5: Cloud Deployment & Production Infrastructure
© 2025 Dowek Analytics Ltd.

## 🚀 Overview

Part 5 transforms Oracle Samuel into a **production-ready, enterprise-grade cloud service** with:

- ✅ **Containerized Architecture**: Docker + Kubernetes
- ✅ **Multi-Cloud Support**: GCP (Cloud Run) + AWS (ECS) + Kubernetes
- ✅ **Infrastructure as Code**: Terraform for reproducible deployments
- ✅ **CI/CD Pipeline**: GitHub Actions with automated testing & deployment
- ✅ **Monitoring & Observability**: Prometheus + Grafana + custom dashboards
- ✅ **Production Security**: TLS, WAF, secrets management, RBAC
- ✅ **Auto-Scaling**: Horizontal pod autoscaling & serverless scaling
- ✅ **Premium UI**: $1,000,000 website design with luxury aesthetics

---

## 📁 Project Structure

```
oracle-samuel/
├── backend/
│   ├── main.py                 # FastAPI server with REST endpoints
│   ├── Dockerfile              # Backend container image
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── Dockerfile              # Frontend container image
│   └── requirements-frontend.txt
├── k8s/
│   ├── namespace.yaml          # Kubernetes namespace
│   ├── secrets.yaml            # Secrets (use sealed-secrets in prod)
│   ├── postgres.yaml           # PostgreSQL StatefulSet
│   ├── redis.yaml              # Redis deployment
│   ├── backend.yaml            # Backend API deployment
│   ├── frontend.yaml           # Frontend deployment
│   └── ingress.yaml            # Ingress + TLS configuration
├── helm/
│   └── oracle-samuel/
│       ├── Chart.yaml          # Helm chart metadata
│       └── values.yaml         # Configurable deployment values
├── terraform/
│   ├── gcp/
│   │   └── main.tf             # GCP Cloud Run + Cloud SQL + GCS
│   └── aws/
│       └── main.tf             # AWS ECS + RDS + S3
├── .github/
│   └── workflows/
│       └── ci-cd.yml           # GitHub Actions pipeline
├── monitoring/
│   ├── prometheus.yml          # Prometheus scrape config
│   ├── alerts/
│   │   └── oracle-alerts.yml   # Alert rules
│   └── grafana/
│       └── dashboards/
│           └── oracle-overview.json
├── assets/
│   ├── luxury_theme.css        # Original theme
│   └── premium_enhanced.css    # $1M website design
├── premium_ui_enhancements.py  # Premium UI components
├── docker-compose.yml          # Local development environment
├── env.template                # Environment variables template
├── DEPLOYMENT.md               # Comprehensive deployment guide
├── RUNBOOK.md                  # Operations runbook
├── SECURITY.md                 # Security best practices
└── README_PART5.md             # This file
```

---

## 🎯 Quick Start

### Local Development (Docker Compose)

```bash
# 1. Clone repository
git clone https://github.com/dowek-analytics/oracle-samuel.git
cd oracle-samuel

# 2. Setup environment
cp env.template .env
nano .env  # Fill in your values

# 3. Start services
docker-compose up -d

# 4. Access application
# Frontend: http://localhost:8501
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000 (admin/admin)

# 5. View logs
docker-compose logs -f

# 6. Stop services
docker-compose down
```

---

## ☁️ Cloud Deployment

### Option 1: GCP (Recommended for Fast Deployment)

```bash
# Prerequisites
# - GCP account with billing enabled
# - gcloud CLI installed
# - Terraform installed

# 1. Authenticate
gcloud auth login
gcloud auth application-default login

# 2. Set project
export GCP_PROJECT_ID="your-project-id"
gcloud config set project $GCP_PROJECT_ID

# 3. Enable APIs
gcloud services enable \
  run.googleapis.com \
  sqladmin.googleapis.com \
  storage-api.googleapis.com \
  secretmanager.googleapis.com

# 4. Deploy with Terraform
cd terraform/gcp
terraform init
terraform apply

# 5. Get URLs
terraform output backend_url
terraform output frontend_url
```

**Cost Estimate (GCP)**:
- Cloud Run (backend + frontend): ~$50-150/month (scales to zero)
- Cloud SQL (db.custom-2-7680): ~$200/month
- Cloud Storage: ~$5-20/month
- Redis (5GB HA): ~$100/month
- **Total**: ~$355-470/month (production tier)

### Option 2: AWS (Enterprise Production)

```bash
# Prerequisites
# - AWS account
# - AWS CLI configured
# - Terraform installed

# 1. Create S3 bucket for Terraform state
aws s3 mb s3://oracle-samuel-terraform-state

# 2. Deploy infrastructure
cd terraform/aws
terraform init
terraform apply

# 3. Build and push images
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

docker build -t ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/oracle-backend:latest ./backend
docker push ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/oracle-backend:latest

# 4. Get ALB URL
terraform output alb_dns_name
```

**Cost Estimate (AWS)**:
- ECS Fargate (2 tasks @ 2 vCPU, 4GB): ~$100/month
- RDS PostgreSQL (db.t3.large Multi-AZ): ~$300/month
- ElastiCache Redis (cache.t3.medium): ~$70/month
- ALB: ~$25/month
- S3 + Data Transfer: ~$20/month
- **Total**: ~$515/month

### Option 3: Kubernetes (Any Provider)

```bash
# For GKE
gcloud container clusters create oracle-cluster \
  --region us-central1 \
  --num-nodes 3 \
  --machine-type n1-standard-2

# Get credentials
gcloud container clusters get-credentials oracle-cluster --region us-central1

# Deploy with kubectl
kubectl apply -f k8s/

# OR deploy with Helm
cd helm/oracle-samuel
helm install oracle-samuel . -n oracle-samuel --create-namespace

# Check deployment
kubectl get pods -n oracle-samuel
kubectl get services -n oracle-samuel
kubectl get ingress -n oracle-samuel
```

---

## 🔐 Security Checklist

Before going to production:

- [ ] Rotate all default passwords in `k8s/secrets.yaml`
- [ ] Use secret manager (GCP Secret Manager / AWS Secrets Manager)
- [ ] Enable TLS/SSL certificates (cert-manager or ACM)
- [ ] Configure WAF (Cloud Armor / AWS WAF)
- [ ] Set up rate limiting
- [ ] Enable audit logging
- [ ] Configure network policies
- [ ] Set up backup schedules
- [ ] Configure alerts
- [ ] Review IAM permissions (least privilege)

**See [SECURITY.md](SECURITY.md) for comprehensive security guide.**

---

## 📊 Monitoring & Observability

### Access Dashboards

After deployment:

- **Grafana**: `http://your-domain:3000`
  - Username: `admin`
  - Password: Set in `values.yaml` or `docker-compose.yml`

- **Prometheus**: `http://your-domain:9090`

### Key Metrics

| Metric | Target | Alert Threshold |
|--------|--------|----------------|
| Error Rate | <1% | >5% for 5 minutes |
| P99 Latency | <500ms | >2s for 10 minutes |
| CPU Usage | <70% | >90% for 5 minutes |
| Memory Usage | <80% | >95% for 5 minutes |
| Model MAE | Baseline | >20% degradation |

### Grafana Dashboards

Pre-configured dashboards located in `monitoring/grafana/dashboards/`:
- **oracle-overview.json**: Production overview dashboard
  - Request rate & error rate
  - API latency (p50, p95, p99)
  - Model performance (MAE, R²)
  - Database connections
  - Resource usage

---

## 🔄 CI/CD Pipeline

Automated deployment via GitHub Actions (`.github/workflows/ci-cd.yml`):

### Workflow Stages

1. **Test & Lint**
   - Run pytest
   - Code formatting (black, flake8)
   - Type checking (mypy)
   - Coverage reports

2. **Security Scan**
   - Trivy vulnerability scanning
   - Dependency checking

3. **Build & Push**
   - Build Docker images (multi-arch: amd64, arm64)
   - Push to GitHub Container Registry

4. **Deploy**
   - GCP: Cloud Run deployment
   - AWS: ECS service update
   - K8s: Rolling update

5. **Smoke Tests**
   - Health checks
   - API endpoint tests

6. **Notify**
   - Slack notification
   - Email alerts

### Required GitHub Secrets

```bash
# GCP
GCP_PROJECT_ID
GCP_SA_KEY (service account JSON)
GCP_REGION

# AWS
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION

# Application
DATABASE_URL
REDIS_URL
API_SECRET_KEY
BACKEND_URL
FRONTEND_URL

# Notifications
SLACK_WEBHOOK
SMTP_HOST
SMTP_PORT
SMTP_USER
SMTP_PASSWORD
ALERT_EMAIL
```

---

## 🎨 Premium UI Design

### $1,000,000 Website Features

**Design Philosophy**:
- **Luxury**: Gold accents, premium typography, sophisticated animations
- **Trust**: Financial blue palette, professional imagery
- **Innovation**: 3D effects, glassmorphism, particle animations

**Key Components** (in `premium_ui_enhancements.py`):

```python
from premium_ui_enhancements import *

# Apply all enhancements
apply_premium_enhancements()

# Or use individual components
create_hero_section()
create_stats_section()
create_analytics_showcase()
create_ai_technology_section()
create_property_showcase()

# Premium metric cards
create_premium_metric_card("Accuracy", "99.2%", "🎯", color="gold")

# Premium loading animation
show_premium_loading()
```

**Image Integration**:
The design integrates the professional images you provided:
1. **Financial Analytics Dashboard** - Market intelligence section
2. **Smart City Technology** - Urban real estate insights
3. **AI Partnership** - Technology collaboration showcase
4. **Luxury Properties** - Premium property analysis

**Typography**:
- **Display**: Playfair Display (elegant serif for headings)
- **Body**: Inter (clean sans-serif for readability)
- **Tech**: Space Grotesk (modern for data/metrics)

**Animations**:
- Cinematic hero with particle effects
- Scroll-triggered reveal animations
- 3D card hover effects
- Gradient border animations
- Wave dividers

---

## 📈 Scaling Strategy

### Auto-Scaling Configuration

**GCP Cloud Run**:
- Min instances: 2 (always warm)
- Max instances: 10
- Concurrency: 80 requests/instance
- Scales based on: Request load

**AWS ECS**:
- Min tasks: 2
- Max tasks: 10
- Scaling policy: CPU >70% or Memory >80%

**Kubernetes HPA**:
```yaml
minReplicas: 2
maxReplicas: 10
targetCPUUtilizationPercentage: 70
targetMemoryUtilizationPercentage: 80
```

### Manual Scaling

```bash
# GCP
gcloud run services update oracle-backend --min-instances=5 --max-instances=20

# AWS
aws ecs update-service --desired-count 5 ...

# K8s
kubectl scale deployment oracle-backend --replicas=5 -n oracle-samuel
```

---

## 💾 Backup & Disaster Recovery

### Automated Backups

**Database**:
- **GCP Cloud SQL**: Daily automated backups, 30-day retention, point-in-time recovery
- **AWS RDS**: Daily snapshots, 30-day retention, Multi-AZ for HA

**Object Storage**:
- **GCS**: Versioning enabled, lifecycle policies (Nearline after 90 days)
- **S3**: Versioning enabled, lifecycle policies (Glacier after 90 days)

### Recovery Procedures

**Database Restore**:
```bash
# GCP
gcloud sql backups restore BACKUP_ID --backup-instance=INSTANCE

# AWS
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier oracle-restored \
  --db-snapshot-identifier SNAPSHOT_ID
```

**Model Restore**:
```bash
# GCS
gsutil -m cp -r gs://oracle-models-backup/* gs://oracle-models/

# S3
aws s3 sync s3://oracle-samuel-models-backup/ s3://oracle-samuel-models/
```

**Recovery Targets**:
- **RTO** (Recovery Time Objective): 1 hour
- **RPO** (Recovery Point Objective): 15 minutes

---

## 🛠️ Troubleshooting

### Common Issues

#### 1. Service Won't Start
```bash
# Check logs
kubectl logs -f deployment/oracle-backend -n oracle-samuel
docker-compose logs backend

# Common causes:
# - Missing environment variables
# - Database connection failure
# - Port already in use
```

#### 2. Database Connection Errors
```bash
# Test connection
kubectl exec -it deployment/oracle-backend -n oracle-samuel -- \
  psql $DATABASE_URL -c "SELECT 1"

# Check credentials
echo $DATABASE_URL
```

#### 3. High Error Rate
```bash
# Check error logs
kubectl logs deployment/oracle-backend -n oracle-samuel | grep ERROR

# Rollback if needed
kubectl rollout undo deployment/oracle-backend -n oracle-samuel
```

**See [RUNBOOK.md](RUNBOOK.md) for comprehensive troubleshooting guide.**

---

## 📚 Documentation

- **[DEPLOYMENT.md](DEPLOYMENT.md)**: Step-by-step deployment instructions for all platforms
- **[RUNBOOK.md](RUNBOOK.md)**: Operational procedures, maintenance tasks, incident response
- **[SECURITY.md](SECURITY.md)**: Security best practices, compliance, audit logging

---

## 🚦 Health Checks

### Endpoints

```bash
# Backend health (liveness)
curl https://api.oracle-samuel.com/health

# Backend readiness
curl https://api.oracle-samuel.com/ready

# Frontend health
curl https://oracle-samuel.com/_stcore/health

# Metrics
curl https://api.oracle-samuel.com/metrics
```

### Expected Responses

```json
// /health
{"status": "healthy", "timestamp": "2025-01-14T10:30:00Z"}

// /ready
{"status": "ready", "timestamp": "2025-01-14T10:30:00Z"}
```

---

## 📞 Support

- **DevOps Issues**: devops@dowekanalytics.com
- **Security Incidents**: security@dowekanalytics.com
- **General Support**: support@dowekanalytics.com
- **Documentation**: https://docs.oracle-samuel.com

---

## 📄 License

© 2025 Dowek Analytics Ltd. All Rights Reserved.

**Proprietary Software** - Unauthorized copying, distribution, or modification is strictly prohibited.

---

## 🎉 What's Next?

After completing Part 5, you have:

✅ Production-ready cloud infrastructure  
✅ Automated CI/CD pipeline  
✅ Comprehensive monitoring & alerting  
✅ Enterprise-grade security  
✅ Premium $1,000,000 UI design  
✅ Multi-cloud deployment options  
✅ Complete documentation & runbooks  

**Recommended Next Steps**:

1. **Go Live**: Deploy to production environment
2. **Custom Domain**: Configure DNS with your domain
3. **Load Testing**: Validate auto-scaling under high load
4. **User Onboarding**: Create API documentation for customers
5. **Marketing**: Launch with premium design showcasing AI capabilities

---

**Built with ❤️ by Dowek Analytics Ltd.**


# Oracle Samuel - Operations Runbook
© 2025 Dowek Analytics Ltd.

## 🚨 Emergency Procedures

### P1 - Service Down (Critical)
**Symptoms**: API returning 503, no responses, health checks failing

**Immediate Actions**:
```bash
# 1. Check service status
kubectl get pods -n oracle-samuel
gcloud run services describe oracle-backend --region us-central1

# 2. Check recent deployments
kubectl rollout history deployment/oracle-backend -n oracle-samuel

# 3. Rollback if recent deployment
kubectl rollout undo deployment/oracle-backend -n oracle-samuel

# 4. Check database
kubectl exec -it statefulset/postgres -n oracle-samuel -- pg_isready

# 5. Check logs
kubectl logs -f deployment/oracle-backend -n oracle-samuel --tail=100

# 6. Scale up if resource issue
kubectl scale deployment oracle-backend --replicas=5 -n oracle-samuel
```

**Communication**:
- Post in #oracle-incidents immediately
- Page on-call SRE via PagerDuty
- Update status page: https://status.oracle-samuel.com

---

### P1 - Database Down
**Symptoms**: Connection errors, timeout errors

**Immediate Actions**:
```bash
# 1. Check database status
kubectl get statefulset postgres -n oracle-samuel
gcloud sql instances describe oracle-samuel-postgres-production

# 2. Check connections
kubectl exec -it statefulset/postgres -n oracle-samuel -- \
  psql -U oracle -d oracle_db -c "SELECT count(*) FROM pg_stat_activity;"

# 3. Restart database (last resort)
kubectl rollout restart statefulset/postgres -n oracle-samuel

# 4. Restore from backup if corrupted
gcloud sql backups list --instance=oracle-samuel-postgres-production
gcloud sql backups restore BACKUP_ID --backup-instance=oracle-samuel-postgres-production
```

---

### P1 - Data Breach Suspected
**Immediate Actions**:
1. **Isolate**: Block all public traffic immediately
```bash
kubectl patch ingress oracle-ingress -n oracle-samuel -p '{"spec":{"rules":[]}}'
```

2. **Preserve Evidence**: Take snapshots
```bash
kubectl exec deployment/oracle-backend -n oracle-samuel -- tar czf /tmp/logs.tar.gz /var/log
kubectl cp oracle-samuel/POD:/tmp/logs.tar.gz ./evidence/logs-$(date +%Y%m%d-%H%M%S).tar.gz
```

3. **Notify**:
   - CISO: security@dowekanalytics.com
   - Legal team
   - Affected users (if confirmed)

4. **Investigate**: Review access logs
```bash
kubectl logs deployment/oracle-backend -n oracle-samuel --since=24h | grep -i "unauthorized\|breach\|intrusion"
```

5. **Rotate all credentials**
```bash
# Rotate API keys
gcloud secrets versions add api-secret-key --data-file=<(openssl rand -base64 32)

# Rotate DB password (requires downtime)
```

---

## 🔄 Routine Operations

### Daily Health Check
```bash
#!/bin/bash
# Run every morning at 9 AM

echo "=== Daily Oracle Samuel Health Check ==="

# 1. Service status
kubectl get pods -n oracle-samuel -o wide

# 2. Error rate (last 24h)
curl -s "http://prometheus:9090/api/v1/query?query=rate(http_requests_total{status=~\"5..\"}[24h])" | jq

# 3. Database size
kubectl exec -it statefulset/postgres -n oracle-samuel -- \
  psql -U oracle -d oracle_db -c "SELECT pg_size_pretty(pg_database_size('oracle_db'));"

# 4. Model performance
curl -s https://api.oracle-samuel.com/api/v1/models -H "Authorization: Bearer $API_KEY" | jq

# 5. Storage usage
gsutil du -sh gs://oracle-samuel-models-production/

# 6. Active users (last 24h)
kubectl exec -it statefulset/postgres -n oracle-samuel -- \
  psql -U oracle -d oracle_db -c "SELECT COUNT(DISTINCT user_id) FROM predictions WHERE created_at > NOW() - INTERVAL '24 hours';"
```

---

### Weekly Maintenance

#### 1. Database Vacuum & Analyze
```bash
# Every Sunday 3 AM
kubectl exec -it statefulset/postgres -n oracle-samuel -- \
  psql -U oracle -d oracle_db -c "VACUUM ANALYZE;"
```

#### 2. Clean Old Uploads
```bash
# Delete uploads older than 30 days
gsutil -m rm -r gs://oracle-samuel-uploads-production/**/$(date -d '30 days ago' +%Y-%m-%d)*
```

#### 3. Rotate Logs
```bash
# Archive logs older than 7 days
kubectl logs deployment/oracle-backend -n oracle-samuel --since=168h > logs-archive-$(date +%Y%m%d).log
gsutil cp logs-archive-*.log gs://oracle-samuel-logs/
rm logs-archive-*.log
```

#### 4. Update Dependencies
```bash
# Check for security updates
docker pull python:3.11-slim
docker pull postgres:15-alpine
docker pull redis:7-alpine

# Rebuild with updated base images
docker-compose build --no-cache
```

---

### Monthly Maintenance

#### 1. Model Retraining
```bash
# Trigger full retraining on all historical data
curl -X POST https://api.oracle-samuel.com/api/v1/retrain \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"mode": "full", "notify": true}'
```

#### 2. Performance Review
```bash
# Generate performance report
python scripts/generate_monthly_report.py --month=$(date +%Y-%m)

# Review metrics:
# - Average prediction latency
# - Model MAE/R² trends
# - User satisfaction scores
# - Cost analysis
```

#### 3. Security Audit
```bash
# Run security scan
trivy image ghcr.io/dowek-analytics/oracle-backend:latest
trivy image ghcr.io/dowek-analytics/oracle-frontend:latest

# Check for CVEs
docker scan ghcr.io/dowek-analytics/oracle-backend:latest

# Review access logs
kubectl logs deployment/oracle-backend -n oracle-samuel --since=720h | grep -E "401|403" | wc -l
```

#### 4. Backup Verification
```bash
# Test restore process
# 1. Create test instance
# 2. Restore latest backup
# 3. Verify data integrity
# 4. Document any issues
```

---

## 🔧 Common Tasks

### Deploy New Model Version
```bash
# 1. Upload model to storage
gsutil cp new_model.pkl gs://oracle-samuel-models-production/models/v2.0.0/

# 2. Update model metadata in database
kubectl exec -it statefulset/postgres -n oracle-samuel -- \
  psql -U oracle -d oracle_db -c "INSERT INTO models (version, path, md5_hash, is_active) VALUES ('2.0.0', 'models/v2.0.0/new_model.pkl', 'abc123', true);"

# 3. Deactivate old model
kubectl exec -it statefulset/postgres -n oracle-samuel -- \
  psql -U oracle -d oracle_db -c "UPDATE models SET is_active = false WHERE version = '1.0.0';"

# 4. Restart backend to load new model
kubectl rollout restart deployment/oracle-backend -n oracle-samuel
```

---

### Scale for High Traffic Event
```bash
# Expected high traffic (e.g., product launch)

# 1. Pre-scale services
kubectl scale deployment oracle-backend --replicas=10 -n oracle-samuel
kubectl scale deployment oracle-frontend --replicas=5 -n oracle-samuel

# 2. Increase database connections
kubectl exec -it statefulset/postgres -n oracle-samuel -- \
  psql -U oracle -d oracle_db -c "ALTER SYSTEM SET max_connections = 500;"
kubectl rollout restart statefulset/postgres -n oracle-samuel

# 3. Increase Redis memory
kubectl patch deployment redis -n oracle-samuel -p '{"spec":{"template":{"spec":{"containers":[{"name":"redis","resources":{"limits":{"memory":"2Gi"}}}]}}}}'

# 4. Monitor closely
watch -n 5 'kubectl top pods -n oracle-samuel'

# 5. After event, scale down
kubectl scale deployment oracle-backend --replicas=3 -n oracle-samuel
```

---

### Add New API Key for Customer
```bash
# 1. Generate API key
API_KEY=$(openssl rand -hex 32)

# 2. Store in database
kubectl exec -it statefulset/postgres -n oracle-samuel -- \
  psql -U oracle -d oracle_db -c "INSERT INTO api_keys (key, customer_name, rate_limit, expires_at) VALUES ('$API_KEY', 'Customer Name', 1000, NOW() + INTERVAL '1 year');"

# 3. Send to customer securely (encrypted email)
echo "API Key: $API_KEY" | gpg --encrypt --recipient customer@example.com > api_key.gpg
```

---

### Investigate Slow Queries
```bash
# 1. Enable query logging
kubectl exec -it statefulset/postgres -n oracle-samuel -- \
  psql -U oracle -d oracle_db -c "ALTER SYSTEM SET log_min_duration_statement = 1000;"

# 2. Reload config
kubectl exec -it statefulset/postgres -n oracle-samuel -- \
  psql -U oracle -d oracle_db -c "SELECT pg_reload_conf();"

# 3. Monitor logs
kubectl logs -f statefulset/postgres -n oracle-samuel | grep "duration"

# 4. Analyze slow queries
kubectl exec -it statefulset/postgres -n oracle-samuel -- \
  psql -U oracle -d oracle_db -c "SELECT query, mean_exec_time, calls FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10;"

# 5. Create indexes if needed
kubectl exec -it statefulset/postgres -n oracle-samuel -- \
  psql -U oracle -d oracle_db -c "CREATE INDEX CONCURRENTLY idx_predictions_created_at ON predictions(created_at);"
```

---

### Rotate SSL Certificate
```bash
# For Kubernetes with cert-manager (automatic)
# Cert-manager auto-renews 30 days before expiry

# Manual verification:
kubectl get certificate -n oracle-samuel
kubectl describe certificate oracle-tls-cert -n oracle-samuel

# Force renewal:
kubectl delete secret oracle-tls-cert -n oracle-samuel
# cert-manager will recreate automatically
```

---

## 📊 Performance Tuning

### Backend API Optimization
```bash
# 1. Increase workers (if CPU usage low)
kubectl set env deployment/oracle-backend WORKERS=4 -n oracle-samuel

# 2. Enable connection pooling
kubectl set env deployment/oracle-backend \
  DB_POOL_SIZE=20 \
  DB_MAX_OVERFLOW=10 \
  -n oracle-samuel

# 3. Increase memory if needed
kubectl patch deployment oracle-backend -n oracle-samuel -p '{"spec":{"template":{"spec":{"containers":[{"name":"backend","resources":{"limits":{"memory":"4Gi"}}}]}}}}'
```

### Database Tuning
```bash
# Optimize PostgreSQL settings
kubectl exec -it statefulset/postgres -n oracle-samuel -- \
  psql -U oracle -d oracle_db <<EOF
ALTER SYSTEM SET shared_buffers = '2GB';
ALTER SYSTEM SET effective_cache_size = '6GB';
ALTER SYSTEM SET work_mem = '50MB';
ALTER SYSTEM SET maintenance_work_mem = '512MB';
ALTER SYSTEM SET random_page_cost = 1.1;
EOF

# Restart to apply
kubectl rollout restart statefulset/postgres -n oracle-samuel
```

### Redis Optimization
```bash
# Increase maxmemory
kubectl exec -it deployment/redis -n oracle-samuel -- \
  redis-cli CONFIG SET maxmemory 2gb

# Set eviction policy
kubectl exec -it deployment/redis -n oracle-samuel -- \
  redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

---

## 🔍 Debugging

### Enable Debug Mode
```bash
# Temporarily enable debug logging
kubectl set env deployment/oracle-backend LOG_LEVEL=DEBUG -n oracle-samuel

# Revert after debugging
kubectl set env deployment/oracle-backend LOG_LEVEL=INFO -n oracle-samuel
```

### Capture Request/Response
```bash
# Enable request logging
kubectl set env deployment/oracle-backend ENABLE_REQUEST_LOGGING=true -n oracle-samuel

# View requests
kubectl logs -f deployment/oracle-backend -n oracle-samuel | grep "REQUEST:"
```

### Network Debugging
```bash
# Exec into pod
kubectl exec -it deployment/oracle-backend -n oracle-samuel -- /bin/bash

# Test connectivity
apt-get update && apt-get install -y curl netcat
curl -v http://postgres:5432
nc -zv postgres 5432
nslookup postgres
```

---

## 📋 Checklists

### Pre-Deployment Checklist
- [ ] All tests passing in CI/CD
- [ ] Database migrations tested
- [ ] Secrets updated if needed
- [ ] Backup taken
- [ ] Stakeholders notified
- [ ] Rollback plan prepared
- [ ] Monitoring dashboards open
- [ ] Change ticket created

### Post-Deployment Checklist
- [ ] Health checks passing
- [ ] Error rate < 1%
- [ ] Latency within SLA (<500ms p99)
- [ ] Database connections stable
- [ ] No alerts firing
- [ ] Smoke tests passed
- [ ] Change ticket updated
- [ ] Team notified

### Incident Response Checklist
- [ ] Incident declared in #oracle-incidents
- [ ] Severity assigned (P1-P4)
- [ ] On-call engineer paged (P1/P2)
- [ ] Status page updated
- [ ] Mitigation steps documented
- [ ] Root cause identified
- [ ] Postmortem scheduled (within 48h)
- [ ] Action items created

---

## 📞 Contacts

### On-Call Rotation
- **Primary**: Check PagerDuty schedule
- **Secondary**: Check PagerDuty schedule
- **Escalation**: CTO (cto@dowekanalytics.com)

### Team Contacts
- **DevOps Lead**: devops-lead@dowekanalytics.com
- **Backend Lead**: backend-lead@dowekanalytics.com
- **Data Science Lead**: ds-lead@dowekanalytics.com
- **Security Team**: security@dowekanalytics.com

### Vendor Support
- **GCP Support**: Premium Support Portal
- **AWS Support**: Business Support Portal
- **OpenAI**: platform.openai.com/support

---

## 📚 References

- [Deployment Guide](DEPLOYMENT.md)
- [API Documentation](https://api.oracle-samuel.com/docs)
- [Architecture Diagram](docs/architecture.png)
- [Grafana Dashboards](http://grafana.oracle-samuel.com)
- [Prometheus Alerts](http://prometheus.oracle-samuel.com/alerts)

---

**Last Updated**: 2025-01-14
**Maintained By**: DevOps Team
**Review Cycle**: Monthly


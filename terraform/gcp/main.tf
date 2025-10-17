# © 2025 Dowek Analytics Ltd.
# Oracle Samuel - GCP Infrastructure (Terraform)

terraform {
  required_version = ">= 1.5.0"
  
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
  
  backend "gcs" {
    bucket = "oracle-samuel-terraform-state"
    prefix = "terraform/state"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Variables
variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "us-central1"
}

variable "environment" {
  description = "Environment (dev/staging/prod)"
  type        = string
  default     = "production"
}

variable "db_tier" {
  description = "Cloud SQL instance tier"
  type        = string
  default     = "db-custom-2-7680"
}

# Cloud SQL (PostgreSQL)
resource "google_sql_database_instance" "oracle_postgres" {
  name             = "oracle-samuel-postgres-${var.environment}"
  database_version = "POSTGRES_15"
  region           = var.region
  
  settings {
    tier              = var.db_tier
    availability_type = "REGIONAL"
    disk_size         = 100
    disk_type         = "PD_SSD"
    disk_autoresize   = true
    
    backup_configuration {
      enabled                        = true
      start_time                     = "03:00"
      point_in_time_recovery_enabled = true
      transaction_log_retention_days = 7
      backup_retention_settings {
        retained_backups = 30
      }
    }
    
    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.oracle_vpc.id
      require_ssl     = true
    }
    
    database_flags {
      name  = "max_connections"
      value = "200"
    }
    
    insights_config {
      query_insights_enabled  = true
      query_plans_per_minute  = 5
      query_string_length     = 1024
      record_application_tags = true
    }
  }
  
  deletion_protection = true
  
  depends_on = [google_service_networking_connection.private_vpc_connection]
}

resource "google_sql_database" "oracle_db" {
  name     = "oracle_db"
  instance = google_sql_database_instance.oracle_postgres.name
}

resource "google_sql_user" "oracle_user" {
  name     = "oracle"
  instance = google_sql_database_instance.oracle_postgres.name
  password = var.db_password
}

# VPC Network
resource "google_compute_network" "oracle_vpc" {
  name                    = "oracle-samuel-vpc-${var.environment}"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "oracle_subnet" {
  name          = "oracle-subnet-${var.environment}"
  ip_cidr_range = "10.0.0.0/24"
  region        = var.region
  network       = google_compute_network.oracle_vpc.id
  
  private_ip_google_access = true
}

# Private Service Connection for Cloud SQL
resource "google_compute_global_address" "private_ip_address" {
  name          = "oracle-private-ip"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.oracle_vpc.id
}

resource "google_service_networking_connection" "private_vpc_connection" {
  network                 = google_compute_network.oracle_vpc.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_address.name]
}

# Cloud Storage Bucket (Models)
resource "google_storage_bucket" "models" {
  name          = "${var.project_id}-oracle-models-${var.environment}"
  location      = var.region
  force_destroy = false
  
  uniform_bucket_level_access = true
  
  versioning {
    enabled = true
  }
  
  lifecycle_rule {
    condition {
      age = 90
    }
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }
  
  lifecycle_rule {
    condition {
      age = 365
    }
    action {
      type          = "SetStorageClass"
      storage_class = "COLDLINE"
    }
  }
}

# Cloud Storage Bucket (Uploads)
resource "google_storage_bucket" "uploads" {
  name          = "${var.project_id}-oracle-uploads-${var.environment}"
  location      = var.region
  force_destroy = false
  
  uniform_bucket_level_access = true
  
  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete"
    }
  }
}

# Cloud Memorystore (Redis)
resource "google_redis_instance" "oracle_redis" {
  name           = "oracle-redis-${var.environment}"
  tier           = "STANDARD_HA"
  memory_size_gb = 5
  region         = var.region
  
  authorized_network = google_compute_network.oracle_vpc.id
  connect_mode       = "PRIVATE_SERVICE_ACCESS"
  
  redis_version     = "REDIS_7_0"
  display_name      = "Oracle Samuel Redis"
  
  persistence_config {
    persistence_mode    = "RDB"
    rdb_snapshot_period = "TWELVE_HOURS"
  }
}

# Cloud Run - Backend API
resource "google_cloud_run_service" "backend" {
  name     = "oracle-backend-${var.environment}"
  location = var.region
  
  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/oracle-backend:latest"
        
        ports {
          container_port = 8000
        }
        
        env {
          name  = "DATABASE_URL"
          value = "postgresql://oracle:${var.db_password}@/oracle_db?host=/cloudsql/${google_sql_database_instance.oracle_postgres.connection_name}"
        }
        
        env {
          name  = "REDIS_URL"
          value = "redis://${google_redis_instance.oracle_redis.host}:${google_redis_instance.oracle_redis.port}"
        }
        
        env {
          name = "API_SECRET_KEY"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.api_secret.secret_id
              key  = "latest"
            }
          }
        }
        
        env {
          name = "OPENAI_API_KEY"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.openai_key.secret_id
              key  = "latest"
            }
          }
        }
        
        env {
          name  = "GCS_BUCKET"
          value = google_storage_bucket.models.name
        }
        
        resources {
          limits = {
            cpu    = "2"
            memory = "2Gi"
          }
        }
      }
      
      service_account_name = google_service_account.backend_sa.email
    }
    
    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale"      = "2"
        "autoscaling.knative.dev/maxScale"      = "10"
        "run.googleapis.com/cloudsql-instances" = google_sql_database_instance.oracle_postgres.connection_name
        "run.googleapis.com/vpc-access-connector" = google_vpc_access_connector.connector.id
      }
    }
  }
  
  traffic {
    percent         = 100
    latest_revision = true
  }
}

# Cloud Run - Frontend
resource "google_cloud_run_service" "frontend" {
  name     = "oracle-frontend-${var.environment}"
  location = var.region
  
  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/oracle-frontend:latest"
        
        ports {
          container_port = 8501
        }
        
        env {
          name  = "BACKEND_URL"
          value = google_cloud_run_service.backend.status[0].url
        }
        
        env {
          name  = "DATABASE_URL"
          value = "postgresql://oracle:${var.db_password}@/oracle_db?host=/cloudsql/${google_sql_database_instance.oracle_postgres.connection_name}"
        }
        
        resources {
          limits = {
            cpu    = "1"
            memory = "1Gi"
          }
        }
      }
      
      service_account_name = google_service_account.frontend_sa.email
    }
    
    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale"      = "2"
        "autoscaling.knative.dev/maxScale"      = "5"
        "run.googleapis.com/cloudsql-instances" = google_sql_database_instance.oracle_postgres.connection_name
        "run.googleapis.com/vpc-access-connector" = google_vpc_access_connector.connector.id
      }
    }
  }
  
  traffic {
    percent         = 100
    latest_revision = true
  }
}

# VPC Access Connector
resource "google_vpc_access_connector" "connector" {
  name          = "oracle-vpc-connector"
  region        = var.region
  network       = google_compute_network.oracle_vpc.name
  ip_cidr_range = "10.8.0.0/28"
}

# IAM Service Accounts
resource "google_service_account" "backend_sa" {
  account_id   = "oracle-backend-sa"
  display_name = "Oracle Backend Service Account"
}

resource "google_service_account" "frontend_sa" {
  account_id   = "oracle-frontend-sa"
  display_name = "Oracle Frontend Service Account"
}

# IAM Bindings
resource "google_storage_bucket_iam_member" "backend_storage_admin" {
  bucket = google_storage_bucket.models.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.backend_sa.email}"
}

resource "google_project_iam_member" "backend_cloudsql_client" {
  project = var.project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.backend_sa.email}"
}

# Secret Manager
resource "google_secret_manager_secret" "api_secret" {
  secret_id = "api-secret-key"
  
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret" "openai_key" {
  secret_id = "openai-api-key"
  
  replication {
    automatic = true
  }
}

# Cloud Run IAM (allow public access - add authentication layer if needed)
resource "google_cloud_run_service_iam_member" "backend_public" {
  service  = google_cloud_run_service.backend.name
  location = google_cloud_run_service.backend.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

resource "google_cloud_run_service_iam_member" "frontend_public" {
  service  = google_cloud_run_service.frontend.name
  location = google_cloud_run_service.frontend.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# Cloud Scheduler (for periodic tasks)
resource "google_cloud_scheduler_job" "model_retrain" {
  name        = "oracle-model-retrain"
  description = "Trigger model retraining"
  schedule    = "0 2 * * *" # Daily at 2 AM
  time_zone   = "UTC"
  
  http_target {
    uri         = "${google_cloud_run_service.backend.status[0].url}/api/v1/retrain"
    http_method = "POST"
    
    headers = {
      "Content-Type" = "application/json"
    }
  }
}

# Outputs
output "backend_url" {
  value       = google_cloud_run_service.backend.status[0].url
  description = "Backend API URL"
}

output "frontend_url" {
  value       = google_cloud_run_service.frontend.status[0].url
  description = "Frontend URL"
}

output "postgres_connection" {
  value       = google_sql_database_instance.oracle_postgres.connection_name
  description = "PostgreSQL connection name"
  sensitive   = true
}

output "redis_host" {
  value       = google_redis_instance.oracle_redis.host
  description = "Redis host"
}

output "models_bucket" {
  value       = google_storage_bucket.models.name
  description = "Models storage bucket"
}


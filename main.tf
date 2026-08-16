terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.30.0"
    }
  }
}

variable "project_id" {
  type        = string
  default     = "eheps-ai-platform"
  description = "Google Cloud Project ID for EHEPS"
}

variable "region" {
  type        = string
  default     = "us-central1"
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# 1. Enable Required GCP APIs
resource "google_project_service" "enabled_apis" {
  for_each = toset([
    "aiplatform.googleapis.com",
    "run.googleapis.com",
    "documentai.googleapis.com",
    "bigquery.googleapis.com",
    "secretmanager.googleapis.com",
    "cloudbilling.googleapis.com",
    "billingbudgets.googleapis.com"
  ])
  service            = each.key
  disable_on_destroy = false
}

# 2. Service Account for AI Engine
resource "google_service_account" "ai_engine_sa" {
  account_id   = "eheps-ai-engine-sa"
  display_name = "EHEPS AI Platform Service Account"
}

# 3. IAM Roles (Least Privilege)
resource "google_project_iam_member" "vertex_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.ai_engine_sa.email}"
}

resource "google_project_iam_member" "bq_editor" {
  project = var.project_id
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${google_service_account.ai_engine_sa.email}"
}

# 4. BigQuery Audit & Vector Dataset
resource "google_bigquery_dataset" "audit_dataset" {
  dataset_id                  = "audit_dataset"
  friendly_name               = "EHEPS AI Audit & Intelligence Logs"
  location                    = var.region
  default_table_expiration_ms = 31536000000 # 1 Year Retention
}

resource "google_bigquery_table" "ai_access_logs" {
  dataset_id = google_bigquery_dataset.audit_dataset.dataset_id
  table_id   = "ai_access_logs"

  schema = <<EOF
[
  {"name": "timestamp", "type": "TIMESTAMP", "mode": "REQUIRED"},
  {"name": "source_identity", "type": "STRING", "mode": "NULLABLE"},
  {"name": "action_executed", "type": "STRING", "mode": "REQUIRED"},
  {"name": "input_char_length", "type": "INTEGER", "mode": "NULLABLE"}
]
EOF
}

# 5. Cloud Run Microservice Deployment
resource "google_cloud_run_v2_service" "ai_backend" {
  name     = "eheps-ai-engine"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    service_account = google_service_account.ai_engine_sa.email
    containers {
      image = "gcr.io/${var.project_id}/eheps-ai-engine:latest"
      resources {
        limits = {
          cpu    = "2"
          memory = "2Gi"
        }
      }
      env {
        name  = "GOOGLE_CLOUD_PROJECT"
        value = var.project_id
      }
      env {
        name  = "GOOGLE_CLOUD_REGION"
        value = var.region
      }
    }
    scaling {
      min_instance_count = 0
      max_instance_count = 5 # Prevents budget overruns
    }
  }

  depends_on = [google_project_service.enabled_apis]
}

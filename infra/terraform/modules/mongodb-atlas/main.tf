# MongoDB Atlas module: dedicated M30+ cluster with backup and 2dsphere-ready sharding disabled (single-region for now).
variable "project_name" { type = string }
variable "environment" { type = string }
variable "atlas_org_id" { type = string }

resource "mongodbatlas_project" "main" {
  name   = "${var.project_name}-${var.environment}"
  org_id = var.atlas_org_id
}

resource "mongodbatlas_advanced_cluster" "main" {
  project_id   = mongodbatlas_project.main.id
  name         = "relief-cluster"
  cluster_type = "REPLICASET"

  replication_specs {
    region_configs {
      electable_specs {
        instance_size = "M30"
        node_count    = 3
      }
      provider_name = "AWS"
      region_name   = "US_EAST_1"
      priority      = 7
    }
  }

  backup_enabled = true
}

output "connection_string" {
  value     = mongodbatlas_advanced_cluster.main.connection_strings[0].standard_srv
  sensitive = true
}

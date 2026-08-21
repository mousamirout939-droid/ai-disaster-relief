output "eks_cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

output "mongodb_connection_string" {
  value     = module.mongodb_atlas.connection_string
  sensitive = true
}

output "vpc_id" {
  value = module.vpc.vpc_id
}

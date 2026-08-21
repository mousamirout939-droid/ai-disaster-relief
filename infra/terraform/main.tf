terraform {
  required_version = ">= 1.7"
  required_providers {
    aws    = { source = "hashicorp/aws", version = "~> 5.0" }
    mongodbatlas = { source = "mongodb/mongodbatlas", version = "~> 1.16" }
  }
  backend "s3" {
    bucket = "disaster-relief-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region
}

module "vpc" {
  source     = "./modules/vpc"
  cidr_block = var.vpc_cidr
  env        = var.environment
}

module "eks" {
  source          = "./modules/eks"
  vpc_id          = module.vpc.vpc_id
  private_subnets = module.vpc.private_subnet_ids
  cluster_name    = "${var.project_name}-${var.environment}"
  node_instance_type = var.node_instance_type
}

module "mongodb_atlas" {
  source       = "./modules/mongodb-atlas"
  project_name = var.project_name
  environment  = var.environment
  atlas_org_id = var.atlas_org_id
}

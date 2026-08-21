variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "project_name" {
  type    = string
  default = "disaster-relief-platform"
}

variable "environment" {
  type    = string
  default = "production"
}

variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}

variable "node_instance_type" {
  type    = string
  default = "t3.large"
}

variable "atlas_org_id" {
  type        = string
  description = "MongoDB Atlas organization ID"
}

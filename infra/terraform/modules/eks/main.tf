# EKS module: managed control plane + autoscaling node group for backend workloads.
variable "vpc_id" { type = string }
variable "private_subnets" { type = list(string) }
variable "cluster_name" { type = string }
variable "node_instance_type" { type = string }

resource "aws_eks_cluster" "main" {
  name     = var.cluster_name
  role_arn = aws_iam_role.eks_cluster_role.arn
  vpc_config {
    subnet_ids = var.private_subnets
  }
}

resource "aws_iam_role" "eks_cluster_role" {
  name = "${var.cluster_name}-cluster-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "eks.amazonaws.com" }
    }]
  })
}

resource "aws_eks_node_group" "main" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "${var.cluster_name}-nodes"
  node_role_arn   = aws_iam_role.eks_node_role.arn
  subnet_ids      = var.private_subnets
  instance_types  = [var.node_instance_type]
  scaling_config {
    desired_size = 3
    max_size     = 10
    min_size     = 3
  }
}

resource "aws_iam_role" "eks_node_role" {
  name = "${var.cluster_name}-node-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
    }]
  })
}

output "cluster_endpoint" { value = aws_eks_cluster.main.endpoint }
output "cluster_name" { value = aws_eks_cluster.main.name }

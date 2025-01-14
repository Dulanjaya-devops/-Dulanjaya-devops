# Define AWS region 
provider "aws" {
  region = "ap-south-1"
}


# Calling module from loacal path
module "aws_security_group_sg" {
  source      = "./modules/security Group"  # Adjust the path if necessary
  name        = var.name
  description = var.description
  vpc_id      = var.vpc_id
  cidr_blocks = var.cidr_blocks
  tags        = var.tags
}



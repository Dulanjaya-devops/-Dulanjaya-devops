# Define AWS region 
provider "aws" {
  region = var.region
}


# Calling module from loacal path
module "ec2_instance" {
  source                 = "./modules/ec2-instance"
  ami_id                 = var.ami_id
  instance_type          = var.instance_type
  key_name               = var.key_name
  existing_iam_role_name = var.existing_iam_role_name
  vpc_id                 = var.vpc_id
  subnet_id              = var.subnet_id
  instance_name          = var.instance_name
  user_data              = var.user_data
}



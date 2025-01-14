variable "ami_id" {
  description = "AMI ID for the EC2 instance"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
}

variable "key_name" {
  description = "EC2 Key Pair name"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID for the EC2 instance"
  type        = string
}

variable "subnet_id" {
  description = "Subnet ID for the EC2 instance"
  type        = string
}

variable "instance_name" {
  description = "The name of the EC2 instance"
  type        = string
}

variable "user_data" {
  description = "User data script to configure the EC2 instance"
  type        = string
  default     = "" # Default to empty if not provided
}

variable "existing_iam_role_name" {
  description = "The name of the existing IAM role to attach to the EC2 instance"
  type        = string
}
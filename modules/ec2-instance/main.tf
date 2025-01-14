provider "aws" {
  region = "ap-south-1" # Specify your desired region
}

resource "aws_instance" "instance" {
  ami                         = var.ami_id
  instance_type               = var.instance_type
  key_name                    = var.key_name
  subnet_id                   = var.subnet_id
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.Jenkins.id]
  iam_instance_profile        = var.existing_iam_role_name
  user_data                   = var.user_data
  tags = {
    Name = var.instance_name
  }
}


resource "aws_security_group" "Jenkins" {
  name        = "Jenkins-sg"
  description = "Jenkins security group"
  vpc_id      = "vpc-038654ba754d82418" # Replace with your VPC ID

  # Ingress rules
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Allow SSH access from anywhere
  }

  ingress {
    from_port   = 0
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Allow HTTP access from anywhere
  }

  # Egress rules (optional, by default all outbound traffic is allowed)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1" # Allow all outbound traffic
    cidr_blocks = ["0.0.0.0/0"]
  }
}


variable "region" {
  description = "AWS Region"
  type        = string
  default     = "ap-south-1"
}

variable "ami_id" {
  description = "Ubuntu 24.04 AMI ID for Mumbai"
  type        = string
  default     = "ami-05d2d839d4f73aafb"
}

variable "instance_type" {
  description = "EC2 Instance Size"
  type        = string
  default     = "t2.micro"
}

variable "key_name" {
  description = "Name of the EC2 Key Pair (without .pem)"
  type        = string
  default     = "terra-server-key"
}
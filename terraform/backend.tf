terraform {
  backend "s3" {
    bucket         = "soumi-terraform-state-bucket"
    key            = "devops-project/terraform.tfstate"
    region         = "ap-south-1"
    encrypt        = true
    dynamodb_table = "terraform-lock"
  }
}
variable "db_password" {
  description = "RDS root password"
  type        = string
  default     = "password123"
}

variable "db_username" {
  description = "RDS root username"
  type        = string
  default     = "admin"
}
output "server_public_ip" {
  description = "Public IP address of the Flask Server"
  value       = aws_instance.flask_server.public_ip
}

output "vpc_id" {
  description = "ID of the project VPC"
  value       = aws_vpc.main.id
}
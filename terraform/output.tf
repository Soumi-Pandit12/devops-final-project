output "server_public_ip" {
  value = aws_instance.flask_server.public_ip
}

output "rds_endpoint" {
  value = aws_db_instance.mysql.endpoint
}
# 1. VPC 
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  tags = { Name = "devops-final-vpc" }
}

# 2. Public Subnet
resource "aws_subnet" "public_sub" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "ap-south-1a" 
  tags = { Name = "public-subnet" }
}

# 3. Internet Gateway
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id
  tags = { Name = "main-igw" }
}

# 4. Route Table
resource "aws_route_table" "rt" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
}

# 5. Route Table Association
resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.public_sub.id
  route_table_id = aws_route_table.rt.id
}

# 6. Security Group (The Firewall)
resource "aws_security_group" "web_sg" {
  name   = "allow_web_traffic" # Kept the original name to avoid the "Still destroying" error
  vpc_id = aws_vpc.main.id

  ingress {
    description = "SSH Access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Flask App Traffic"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Jenkins UI"
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# 7. EC2 Instance
resource "aws_instance" "flask_server" {
  ami           = var.ami_id
  instance_type = var.instance_type
  
  subnet_id              = aws_subnet.public_sub.id
  vpc_security_group_ids = [aws_security_group.web_sg.id]
  key_name               = var.key_name

  user_data = <<-EOF
              #!/bin/bash
              sudo apt-get update -y
              sudo apt-get install -y docker.io
              sudo systemctl start docker
              sudo systemctl enable docker
              sudo usermod -aG docker ubuntu
              EOF

  tags = { Name = "DevOps-Final-Server" }
}
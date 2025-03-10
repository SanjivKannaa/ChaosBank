provider "aws" {
  region = "ap-south-1"
}

# VPC
resource "aws_vpc" "reliabank_vpc" {
  cidr_block = "10.0.0.0/16"
  enable_dns_support = true
  enable_dns_hostnames = true
  tags = { Name = "ReliabankVPC" }
}

# Subnets
resource "aws_subnet" "subnet_apsouth1" {
  vpc_id = aws_vpc.reliabank_vpc.id
  cidr_block = "10.0.1.0/24"
  availability_zone = "ap-south-1a"
  map_public_ip_on_launch = true
  tags = { Name = "SubnetAPSouth1" }
}

resource "aws_subnet" "subnet_apsouth2" {
  vpc_id = aws_vpc.reliabank_vpc.id
  cidr_block = "10.0.2.0/24"
  availability_zone = "ap-south-1b"
  map_public_ip_on_launch = true
  tags = { Name = "SubnetAPSouth2" }
}

# Internet Gateway
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.reliabank_vpc.id
  tags = { Name = "ReliabankIGW" }
}

# Route Table
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.reliabank_vpc.id
  tags = { Name = "PublicRouteTable" }
}

resource "aws_route" "default_route" {
  route_table_id = aws_route_table.public_rt.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id = aws_internet_gateway.gw.id
}

resource "aws_route_table_association" "subnet1_assoc" {
  subnet_id = aws_subnet.subnet_apsouth1.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table_association" "subnet2_assoc" {
  subnet_id = aws_subnet.subnet_apsouth2.id
  route_table_id = aws_route_table.public_rt.id
}

# Security Groups
resource "aws_security_group" "nginx_sg" {
  vpc_id = aws_vpc.reliabank_vpc.id
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = { Name = "NginxSG" }
}

# Auto Scaling for Nginx
resource "aws_launch_template" "nginx_lt" {
  name_prefix   = "nginx-lt"
  image_id      = "ami-12345678"
  instance_type = "t2.micro"
  security_group_names = [aws_security_group.nginx_sg.name]
  
  tag_specifications {
    resource_type = "instance"
    tags = { Name = "NginxInstance" }
  }
}

resource "aws_autoscaling_group" "nginx_asg" {
  desired_capacity     = 1
  max_size            = 1
  min_size            = 1
  vpc_zone_identifier = [aws_subnet.subnet_apsouth1.id]
  launch_template {
    id      = aws_launch_template.nginx_lt.id
    version = "$Latest"
  }
}

# Elastic IP for Nginx
resource "aws_eip" "nginx_eip" {
  instance = aws_autoscaling_group.nginx_asg.id
  tags = { Name = "NginxElasticIP" }
}

# Backend ASG
resource "aws_autoscaling_group" "backend_asg_1" {
  desired_capacity     = 1
  max_size            = 5
  min_size            = 2
  vpc_zone_identifier = [aws_subnet.subnet_apsouth1.id]
  launch_template {
    id      = aws_launch_template.nginx_lt.id
    version = "$Latest"
  }
}

resource "aws_autoscaling_group" "backend_asg_2" {
  desired_capacity     = 1
  max_size            = 5
  min_size            = 2
  vpc_zone_identifier = [aws_subnet.subnet_apsouth2.id]
  launch_template {
    id      = aws_launch_template.nginx_lt.id
    version = "$Latest"
  }
}

# Database EC2 Instances
resource "aws_instance" "mysql_master" {
  ami           = "ami-12345678"
  instance_type = "t2.medium"
  subnet_id     = aws_subnet.subnet_apsouth1.id
  tags = { Name = "MySQL-Master" }
}

resource "aws_instance" "mysql_slave1" {
  ami           = "ami-12345678"
  instance_type = "t2.medium"
  subnet_id     = aws_subnet.subnet_apsouth1.id
  tags = { Name = "MySQL-Slave1" }
}

resource "aws_instance" "mysql_slave2" {
  ami           = "ami-12345678"
  instance_type = "t2.medium"
  subnet_id     = aws_subnet.subnet_apsouth1.id
  tags = { Name = "MySQL-Slave2" }
}

resource "aws_instance" "mysql_slave3" {
  ami           = "ami-12345678"
  instance_type = "t2.medium"
  subnet_id     = aws_subnet.subnet_apsouth2.id
  tags = { Name = "MySQL-Slave3" }
}

resource "aws_instance" "mysql_slave4" {
  ami           = "ami-12345678"
  instance_type = "t2.medium"
  subnet_id     = aws_subnet.subnet_apsouth2.id
  tags = { Name = "MySQL-Slave4" }
}

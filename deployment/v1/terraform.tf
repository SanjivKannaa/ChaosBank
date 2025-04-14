# Terraform script to deploy Monolithic Hosting on a Single EC2 Instance

provider "aws" {
  region = "ap-south-1" # Change as needed
}

resource "aws_vpc" "monolith_vpc" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_internet_gateway" "monolith_igw" {
  vpc_id = aws_vpc.monolith_vpc.id
}

resource "aws_subnet" "monolith_subnet" {
  vpc_id                  = aws_vpc.monolith_vpc.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
}

resource "aws_route_table" "monolith_rt" {
  vpc_id = aws_vpc.monolith_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.monolith_igw.id
  }
}

resource "aws_route_table_association" "monolith_rta" {
  subnet_id      = aws_subnet.monolith_subnet.id
  route_table_id = aws_route_table.monolith_rt.id
}

resource "aws_security_group" "monolith_sg" {
  vpc_id = aws_vpc.monolith_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

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
    from_port   = 61208
    to_port     = 61208
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

resource "aws_instance" "monolith_ec2" {
  ami           = "ami-03c68e52484d7488f"
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.monolith_subnet.id
  vpc_security_group_ids = [aws_security_group.monolith_sg.id]
  key_name      = "aws-default"
  associate_public_ip_address = true

  tags = {
    Name = "Monolithic-Server"
  }

  user_data = <<-EOF
    #!/bin/bash
    sudo apt update -y
    sudo apt install -y ansible git

    # Run ansible-pull with the correct playbook path
    /usr/bin/ansible-pull -U https://github.com/sanjivkannaa/chaosbank.git -i localhost deployment/v1/playbook.yml \
    -o | tee -a /var/log/ansible-pull.log

    # Optional: Set up a cron job for periodic updates (every 5 minutes)
    echo "*/5 * * * * root /usr/bin/ansible-pull -U https://github.com/sanjivkannaa/chaosbank.git -i localhost deployment/v1/playbook.yml -o >> /var/log/ansible-pull.log 2>&1" | sudo tee -a /etc/crontab
  EOF
}

output "instance_ip" {
  value = aws_instance.monolith_ec2.public_ip
}

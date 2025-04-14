provider "aws" {
  region = "ap-south-1"
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  enable_dns_support = true
  enable_dns_hostnames = true
  tags = {
    Name = "Chaos Testing in Sandbox"
  }
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
}

resource "aws_route" "internet_access" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.gw.id
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "ap-south-1a"
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

resource "aws_security_group" "LB_sg" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
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

resource "aws_security_group" "BE_sg" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["10.0.1.0/24"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
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

resource "aws_security_group" "FE_sg" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["10.0.1.0/24"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
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

resource "aws_security_group" "DB_sg" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["10.0.1.0/24"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
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

# Create IAM Role for Load Balancer
resource "aws_iam_role" "lb_role" {
  name = "lb-instance-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = { Service = "ec2.amazonaws.com" }
    }]
  })
}

# Attach AmazonEC2ReadOnlyAccess Policy
resource "aws_iam_policy_attachment" "lb_readonly_access" {
  name       = "lb-readonly-access"
  roles      = [aws_iam_role.lb_role.name]
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess"
}

# Create IAM Instance Profile for Load Balancer
resource "aws_iam_instance_profile" "lb_instance_profile" {
  name = "lb-instance-profile"
  role = aws_iam_role.lb_role.name
}

resource "aws_instance" "LB_ec2" {
  ami                    = "ami-03c68e52484d7488f"
  instance_type          = "t3.micro"
  key_name               = "aws-default"
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.LB_sg.id]
  associate_public_ip_address = true
  iam_instance_profile = aws_iam_instance_profile.lb_instance_profile.name
  
  tags = {
    Name = "Load Balancer"
  }
  user_data = <<-EOF
    #!/bin/bash
    sudo apt update -y
    sudo apt install -y ansible git

    # Run ansible-pull with the correct playbook path
    /usr/bin/ansible-pull -U https://github.com/sanjivkannaa/chaosbank.git -i localhost deployment/v2/playbook.loadbalancer.yml \
    -o | tee -a /var/log/ansible-pull.log

    # Optional: Set up a cron job for periodic updates (every 5 minutes)
    echo "*/5 * * * * root /usr/bin/ansible-pull -U https://github.com/sanjivkannaa/chaosbank.git -i localhost deployment/v2/playbook.loadbalancer.yml -o >> /var/log/ansible-pull.log 2>&1" | sudo tee -a /etc/crontab
  EOF
}

resource "aws_instance" "DB_ec2" {
  ami                    = "ami-03c68e52484d7488f"
  instance_type          = "t3.micro"
  key_name               = "aws-default"
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.DB_sg.id]
  associate_public_ip_address = true
  
  tags = {
    Name = "Database"
  }
  user_data = <<-EOF
    #!/bin/bash
    sudo apt update -y
    sudo apt install -y ansible git

    # Run ansible-pull with the correct playbook path
    /usr/bin/ansible-pull -U https://github.com/sanjivkannaa/chaosbank.git -i localhost deployment/v2/playbook.database.yml \
    -o | tee -a /var/log/ansible-pull.log

    # Optional: Set up a cron job for periodic updates (every 5 minutes)
    echo "*/5 * * * * root /usr/bin/ansible-pull -U https://github.com/sanjivkannaa/chaosbank.git -i localhost deployment/v2/playbook.database.yml -o >> /var/log/ansible-pull.log 2>&1" | sudo tee -a /etc/crontab
  EOF
}

# Create an SSM Parameter to store the private IP of the DB
resource "aws_ssm_parameter" "db_private_ip" {
  name  = "/chaosbank/db_private_ip"
  type  = "String"
  value = aws_instance.DB_ec2.private_ip
}

# Create an IAM Policy to allow read access to this specific SSM Parameter
resource "aws_iam_policy" "ssm_read_policy" {
  name        = "ChaosBankReadSSMPolicy"
  description = "Allow read access to specific SSM parameter"
  policy      = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = "ssm:GetParameter"
        Resource = aws_ssm_parameter.db_private_ip.arn
      }
    ]
  })
}

# Create an IAM Role for Backend ASG
resource "aws_iam_role" "backend_role" {
  name = "BackendSSMRole"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# Attach the IAM Policy to the IAM Role (Only for Backend ASG)
resource "aws_iam_policy_attachment" "ssm_read_attachment" {
  name       = "ssm-read-attachment"
  policy_arn = aws_iam_policy.ssm_read_policy.arn
  roles      = [aws_iam_role.backend_role.name]
}

# Create an IAM Instance Profile (Only for Backend ASG)
resource "aws_iam_instance_profile" "backend_instance_profile" {
  name = "BackendSSMInstanceProfile"
  role = aws_iam_role.backend_role.name
}

resource "aws_launch_configuration" "BE_lc" {
  name_prefix          = "backend-lc-"
  image_id            = "ami-03c68e52484d7488f"
  instance_type       = "t3.micro"
  key_name            = "aws-default"
  security_groups     = [aws_security_group.BE_sg.id]
  associate_public_ip_address = true
  iam_instance_profile = aws_iam_instance_profile.backend_instance_profile.name
  user_data = <<-EOF
    #!/bin/bash
    sudo apt update -y
    sudo apt install -y ansible git

    # Run ansible-pull with the correct playbook path
    /usr/bin/ansible-pull -U https://github.com/sanjivkannaa/chaosbank.git -i localhost deployment/v2/playbook.backend.yml \
    -o | tee -a /var/log/ansible-pull.log

    # Optional: Set up a cron job for periodic updates (every 5 minutes)
    echo "*/5 * * * * root /usr/bin/ansible-pull -U https://github.com/sanjivkannaa/chaosbank.git -i localhost deployment/v2/playbook.backend.yml -o >> /var/log/ansible-pull.log 2>&1" | sudo tee -a /etc/crontab
  EOF
}

resource "aws_launch_configuration" "FE_lc" {
  name_prefix          = "frontend-lc-"
  image_id            = "ami-03c68e52484d7488f"
  instance_type       = "t3.micro"
  key_name            = "aws-default"
  security_groups     = [aws_security_group.FE_sg.id]
  associate_public_ip_address = true
  user_data = <<-EOF
    #!/bin/bash
    sudo apt update -y
    sudo apt install -y ansible git

    # Run ansible-pull with the correct playbook path
    /usr/bin/ansible-pull -U https://github.com/sanjivkannaa/chaosbank.git -i localhost deployment/v2/playbook.frontend.yml \
    -o | tee -a /var/log/ansible-pull.log

    # Optional: Set up a cron job for periodic updates (every 5 minutes)
    echo "*/5 * * * * root /usr/bin/ansible-pull -U https://github.com/sanjivkannaa/chaosbank.git -i localhost deployment/v2/playbook.frontend.yml -o >> /var/log/ansible-pull.log 2>&1" | sudo tee -a /etc/crontab
  EOF
}

resource "aws_autoscaling_group" "Backend_asg" {
  desired_capacity     = 2
  min_size            = 1
  max_size            = 4
  vpc_zone_identifier = [aws_subnet.public.id]

  launch_configuration = aws_launch_configuration.BE_lc.id

  tag {
    key                 = "Name"
    value               = "Backend"
    propagate_at_launch = true
  }
}

resource "aws_autoscaling_group" "Frontend_asg" {
  desired_capacity     = 2
  min_size            = 1
  max_size            = 4
  vpc_zone_identifier = [aws_subnet.public.id]

  launch_configuration = aws_launch_configuration.FE_lc.id

  tag {
    key                 = "Name"
    value               = "Frontend"
    propagate_at_launch = true
  }
}

output "load_balancer_public_ip" {
  description = "The public IP of the Load Balancer EC2 instance"
  value       = aws_instance.LB_ec2.public_ip
}

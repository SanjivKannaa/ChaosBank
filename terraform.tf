terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

// Configure the AWS Provider
provider "aws" {
  region = "ap-south-1"
}

// ssh key pair
resource "aws_key_pair" "aws-test" {
  key_name   = "aws-test"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCT37uHN7IKLovo9vGEzf5L0yJQobudWVTunGxsHT47GkUUQJg03a3w+BTJJwXCNuO25eFNpOsYdaf0xamryT54jnf+hnOpiPZC0NSTlR1/lJ1ex6GrZiF0D8ml9JTENy9PSSQRRqWYboEGMdeAeunV5eg3CUUqpkWl0GxdwOxN+qlXIcxYkTXHEEtq8w5bI0kXh5zOKkXYxi9vw1w9+twgFQkjrEgmzJwO9cs7FXlQdJ0w8DdMcdzOWyhJvqBUIb4Zjatlj//t/VUw0EgZllnNTx6NUrYbKvcCdzFP6tfmd5uwj8ZuwQJNToqtW03Z/b2AzLll2yMCtAVrhOufesuN aws_test"
}


// Create a EC2 (loadbalancer+backup)
resource "aws_instance" "chaosbank_load_balancer" {
  ami              = "ami-0212a8e7fb09718ec"
  instance_type    = "t3.small"
  vpc_security_group_ids  = ["sg-0c8d056e2c42f3a23"]
  key_name         = aws_key_pair.aws-test.key_name
  tags = {
    Name = "chaosbank_load_balancer"
  }
}

// allocating the elestic ip (hardcoded) to the new ec2 instance 0
resource "aws_eip_association" "eip_assoc0" {
  instance_id = aws_instance.chaosbank_load_balancer.id
  allocation_id = "eipalloc-02ae67e855f07f85d"
}





// Create a EC2 (1)
resource "aws_instance" "chaosbank1" {
  ami              = "ami-0212a8e7fb09718ec"
  instance_type    = "t3.medium"
  vpc_security_group_ids  = ["sg-0c8d056e2c42f3a23"]
  key_name         = aws_key_pair.aws-test.key_name
  tags = {
    Name = "chaosbank1"
  }
}

// allocating the elestic ip (hardcoded) to the new ec2 instance 1
resource "aws_eip_association" "eip_assoc1" {
  instance_id = aws_instance.chaosbank1.id
  allocation_id = "eipalloc-0668e7746e2d7d2ca"
}





// Create a EC2 (2)
resource "aws_instance" "chaosbank2" {
  ami              = "ami-0212a8e7fb09718ec"
  instance_type    = "t3.medium"
  vpc_security_group_ids  = ["sg-0c8d056e2c42f3a23"]
  key_name         = aws_key_pair.aws-test.key_name
  tags = {
    Name = "chaosbank2"
  }
}

// allocating the elestic ip (hardcoded) to the new ec2 instance 2
resource "aws_eip_association" "eip_assoc2" {
  instance_id = aws_instance.chaosbank2.id
  allocation_id = "eipalloc-0e0fc222b9d330d04"
}
# ReliaBank

## Tech-Stack
Flask (python) <br>
JWT <br>
bcrypt <br>
Docker <br>
MySQL <br>
Terraform (AWS) <br>
Ansible <br>
Nginx <br>


## Contributors
Sanjiv Kannaa J <br>


## How To Run (local)

```
$ git clone https://github.com/sanjivkannaa/reliabank.git
$ cd reliabank
$ cp .env.example .env
```

setup .env

```
$ docker-compose up -d
```

now visit localhost:5000


## How To Run (AWS using terraform)

Make sure to have terraform and aws-cli installed and setup (aws creds must  be stored in the default location. ref: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html)

1. setup the EC2 instances

```
$ terraform init
$ terraform apply
```

2. setup ansible inventory (and do dns mapping)

```
$ ansible-playbook -i inventory.ini playbook.yml
```

now visit the domain

## To destroy AWS infrastructure
```
$ terraform destroy
```
# ReliaBank

## Tech-Stack

### Frontend

React JS <br>

### Backend

Flask (python) <br>
JWT <br>
bcrypt <br>

### Database

MySQL (with master-slave architecture) <br>

### DevOps

Docker <br>
Terraform (AWS) <br>
Ansible <br>

### Cloud

- AWS

## Contributors

Sanjiv Kannaa J <br>

## How To Run (local)

For running each microservice seperately, refer README.md inside each folder

```
$ git clone https://github.com/sanjivkannaa/chaosbank.git
$ cd chaosbank
$ cp ./backend/.env.example ./backend/.env
$ cp ./frontend/.env.example ./frontend/.env
```

setup .env [make sure to set strong username and P4$$w0=D]

```
$ docker-compose up -d
```

now visit localhost:3000

## How To Deploy to AWS (using terraform)

Make sure to have terraform and aws-cli installed and setup (aws creds must be stored in the default location. ref: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html)

1. setup the compute instances

```
$ terraform init
$ terraform apply -var mysql_username="your_username" -var mysql_password="your_password"
```

2. terraform output will contain the DB endpoint, update it in the .env file

3. setup ansible inventory (and do dns mapping)

```
$ ansible-playbook -i inventory.ini playbook.yml
```

now visit the chaosbank.magickite.tech (or the domain you have set)

## To destroy AWS infrastructure

```
$ terraform destroy
```

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

Refer to IaC/ directory

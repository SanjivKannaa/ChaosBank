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

### set up mySQL master-slave architecture

1. shell into master

```
docker exec -it reliabank-mysql mysql -u root -p
```

2. copy paste the contents of backend/mysql_files/master.sql into the terminal

```
GRANT REPLICATION SLAVE ON *.* TO 'reliabank'@'%';
FLUSH PRIVILEGES;
FLUSH TABLES WITH READ LOCK;
SHOW MASTER STATUS;
UNLOCK TABLES;
```

3. copy "SOURCE_LOG_FILE" and "SOURCE_LOG_POS" displayed in the output of [2]
4. shell into slave (do for each slave)

```
docker exec -it reliabank-mysql-slave<number> mysql -u root -p
```

5. copy paste the contents of backend/mysql_files/slave.sql into the terminal (dont forget to replace "SOURCE_LOG_FILE" and "SOURCE_LOG_POS")
   '''
   CHANGE REPLICATION SOURCE TO
   SOURCE_HOST='mysql',
   SOURCE_USER='reliabank',
   SOURCE_PASSWORD='reliabank',
   SOURCE_LOG_FILE='binlog.000002', // update this
   SOURCE_LOG_POS=1684; // update this
   GET_MASTER_PUBLIC_KEY=1;
   START REPLICA;
   SHOW REPLICA STATUS;
   '''

now visit localhost:3000

## How To Deploy to AWS (using terraform)

Refer to IaC/ directory

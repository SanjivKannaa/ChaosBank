# ReliaBank - Backend

## How To Run (local)

### both backend and DB service

```
$ git clone https://github.com/sanjivkannaa/chaosbank.git
$ cd chaosbank/backend
$ cp .env.example .env
```

setup .env [make sure to set strong username and P4$$w0=D]

```
$ docker-compose -f docker-compose.backend_with_db.yml up -d
```

now visit localhost:3000

### only DB service

```
$ git clone https://github.com/sanjivkannaa/chaosbank.git
$ cd chaosbank/backend
$ cp .env.example .env
```

setup .env [make sure to set strong username and P4$$w0=D]

```
$ docker-compose -f docker-compose.db.yml up -d
```

### only backend service

```
$ git clone https://github.com/sanjivkannaa/chaosbank.git
$ cd chaosbank/backend
$ cp .env.example .env
```

setup .env [make sure to set strong username and P4$$w0=D]

```
$ docker-compose -f docker-compose.backend.yml up -d
```

now visit localhost:3000

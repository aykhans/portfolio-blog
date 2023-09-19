# Run for development

### 1. Rename and fill env files
    /src/app/app.env.example -> /src/app/app.env
    /src/mongodb/mongodb.env.example -> /src/mongodb/mongodb.env
    /src/postgres/postgres.env.example -> /src/postgres/postgres.env

### 2. Run all services with docker compose
    docker compose -f docker-compose-dev.yml --build -d

### Create user
    docker exec -it {container_name} poetry run python3 commands/create_user.py
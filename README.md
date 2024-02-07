# Run for development

### 1. Rename and fill env files
    /config/app/app.env.example -> /src/app/app.env
    /config/mongodb/mongodb.env.example -> /src/mongodb/mongodb.env
    /config/postgres/postgres.env.example -> /src/postgres/postgres.env

### 2. Run all services with docker compose
    docker compose up --build -d

### Create user
    docker exec -it {container_name} poetry run python3 commands/create_user.py

# Wallet API

An API application for managing digital wallets. It allows users to create
accounts and wallets, retrieve wallet information, and perform deposit and
withdrawal operations.

## Technologies

- Python 3.14
- FastAPI
- PostgreSQL
- SQLAlchemy and Alembic
- Docker and Docker Compose

## Running on another device

Git and Docker Desktop (or Docker Engine with the Docker Compose plugin) are
required. Python and PostgreSQL do not need to be installed separately.

1. Clone the repository and open the project directory:

   ```bash
   git clone https://github.com/zakhar-vodolazsky/custom_wallet_api.git
   cd custom_wallet_api
   ```

2. Create a local environment file.

   Windows PowerShell:

   ```powershell
   Copy-Item .env.example .env
   ```

   Linux or macOS:

   ```bash
   cp .env.example .env
   ```

   If necessary, update the database name, user, password, and application port
   in `.env`. Do not commit the `.env` file to Git.

3. Build and start the entire system with one command:

   ```bash
   docker compose up --build
   ```

Docker Compose starts PostgreSQL, waits until it is ready, applies the Alembic
migrations, and then starts the application.

The following endpoints are available after startup:

- API: <http://localhost:8000>
- Swagger UI: <http://localhost:8000/docs>
- health check: <http://localhost:8000/ping>

Run the system in the background:

```bash
docker compose up --build -d
```

Check the container status:

```bash
docker compose ps --all
```

Stop the application while preserving the PostgreSQL data:

```bash
docker compose down
```

The database is stored in a Docker volume and remains available after the
containers are stopped normally.

## License

This project is source-available. You may clone and run an unmodified copy
locally for personal, educational, or evaluation purposes. Modification,
redistribution, commercial use, and public deployment are prohibited. See the
[LICENSE](./LICENSE) file for the complete terms.

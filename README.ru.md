# Wallet API

API-приложение для работы с электронными кошельками. Оно позволяет создавать
пользователей и кошельки, получать информацию о кошельках и выполнять операции
пополнения и списания средств.

## Технологии

- Python 3.14
- FastAPI
- PostgreSQL
- SQLAlchemy и Alembic
- Docker и Docker Compose

## Запуск на другом устройстве

Для запуска необходимы Git и Docker Desktop (либо Docker Engine с плагином
Docker Compose). Устанавливать Python и PostgreSQL отдельно не нужно.

1. Клонируйте репозиторий и перейдите в папку проекта:

   ```bash
   git clone https://github.com/zakhar-vodolazsky/custom_wallet_api.git
   cd custom_wallet_api
   ```

2. Создайте локальный файл с переменными окружения.

   Windows PowerShell:

   ```powershell
   Copy-Item .env.example .env
   ```

   Linux или macOS:

   ```bash
   cp .env.example .env
   ```

   При необходимости измените в `.env` имя базы данных, пользователя, пароль и
   внешний порт приложения. Файл `.env` нельзя добавлять в Git.

3. Соберите и запустите всю систему одной командой:

   ```bash
   docker compose up --build
   ```

Docker Compose автоматически запустит PostgreSQL, дождётся его готовности,
применит миграции Alembic и запустит приложение.

После запуска доступны:

- API: <http://localhost:8000>
- Swagger UI: <http://localhost:8000/docs>
- проверка состояния: <http://localhost:8000/ping>

Для запуска в фоновом режиме:

```bash
docker compose up --build -d
```

Проверить состояние контейнеров:

```bash
docker compose ps --all
```

Остановить приложение с сохранением данных PostgreSQL:

```bash
docker compose down
```

Данные базы хранятся в Docker volume и сохраняются после обычной остановки
контейнеров.

## Лицензия

Исходный код проекта доступен для просмотра. Разрешается клонировать и запускать
неизменённую копию локально в личных, учебных целях или для оценки проекта.
Изменение, распространение, коммерческое использование и публичное развёртывание
запрещены. Полные условия приведены в файле [LICENSE](./LICENSE).

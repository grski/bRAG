import pugsql

from settings import settings

DATABASE_URI = f"postgresql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_ENDPOINT}:{settings.DB_PORT}/{settings.DB_NAME}"
ASYNC_DATABASE_URI: str = f"postgresql+asyncpg://{DATABASE_URI}"
# DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres?sslmode=disable"
# DATABASE_URL="postgresql://application:secret_pass@0.0.0.0:5432/application?sslmode=disable"

user_queries = pugsql.module("db/queries/users")
query_connection = user_queries.connect(settings.DATABASE_URL)

chat_queries = pugsql.module("db/queries/messages")
chat_query_connection = chat_queries.connect(settings.DATABASE_URL)

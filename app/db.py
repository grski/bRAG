import pugsql

from settings import settings

messages_queries = pugsql.module("./db/queries/messages")
messages_queries.connect(settings.DATABASE_URL)

import pugsql

from settings import settings

messages_queries = pugsql.module("./db/queries/messages")
messages_queries.connect(settings.DATABASE_URL)

chats_queries = pugsql.module("./db/queries/chats")
chats_queries.connect(settings.DATABASE_URL)

assistants_queries = pugsql.module("./db/queries/assistants")
assistants_queries.connect(settings.DATABASE_URL)

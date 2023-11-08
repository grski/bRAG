-- migrate:up
CREATE TABLE chat (
    id SERIAL PRIMARY KEY,
    uuid UUID NOT NULL UNIQUE,
    openai_id VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE message (
    id SERIAL PRIMARY KEY,
    chat_uuid UUID NOT NULL UNIQUE REFERENCES chat(uuid) ON DELETE CASCADE,
    model VARCHAR(255),
    role VARCHAR(255),
    message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE assistant (
    id SERIAL PRIMARY KEY,
    uuid UUID NOT NULL UNIQUE,
    openai_id VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);


-- migrate:down

DROP TABLE IF EXISTS message;

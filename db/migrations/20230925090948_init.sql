-- migrate:up

CREATE TABLE message (
    id SERIAL PRIMARY KEY,
    model VARCHAR(255),
    role VARCHAR(255),
    message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- migrate:down

DROP TABLE IF EXISTS message;

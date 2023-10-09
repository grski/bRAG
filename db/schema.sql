CREATE TABLE IF NOT EXISTS "schema_migrations" (version varchar(128) primary key);
CREATE TABLE Message (
    id SERIAL PRIMARY KEY,
    user_uuid VARCHAR(255),
    output_message TEXT

);
CREATE TABLE Chat (
    id SERIAL PRIMARY KEY,
    uuid VARCHAR(255),
    user_uuid VARCHAR(255),
    is_active BOOLEAN

);
-- Dbmate schema migrations
INSERT INTO "schema_migrations" (version) VALUES
  ('20231008214110');

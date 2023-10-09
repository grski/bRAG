-- migrate:up
-- Create the Message table
CREATE TABLE Message (
    id SERIAL PRIMARY KEY,
    user_uuid VARCHAR(255),
    output_message TEXT

);

-- Create the Chat table
CREATE TABLE Chat (
    id SERIAL PRIMARY KEY,
    uuid VARCHAR(255),
    user_uuid VARCHAR(255),
    is_active BOOLEAN

);



-- migrate:down

DROP TABLE IF EXISTS Chat;
DROP TABLE IF EXISTS Message;


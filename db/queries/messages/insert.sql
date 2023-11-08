-- :name insert :insert
INSERT INTO message (chat_uuid, model, role, message)
VALUES (:chat_uuid, :model, :role, :message);
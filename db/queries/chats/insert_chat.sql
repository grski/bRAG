-- :name insert_chat :insert
INSERT INTO chat (uuid, openai_id)
VALUES (:uuid, :openai_thread_id);

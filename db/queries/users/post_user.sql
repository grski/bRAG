-- :name post_user :insert
INSERT INTO users (name, email, is_confirmed, uuid, created_at, updated_at)
VALUES (:name, :email, :is_confirmed, :uuid, NOW(), NOW());

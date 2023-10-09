-- :name post_invitation_key :insert
INSERT INTO invitation_keys (uuid, user_email, message_limit, is_used, created_at, updated_at)
VALUES (:uuid, :user_email, :message_limit, :is_used, NOW(), NOW());
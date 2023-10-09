-- :name get_invitation_key :many
SELECT uuid, is_used, user_email, message_limit FROM invitation_keys 
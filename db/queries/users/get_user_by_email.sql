-- :name get_user_by_email :one
SELECT * FROM users WHERE email = :email
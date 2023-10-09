-- :name update_user_is_confirmed 
UPDATE users SET is_confirmed = :is_confirmed WHERE email = :email

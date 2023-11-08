-- :name get_chat :one
SELECT * FROM chat WHERE uuid = :uuid;
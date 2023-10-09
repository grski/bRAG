-- :name update_invitation_key_is_used
UPDATE invitation_keys SET is_used = :is_used WHERE uuid = :uuid
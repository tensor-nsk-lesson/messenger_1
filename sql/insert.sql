// Added user
INSERT INTO users (first_name, second_name, created_at, last_visit, is_blocked, is_active, is_deleted) VALUES ('Petor','Petrov', NOW(), NOW(), false, true, false);
	// Другим запросом //
INSERT INTO authentications (user_id, login, password) VALUES (2, 'petrov1234', 'petrov1234');

// Deleted user
UPDATE users SET is_deleted = true WHERE id = 2;

// Update user
UPDATE users SET first_name = 'Lizaa', second_name = 'Petrova' WHERE id = 2;

// Show all user
SELECT * FROM users;

// Show user
SELECT * FROM users WHERE id = 0;

// Added friend(blocklist)
INSERT INTO relationships (id, user_id, status) VALUES ('0', '1', '0');

// Deleted friend(blocklist)
DELETE FROM relationships WHERE (id = '0' and user_id = '1');
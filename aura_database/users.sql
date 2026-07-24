USE aura_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
SHOW TABLES;
DESCRIBE users;

INSERT INTO users
(name, email, hashed_password)
VALUES
(
    'Vedant',
    'vedant@example.com',
    'dummy_password'
);
SELECT * FROM users;
desc users;
SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE users;

SET FOREIGN_KEY_CHECKS = 1;
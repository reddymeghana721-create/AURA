USE aura_db;

CREATE TABLE competitors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    idea_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    strengths TEXT,
    weaknesses TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (idea_id) REFERENCES ideas(id)
);
SHOW TABLES;
DESCRIBE competitors;
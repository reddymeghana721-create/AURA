USE aura_db;

CREATE TABLE roadmaps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    idea_id INT NOT NULL,
    phase VARCHAR(100),
    milestones_json JSON,
    timeline VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (idea_id) REFERENCES ideas(id)
);
SHOW TABLES;
DESCRIBE roadmaps;
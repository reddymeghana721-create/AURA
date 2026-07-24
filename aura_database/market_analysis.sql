USE aura_db;

CREATE TABLE market_analysis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    idea_id INT NOT NULL,
    tam BIGINT,
    sam BIGINT,
    som BIGINT,
    insights_json JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (idea_id) REFERENCES ideas(id)
);
SHOW TABLES;
DESCRIBE market_analysis;
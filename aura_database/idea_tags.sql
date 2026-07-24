USE aura_db;

CREATE TABLE idea_tags (
    idea_id INT NOT NULL,
    tag_id INT NOT NULL,

    PRIMARY KEY (idea_id, tag_id),

    FOREIGN KEY (idea_id) REFERENCES ideas(id),
    FOREIGN KEY (tag_id) REFERENCES tags(id)
);
SHOW TABLES;
DESCRIBE idea_tags;
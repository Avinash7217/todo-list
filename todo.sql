CREATE DATABASE todo_db;

USE todo_db;

CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text VARCHAR(255) NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    color VARCHAR(7)
);

DROP USER 'ashu'@'localhost';
FLUSH PRIVILEGES;

CREATE USER 'ashu'@'localhost' IDENTIFIED BY 'ashu@123';
GRANT ALL PRIVILEGES ON todo_db.* TO 'ashu'@'localhost';
FLUSH PRIVILEGES;

select * from tasks;

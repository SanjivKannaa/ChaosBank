-- CREATE USER 'repl'@'%' IDENTIFIED WITH mysql_native_password BY 'repl_password';

GRANT REPLICATION SLAVE ON *.* TO 'reliabank'@'%';
FLUSH PRIVILEGES;

FLUSH TABLES WITH READ LOCK;
SHOW MASTER STATUS;
UNLOCK TABLES;

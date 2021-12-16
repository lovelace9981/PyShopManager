DROP USER IF EXISTS 'tiendabd'@'localhost';
DROP DATABASE IF EXISTS tiendabd;

CREATE USER 'tiendabd'@'localhost' IDENTIFIED BY 'password';

CREATE DATABASE tiendabd;

GRANT ALL PRIVILEGES ON tiendabd.* TO 'tiendabd'@'localhost';

FLUSH PRIVILEGES;
CREATE USER 'tiendabd'@'localhost' IDENTIFIED BY 'password';

CREATE DATABASE tiendabd;

GRANT ALL PRIVILEGES ON tiendabd.* TO 'tiendabd'@'localhost';

FLUSH PRIVILEGES;
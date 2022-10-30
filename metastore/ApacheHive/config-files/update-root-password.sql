--USE mysql;
--UPDATE user SET authentication_string=PASSWORD('root') WHERE User='root';
ALTER USER 'root'@'localhost' IDENTIFIED BY 'root';
FLUSH PRIVILEGES;
EXIT;
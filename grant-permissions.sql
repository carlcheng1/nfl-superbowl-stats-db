DROP USER 'sbadmin'@'localhost';
CREATE USER 'sbadmin'@'localhost' IDENTIFIED BY 'adminpw';
DROP USER 'sbclient'@'localhost';
CREATE USER 'sbclient'@'localhost' IDENTIFIED BY 'clientpw';

GRANT ALL PRIVILEGES ON superbowl.* TO 'sbadmin'@'localhost';
GRANT SELECT ON superbowl.* TO 'sbclient'@'localhost';
FLUSH PRIVILEGES;
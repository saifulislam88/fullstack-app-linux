sudo apt -y install mariadb-server mariadb-client



sudo mysql_secure_installation



# Load schema from the project (copy there first)
sudo mysql -uroot -p < /opt/dipti/db/schema.sql
sudo mysql -uroot -p -e "CREATE USER 'dipti'@'%' IDENTIFIED BY 'changeme';
GRANT ALL PRIVILEGES ON dipti_portal.* TO 'dipti'@'%'; FLUSH PRIVILEGES;"
# Optional: if backend is remote, bind 0.0.0.0 then restart
# sudo sed -i 's/^bind-address.*/bind-address = 0.0.0.0/' /etc/mysql/mariadb.conf.d/50-server.cnf
sudo systemctl restart mariadb


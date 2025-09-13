## Step-by-Step `MariaDB` Installation and Setup

### 1. Install MariaDB Server and Client
Update your package index and install MariaDB:

```bash
sudo apt -y install mariadb-server mariadb-client
```

### 2. Secure MariaDB Installation

Run the secure installation script to set root password and apply security best practices:

```bash
sudo mysql_secure_installation
```
  - Follow the prompts to:
  - Set a root password
  - Remove anonymous users
  - Disallow remote root login
  - Remove test databases
  - Reload privilege tables

### 3. Prepare Project Schema Directory and Download Schema File

```bash
mkdir /opt/dipti/
cd /opt/dipti/
wget https://raw.githubusercontent.com/saifulislam88/fullstack-app-linux/main/db/schema.sql -O schema.sql
```
### 4. Load Schema into MariaDB

```bash
sudo mysql -uroot -p < /opt/dipti/schema.sql
```
### 5. Create Application User
Create a dedicated database user with full privileges on the project database:
```bash
sudo mysql -uroot -p -e "CREATE USER 'dipti'@'%' IDENTIFIED BY 'changeme'; \
GRANT ALL PRIVILEGES ON dipti_portal.* TO 'dipti'@'%'; \
FLUSH PRIVILEGES;"
```
### 6. Allow Remote Connections
If your backend is running remotely, bind MariaDB to all interfaces:

```bash
sudo sed -i 's/^bind-address.*/bind-address = 0.0.0.0/' /etc/mysql/mariadb.conf.d/50-server.cnf
sudo systemctl restart mariadb
```

### 6. DB accessiblity testing from application server

```bash
sudo apt -y install mariadb-client
```
```bash
mysql -h <DB_SERVER_IP> -u dipti -p

```bash
SHOW DATABASES;
USE dipti_portal;
SHOW TABLES;
SELECT NOW();

```bash
mysql -h <DB_SERVER_IP> -u dipti -p'changeme' -e "SHOW DATABASES;"
mysql -h <DB_SERVER_IP> -u dipti -p'changeme' -e "USE dipti_portal; SHOW TABLES;"
mysql -udipti -p -h 192.168.1.104 -e "SELECT id,name,email FROM dipti_portal.students ORDER BY id DESC LIMIT 5

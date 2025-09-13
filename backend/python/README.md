
```bash
sudo apt -y install python3-venv python3-pip
```

```bash
sudo mkdir -p /opt/dipti/
cd /opt/dipti/
git clone https://github.com/saifulislam88/fullstack-app-linux.git
```

```bash
cd /opt/dipti/fullstack-app-linux/backend/
python3 -m venv venv
source venv/bin/activate
pip install -r python/requirements.txt
```

```bash
cp /opt/dipti/fullstack-app-linux/backend/python/.env.example /opt/dipti/fullstack-app-linux/backend/python/.env
```

`vim /opt/dipti/fullstack-app-linux/backend/python/.env`

```bash
DB_HOST=192.168.1.104
DB_PORT=3306
DB_NAME=dipti_portal
DB_USER=dipti
DB_PASSWORD=changeme
JWT_SECRET=9b15f2b6b5e08df0c2b8f77a6cfc3f83f55d28b4db74cfb5a1d8c3eaf2c98271
UPLOAD_DIR=/opt/dipti/uploads
```



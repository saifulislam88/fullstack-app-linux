
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
pip install -r requirements.txt
```

```bash
cp /opt/dipti/fullstack-app-linux/backend/.env.example /opt/dipti/fullstack-app-linux/backend/.env
```

```bash
vim /opt/dipti/fullstack-app-linux/backend/.env
```

```bash
DB_HOST=192.168.1.104
DB_PORT=3306
DB_NAME=dipti_portal
DB_USER=dipti
DB_PASSWORD=changeme
JWT_SECRET=9b15f2b6b5e08df0c2b8f77a6cfc3f83f55d28b4db74cfb5a1d8c3eaf2c98271
UPLOAD_DIR=/opt/dipti/fullstack-app-linux/uploads          # this is the NFS mount path
```

mkdir -p /opt/dipti/fullstack-app-linux/uploads
sudo chown -R www-data:www-data /opt/dipti/fullstack-app-linux/backend


### nfs mount in all backend nodes

```bash
sudo apt -y install nfs-common
sudo mount -t nfs 10.0.0.21:/srv/dipti-uploads /opt/dipti/fullstack-app-linux/uploads
#for permanent mount
#echo "10.0.0.21:/srv/dipti-uploads /opt/dipti/fullstack-app-linux/uploads nfs defaults,_netdev 0 0" | sudo tee -a /etc/fstab
sudo mount -a
df -hT
sudo mkdir -p /opt/dipti/fullstack-app-linux/uploads/students
sudo chown -R www-data:www-data /opt/dipti/uploads
```

## Daemon service creation for frontend
```bash
vim /etc/systemd/system/dipti-backend.service
```


```bash
[Unit]
Description=DIPTI Backend (FastAPI v2)
After=network.target mariadb.service

[Service]
WorkingDirectory=/opt/dipti/fullstack-app-linux/backend/
Environment="PYTHONPATH=/opt/dipti/fullstack-app-linux/backend/"
EnvironmentFile=/opt/dipti/fullstack-app-linux/backend/.env
ExecStart=/opt/dipti/fullstack-app-linux/backend/venv/bin/uvicorn app:app --host 0.0.0.0 --port 8000
User=www-data
Group=www-data
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now dipti-backend
```

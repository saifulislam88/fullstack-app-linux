## NodeJs Installation

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt -y install nodejs nginx
```

```bash
sudo mkdir -p /opt/dipti/
git clone https://github.com/saifulislam88/fullstack-app-linux.git
cd /opt/dipti/fullstack-app-linux/frontend/
npm install
```

### Set Node .env (very important):

```bash
vim /opt/dipti/fullstack-app-linux/frontend/.env
```
```bash
BACKEND_API_BASE_URL=http://127.0.0.1:8000   # local backend on the same node or update if it separate server.
SESSION_SECRET=4f2d0a7c1e7c3d8a8f21bc67e9d2f89abef2d6d1a7c9bbf8a6cfeaf9e9d01f3a
PORT=3000
```

### Daemon service creation for frontend
`vim /etc/systemd/system/dipti-frontend.service`

```bash
[Unit]
Description=DIPTI Frontend (Node.js v2)
After=network.target

[Service]
WorkingDirectory=/opt/dipti/fullstack-app-linux/frontend/
EnvironmentFile=/opt/dipti/fullstack-app-linux/frontend/.env
ExecStart=/usr/bin/node src/server.js
User=www-data
Group=www-data
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now dipti-frontend
sudo systemctl start dipti-frontend
```

## Nginx Configuration

vim /etc/nginx/sites-available/dipti_frontend.conf

```bash
server {
    listen 80;
    server_name reg.dipti.com;
    client_max_body_size 10m;

    location = /healthz {
        access_log off;
        add_header Content-Type text/plain;
        return 200 "ok";
    }

    location /static/ {
        alias /opt/dipti/fullstack-app-linux/frontend/src/public/;
        access_log off;
    }

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/dipti_frontend.conf /etc/nginx/sites-enabled/dipti_frontend.conf || true
sudo nginx -t && sudo systemctl restart nginx
```

### NodeJs Installation

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt -y install nodejs nginx
```

```bash
sudo mkdir -p /opt/dipti/
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

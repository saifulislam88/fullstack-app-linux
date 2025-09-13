## Linux Project Setup (Ubuntu 24.04)

This guide provides a **step-by-step setup** of a 6-VM/server architecture with **7 IP addresses** for a highly available web application stack.  

---

### 📌 Infrastructure Plan

| Role                   | Hostname  | IP Address | Notes |
|-------------------------|-----------|------------|-------|
| Load Balancer (HAProxy) | lb1       | 10.0.0.9   | Primary HAProxy node |
| Load Balancer (HAProxy) | lb2       | 10.0.0.10  | Secondary HAProxy node |
| Virtual IP (VIP)        | lb-vip    | 10.0.0.11  | Shared VIP for HAProxy |
| App Server #1           | app1      | 10.0.0.12  | Node.js frontend + FastAPI backend |
| App Server #2           | app2      | 10.0.0.13  | Node.js frontend + FastAPI backend |
| Database (MariaDB)      | db1       | 10.0.0.14  | MariaDB server |
| NFS Storage             | nfs1      | 10.0.0.15  | NFS shared storage |

⚠️⚠️⚠️ For **lab/testing**, you can run all components on **one VM** and point `.env` to `127.0.0.1`.

---

### 📌 Ports

| Service   | Port(s)          |                 Notes                   |
|-----------|------------------|-----------------------------------------|
| HAProxy   | 80, 443, 8404    | HTTPS with self-signed certificates     |
| Nginx     | 8080             | Reverse proxy to frontend/backend       |
| Frontend  | 3000             | Node.js frontend                        |
| Backend   | 8000             | FastAPI backend (API)                   |
| MariaDB   | 3306             | Database access                         |

---

#### ⚙️ Step 1: Install and OS Preparation (In all 6 Hosts)

```bash
sudo apt update && sudo apt -y upgrade
sudo apt -y install curl git
sudo timedatectl set-timezone Asia/Dhaka
```

#### ⚙️ Step 2: Configure Firewall

#### ⚙️ Step 3: Setup HAProxy (lb1 + lb2)

- **Install HAProxy + Keepalived on lb1 (10.0.0.9) and lb2 (10.0.0.10):**

```sh
sudo apt -y install haproxy keepalived openssl
sudo mkdir -p /etc/haproxy/certs
openssl req -new -x509 -days 365 -nodes -out /etc/haproxy/certs/haproxy.pem -keyout /etc/haproxy/certs/haproxy.pem
chmod 600 /etc/haproxy/certs/haproxy.pem
```
- **Update Haproxy configuration**

```sh
cp /etc/haproxy/haproxy.cfg /etc/haproxy/haproxy.cfg_ori_backup
```
```sh
vim /etc/haproxy/haproxy.cfg
```

```bash

# Global settings
global
    log /dev/log local0
    log /dev/log local1 notice
    daemon
    maxconn 2048
    user haproxy
    group haproxy

# Default settings for all sections
defaults
    log     global
    mode    http
    option  httplog
    option  dontlognull
    timeout connect 5s
    timeout client  50s
    timeout server  50s
    retries 3

# Frontend configuration
frontend http_front
    bind *:80
    bind *:443 ssl crt /etc/haproxy/certs/haproxy.pem
    http-request redirect scheme https unless { ssl_fc }
    default_backend app_servers
    option http-server-close
    option forwardfor

# Backend configuration
backend app_servers
    balance roundrobin
    server app1 10.0.0.12:80 check
    server app2 10.0.0.12:80 check

# Optional: stats interface
listen stats
    bind *:8404
    mode http
    stats enable
    stats uri /stats
    stats refresh 10s
    stats auth admin:admin123
```

- **Update Haproxy configuration**

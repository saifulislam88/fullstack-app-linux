## HA microservice architecture–based Linux learning deployment project on Ubuntu 24.04

This guide provides a **step-by-step setup** of a 6-VM/server architecture with **7 IP addresses** for a highly available web application stack.

### Learning stage:
- Loadbalancing
- VRRP with Keepalived
- HA
- Linux
- Modern Arch


<img src="https://github.com/user-attachments/assets/8bd002e5-d0f3-4e57-9ec3-11eafa1553cf" alt="Signature" height="500" width="650"/>


### 📌 Infrastructure Plan

| Role                   | Hostname  | IP Address | Notes |
|-------------------------|-----------|------------|-------|
| Load Balancer (HAProxy) | lb1       | 192.168.1.11   | Primary HAProxy node |
| Load Balancer (HAProxy) | lb2       | 192.168.1.12  | Secondary HAProxy node |
| Virtual IP (VIP)        | lb-vip    | 192.168.1.13  | Shared VIP for HAProxy |
| App Server #1           | app1      | 192.168.1.14  | Node.js frontend + FastAPI backend |
| App Server #2           | app2      | 192.168.1.15  | Node.js frontend + FastAPI backend |
| Database (MariaDB)      | db1       | 192.168.1.16  | MariaDB server |
| NFS Storage             | nfs1      | 192.168.1.17 | NFS shared storage |

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

#### ⚙️ Step 2: Configure Firewall(Disable)


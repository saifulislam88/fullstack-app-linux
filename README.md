## Linux Project Setup (Ubuntu 24.04)

This guide provides a **step-by-step setup** of a 6-VM/server architecture with **7 IP addresses** for a highly available web application stack.  

![Brac TMP v2-Service_Port_IP](https://github.com/user-attachments/assets/aa10433c-c80a-40e0-8348-20c95b524152)


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

#### ⚙️ Step 2: Configure Firewall(Disable)


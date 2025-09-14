
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

- **Update Keepalived configuration**
```sh
cp /etc/keepalived/keepalived.conf /etc/keepalived/keepalived.conf_ori_backup
```
```sh
vim /etc/keepalived/keepalived.conf
```

- lb1
```sh
vim /etc/keepalived/keepalived.conf
```
```ini
vrrp_instance VI_1 {
    state MASTER
    interface ens33  # Replace with your actual NIC (e.g., eth0, ens160)
    virtual_router_id 51
    priority 100
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 1111
    }
    virtual_ipaddress {
        10.0.0.11  # # Replace with your actual vip
    }
}
```

- lb2
```sh
vim /etc/keepalived/keepalived.conf
```
```ini
vrrp_instance VI_1 {
    state BACKUP
    interface ens33  # Replace with your actual NIC (e.g., eth0, ens160)
    virtual_router_id 51
    priority 99
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 1111
    }
    virtual_ipaddress {
        10.0.0.11  # # Replace with your actual vip
    }
}
```

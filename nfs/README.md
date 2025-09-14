## NFS Server Installation

```sh
sudo apt -y install nfs-kernel-server
sudo mkdir -p /srv/dipti-uploads/students
sudo chown -R www-data:www-data /srv/dipti-uploads   #sudo chown -R nobody:nogroup /srv/dipti-uploads
echo "/srv/dipti-uploads 10.0.0.0/24(rw,sync,no_subtree_check)" | sudo tee -a /etc/exports
sudo exportfs -ar
sudo systemctl enable --now nfs-server || sudo systemctl enable --now nfs-kernel-server
```



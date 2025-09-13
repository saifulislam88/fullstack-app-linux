
sudo apt -y install python3-venv python3-pip

cd /opt/dipti/
git clone https://github.com/saifulislam88/fullstack-app-linux.git
sudo cp -r /opt/dipti/dipti-portal-three-tier-v2/backend/python/* /opt/dipti/backend/python/
cd /opt/dipti/backend
python3 -m venv venv
source venv/bin/activate
pip install -r python/requirements.txt
cp /opt/dipti/backend/python/.env.example /opt/dipti/backend/python/.env

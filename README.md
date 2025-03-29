# Flask Koha Top Users Setup

## Installation and Setup

```sh
sudo su
apt update && apt upgrade -y
apt install -y python3 python3-venv python3-pip
python3 -m venv myenv
source myenv/bin/activate
pip install flask mysql-connector-python python-dotenv
```

## Clone Repository

```sh
git clone https://github.com/maheshpalamuttath/ktuwa.git
cd ktuwa
nano .env  # Change Koha database credentials and save
```

## Set Permissions and Run Application

```sh
cd app
chmod +x run.sh
./run.sh
```

Access the application via:
```
http://your-server-ip:5000
```

## Setting up Systemd Service

Create a systemd service file:

```sh
sudo nano /etc/systemd/system/flaskapp.service
```

Add the following content:

```ini
[Unit]
Description=Flask Koha Top Users Service
After=network.target

[Service]
User=koha
WorkingDirectory=/home/koha/koha_top_users
ExecStart=/home/koha/koha_top_users/myenv/bin/python app/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```sh
sudo systemctl daemon-reload && sudo systemctl enable flaskapp && sudo systemctl start flaskapp && sudo systemctl status flaskapp
```

## Embedding in Koha OPAC

Navigate to:
```
Koha >> Tools >> Additional content >> HTML customizations >> OpacNav
```
Click the code icon and paste the following:

```html
<iframe src="http://your-server-ip:5000/" width="100%" height="650px" style="border: none;"></iframe>
```

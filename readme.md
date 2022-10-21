/etc/systemd/system

[Unit]
Description=Remote Control Server  service
After=multi-user.target

[Service]
User=morsserver
Group=adm
Type=simple
Restart=always
ExecStart=/usr/bin/python3 /home/morsserver/server.py

[Install]
WantedBy=multi-user.target

# Stock-watcher
This simply script meant to parse stock price and to send SMS if a threshold is passed
sudo crontab -e
0 4   *   *   *    /sbin/shutdown -r +5
this allows reboot server every day at 04:05 am

@reboot sleep 60 && stock-watcher.py

another variant:

To do so create file /etc/systemd/system/my_script.service with following contents:

[Unit]
Description=My script that requires network

After=network.target

[Service]
Type=oneshot

ExecStart=/full/path/to/my_script.sh

[Install]
WantedBy=multi-user.target



Then execute:

sudo systemctl daemon-reload

sudo systemctl enable my_script
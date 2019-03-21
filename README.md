# Stock-watcher
This simply script meant to parse a stock price and to send SMS if a threshold is passed.

## Requirements

1. Python 3.6 or newer (`python --version` or `python3 --version`)
2. Update your pip: `sudo python -m pip install --upgrade pip` (if don't have any, for installation `sudo apt-get install python3-pip`)
3. Install Beautiful soup `sudo pip install bs4`
4. Install Requests `sudo pip install requests`
5. Install Requests-HTML `sudo pip install requests_html` (this one is requires Python 3.6 and is used with trading-view data provider)

## Installation
Please, do the following:

1. You need to obtain a valid API key for SMS.RU service 
2. You need to create a file key.txt, and insert the API key into the file
3. You need to create a file config.txt, and insert your phone number into the file (please look into example config-example.txt)
4. You need to create a task with autostarting stock-watcher.py. You can do it via crontab or via systemd
5. You need to create a task with server rebooting (because this allows you to flush sent SMS counter)
6. You need to make stock-watcher.py executable (chmod +x)
 

## Crontab editing (examples shown)
`crontab -e`

this allows reboot server every day at 04:05 am (at server local time)

`0 4   *   *   *    /sbin/shutdown -r +5`

`@reboot sleep 120 && /home/user/git/Stock-watcher/stock-watcher.py >> /home/user/git/Stock-watcher/stock-watcher.log 2>&1`




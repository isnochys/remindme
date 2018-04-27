# remindme
simple bot to remind me on the steem blockchain

## Installation

create a python virtual env.
Install requirements:
```pip install -r requirements.txt```

Copy settings and edit it accordingly:

```cp settings-example.ini settings.ini```
  
add in settings.ini the bots steem username, wallet password and your mysql settings

Import remindme.sql to your Mysql DB

Edit remindme_scan.py the user the bot should follow under username.

Add 2 entries in your crontab:

```*/2 * * * * /bin/sh /home/rmb/remindme/cron.sh -d /home/rmb/remindme -p /home/rmb/env/bin/python -e remindme_scan.py```

```* * * * * /bin/sh /home/rmb/remindme/cron.sh -d /home/rmb/remindme -p /home/rmb/env/bin/python -e remindme_bot.py```

## Usage

On steem anytime you post something with folowing pattern:

```#remindme: YEAR-Month-Day hour:min:sec timezone```

or

```#remindme: [+/-][number][s,m,h,d,w]```

the bot will ad this entry to the DB and post a reminder comment to the scheduled time

for example:

```#remindme: +1d-5h+1m```

That would be in 19 hours and 1 minute


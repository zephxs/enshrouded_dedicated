# enshrouded_dedicated tools

Simple shell scripts to monitor Enshrouded dedicated servers:


### "enshrd_query" :

- Show Server_Query infos (cf. https://developer.valvesoftware.com/wiki/Server_Queries)
- Show Currently connected User(s)

[requires: python3 'pip' for SteamQuery lib install and the script 'steamquery.py' from this repository in the PATH]



### "enshrd_steamuser_check" :

- Monitor enshroudedserver.log for [successfull/failed] connection attempts
- maintain a list of currently logged in Usernames
- (Optional) send custom message to telegram channel on [Login/Logout]

Crontab every minute :
*/1 * * * * /usr/local/sbin/enshrd_steamuser_check

telegram-alert sample script can be found here :
```
https://raw.githubusercontent.com/zephxs/ncat-ipset-honeypot/master/telegram-send
```

# enshrouded_dedicated toolset

Simple Shell script-set to "Monitor / Backup / Update" Enshrouded dedicated servers.


Server-Side: 
- `All the scripts` work together to collect realtime informations (every minutes), and once a day backup the server map and upgrade server core files if needed (with SteamCMD). 
- They all need to be placed in the PATH of the "enshrouded user" that runs the server binary (enshrouded_server.exe).


Client-Side: 
- `enshrd_query` + `steamquery.py` scripts are used to get Enshrouded Server status, base informations, SVN version, and Username(s) that are currently logged in to the server.

<br />
<br />

### enshrd_query + steamquery.py

- [x] Show Server_Query infos (cf. https://developer.valvesoftware.com/wiki/Server_Queries)
- [x] Show Currently connected Username(s)

> [!NOTE]
> requires: python3 `pip` for SteamQuery lib install and use, `ssh access` to the server (preferably with a running agent), 

<br />

enshrd_query screenshot:

![script run](/assets/steamq.png)

<br />
<br />

### enshrd_steamuser_check

- [x] Monitor enshroudedserver.log for [successfull/failed] connection attempts
- [x] maintain a list of currently logged in Usernames
- [x] Optional - send custom message to telegram channel on User Login/Logout

> [!TIP]
> Crontab every minute :
> */1 * * * * /usr/local/sbin/enshrd_steamuser_check
>
> telegram-alert sample script can be found here :
> https://raw.githubusercontent.com/zephxs/ncat-ipset-honeypot/master/telegram-send

<br />
Sample logs:
```
$cat ~/enshrd-monitor/user-connection.log
[2024-04-15 10:31:30] [INFO] New ID(s) detected = 0(1)
[2024-04-15 10:31:36] [INFO] User Connected = Ares 0(1)
[2024-04-15 11:57:34] [INFO] User Logout = Ares
```
<br />
<br />

### enshrd_backupgrade

- [x] Auto backup Map files (server 'savegame' folder)
- [x] Auto Update Game Server Files with SteamCMD if Steam Game Repository show a new update

> [!NOTE]
> requires: `enshrd_query` to block process if users are connected

> [!TIP]
> Crontab every day @4h30 AM :
> 30 4 * * * /usr/local/sbin/enshrd_backupgrade

<br />
Sample logs:
```
[2024-04-15 04:05:32] [START] Enshrouded server Backup / Update started
[2024-04-15 04:05:32] [INFO] Current version: 511168
[2024-04-15 04:05:32] [INFO] Steam Game Repo last update: Thu Mar 28 10:35:39 UTC 2024
[2024-04-15 04:05:32] [INFO] Active User(s) detected: '0'
[2024-04-15 04:05:32] [INFO] Stopping service: enshrd.service
[2024-04-15 04:07:08] [INFO] Backuping Map files: /home/enshrouded/enshrd-bak/Enshrouded_Map-15042024-0407.zip
[2024-04-15 04:07:08] [INFO] Steam Repo Check: Update not needed
[2024-04-15 04:07:08] [INFO] Restarting service: enshrd.service
[2024-04-15 04:07:08] [END] Enshrouded Server [Version:511168] - Backup/Update Complete!
```

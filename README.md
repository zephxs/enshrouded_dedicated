# enshrouded_dedicated toolset

Simple Shell script-set to "Monitor / Backup / Update" Enshrouded dedicated servers.


Server-Side: 
- `All the scripts` work together to collect realtime informations (every minutes), and once a day backup the server map and upgrade server core files if needed (with SteamCMD). 
- They all need to be placed in the PATH of the "enshrouded user" that runs the server binary (enshrouded_server.exe). 
- The "enshourded user" MUST have "sudo NOPASSWD" properly configured for managing the Enshrouded Systemd Service during the Backup / Upgrade process (see "Sample Sudoer" at the end of this doc).


Client-Side: 
- `enshrd_query` + `steamquery.py` scripts are used to get Enshrouded Server status, base informations, SVN version, and Username(s) that are currently logged in to the server.

<br />
<br />

### `enshrd_query` + `steamquery.py`

- [x] Show Server_Query infos (cf. https://developer.valvesoftware.com/wiki/Server_Queries) via 'steamquery.py <server> <port>' (can be used alone)
- [x] Show Currently connected Username ("SteamID to Usename" uses https://steamid.io or Steam directly if API Key is provided)

```
enshrd_query -h

Server infos:
  -s|--server <Ip-Hostname>
  -p|--port   <query_port>

  exemple: "enshrd_query <server>:<port>"
  or: "enshrd_query -s <server> -p <port>"
  *** Server infos can be set in script variable to avoid input

Modes:
  [default] No Argument                  # Query All Steam Server Infos
  -u|--user                              # Query currently connected user(s)
  -n|--number                            # Output only the number [0-9] of connected users (used locally for server restart/update)
  -l|--local                             # Used for server-side local run
```


> [!NOTE]
> requires: python3 `pip` for SteamQuery lib install and use, `ssh access` to the server (preferably with a running agent), 

<br />

_screenshot:_

<img src="https://github.com/dr34dl10n/enshrouded_dedicated/blob/main/assets/steamq.png" width="650">
<br />
<br />

### `enshrd_steamuser_check`

- [x] Monitor enshroudedserver.log for [successfull/failed] connection attempts
- [x] maintain a list of currently logged in Usernames
- [x] Optional - send custom message to telegram channel on User Login/Logout

> [!TIP]
> Crontab every minute :
> ```
> */1 * * * * /usr/local/sbin/enshrd_steamuser_check
> ```
>
> telegram-alert sample script can be found here :
> ```
> https://raw.githubusercontent.com/zephxs/ncat-ipset-honeypot/master/telegram-send
> ```

<br />

_Sample logs:_
```
$cat ~/enshrd-monitor/user-connection.log
[2024-04-15 10:31:30] [INFO] New ID(s) detected = 0(1)
[2024-04-15 10:31:36] [INFO] User Connected = Ares 0(1)
[2024-04-15 11:57:34] [INFO] User Logout = Ares
```

<br />
<br />

### `enshrd_backupgrade`

- [x] Auto backup Map files (server 'savegame' folder)
- [x] Auto Update Game Server Files with SteamCMD if Steam Game Repository show a new update

> [!NOTE]
> requires: `enshrd_query` to block process if users are connected

> [!TIP]
> Crontab every day @4h30 AM :
> ```
> 30 4 * * * /usr/local/sbin/enshrd_backupgrade
> ```

<br />

_Sample logs:_
```
$cat ~/enshrd-monitor/update.log
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
<br />
<br />

### `proton-update` [Option within `enshrd_backupgrade`]
- [x] Transparently Update Proton Installation if new latest version on repository (cf. https://github.com/GloriousEggroll/proton-ge-custom/releases) 

<br />
<br />

### Server Config for educational purpose : 

<br />

_Sample Proton Service: /etc/systemd/system/enshrd.service_
```
cat /etc/systemd/system/enshrd.service
[Unit]
Description=Enshrouded Server
Wants=network-online.target
After=network-online.target
[Service]
User=enshrouded
Group=enshrouded
Environment="STEAM_COMPAT_CLIENT_INSTALL_PATH=/home/enshrouded/Steam"
Environment="STEAM_COMPAT_DATA_PATH=/home/enshrouded/Steam/steamapps/compatdata"
WorkingDirectory=/home/enshrouded/enshroudedserver/
ExecStart=/home/enshrouded/.steam/root/compatibilitytools.d/Proton-latest/proton run enshrouded_server.exe
Restart=always
[Install]
WantedBy=multi-user.target
```

<br />

_Sample Wine Service: /etc/systemd/system/enshrd.service_
```
[Unit]
Description=Enshrouded Server
Wants=network-online.target
After=network-online.target
[Service]
User=enshrouded
Group=enshrouded
WorkingDirectory=/home/enshrouded/
ExecStart=/usr/local/bin/wine64 /home/enshrouded/enshroudedserver/enshrouded_server.exe
Restart=always
[Install]
WantedBy=multi-user.target
```

<br />

_Sample Sudoer file: visudo /etc/sudoers.d/enshrouded-user_
```
enshrouded ALL=(ALL) NOPASSWD:/usr/bin/systemctl start enshrd.service,/usr/bin/systemctl stop enshrd.service,/usr/bin/systemctl restart enshrd.service,/usr/bin/systemctl is-active enshrd.service
```

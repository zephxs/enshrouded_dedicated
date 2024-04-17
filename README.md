# enshrouded_dedicated toolset

Simple Shell script-set to "Monitor / Backup / Update" Enshrouded dedicated servers.


Server-Side: 
- `All the scripts` work together to collect realtime informations (every minutes), and once a day backup the server map and upgrade server core files if needed (with SteamCMD). 
- They all need to be placed in the PATH of the "enshrouded user" that runs the server binary (enshrouded_server.exe). 
- The *"Enshourded User"* MUST have *"sudo"* properly configured for managing the Enshrouded Systemd Service during the Backup / Upgrade process (see "Sample Sudoer" at the end of this doc).


Client-Side: 
- `enshrd_query` + `steamquery.py` scripts are used to get Enshrouded Server status, base informations, Enshrouded SVN Server version, and Steam Username(s) that are currently logged in to the server.

<br />
<br />

### `enshrd_query` + `steamquery.py`

- [x] Show Server_Query informations: `steamquery.py <server> <port>` can be used separately without any private access to the server (cf. https://developer.valvesoftware.com/wiki/Server_Queries)
- [x] Display Currently connected Steam Usernames
- [x] Display Enshrouded Server Version

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
- [x] Convert Steam ID to Steam Username (uses 'Steam Api' if `_APIKEY='XXXXXX'` is provided or 'https://steamid.io')
- [x] Keep a fresh list of currently logged in Users
- [x] Optional [`_TELEGRAM_ALERT="true"`] - send custom message to telegram channel on User Login/Logout

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
- [x] Auto Update Game Server Files with `SteamCMD` if Steam Game Repository have a new update
- [x] Optional [`_PROTON_UPDATE="true"`] - Auto Update Proton binary with `proton-update` script

> [!NOTE]
> requires: `enshrd_query` to block process if users are connected to the instance

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
- [x] Transparently Update Proton Installation if new latest version is availaible on Github "GloriousEggroll" Repository (cf. https://github.com/GloriousEggroll/proton-ge-custom/releases)
- [x] Defined install directory: _\<Enshrouded User Homedir\>/.steam/root/compatibilitytools.d/Proton-latest_
- [x] Automatic Symlink / test new install / and revert back in case of error

```
ls -lah $HOME/.steam/root/compatibilitytools.d/
total 16K
drwxrwxr-x  3 enshrouded enshrouded 4.0K Apr 16 13:28 .
drwx------ 25 enshrouded enshrouded 4.0K Apr 12 21:42 ..
drwxr-xr-x  5 enshrouded enshrouded 4.0K Apr 16 13:21 GE-Proton9-4
lrwxrwxrwx  1 enshrouded enshrouded   62 Apr 16 13:02 Proton-latest -> /home/enshrouded/.steam/root/compatibilitytools.d/GE-Proton9-4
```

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

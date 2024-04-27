# enshrouded_dedicated server toolset

Simple Shell script-set to "Monitor / Backup / Update" Enshrouded dedicated servers.

<br />

## Overview

Server-Side: 
- `enshrd_steamuser_check` : collect server login/logout informations (every minutes), and convert steamID to Username.
- `enshrd_backupgrade` + `enshrd_query` + `a2squery.py` : work together once a day to backup the server map and upgrade server core files with SteamCMD if needed (Optional: `proton-update` updates Proton-GE to latest version during the process). 
- They all need to be placed in the PATH of the "enshrouded user" that runs the server binary (enshrouded_server.exe). 
- The *"Enshourded User"* MUST have *"sudo"* properly configured for managing the Enshrouded Systemd Service during the Backup / Upgrade process (see "Sample Sudoer" at the end of this doc).


Client-Side: 
- `enshrd_query` + `a2squery.py` scripts are used to get Enshrouded Server status, base informations, Enshrouded SVN Server version, and Steam Username(s) that are currently logged in to the server.

<br />
<br />

## Details

### `enshrd_query` + `a2squery.py`

- [x] Show Server_Query informations: `a2squery.py <server> <port>` can be used separately without any private access to the server (cf. https://developer.valvesoftware.com/wiki/Server_Queries)
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
  -f|--full                              # Output all 'a2s' informations available
```


> [!NOTE]
> requires: python3 `pip` for SteamQuery lib install and use, `ssh access` to the server (preferably with a running agent), 
> `python3 -m pip install python-a2s`

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
> Crontab every day for ex. @4:30 AM :
> ```
> 30 4 * * * /usr/local/sbin/enshrd_backupgrade
> ```

<br />

_Sample logs:_
```
$cat ~/enshrd-monitor/update.log
[2024-04-17 13:25:07] [START] Enshrouded server Backup / Update started
[2024-04-17 13:25:07] [INFO] Current version: 511168
[2024-04-17 13:25:07] [INFO] Steam Game Repo last update: Wed Apr 17 08:26:12 UTC 2024
[2024-04-17 13:25:08] [INFO] Active User(s) detected: '0'
[2024-04-17 13:25:08] [INFO] Stopping service: enshrd.service
[2024-04-17 13:26:43] [INFO] Backup Map files: /home/enshrouded/enshrd-bak/Enshrouded_Map-17042024-1326.zip
[2024-04-17 13:26:44] [INFO] SteamCMD Update Starting
[2024-04-17 13:27:41] [INFO] SteamCMD Update Finished!
[2024-04-17 13:27:41] [INFO] Proton Repo Check: Update not needed
[2024-04-17 13:27:41] [INFO] Restarting service: enshrd.service
[2024-04-17 13:28:06] [END] Enshrouded Server [Version:516139] - Backup/Update Complete!
```

<br />
<br />

### `proton-update` [Option in `enshrd_backupgrade`]
- [x] Transparently Update Proton Installation if new latest version is availaible on Github "GloriousEggroll" Repository (cf. https://github.com/GloriousEggroll/proton-ge-custom/releases)
- [x] Defined Proton install directory: _\<Enshrouded User Homedir\>/.steam/root/compatibilitytools.d/Proton-latest_
- [x] Automatic Symlink / test new Proton and its embedded wine64 binaries before installing

```
ls -lah $HOME/.steam/root/compatibilitytools.d/

drwxr-xr-x 4 enshrouded enshrouded 4.0K Apr 15 18:58 GE-Proton9-3
drwxr-xr-x 4 enshrouded enshrouded 4.0K Apr 18 11:30 GE-Proton9-4
lrwxrwxrwx 1 enshrouded enshrouded   58 Apr 18 11:30 Proton-latest -> /home/enshrouded/.steam/root/compatibilitytools.d/GE-Proton9-4
```

<br />
<br />

### Server Config for educational purpose : 

<br />

Sample Proton Service: _/etc/systemd/system/enshrd.service_
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

Sample Wine Service: _/etc/systemd/system/enshrd.service_
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

Sample _Sudoer file_: visudo /etc/sudoers.d/enshrouded-user
```
enshrouded ALL=(ALL) NOPASSWD:/usr/bin/systemctl start enshrd.service,/usr/bin/systemctl stop enshrd.service,/usr/bin/systemctl restart enshrd.service,/usr/bin/systemctl is-active enshrd.service
```

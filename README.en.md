Snoop Project
=============

## Snoop Project One of the most promising OSINT tools to search for nicknames.
- [X] This is the most powerful software taking into account the CIS location.

<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/EN__snoop.png" />

Is your life slideshow? Ask Snoop.  
Snoop project is developed without taking into account the opinions of the NSA and their friends,  
that is, it is available to the average user.  

Snoop is a research dev-work (own database/closed bugbounty)  
in the search and processing of public data on the Internet.  
According to Snoop's specialized search, it is capable of competing with traditional search engines.  

Comparison of indexations of bd-nikinal such tools:  
<img src="https://img.shields.io/badge/Snoop-~2000+%20websites-success" width="30%" />  
<img src="https://img.shields.io/badge/Sherlock-~350 websites-yellowgreen" width="20%" />  
<img src="https://img.shields.io/badge/Spiderfoot-~350 websites-yellowgreen" width="20%" />  
<img src="https://img.shields.io/badge/Whatsmyname-~300 websites-yellowgreen" width="20%" />  
<img src="https://img.shields.io/badge/Namechk-~100 websites-red" width="15%" />  


| Platform              | Support |
|-----------------------|:---------:|
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/Linux.png" width="5%" /> GNU/Linux             |     ✅    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/Windows.png" width="5%" /> Windows 7/10 (32/64)  |     ✅    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/Android.png" width="5%" /> Android (Termux)      |     ✅    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/macOS.png" width="5%" /> macOS                 |     ❗️    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/IOS.png" width="5%" /> IOS                   |     🚫    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/WSL.png" width="5%" /> WSL                   |     🚫    |  


Snoop for OS Windows and GNU/Linux
==================================

**Snoop Local database**  
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/EN_DB.png" />  
[Snoop Full version database 2000+ websites ⚡️⚡️⚡️](https://github.com/snooppr/snoop/blob/master/websites.md "Database Snoop")  

## Release

snoop.exe (for Windows) and snoop (for GNU/Linux)  
🇷🇺 🇺🇸 [Download Snoop Project](https://github.com/snooppr/snoop/releases "download the ready-made SNOOP assembly for Windows и GNU/Linux")  

Snoop comes with ready-made assemblies (release) and does not require dependencies (libraries) or python3 installation, that is, it runs on a clean machine with OS Windows or GNU/Linux.  
 
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/Run.gif"/>  


Snoop Project Plugins
=====================

## 1. Demonstration of one of the methods in the Plugin — [GEO_IP/domain]  
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/GEO_IP.gif" />  

**Reports are also available in csv/txt/CLI/maps**  
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/GEO_IPcsv.jpeg" />  

## 2. Demonstration of one of the methods in the Plugin — [Yandex_parser]  
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/Yandex_parser.gif" />  

**Search report dozen username (Plugin — Yandex_parser)**  
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/Yandex_parser 4.png" />  

## 3. Demonstration of one of the methods in the Plugin — [Reverse Vgeocoder]  
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/RVG.gif" /> 

<details>
<summary>Self-build software from source</summary>  

**Native Installation**  
Note: The required version of Python 3.7; 3.8 or 3.9

```
# Clone the repository
$ git clone https://github.com/snooppr/snoop

# Log in to the working directory
$ cd ~/snoop

# Install python3 and python3-pip if they are not installed
$ apt-get update && apt-get install python3 python3-pip

# Install dependencies 'requirements'
$ pip install --upgrade pip
$ python3 -m pip install -r requirements.txt
# Or install all dependencies from 'requirements.txt' to manual through
$ pip3 install module1 module2...
# If instead of the flags of countries are displayed in special mixtures, deliver a font package, such as monochrome
$ apt-get install ttf-ancient-fonts or color apt-get install fonts-noto-color-emoji
# On Windows OS use CMD or PowerShell (to choose from convenience), but not WSL!
```
</details>

<details>
<summary>Using</summary>  

**English version — of Snoop see release (available 'OLD Snoop EN version 1.2.5').**
```
$ snoop --help #manual snoop build version GNU/Linux

optional arguments:
  -h, --help           show this help message and exit

service arguments:
  --version, -V        About: Print to print versions :: OS; Snoop;
                       Python and Licenses
  --list all           Print detailed information about
                       the Snoop database
  --donate y, -d y     Donate on the development of Snoop Project,
                       get/purchase Snoop Full Version
  --autoclean y, -a y  Delete all reports, clean the place
  --update y, -U y     Update Snoop Project

plugins arguments:
  --module y, -m y     OSINT search: use various plugins
                       Snoop:: IP/GEO/YANDEX
                       (the list of plugins will be updated)

search arguments:
  nickname             The nickname of the wanted user.
                       It supports the search for several nicknames at the same time.
                       A nickname containing a space in its name is enclosed in quotation marks
  --verbose, -v        Print detailed verbalization 
                       during the search for 'username' 
  --base , -b          Specify another database to search for 'username' 
                       (Local)
  --web-base, -w       Connect to the updated web database to search for 'username'
                       (Online)
  --site , -s chess    Specify the site name from the database '--list all'. Search
                       for 'username' on one specified resource
  --time-out , -t 9    Set the allocation of max time to wait for a response from the server (seconds).
                       Affects the duration of the search. Affects the 'Timeout errors.'
                       It is necessary to enable this option almost always with a slow Internet connection,
                       in order to avoid prolonged freezes in case of network problems (default 9s)
  --found-print, -f    Print only found accounts
  --no-func, -n        ✓Monochrome terminal, do not use colors in url
                       ✓Mute
                       ✓Prevent opening a web browser
                       ✓Disable printing of country flags
                       ✓Disable display and progress status.
                       Saves system resources and speeds up searches
  --userload , -u      Specify a file with a list of users. Example:
                       'snoop -u ~/listusers.txt start'
  --country, -c        Sorting 'print output/record_results' 
                       by country, not alphabetically
  --save-page, -S      Save the found user pages to local files
  --cert-on, -C        Enable certificate verification on servers. 
                       By default, certificate verification on servers is disabled, 
                       which gives fewer errors and more positive results when searching for nickname
  --normal, -N         Change the SNOOPnina mode > normal mode.
                       On_ Silence on_ SNOOPninja mode: search acceleration ~25pct,
                       RAM saving ~50pct, repeated 'flexible' connection on failed resources
```

**Example**
```
# To search for only one user:
$ python3 snoop.py username1 #Running from source
$ snoop username1 #Running from release
# Or, for example, Cyrillic is supported:
$ python3 snoop.py олеся #Running from source
# To search for a name containing a space:
$ snoop "bob dylan" #Running from release
$ snoop dob_dylan #Running from release
$ snoop bob-dylan #Running from release

# Running on Windows OS:
$ python snoop.py username1 #Running from source
$ snoop.exe username1 #Running from release
# To search for one or more users:
$ snoop.exe username1 username2 username3 username4 #Running from release

# Search for a lot of users-sorting the output of results by country;
# avoiding freezes on websites (more often the "dead zone" depends on the user's ip address);
# print only found accounts; save pages of found accounts locally; 
# specify a file with a list of wanted accounts; 
# connect to the expandable and updated web-base Snoop for search:
$ snoop -с -t 6 -f -S -u ~/file.txt -w start #Running from release
# check the Snoop database:
$ snoop --list all #Running from release
# print the help for Snoop functions:
$ snoop --help #Running from release

# Enable Snoop plugins:
$ snoop --module y #Running from release

# 'ctrl-c/z' — interrupt the search #it is not recommended to interrupt the search in this way in the 'SNOOPnina' mode.
$ kill $(ps aux | grep python/snoop | awk '{print $2}') #fix' for unloading RAM during interrupts.
```
The found accounts will be stored in ~/snoop/results/*/username.{txt.csv.html}.  
To access the browser to the search results on the Android platform, it is desirable to have root rights.  
open csv in office in **utf-8** encoding, field separator **comma**.  

Destroy **all** search results — delete the '~/snoop/results' directory.  
or ```snoop.exe --autoclean y #Running from release OS Windows```
```
# Update Snoop to test new features in the software
$ python3 snoop.py --update y #Git installation is required.
```
</details>  

<details>
<summary>Snoop for Android</summary>  

search username  
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/snoopandroid.png" width="60%" />  

plugins  
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/Snoop_termux.plugins.png" />  

**Native Installation**  

Install [Termux](https://f-droid.org/en/packages/com.termux/ "F-Droid")  
```
# Note: The installation of Snoop on Termux is time-consuming
# Enter the Termux home folder (i.e. just open Termux)
$ termux-setup-storage
$ pwd #/data/data/com.termux/files/home #default/home directory

# Install python3 and dependencies
$ apt update && pkg upgrade && pkg install python libcrypt libxml2 libxslt git
$ pip install --upgrade pip

# Clone a repository
$ git clone https://github.com/snooppr/snoop -b snoop_termux
# (If the flash drive is FAT (neither ext4), in this case, 
# clone the repository only to the Termux HOME directory)

# Log in to the Snoop working directory
$ cd ~/snoop
# Install the 'requirements' dependencies
$ python3 -m pip install -r requirements.txt

# To expand the terminal output in Termux (by default, 2k lines are displayed in the CLI),  
for example, displaying the entire database of the option '--list all [1/2]'  
add the line 'terminal-transcript-rows=10000' to the file '~/.termux/termux.properties'  
(the feature is available in Termux v0.114+).  
Restart Termux. 

# The user can also launch the Snoop Project on the snoop command from anywhere in the cli by creating an alias.
$ printf "alias snoop='cd && cd snoop && python snoop.py'" >> .bashrc

# The user can also run a quick check on the database of the site he is interested in, without using the 'list all' option, using the 'snoopcheck'command
$ alias snoopcheck='cd && cd snoop && printf 2 | python snoop.py --list all | grep -i' >> .bashrc  
# restart Termux.
```
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/snoop_alias.gif" width="40%" />  

</details>

<details>
<summary>Basic errors in</summary>

|  Side     |                         Problem                       | Solving |
|:---------:| ------------------------------------------------------|:-------:|
| ========= |=======================================================| ======= |
| Client    |Block the connection with proactive protection Firewall|    1    |
|           |Insufficient speed of the EDGE/3G Internet connection  |    2    |
|           |The value of the '-t' option is too low                |    2    |
|           |invalid username                                       |    3    |
|           |Connection errors: [GipsysTeam; RamblerDaing; Mamochki]|    7    |
|           |Connection errors: [Virtualireland; Forum_rzn; Ddo]    |    7    |
| ========= |=======================================================| ======= |
| Provider  |Internet Censorship                                    |    4    |
| ========= |=======================================================| ======= |
| Server    |The site has changed its response/API;                 |    5    |
|           |CF/WAF has been updated          |                     |    5    |
|           |Blocking the client's IP address range by the server   |    4    |
|           |Triggering/protecting a captcha resource               |    4    |
|           |Some sites are temporarily unavailable, technical work |    6    |
| ========= |=======================================================| ======= |

Solving:
1. Reconfigure your Firewall (for example, Kaspersky blocks Resources for adults).

2. Check the speed of your Internet connection:  
$ python3 snoop.py -v username  
If any of the network parameters are highlighted in red, Snoop may hang during the search.  
If the speed is low, increase the value of ' x 'of the'--time-out x ' option:  
$ python3 snoop.py -t 15 username  

3. In fact, this is not a mistake. Fix username  
(for example, some sites do not allow Cyrillic characters; "spaces"; or "Vietnamese-Chinese encoding"  
in user names, in order to save time: - requests are filtered).

4. **Change your IP address**  
("Gray" ip and censorship are the most common reasons why the user receives skip errors/false positives/and in some cases '**Alas**'.  
When using Snoop from the IP address of the mobile operator's provider, the speed **may * * drop significantly, depending on the provider.  
For example, the most effective way to solve the problem is **TO USE A VPN**, Tor is not very well suited for this task.  
Rule: one scan from one ip is not enough to get the most out of Snoop).

5. Open in the Snoop repository on Github-e Issue/Pull request  
(inform the developer about this).

6. Do not pay attention, sites sometimes go for repair work and return to operation.

7. There is [problem](https://wiki.debian.org/ContinuousIntegration/TriagingTips/openssl-1.1.1 "the problem is simple and solvable") with openssl in some GNU/Linux distributions.  
Solving:
```
$ sudo nano /etc/ssl/openssl.cnf

# Edit the lines at the very bottom of the file:
[MinProtocol = TLSv1.2]
on
[MinProtocol = TLSv1]

[CipherString = DEFAULT@SECLEVEL=2]
on
[CipherString = DEFAULT@SECLEVEL=1]
```
</details>

<details>
<summary>Additional information</summary>

 • [Project development history](https://raw.githubusercontent.com/snooppr/snoop/master/changelog.txt "changelog")  

 • [License](https://github.com/snooppr/snoop/blob/master/COPYRIGHT "The version of the License in English can be found in the EN-version of Snoop Build")  

 • [Documentation/ru](https://drive.google.com/open?id=12DzAQMgTcgeG-zJrfDxpUbFjlXcBq5ih)  

 • **Public key fingerprint:**	[076DB9A00B583FFB606964322F1154A0203EAE9D](https://raw.githubusercontent.com/snooppr/snoop/master/PublicKey.asc "pgp key")  

 • **Information for civil servants/RU:** Snoop Project is included in the register of domestic software with the declared code: 26.30.11.16 Software that ensures the implementation of established actions during operational search activities.
Order of the Ministry of Communications of the Russian Federation No. 515 registered No. 7012.  

 • **Snoop is not perfect**: web sites are falling; closing tags are missing; hosting services are not paid on time.  
From time to time, it is necessary to follow all this "Web rock' n 'roll", so donations are welcome:
[Example close/bad websites](https://drive.google.com/file/d/1CJxGRJECezDsaGwxpEw34iJ8MJ9LXCIG/view?usp=sharing)  
BTC (donation): 1Ae5uUrmUnTjRzYEJ1KkvEY51r4hDGgNd8  

 • **email:** snoopproject@protonmail.com
</details>
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/zvezda.jpeg" width="10%" />  
*Please feel free to improve the translation of this page.*

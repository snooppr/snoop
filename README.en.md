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

Comparison of indexations of databases such tools:  
<img src="https://img.shields.io/badge/Snoop-~2600+%20websites-success" width="30%" />  
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
[Snoop Full version database 2600+ websites ⚡️⚡️⚡️](https://github.com/snooppr/snoop/blob/master/websites.md "Database Snoop")  

## Release
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/snoop box.png" width="35%" />  

snoop.exe (for Windows) and snoop (for GNU/Linux)  
[Download Snoop Project](https://github.com/snooppr/snoop/releases "download the ready-made SNOOP assembly for Windows и GNU/Linux")  

Snoop comes with ready-made assemblies (release) and does not require dependencies (libraries) or python3 installation, that is, it runs on a clean machine with OS Windows or GNU/Linux.  
 
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/Run.gif"/>  

<details>
<summary>Snoop Project Plugins</summary>  

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
</details>

<details>
<summary>Self-build software from source</summary>  

**Native Installation**  
Note: The required version of Python 3.7+

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

```
$ snoop --help #manual snoop build version GNU/Linux

Help

optional arguments:
  -h, --help            show this help message and exit

service arguments:
  --version, -V         printing versions of :: OS; Snoop;
                        Python and Licenses
  --list-all, -l        Print detailed information about the 
                        Snoop database
  --donate, -d          Donate to the development of the Snoop Project,
                        get/buy Snoop Full Version
  --autoclean, -a       Delete all reports, clear space
  --update, -U          Update Snoop

plugins arguments:
  --module, -m          OSINT search: use various plugins Snoop ::
                        IP/GEO/YANDEX (the list of plugins will continue
                        to grow)

search arguments:
  nickname              The nickname of the wanted user.
                        Searching for several names at the same time is 
                        supported. Nicknames containing a space in their name
                        are enclosed in quotation marks
  --verbose, -v         When searching for 'username', print detailed
                        verbalization
  --base , -b <path>    Specify another database for search for 'username'
                        (Local)/In demo version the function is disabled
  --web-base, -w        Connect to search for 'username' to the updated web_DB
                        (Online)/In demo version the function is disabled
  --site , -s <site_name> 
                        Specify the name of the site from the database 
                        '--list-all'. Search for 'username' on one specified
                        resource, it is acceptable to use the '-s' option
                        multiple times
  --exclude , -e <country_code> 
                        Exclude the selected region from the search,
                        it is permissible to use the '-e' option several times,
                        for example, '-e RU -e WR' exclude Russia and World from search
  --one-level , -o <country_code> 
                        Include only the selected region in the search,
                        it is permissible to use the '-o' option several times,
                        for example, '-o US -o UA' search for USA and Ukraine
  --country, -c         Sort 'print/record_results' by country,
                        not alphabetically
  --time-out , -t <digit> 
                        Set maximum time allocation for waiting for a response 
                        from the server (seconds). Affects the search duration.
                        Affects 'Timeout errors:' On. this option is necessary
                        with a slow Internet connection to avoid long freezes
                        in case of network problems
                        (by default, the value is set to 5s)
  --found-print, -f     Print only found accounts
  --no-func, -n         ✓Monochrome terminal, do not use colors in url 
                        ✓Disable sound ✓Disable opening web browser
                        ✓Disable printing of country flags 
                        ✓Disable indication and progress status. 
                        Saves system resources and speeds up searches
  --userlist , -u <path> 
                        Specify a file with a list of users.
                        Example: 'python snoop.py -u
                        /storage/emulated/0/Download/listusers.txt'
  --save-page, -S       Save found user pages to local files
  --cert-off, -C        Disable verification of certificates on servers. 
                        By default, server certificate checking is enabled on
                        Snoop for Android, which improves search speed, 
                        but may result in higher percentages of false positives
  --headers , -H <name> 
                        Set the user-agent manually, the agent is enclosed in 
                        quotes, by default a random or overridden user-agent
                        from the snoop database is set for each site.
                        https://юзерагент.рф/
  --normal-mode, -N     Mode switch: SNOOPninja> normal mode> SNOOPninja. 
                        By_default (GNU/Linux Full Version) on 
                        'SNOOPninja mode': search acceleration ~ 25pct,
                        RAM saving ~ 50pct, repeated 'flexible' connection on
                        failed resources. SNOOPninja mode is only effective for
                        Snoop for GNU/Linux Full Version. The default
                        (on Windows) is 'normal mode'. 
                        In Demo Version, the mode switch is deactivated
  --quick-mode , -q     Quiet search mode on. Intermediate
                        the results are not printed. Repeated flexible
                        connections on faulty resources without slowing down
                        the software. The most advanced search mode 
                        (in development - not use)
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

# 'ctrl-c', 'ctrl-\' — interrupt the search #it is not recommended to interrupt the search in this way in the 'SNOOPnina' mode.
$ kill $(ps aux | grep python/snoop | awk '{print $2}') #fix' for unloading RAM during interrupts.
```
The found accounts will be stored in ~/snoop/results/*/username.{txt.csv.html}.  
open csv in office in, field separator **comma**.  

Destroy **all** search results — delete the '~/snoop/results' directory.  
or ```snoop.exe --autoclean y #Running from release OS Windows```
```
# Update Snoop to test new features in the software
$ python3 snoop.py --update y #Git installation is required.
```
</details>  

<details>
<summary>Snoop for Android</summary>  

 • [Detailed manual in English](https://github.com/snooppr/snoop/blob/snoop_termux/README.en.md "Snoop for Android")  

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

 • **email:** snoopproject@protonmail.com
</details>

This is a translated "Readme" and is incomplete. Full [Readme in Russian](https://github.com/snooppr/snoop)  
Please feel free to improve the translation of this page.

Snoop Project
=============

### Snoop Project is one of the most promising OSINT tools allowing to search by nickname
- [X] This is the most powerful software taking into account the CIS location.

<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/EN__snoop.png" />

Is your life slideshow? Ask Snoop.  
Snoop project is developed without taking into account the opinions of the NSA and their friends;  
that is, it is available to the average user *(project creation date: February 14, 2020)*.  


   🌎 **ENGLISH readme**  
 • [🇷🇺 РУССКИЙ readme](https://github.com/snooppr/snoop)  
 • [🇪🇸 ESPAÑOL readme](https://github.com/snooppr/snoop/blob/master/README.es.md "Por favor, siéntase libre de mejorar la traducción de esta página.")  
 • [🇩🇪 DEUTSCHE readme](https://github.com/snooppr/snoop/blob/master/README.de.md "Bitte zögern Sie nicht, die Übersetzung dieser Seite zu verbessern..")  
 • [🇨🇳 中国人 readme](https://github.com/snooppr/snoop/blob/master/README.cn.md "请随时改进此页面的翻译。")  
 • [🇫🇷 FRANÇAIS readme](https://github.com/snooppr/snoop/blob/master/README.fr.md "N'hésitez pas à améliorer la traduction de cette page.")  

 ---

> [!NOTE]
> <sub>*Snoop is a research project in the field of searching and processing public data on the Internet
> (own database, algorithms, closed bug bounties). In terms of specialized search, Snoop is able to compete
> with traditional search engines.*</sub>  

**The functionality of the tool is simple and does not require users to have knowledge or any technical skills.**  
*(downloaded the software, specify the goal, received the results).*  

Comparison of similar tool databases:

<a href="https://raw.githubusercontent.com/snooppr/snoop/master/websites.md" Target="_blank"><img src="https://img.shields.io/badge/Snoop-~5300+%20websites-success" width="50%" />  
<img src="https://img.shields.io/badge/Whatsmyname-~600 websites-yellowgreen" width="25%" />  
<img src="https://img.shields.io/badge/Sherlock-~400 websites-yellowgreen" width="20%" />  
<img src="https://img.shields.io/badge/Spiderfoot-~350 websites-yellowgreen" width="20%" />  
<img src="https://img.shields.io/badge/Namechk-~100 websites-red" width="15%" />  


| Platform                                                                                                           | Support |
|--------------------------------------------------------------------------------------------------------------------|:---------:|
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/Linux.png" width="5%" /> 𝔾ℕ𝕌/𝕃𝕚𝕟𝕦𝕩                      |     ✅    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/Windows.png" width="5%" /> 𝕎𝕚𝕟𝕕𝕠𝕨𝕤 𝟟/𝟙𝟙          |    ✅    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/Android.png" width="5%" /> 𝔸𝕟𝕕𝕣𝕠𝕚𝕕 (𝕋𝕖𝕣𝕞𝕦𝕩) |     ✅    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/macOS.png" width="5%" /> 𝕞𝕒𝕔𝕆𝕊                                |     ❗️    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/IOS.png" width="5%" /> 𝕚𝕆𝕊                                         |     🚫    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/WSL.png" width="5%" /> 𝕎𝕊𝕃                                         |     🚫    |


Snoop for OS Windows and GNU/Linux
==================================

**Snoop Local database**  
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/EN_DB.png" />  
[Snoop Full version database 5300+ websites ⚡️⚡️⚡️](https://raw.githubusercontent.com/snooppr/snoop/master/websites.md "Database Snoop")  

## Release
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/snoop box.png" width="35%" />  

Snoop comes as a binary and does not require any dependencies, libraries or Python installation. 
It runs on a clean machine with Windows or GNU/Linux.  
┗━━ ⬇️[Download Snoop Project](https://github.com/snooppr/snoop/releases "download the ready-made SNOOP assembly for Windows and GNU/Linux")  

<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/Run.gif"/>  

<details>
<summary> 🟣 Snoop Project Plugins</summary>  

### 1. Demonstration of one of the methods in the Plugin — 〘GEO_IP/domain〙  
https://github.com/snooppr/snoop/assets/61022210/ab20ec4f-8eb2-40ff-b773-4e3443ad2a70  

$$$$

Reports are also available in csv/txt/CLI/maps  
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/GEO_IPcsv.jpeg" />  

$$$$

Report in HTML format on the OSM map (Snoop full version)  
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/plugin GEO_IP_domain.jpg" />  

$$$$

### 2. Demonstration of one of the methods in the Plugin — 〘Yandex_parser〙  
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/Yandex_parser.gif" />  

$$$$

Search report a dozen username (Plugin — Yandex_parser)  
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/Yandex_parser 4.png" />  

$$$$

### 3. Demonstration of one of the methods in the Plugin — 〘Reverse Vgeocoder〙  
https://github.com/snooppr/snoop/assets/61022210/0be6ac32-c72f-4a18-9c9e-3413085f57c3  

Snoop selects geo coordinates from dirty data (numbers, letters, special characters),
places markers on the map based on them and labels them with nearby populated areas/objects.  

Visualization of signed geo coordinates as HTML report (Snoop full version)  
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/plugin Reverse Vgeocoder.jpg" />  

</details>

<details>
<summary> 🟤 Self-build software from source</summary>  

**Native Installation**  
+ Note: don't do this if you want to install snoop on android/termux
*(installation is different, see the dedicated section below for that).*  
+ Note: the required version of Python 3.7+

```sh
# Clone the repository
$ git clone https://github.com/snooppr/snoop

# Log in to the working directory
$ cd ~/snoop

# Install python3 and python3-pip if they are not installed
$ apt-get update && apt-get install python3 python3-pip

# Install dependencies 'requirements'
$ pip install --upgrade pip
$ python3 -m pip install -r requirements.txt
# If instead of the flags of countries are displayed in letter country code, deliver a font package, such as color
$ apt-get install fonts-noto-color-emoji #or (monochrome) $ apt-get install ttf-ancient-fonts
# On Windows OS use CMD, but not WSL!
# OS Windows. If the user's fonts are not displayed correctly, right-click in cmd, properties and select the font:
# "Lucida Console" or "TrueType".
# Added macOS support (experimental).
```
</details>

<details>
<summary> 🟢 Using</summary>  

```
usage: snoop_cli.bin [search arguments...] nickname
or
usage: snoop_cli.bin [service arguments | plugins arguments]


$ snoop_cli.bin --help #manual snoop build version GNU/Linux

Help

optional arguments:
  -h, --help            show this help message and exit

service arguments:
  --version, -V         About: print software version, snoop info and licenses
  --list-all, -l        Print detailed information about the 
                        Snoop database
  --donate, -d          Donate to the development of the Snoop Project,
                        get/buy Snoop Full Version
  --autoclean, -a       Delete all reports, clear cache
  --update, -U          Update Snoop

plugins arguments:
  --module, -m          OSINT search: use various plugins Snoop ::
                        IP/GEO/YANDEX

search arguments:
  nickname              The nickname of the wanted user.
                        Searching for several names at the same time is 
                        supported. Nicknames containing a space in their name
                        are enclosed in quotation marks
  --web-base, -w        Connect to search for 'nickname' to the updated web_DB
                        (5300+ websites). In demo version the function is disabled
  --site , -s <site_name> 
                        Specify the name of the site from the database 
                        '--list-all'. Search for 'nickname' on one specified
                        resource, it is acceptable to use the '-s' option
                        multiple times
  --exclude , -e <country_code> 
                        Exclude the selected region from the search,
                        it is permissible to use the '-e' option several times,
                        for example, '-e RU -e WR' exclude Russia and World from search
  --include , -i <country_code> 
                        Include only the selected region in the search,
                        it is permissible to use the '-i' option several times,
                        for example, '-i US -i UA' search for USA and Ukraine
  --country-sort, -c    Print and record_results' by country, not alphabetically
  --time-out , -t <digit> 
                        Set maximum time allocation for waiting for a response 
                        from the server (seconds). Affects the search duration.
                        Affects 'Timeout errors:' On. this option is necessary
                        with a slow Internet connection (by default 9s)
  --no-func, -n         ✓Monochrome terminal, do not use colors in url
                        ✓Disable opening web browser
                        ✓Disable printing of country flags 
                        ✓Disable indication and progress status
  --found-print, -f     Print only found accounts
  --verbose, -v         When searching for 'nickname', print detailed
                        verbalization
  --userlist , -u <file> 
                        Specify a file with a list of users. Snoop will
                        intelligently process the data and provide additional reports
  --save-page, -S       Save found user pages to local files (slow mode)
  --cert-on, -C         Enable verification of certificates on servers.
                        By default, certificate verification on servers is disabled, 
                        which allows you to process problematic sites without errors
  --headers , -H <User-Agent> 
                        Set the user-agent manually, the agent is enclosed in 
                        quotes, by default a random or overridden user-agent
                        from the snoop database is set for each site
  --pool , -p <digit>   Disable auto-optimization and set manually
                        search speed from 1 to 300 max. processes. By
                        default, high load on computer resources is used
                        in Quick mode, in other modes, moderate power consumption is
                        used. Too low or high value can significantly slow down the
                        operation of software. ~The calculated optimal value for this
                        device is displayed in 'snoop info', parameter
                        'Recommended pool', option [--version/-V]. This option
                        is suggested to be used 1) if the user has a
                        multi-core computer and RAM reserve or, on the contrary, weak,
                        rented VPS 2) It is recommended to speed up and slow down the
                        search in tandem with the option [--found-print/-f']
  --quick, -q           Fast and aggressive search mode. 
                        Does not reprocess failed resources,
                        which speeds up the search,
                        but also slightly increases Bad_raw.
                        Quick mode adapts to PC power,
                        does not print intermediate results,
                        is effective and is designed for Snoop full version
```

**Example**
```sh
# To search for only one user:
$ python3 snoop.py username1 #Running from source
$ snoop_cli.bin username1 #Running from release linux
# Or, for example, Cyrillic is supported:
$ python3 snoop.py олеся #Running from source
# To search for a name containing a space:
$ snoop_cli.bin "bob dylan" #Running from release linux
$ snoop_cli.bin dob_dylan #Running from release linux
$ snoop_cli.bin bob-dylan #Running from release linux

# Running on Windows OS:
$ python snoop.py username1 #Running from source
$ snoop_cli.exe username1 #Running from release win
# To search for one or more users:
$ snoop_cli.exe username1 username2 username3 username4 #Running from release win

# Search for a lot of users;
# avoiding freezes on websites (more often the "dead zone" depends on the user's ip address);
# print only found accounts; save pages of found accounts locally; 
# specify a file with a list of wanted accounts; 
# connect to the expandable and updated web-base Snoop for search:
$ snoop_cli.bin -t 6 -f -S -u ~/file.txt -w #Running from release linux

# check the Snoop database:
$ snoop_cli.bin --list all #Running from release linux

# print the help for Snoop functions:
$ snoop_cli.bin --help #Running from release linux

# Searching for two usernames on two resources:
$ snoop_cli.bin -s habr -s lichess chikamaria irina

# Get Snoop full version:
$ snoop_cli.bin --donate

# Enable Snoop plugins:
$ snoop_cli.bin --module #Running from release linux
```
+ 'ctrl-c' — abort search.  
+ The results will be saved in `~/snoop/results/nicknames/*{txt|csv|html}`.  
+ Open csv in office in, field separator **comma**.  
+ Destroy **all** search results — delete the '~/snoop/results' directory.  
or incl. and reset cache `snoop_cli.exe --autoclean #Running from release OS Windows`.
```sh
# Update Snoop to test new features in the software
$ python3 snoop.py --update #Git installation is required
```
</details>  

<details>
<summary> 🔵 Snoop for Android</summary>  

 • [Detailed manual in English](https://github.com/snooppr/snoop/blob/master/README_android.en.md "Snoop for Android")  

</details>

<details>
<summary> 🔴 Basic errors</summary>

|  Side     |                         Problem                       | Solving |
|:---------:| ------------------------------------------------------|:-------:|
| ========= |=======================================================| ======= |
| Client    |Block the connection with proactive protection Firewall|    1    |
|           |Insufficient speed of the EDGE/3G Internet connection  |    2    |
|           |The value of the '-t' option is too low                |    2    |
|           |Invalid username                                       |    3    |
|           |Connection errors: [GipsysTeam; Nixp; Ddo; Mamochki]   |    7    |
| ========= |=======================================================| ======= |
| Provider  |Internet Censorship                                    |    4    |
| ========= |=======================================================| ======= |
| Server    |The site has changed its response/API;                 |    5    |
|           |CF/WAF has been updated                                |    5    |
|           |Blocking the client's IP address range by the server   |    4    |
|           |Triggering/protecting a captcha resource               |    4    |
|           |Some sites are temporarily unavailable, technical work |    6    |
| ========= |=======================================================| ======= |

Solving:
1. Reconfigure your Firewall *(for example, Kaspersky blocks resources for adults).*

2. Check the speed of your Internet connection:  
`python3 snoop.py -v username`  
If any of the network parameters are highlighted in red, Snoop may hang during the search.  
At low speed, increase the 'x' value of the '--time-out x' option:  
`python3 snoop.py -t 15 username`.  

3. In fact, this is not a mistake. Fix username  
*(for example, some sites do not allow Cyrillic characters; "spaces" or "Vietnamese-Chinese encoding"
in usernames, to save time: - requests are filtered).*

4. **Change your IP address**  
Censorship are the most common reasons why the user receives skip errors/false positives/and in some cases '**Alas**'.  
When using Snoop from the IP address of the mobile operator's provider, the speed **may** drop significantly, depending on the provider.  
For example, the most effective way to solve the problem is **[censored][*](https://www.rbc.ru/technology_and_media/21/11/2024/673f2a269a7947a9377068b2) [**](https://telegra.ph/Roskomnadzor-raskryl-kakuyu-informaciyu-o-VPN-zapretit-v-Rossii-11-30)[/censored]**  

5. Open in the Snoop repository on Github-e Issue/Pull request  
*(inform the developer about this).*

6. Do not pay attention, sites sometimes go for repair work and return to operation.

7. There is [problem](https://wiki.debian.org/ContinuousIntegration/TriagingTips/openssl-1.1.1 "the problem is simple and solvable") with openssl in some GNU/Linux distributions, and also a problem with sites that haven't been updated in years. These problems occur if the user intentionally started snoop with the '--cert-on' option.  
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
<summary> 🟠 Additional information</summary>

 • [Project development history](https://raw.githubusercontent.com/snooppr/snoop/master/changelog.txt "changelog").  

 • [License](https://github.com/snooppr/snoop/blob/master/COPYRIGHT "The version of the License in English can be found in the EN-version of Snoop Build").  

 • [Documentation/ru](https://drive.google.com/open?id=12DzAQMgTcgeG-zJrfDxpUbFjlXcBq5ih).  

 • **Public key fingerprint:**	[076DB9A00B583FFB606964322F1154A0203EAE9D](https://raw.githubusercontent.com/snooppr/snoop/master/PublicKey.asc "pgp key").  

 • **Snoop is not perfect**: websites are falling; closing tags are missing; the network is being censored; certificates are not renewed; hosting services are not paid on time.  
From time to time, it is necessary to follow all this "Web rock' n 'roll", so donations are welcome:
[example close/bad websites](https://drive.google.com/file/d/1CJxGRJECezDsaGwxpEw34iJ8MJ9LXCIG/view?usp=sharing).  

 • **Visualization of commits:** from the birth of the project to Friday the thirteenth, 2023.  

https://user-images.githubusercontent.com/61022210/212534128-bc0e5779-a367-4d0a-86cb-c52503ee53c4.mp4  

 • **Run an aggressive repository compaction on December 11, 2024.** A full history backup was saved. Users building Snoop from source should do a new 'git clone'.  

</details>

【RU → EN】 This is a translated [➰Readme in Russian](https://github.com/snooppr/snoop "If you wish, you can improve (PR) the machine translation of this page in English").

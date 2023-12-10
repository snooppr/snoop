Snoop Project for Termux
========================

## Snoop Project is one of the most promising OSINT tools for finding nicknames.
- [X] This is the most powerful software taking into account the CIS location.

<p align="center">  
  <img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/Snoop_2android.png" />  
</p>  

<p align="center">  
  <img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/snoopandroid.png" />  
</p>  

Is your life slideshow? Ask Snoop.  
Snoop project is developed without taking into account the opinions of the NSA and their friends,  
that is, it is available to the average user.  

## Self-build software from source  
**Snoop for Android/Demo**  
<p align="center">  
  <img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/Snoop_termux.plugins.png" width="90%" />  
</p>  

**Self-build software from source**  
**Native Installation**  

Install [Termux](https://f-droid.org/en/packages/com.termux/ "Termux with F-Droid, GP Termux is no longer updated!")  
```
# NOTE_1!: if the user has errors with $ 'pkg update', for example due to country censorship,
# and/or due to the fact that Termux has not been updated for a long time on the user's device,
# then removing/installing Termux application will not help,
# since after deletion, old repositories remain on the user's device, the solution is:
$ termux-change-repo
# and choose to get updates (for all repo) from another mirror repository.

# Enter Termux home folder (i.e. just open Termux)
$ termux-setup-storage
$ pwd #/data/data/com.termux/files/home # default/home directory

# Install python3 and dependencies
$ apt update && pkg upgrade && pkg install python libcrypt libxml2 libxslt git
$ pip install --upgrade pip

# Clone the repository
$ git clone https://github.com/snooppr/snoop

# Enter the Snoop working directory  
$ cd ~/snoop  
# Install the 'requirements_android.txt' dependencies  
$ python3 -m pip install -r requirements_android.txt  


# Optional↓
# To expand the terminal output in Termux (by default, 2k lines are displayed in the CLI),  
# for example, displaying the entire database of the option '--list-all [1/2]'  
# add the line 'terminal-transcript-rows=10000' to the file '~/.termux/termux.properties'  
# (the feature is available in Termux v0.114+).  
# Restart Termux.  

# The user can also launch the Snoop Project on the snoop command from anywhere in  
# the cli by creating an alias.  
$ cd && echo "alias snoop='cd && cd snoop && python snoop.py'" >> .bashrc && bash  

# The user can also run a quick check on the database of the site he is interested in,  
# without using the 'list-all' option, using the 'snoopcheck'command  
$ cd && echo "alias snoopcheck='cd && cd snoop && echo 2 | python snoop.py --list-all | grep -i'" >> .bashrc && bash  
# restart Termux.  
# At the end of the search work snoop on the request to select "with which to open the search results" select the default / system HTMLviewer.  

# NOTE_2!: to auto-open search results in an external web-browser:  
$ cd && pkg install termux-tools; echo 'allow-external-apps=true' >>.termux/termux.properties  
```
NOTE_3!: if the Android user has a flawed (that is, 12+) and breaks Termux, read the instructions for solving the problem [here](https://github.com/agnostic-apollo/Android-Docs/blob/master/en/docs/apps/processes/phantom-cached-and-empty-processes.md#how-to-disable-the-phantom-processes-killing).  
NOTE_4!: old patched python versions 3.7-3.10 from are supported [termux_tur repo](https://github.com/termux-user-repository/tur/tree/master/tur).  
<p align="center">  
  <img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/snoop_alias.gif" width="40%" />  
</p>  


## Using
```
usage: snoop_cli [search arguments...] nickname
or
usage: snoop_cli [service arguments | plugins arguments]

$ python snoop.py --help

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
                        IP/GEO/YANDEX

search arguments:
  nickname              The nickname of the wanted user.
                        Searching for several names at the same time is 
                        supported. Nicknames containing a space in their name
                        are enclosed in quotation marks
  --verbose, -v         When searching for 'nickname', print detailed
                        verbalization
  --web-base, -w        Connect to search for 'nickname' to the updated web_DB
                        (3000+ websites). In demo version the function is disabled
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
  --country-sort, -c    Print and record_results' by country,
                        not alphabetically
  --time-out , -t <digit> 
                        Set maximum time allocation for waiting for a response 
                        from the server (seconds). Affects the search duration.
                        Affects 'Timeout errors:' On. this option is necessary
                        with a slow Internet connection (by default 9s)
  --found-print, -f     Print only found accounts
  --no-func, -n         ✓Monochrome terminal, do not use colors in url 
                        ✓Disable opening web browser
                        ✓Disable printing of country flags 
                        ✓Disable indication and progress status
  --userlist , -u <file> 
                        Specify a file with a list of users. Snoop will
                        intelligently process the data and provide additional reports
  --save-page, -S       Save found user pages to local files
  --cert-on, -C         Enable verification of certificates on servers.
                        By default, certificate verification on servers is disabled, 
                        which allows you to process problematic sites without errors
  --headers , -H <User-Agent> 
                        Set the user-agent manually, the agent is enclosed in 
                        quotes, by default a random or overridden user-agent
                        from the snoop database is set for each site
  --quick, -q           Fast and aggressive search mode. Does not reprocess bad
                        resources, as a result of which the search is accelerated,
                        but Bad_raw also increases. Does not print intermediate results.
                        Consumes more resources. The mode is effective in full version
```

**Example**
```
# To search for just one user:
$ python3 snoop.py username1
# Or, for example, Cyrillic is supported:
$ python3 snoop.py олеся
# To search for a name containing a space:
$ python3 snoop.py "bob dylan"
$ python3 snoop.py bob_dylan
$ python3 snoop.py bob-dylan

# To search for one or more users:
$ python3 snoop.py username1 username2 username3 username4

# Search for multiple users - sorting the output of results by country;
# avoid long freezes on sites (more often the 'dead zone' depends on your ip-address);
# print only found accounts; save pages found
# of accounts locally; specify a file with a list of wanted accounts;
# connect to search for Snoop's extensible and updatable web-base:
$ python3 snoop.py -c -t 9 -f -S -u ~/file.txt -w

# Search for two usernames on two resources:
$ snoop_cli -s habr -s lichess chikamaria irina

# Get Snoop full version:
$ snoop_cli --donate

# 'ctrl-c' — abort search
```
Found accounts will be stored in '/storage/emulated/0/snoop/results/nicknames/*{txt|csv|html}'.  
csv open in *office, field separator **comma**.    

Destroy **all** search results - delete the directory '~/snoop/results'.
or ```python snoop.py --autoclean```

```
# Update Snoop to test new software features:
$ python3 snoop.py --update #requires a Git installation.
```

**An example snoop for android**  
<p align="center">  
  <img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/Android%20snoop_run.gif" width="40%" />  
</p>  

 • **January 27 2022 compress the repository/if you have problems, do a 'git clone' again.**  
 • **October 12, 2023 merged snoop_termux and master branches** To continue receiving updates for Snoop for Android/Termux, switch to the 'master' branch::  
 `$ git checkout master`.  

#! /usr/bin/env python3
# Copyright (c) 2020 Snoop Project <snoopproject@protonmail.com>

import argparse
import base64
import certifi
import click
import csv
import glob
import itertools
import json
import locale
import networktest
import os
import platform
import psutil
import random
import re
import requests
import shutil
import signal
import subprocess
import sys
import time
import webbrowser

from collections import Counter
from colorama import Fore, Style, init
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed, TimeoutError
from multiprocessing import active_children
from playsound import playsound
from rich.progress import BarColumn, SpinnerColumn, TimeElapsedColumn, Progress
from rich.panel import Panel
from rich.style import Style as STL
from rich.console import Console
from rich.table import Table

import snoopbanner
import snoopplugins


if int(platform.python_version_tuple()[1]) >= 8:
    from importlib.metadata import version as version_lib
    python3_8 = True
else:
    python3_8 = False

Android = True if hasattr(sys, 'getandroidapilevel') else False
Windows = True if sys.platform == 'win32' else False
Linux = True if Android is False and Windows is False else False


try:
    if os.environ.get('LANG') is not None and 'ru' in os.environ.get('LANG'):
        rus_unix = True
    else:
        rus_unix = False
    if Windows and "1251" in locale.setlocale(locale.LC_ALL):
        rus_windows = True
    else:
        rus_windows = False
except Exception:
    rus_unix = False
    rus_windows = False


locale.setlocale(locale.LC_ALL, '')
init(autoreset=True)
console = Console()


vers, vers_code, demo_full = 'v1.3.7c', "s", "d"

print(f"""\033[36m
  ___|
\___ \  __ \   _ \   _ \  __ \  
      | |   | (   | (   | |   | 
_____/ _|  _|\___/ \___/  .__/  
                         _|    \033[0m \033[37m\033[44m{vers}\033[0m
""")

_sb = "build" if vers_code == 'b' else "source"
__sb = "demo" if demo_full == 'd' else "full"

if Windows: OS_ = f"ru Snoop for Windows {_sb} {__sb}"
elif Android: OS_ = f"ru Snoop for Termux source {__sb}"
elif Linux: OS_ = f"ru Snoop for GNU/Linux {_sb} {__sb}"

version = f"{vers}_{OS_}"

print(Fore.CYAN + "#Примеры:" + Style.RESET_ALL)
if Windows:
    print(Fore.CYAN + " cd с:\\<path>\\snoop")
    print(Fore.CYAN + " python snoop.py --help" + Style.RESET_ALL, "#справка")
    print(Fore.CYAN + " python snoop.py nickname" + Style.RESET_ALL, "#поиск user-a")
    print(Fore.CYAN + " python snoop.py --module" + Style.RESET_ALL, "#задействовать плагины")
else:
    print(Fore.CYAN + " cd ~/snoop")
    print(Fore.CYAN + " python3 snoop.py --help" + Style.RESET_ALL, "#справка")
    print(Fore.CYAN + " python3 snoop.py nickname" + Style.RESET_ALL, "#поиск user-a")
    print(Fore.CYAN + " python3 snoop.py --module" + Style.RESET_ALL, "#задействовать плагины")
console.rule(characters="=", style="cyan")
print("")


## Date +%s конвертер.
e_mail = 'demo: snoopproject@protonmail.com'
# лицензия: год/месяц/число.
license = 'лицензия'
ts = (2024, 3, 5, 3, 0, 0, 0, 0, 0)
date_up = int(time.mktime(ts))  #дата в секундах с начала эпохи
up1 = time.gmtime(date_up)
Do = (f"{up1.tm_mday}/{up1.tm_mon}/{up1.tm_year}")  #в UTC (-3 часа)
# Чек.
if time.time() > int(date_up):
    print(Style.BRIGHT + Fore.RED + "Версия Snoop " + version + " деактивирована согласно лицензии.")
    sys.exit()


BDdemo = snoopbanner.DB('BDdemo')
BDflag = snoopbanner.DB('BDflag')
flagBS = len(BDdemo)
timestart = time.time()
time_date = time.localtime()
censors = 0
censors_timeout = 0
recensor = 0
lame_workhorse = False
d_g_l = []
symbol_bad = re.compile("[^a-zA-Zа-яА-Я\_\s\d\%\@\-\.\+]")


## Создание директорий результатов.
if Windows:
    dirhome = os.environ['LOCALAPPDATA'] + "\\snoop"
elif Android:
    try:
        dirhome = "/data/data/com.termux/files/home/storage/shared/snoop"
    except Exception:
        dirhome = os.environ['HOME'] + "/snoop"
elif Linux:
    dirhome = os.environ['HOME'] + "/snoop"

dirresults = os.getcwd()
dirpath = dirresults if 'source' in version and not Android else dirhome

os.makedirs(f"{dirpath}/results", exist_ok=True)
os.makedirs(f"{dirpath}/results/nicknames/html", exist_ok=True)
os.makedirs(f"{dirpath}/results/nicknames/txt", exist_ok=True)
os.makedirs(f"{dirpath}/results/nicknames/csv", exist_ok=True)
os.makedirs(f"{dirpath}/results/nicknames/save reports", exist_ok=True)
os.makedirs(f"{dirpath}/results/plugins/ReverseVgeocoder", exist_ok=True)
os.makedirs(f"{dirpath}/results/plugins/Yandex_parser", exist_ok=True)
os.makedirs(f"{dirpath}/results/plugins/domain", exist_ok=True)


## Вывести на печать инфостроку.
def info_str(infostr, nick, color=True):
    if color is True:
        print(f"{Fore.GREEN}[{Fore.YELLOW}*{Fore.GREEN}] {infostr}{Fore.RED} <{Fore.WHITE} {nick} {Fore.RED}>{Style.RESET_ALL}")
    else:
        print(f"\n[*] {infostr} < {nick} >")


## Вывести на печать ошибки.
def print_error(websites_names, errstr, country_code, errX, verbose=False, color=True):
    if color is True:
        print(f"{Style.RESET_ALL}{Fore.RED}[{Style.BRIGHT}{Fore.RED}-{Style.RESET_ALL}{Fore.RED}]{Style.BRIGHT}" \
              f"{Fore.GREEN} {websites_names}: {Style.BRIGHT}{Fore.RED}{errstr}{country_code}{Fore.YELLOW} {errX if verbose else ''}")
        try:
            if 'source' in version:
                playsound('err.wav')
        except Exception:
            pass
    else:
        print(f"[!] {websites_names}: {errstr}{country_code} {errX if verbose else ''}")


## Вывод на печать на разных платформах, индикация.
def print_found_country(websites_names, url, country_Emoj_Code, response_time=False, verbose=False, color=True):
    """Вывести на печать аккаунт найден."""
    if color is True and Windows:
        print(f"{Style.RESET_ALL}{Style.BRIGHT}{Fore.CYAN}{country_Emoj_Code}" \
              f"{Fore.GREEN}  {websites_names}:{Style.RESET_ALL}{Fore.GREEN} {url}{Style.RESET_ALL}")
    elif color is True and not Windows:
        print(f"{Style.RESET_ALL}{country_Emoj_Code}{Style.BRIGHT}{Fore.GREEN}  {websites_names}: " \
              f"{Style.RESET_ALL}{Style.DIM}{Fore.GREEN}{url}{Style.RESET_ALL}")
    else:
        print(f"[+] {websites_names}: {url}")


def print_not_found(websites_names, verbose=False, color=True):
    """Вывести на печать аккаунт не найден."""
    if color is True:
        print(f"{Style.RESET_ALL}{Fore.CYAN}[{Style.BRIGHT}{Fore.RED}-{Style.RESET_ALL}{Fore.CYAN}]" \
              f"{Style.BRIGHT}{Fore.GREEN} {websites_names}: {Style.BRIGHT}{Fore.YELLOW}Увы!{Style.RESET_ALL}")
    else:
        print(f"[-] {websites_names}: Увы!")


## Вывести на печать пропуск сайтов по блок. маске в имени username, gray_list, и пропуск по проблеме с openssl.
def print_invalid(websites_names, message, color=True):
    """Ошибка вывода nickname и gray list"""
    if color is True:
        print(f"{Style.RESET_ALL}{Fore.RED}[{Style.BRIGHT}{Fore.RED}-{Style.RESET_ALL}{Fore.RED}]" \
              f"{Style.BRIGHT}{Fore.GREEN} {websites_names}: {Style.RESET_ALL}{Fore.YELLOW}{message}")
    else:
        print(f"[-] {websites_names}: {message}")


## Вернуть результат future for2.
# Логика: возврат ответа и дуб_метода (из 4-х) в случае успеха, иначе возврат несуществующего метода для повторного запроса.
def request_res(request_future, error_type, websites_names, timeout=None, norm=False,
                print_found_only=False, verbose=False, color=True, country_code=''):
    global censors_timeout, censors
    try:
        res = request_future.result(timeout=timeout + 4)
        if res.status_code:
            return res, error_type, res.elapsed
    except requests.exceptions.HTTPError as err1:
        if norm is False and print_found_only is False:
            print_error(websites_names, "HTTP Error", country_code, err1, verbose, color)
    except requests.exceptions.ConnectionError as err2:
        censors += 1
        if norm is False and ('aborted' in str(err2) or 'None: None' in str(err2) or "SSLZeroReturnError" in str(err2)):
            if print_found_only is False:
                print_error(websites_names, "Ошибка соединения", country_code, err2, verbose, color)
            return "FakeNone", "", -1
        else:
            if norm is False and print_found_only is False:
                print_error(websites_names, "Censorship | SSL", country_code, err2, verbose, color)
    except (requests.exceptions.Timeout, TimeoutError) as err3:
        censors_timeout += 1
        if norm is False and print_found_only is False:
            print_error(websites_names, "Timeout ошибка", country_code, err3, verbose, color)
    except requests.exceptions.RequestException as err4:
        if norm is False and print_found_only is False:
            print_error(websites_names, "Непредвиденная ошибка", country_code, err4, verbose, color)
    return None, "Great Snoop returns None", -1

## Сохранение отчетов опция (-S).
def new_session(url, headers, executor2, requests_future, error_type, username, websites_names, r, t):
    future2 = executor2.submit(requests_future.get, url=url, headers=headers, allow_redirects=True, timeout=t)
    response = future2.result(t + 2)
    session_size = len(response.content)  #подсчет извлеченных данных
    return response, session_size

def sreports(url, headers, executor2, requests_future, error_type, username, websites_names, r):
    os.makedirs(f"{dirpath}/results/nicknames/save reports/{username}", exist_ok=True)

    if r.encoding == "cp-1251":
        r.encoding = "cp1251"
    elif r.encoding == "cp-1252":
        r.encoding = "cp1252"
    elif r.encoding == "windows1251":
        r.encoding = "windows-1251"
    elif r.encoding == "windows1252":
        r.encoding = "windows-1252"

#Сохранять отчеты для метода: redirection.
    if error_type == "redirection":
        try:
            response, session_size = new_session(url, headers, executor2, requests_future,
                                                 error_type, username, websites_names, r, t=4)
        except requests.exceptions.ConnectionError:
            time.sleep(0.1)
            try:
                response, session_size = new_session(url, headers, executor2, requests_future,
                                                     error_type, username, websites_names, r, t=2)
            except Exception:
                session_size = 'Err'  #подсчет извлеченных данных
        except Exception:
            session_size = 'Err'
#Сохранять отчеты для всех остальных методов: status; response; message со стандартными параметрами.
    try:
        with open(f"{dirpath}/results/nicknames/save reports/{username}/{websites_names}.html", 'w', encoding=r.encoding) as rep:
            if 'response' in locals():
                rep.write(response.text)
            elif error_type == "redirection" and 'response' not in locals():
                rep.write("❌ Snoop Project bad_save, timeout")
            else:
                rep.write(r.text)
    except Exception:
        console.log(snoopbanner.err_all(err_="low"), f"\nlog --> [{websites_names}:[bold red] {r.encoding}[/bold red]]")

    if error_type == "redirection":
        return session_size

## Основная функция.
def snoop(username, BDdemo_new, verbose=False, norm=False, reports=False, user=False, country=False,
          print_found_only=False, timeout=None, color=True, cert=False, headerS=None):
# Печать первой инфостроки.
    if '%20' in username:
        username_space = re.sub("%20", " ", username)
        info_str("разыскиваем:", username_space, color)
    else:
        info_str("разыскиваем:", username, color)

    if len(username) < 3:
        console.print(f"⛔️ [bold red]nickname не может быть короче 3-х символов\nПропуск\n")
        return False, False

    username = re.sub(" ", "%20", username)


## Предотвращение 'DDoS' из-за невалидных логинов; номеров телефонов, ошибок поиска из-за спецсимволов.
    with open('domainlist.txt', 'r', encoding="utf-8") as err:
        ermail = err.read().splitlines()

        username_bad = username.rsplit(sep='@', maxsplit=1)
        username_bad = '@bro'.join(username_bad).lower()

        for ermail_iter in ermail:
            if ermail_iter.lower() == username.lower():
                print(f"\n{Style.BRIGHT}{Fore.RED}⛔️ Bad nickname: '{ermail_iter}' (обнаружен чистый домен)\nпропуск\n")
                return False, False
            elif ermail_iter.lower() in username.lower():
                usernameR = username.rsplit(sep=ermail_iter.lower(), maxsplit=1)[1]
                username = username.rsplit(sep='@', maxsplit=1)[0]

                if len(username) == 0: username = usernameR
                print(f"\n{Fore.CYAN}Обнаружен E-mail адрес, извлекаем nickname: '{Style.BRIGHT}{Fore.CYAN}{username}{Style.RESET_ALL}" + \
                      f"{Fore.CYAN}'\nsnoop способен отличать e-mail от логина, например, поиск '{username_bad}'\n" + \
                      f"не является валидной электропочтой, но может существовать как nickname, следовательно — не будет обрезан\n")

                if len(username) == 0 and len(usernameR) == 0:
                    print(f"\n{Style.BRIGHT}{Fore.RED}⛔️ Bad nickname: '{ermail_iter}' (обнаружен чистый домен)\nпропуск\n")
                    return False, False

        del ermail


    err_nick = re.findall(symbol_bad, username)
    if err_nick:
        print(f"⛔️ {Style.BRIGHT + Fore.RED}Недопустимые символы в nickname: {Style.RESET_ALL}" + \
              f"{Fore.RED}{err_nick}{Style.RESET_ALL}\n{Style.BRIGHT + Fore.RED}Пропуск\n")
        return False, False


    ernumber = ['76', '77', '78', '79', '89', "38", "37", "9", "+"]
    if any(ernumber in username[0:2] for ernumber in ernumber):
        if len(username) >= 10 and len(username) <= 13 and username[1:].isdigit() is True:
            print(Style.BRIGHT + Fore.RED + "⛔️ Snoop выслеживает учётки пользователей, но не номера телефонов...\nпропуск\n")
            return False, False
    elif '.' in username and '@' not in username:
        print(Style.BRIGHT + Fore.RED + "⛔️ nickname, содержащий [.] и не являющийся email, невалидный...\nпропуск\n")
        return False, False


    global nick
    nick = username.replace("%20", " ")  #username 2-переменные (args/info)

## Создать многопоточный/процессный сеанс для всех запросов.
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
    requests.packages.urllib3.disable_warnings()
    requests_future = requests.Session()
    requests_future.verify = False if cert is False else True

    if Android:
        try:
            proc_ = len(BDdemo_new) if len(BDdemo_new) < 17 else 17
            executor1 = ProcessPoolExecutor(max_workers=proc_)
            #raise Exception("")
        except Exception:
            console.log(snoopbanner.err_all(err_="high"))
            global lame_workhorse
            lame_workhorse = True
            executor1 = ThreadPoolExecutor(max_workers=8)
    elif Windows:
        if norm is False:
            tread__ = len(BDdemo_new) if len(BDdemo_new) < 12 else 12
        else:
            tread__ = len(BDdemo_new) if len(BDdemo_new) < 16 else 16
        executor1 = ThreadPoolExecutor(max_workers=tread__)
    elif Linux:
        if norm is False:
            proc_ = len(BDdemo_new) if len(BDdemo_new) < 25 else 25
        else:
            proc_ = len(BDdemo_new) if len(BDdemo_new) < 27 else 27
        executor1 = ProcessPoolExecutor(max_workers=proc_)

    if reports:
        executor2 = ThreadPoolExecutor(max_workers=1)
    if norm is False:
        executor3 = ThreadPoolExecutor(max_workers=1)

## Результаты анализа всех сайтов.
    dic_snoop_full = {}
## Создание futures на все запросы. Это позволит распараллелить запросы с прерываниями.
    for websites_names, param_websites in BDdemo_new.items():
        results_site = {}
        # param_websites.pop('comments', None)
        results_site['flagcountry'] = param_websites.get("country")
        results_site['flagcountryklas'] = param_websites.get("country_klas")
        results_site['url_main'] = param_websites.get("urlMain")
        # username = param_websites.get("usernameON")

# Пользовательский user-agent браузера (рандомно на каждый сайт), а при сбое — постоянный с расширенным заголовком.
        majR = random.choice(range(97, 107, 1))
        minR = random.choice(range(2683, 4606, 13))
        patR = random.choice(range(52, 99, 1))
        RandHead=([f"{{'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) " + \
                   f"Chrome/{majR}.0.{minR}.{patR} Safari/537.36'}}",
                   f"{{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) " + \
                   f"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{majR}.0.{minR}.{patR} Safari/537.36'}}"])
        RH = random.choice(RandHead)
        headers = json.loads(RH.replace("'", '"'))

# Переопределить/добавить любые дополнительные заголовки, необходимые для данного сайта из БД или cli.
        if "headers" in param_websites:
            headers.update(param_websites["headers"])
        if headerS is not None:
            headers.update({"User-Agent": ''.join(headerS)})
        #console.print(headers, websites_names)  #проверка u-агентов

# Пропуск временно-отключенного сайта и не делать запрос, если имя пользователя не подходит для сайта.
        exclusionYES = param_websites.get("exclusion")
        if exclusionYES and re.search(exclusionYES, username) or param_websites.get("bad_site") == 1:
            if exclusionYES and re.search(exclusionYES, username) and not print_found_only and not norm:
                print_invalid(websites_names, f"недопустимый ник '{nick}' для данного сайта", color)
            results_site["exists"] = "invalid_nick"
            results_site["url_user"] = '*' * 56
            results_site['countryCSV'] = "****"
            results_site['http_status'] = '*' * 10
            results_site['session_size'] = ""
            results_site['check_time_ms'] = '*' * 15
            results_site['response_time_ms'] = '*' * 15
            results_site['response_time_site_ms'] = '*' * 25
            if param_websites.get("bad_site") == 1 and verbose and not print_found_only and not norm:
                print_invalid(websites_names, f"**Пропуск. Dynamic gray_list", color)
            if param_websites.get("bad_site") == 1:
                d_g_l.append(websites_names)
                results_site["exists"] = "gray_list"
        else:
# URL пользователя на сайте (если он существует).
            url = param_websites["url"].format(username)
            results_site["url_user"] = url
            url_API = param_websites.get("urlProbe")
# Использование api/nickname.
            url_API = url if url_API is None else url_API.format(username)

# Если нужен только статус кода, не загружать тело страницы, экономим память для status/redirect методов.
            if reports or param_websites["errorTypе"] == 'message' or param_websites["errorTypе"] == 'response_url':
                request_method = requests_future.get
            else:
                request_method = requests_future.head

# Сайт перенаправляет запрос на другой URL.
# Имя найдено. Запретить перенаправление чтобы захватить статус кода из первоначального url.
            if param_websites["errorTypе"] == "response_url" or param_websites["errorTypе"] == "redirection":
                allow_redirects = False
# Разрешить любой редирект, который хочет сделать сайт и захватить тело и статус ответа.
            else:
                allow_redirects = True

# Отправить параллельно все запросы и сохранить future для последующего доступа.
            param_websites["request_future"] = executor1.submit(request_method, url=url_API, headers=headers,
                                                                allow_redirects=allow_redirects, timeout=timeout)
# Добавлять во вл. словарь future со всеми другими результатами.
        dic_snoop_full[websites_names] = results_site


## Прогресс_описание.
    if not verbose:
        if not Windows:
            spin_emoj = 'arrow3' if norm else random.choice(["dots", "dots12"])
            progress = Progress(TimeElapsedColumn(), SpinnerColumn(spinner_name=spin_emoj),
                                "[progress.percentage]{task.percentage:>1.0f}%", BarColumn(bar_width=None, complete_style='cyan',
                                finished_style='cyan bold'), refresh_per_second=3.0)  #transient=True) #исчезает прогресс
        else:
            progress = Progress(TimeElapsedColumn(), "[progress.percentage]{task.percentage:>1.0f}%", BarColumn(bar_width=None,
                                complete_style='cyan', finished_style='cyan bold'), refresh_per_second=3.0)  #auto_refresh=False)
    else:
        progress = Progress(TimeElapsedColumn(), "[progress.percentage]{task.percentage:>1.0f}%", auto_refresh=False)  #refresh_per_second=3
# Панель вербализации.
        if not Android:
            if color:
                console.print(Panel("[yellow]об.время[/yellow] | [magenta]об.% выполн.[/magenta] | [bold cyan]отклик сайта[/bold cyan] " + \
                                    "| [bold red]цвет.[bold cyan]об[/bold cyan].скор.[/bold red] | [bold cyan]разм.расп.данных[/bold cyan]",
                                    title="Обозначение", style=STL(color="cyan")))
            else:
                console.print(Panel("об.время | об.% выполн. | отклик сайта | цвет.об.время | разм.расп.данных", title="Обозначение"))
        else:
            if color:
                console.print(Panel("[yellow]time[/yellow] | [magenta]perc.[/magenta] | [bold cyan]response [/bold cyan] " + \
                                    "| [bold red]joint[bold cyan].[/bold cyan]rate[/bold red] | [bold cyan]data[/bold cyan]",
                                    title="Designation", style=STL(color="cyan")))
            else:
                console.print(Panel("time | perc. | response | joint.rate | data", title="Designation"))


## Пройтись по массиву future и получить результаты.
    li_time = [0]
    with progress:
        if color is True:
            task0 = progress.add_task("", total=len(BDdemo_new))
        for websites_names, param_websites in BDdemo_new.items():  #БД:-скоррект.Сайт--> флаг,эмодзи,url, url_сайта, gray_lst, запрос-future
            #print(round(psutil.virtual_memory().available / 1024 / 1024), "Мб")
            if color is True:
                progress.update(task0, advance=1, refresh=True)  #\nprogress.refresh()
# Получить другую информацию сайта, снова.
            url = dic_snoop_full.get(websites_names).get("url_user")
            country_emojis = dic_snoop_full.get(websites_names).get("flagcountry")
            country_code = dic_snoop_full.get(websites_names).get("flagcountryklas")
            country_Emoj_Code = country_emojis if not Windows else country_code
# Пропустить запрещенный никнейм или пропуск сайта из gray-list.
            if dic_snoop_full.get(websites_names).get("exists") is not None:
                continue
# Получить ожидаемый тип данных 4-х методов.
            error_type = param_websites["errorTypе"]
# Получить результаты future.
            r, error_type, response_time = request_res(request_future=param_websites["request_future"], norm=norm,
                                                       error_type=error_type, websites_names=websites_names,
                                                       print_found_only=print_found_only, verbose=verbose,
                                                       color=color, timeout=timeout, country_code=f" ~{country_code}")

# Повторное сбойное соединение через новую сессию быстрее, чем через adapter.
            if norm is False and r == "FakeNone":
                global recensor
                head_duble = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                              'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                              'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)' + \
                                            'Chrome/76.0.3809.100 Safari/537.36'}

                for _ in range(3):
                    recensor += 1
                    future_rec = executor3.submit(requests_future.get, url=url, headers=head_duble,
                                                  allow_redirects=allow_redirects, timeout=2.9)
                    if color is True and print_found_only is False:
                        print(f"{Style.RESET_ALL}{Fore.CYAN}[{Style.BRIGHT}{Fore.RED}-{Style.RESET_ALL}{Fore.CYAN}]" \
                              f"{Style.DIM}{Fore.GREEN}    └──повторное соединение{Style.RESET_ALL}")
                    else:
                        if print_found_only is False:
                            print("повторное соединение")

                    r, error_type, response_time = request_res(request_future=future_rec, error_type=param_websites.get("errorTypе"),
                                                               websites_names=websites_names, print_found_only=print_found_only,
                                                               verbose=verbose, color=color, timeout=2.5, country_code=f" ~{country_code}")

                    if r != "FakeNone":
                        break


## Проверка, 4 методов; #1.
# Ответы message (разные локации).
            if error_type == "message":
                try:
                    if param_websites.get("encoding") is not None:
                        r.encoding = param_websites.get("encoding")
                except Exception:
                    console.log(snoopbanner.err_all(err_="high"))
                error = param_websites.get("errorMsg")
                error2 = param_websites.get("errоrMsg2")
                error3 = param_websites.get("errorMsg3") if param_websites.get("errorMsg3") is not None else "FakeNoneNoneNone"
                if param_websites.get("errorMsg2"):
                    sys.exit()
#                print(r.text) #проверка ответа (+- '-S')
#                print(r.status_code) #Проверка ответа
                if r.status_code > 200 and param_websites.get("ignore_status_code") is None \
                                                             or (error2 in r.text or error in r.text or error3 in r.text):
                    if not print_found_only and not norm:
                        print_not_found(websites_names, verbose, color)
                    exists = "увы"
                else:
                    if not norm:
                        print_found_country(websites_names, url, country_Emoj_Code, response_time, verbose, color)
                    exists = "найден!"
                    if reports:
                        sreports(url, headers, executor2, requests_future, error_type, username, websites_names, r)
## Проверка, 4 методов; #2.
# Проверка username при статусе 301 и 303 (перенаправление и соль).
            elif error_type == "redirection":
#                print(r.text) #проверка ответа (+- '-S')
#                print(r.status_code) #Проверка ответа
                if r.status_code == 301 or r.status_code == 303:
                    if not norm:
                        print_found_country(websites_names, url, country_Emoj_Code, response_time, verbose, color)
                    exists = "найден!"
                    if reports:
                        session_size = sreports(url, headers, executor2, requests_future, error_type, username, websites_names, r)
                else:
                    if not print_found_only and not norm:
                        print_not_found(websites_names, verbose, color)
                        session_size = len(str(r.content))
                    exists = "увы"
## Проверка, 4 методов; #3.
# Проверяет, является ли код состояния ответа 2..
            elif error_type == "status_code":
#                print(r.text) #проверка ответа (+- '-S')
#                print(r.status_code) #Проверка ответа
                if not r.status_code >= 300 or r.status_code < 200:
                    if not norm:
                        print_found_country(websites_names, url, country_Emoj_Code, response_time, verbose, color)
                    if reports:
                        sreports(url, headers, executor2, requests_future, error_type, username, websites_names, r)
                    exists = "найден!"
                else:
                    if not print_found_only and not norm:
                        print_not_found(websites_names, verbose, color)
                    exists = "увы"
## Проверка, 4 методов; #4
# Перенаправление.
            elif error_type == "response_url":
#                print(r.text) #проверка ответа (+- '-S')
#                print(r.status_code) #Проверка ответа
                if 200 <= r.status_code < 300:
                    if not norm:
                        print_found_country(websites_names, url, country_Emoj_Code, response_time, verbose, color)
                    if reports:
                        sreports(url, headers, executor1, requests_future, error_type, username, websites_names, r)
                    exists = "найден!"
                else:
                    if not print_found_only and not norm:
                        print_not_found(websites_names, verbose, color)
                    exists = "увы"
## Если все 4 метода не сработали, например, из-за ошибки доступа (красный) или из-за неизвестной ошибки.
            else:
                exists = "блок"


## Попытка получить информацию из запроса.
            try:
                http_status = r.status_code  #запрос статус-кода.
            except Exception:
                http_status = "сбой"

            try:  #сессия в КБ
                if reports is True:
                    session_size = session_size if error_type == 'redirection' else len(str(r.content))
                else:
                    session_size = len(str(r.content))

                if session_size >= 555:
                    session_size = round(session_size / 1024)
                elif session_size < 555:
                    session_size = round((session_size / 1024), 2)
            except Exception:
                session_size = "Err"


## Считать 2x-тайминги с приемлемой точностью.
# Реакция.
            ello_time = round(float(time.time() - timestart), 2)  #текущее
            li_time.append(ello_time)
            dif_time = round(li_time[-1] - li_time[-2], 2)  #разница
# Отклик.
            try:
                site_time = str(response_time).rsplit(sep=':', maxsplit=1)[1]
                site_time = round(float(site_time), 2)  #реальный ответ
            except Exception:
                site_time = str("-")


## Опция '-v'.
            if verbose is True:
                if session_size == 0 or session_size is None:
                    Ssession_size = "Head"
                elif session_size == "Err":
                    Ssession_size = "Нет"
                else:
                    Ssession_size = str(session_size) + " Kb"

                if color is True:
                    if dif_time > 2.7 and dif_time != ello_time:  #задержка в общем времени
                        console.print(f"[cyan] [*{site_time} s T] >>", f"[bold red][*{ello_time} s t]", f"[cyan][*{Ssession_size}]")
                        console.rule("", style="bold red")
                    else:
                        console.print(f"[cyan] [*{site_time} s T] >>", f"[cyan][*{ello_time} s t]", f"[cyan][*{Ssession_size}]")
                        console.rule("", style="bold blue")
                else:
                    console.print(f" [*{site_time} s T] >>", f"[*{ello_time} s t]", f"[*{Ssession_size}]", highlight=False)
                    console.rule(style="color")


## Служебная информация/CSV (2-й словарь 'объединение словарей', чтобы не вызывать ошибку длины 1-го при итерациях).
            if dif_time > 2.7 and dif_time != ello_time:
                dic_snoop_full.get(websites_names)['response_time_site_ms'] = str(dif_time)
            else:
                dic_snoop_full.get(websites_names)['response_time_site_ms'] = "нет"
            dic_snoop_full.get(websites_names)['exists'] = exists
            dic_snoop_full.get(websites_names)['session_size'] = session_size
            dic_snoop_full.get(websites_names)['countryCSV'] = country_code
            dic_snoop_full.get(websites_names)['http_status'] = http_status
            dic_snoop_full.get(websites_names)['check_time_ms'] = str(site_time)
            dic_snoop_full.get(websites_names)['response_time_ms'] = str(ello_time)
# Добавление результатов этого сайта в окончательный словарь со всеми другими результатами.
            dic_snoop_full[websites_names] = dic_snoop_full.get(websites_names)
# не удерживать сокетом отработанное по всем п. соединение с сервером.
            requests_future.close()
# Высвободить незначительную часть ресурсов.
        try:
            if 'executor2' in locals(): executor2.shutdown()
            if 'executor3' in locals(): executor3.shutdown()
        except Exception:
            console.log(snoopbanner.err_all(err_="low"))
# Вернуть словарь со всеми данными на запрос функции snoop и пробросить удерживаемые ресурсы (позже, закрыть в фоне).
        return dic_snoop_full, executor1


## Опция '-t'.
def timeout_check(value):
    try:
        global timeout
        timeout = int(value)
    except Exception:
        raise argparse.ArgumentTypeError(f"\n\033[31;1mTimeout '{value}' Err,\033[0m \033[36mукажите время в 'секундах'. \033[0m")
    if timeout <= 0:
        raise argparse.ArgumentTypeError(f"\033[31;1mTimeout '{value}' Err,\033[0m \033[36mукажите время > 0sec. \033[0m")
    return timeout


## Обновление Snoop.
def update_snoop():
    print("""
\033[36mВы действительно хотите:
                    __             _  
   ._  _| _._|_ _  (_ ._  _  _ ._   ) 
|_||_)(_|(_| |_(/_ __)| |(_)(_)|_) o  
   |                           |    
Выберите действие:\033[0m [y/n] """, end='')

    upd = input()

    if upd == "y":
        print("\033[36mФункция обновления Snoop требует установки утилиты < Git >\033[0m")
        os.startfile("update.bat") if Windows else os.system("./update.sh")
    print(Style.BRIGHT + Fore.RED + "\nВыход")
    sys.exit()


## Удаление отчетов.
def autoclean():
    print("""
\033[36mВы действительно хотите:\033[0m \033[31;1m
               _                _  
 _| _ |  _.|| |_) _ ._  _ .-_|_  ) 
(_|(/_| (_||| | \(/_|_)(_)|  |_ o  
                    |                      \033[0m
\033[36mВыберите действие:\033[0m [y/n] """, end='')

    del_all = input()

    if del_all == "y":
        try:
# Определение директорий.
            path_build_del = "/results" if not Windows else "\\results"
            rm = dirpath + path_build_del
# Подсчет файлов и размера удаляемого каталога 'results'.
            total_size = 0
            delfiles = []
            for total_file in glob.iglob(rm + '/**/*', recursive=True):
                total_size += os.path.getsize(total_file)
                if os.path.isfile(total_file): delfiles.append(total_file)
# Удаление каталога 'results'.
            shutil.rmtree(rm, ignore_errors=True)
            print(f"\n\033[31;1mdeleted --> {rm}\033[0m\033[36m {len(delfiles)} files, {round(total_size/1024/1024, 2)} Mb\033[0m")
        except Exception:
            console.log("[red]Ошибка")
    else:
        print(Style.BRIGHT + Fore.RED + "\nВыход")
    sys.exit()


## Лицензия/версия.
def license_snoop():
    with open('COPYRIGHT', 'r', encoding="utf8") as copyright:
        wl = 4
        if Windows:
            wl = 5 if int(platform.win32_ver()[0]) < 10 else 4

        cop = copyright.read().replace("\ufeffSnoop", "Snoop")
        cop = cop.replace('=' * 80, "~" * (os.get_terminal_size()[0] - wl)).strip()
        console.print(Panel(cop, title='[bold white]COPYRIGHT[/bold white]', style=STL(color="white", bgcolor="blue")))

    if not Android:
        if Windows and 'full' in version:
            ram_av = 2200
        elif Windows and 'demo' in version:
            ram_av = 650

        if Linux and 'full' in version:
            ram_av = 1200
        elif Linux and 'demo' in version:
            ram_av = 700

        try:
            ram = int(psutil.virtual_memory().total / 1024 / 1024)
            ram_free = int(psutil.virtual_memory().available / 1024 / 1024)
            if ram_free < ram_av:
                A, B = "[bold red]", "[/bold red]"
            else:
                A, B = "[dim cyan]", "[/dim cyan]"
            os_ver = platform.platform(aliased=True, terse=0)
            threadS = f"thread(s) per core: [dim cyan]{int(psutil.cpu_count() / psutil.cpu_count(logical=False))}[/dim cyan]"
        except Exception:
            console.print(f"\n[bold red]Используемая версия Snoop: '{version}' разработана для платформы Android, " + \
                          f"но кажется используется что-то другое 💻\n\nВыход")
            sys.exit()
    elif Android:
        try:
            ram = subprocess.check_output("free -m", shell=True, text=True).splitlines()[1].split()[1]
            ram_free = int(subprocess.check_output("free -m", shell=True, text=True).splitlines()[1].split()[-1])
            if ram_free <= 200:
                A, B = "[bold red]", "[/bold red]"
            else:
                A, B = "[dim cyan]", "[/dim cyan]"
            os_ver = 'Android ' + subprocess.check_output("getprop ro.build.version.release", shell=True, text=True).strip()
            threadS = f'model: [dim cyan]{subprocess.check_output("getprop ro.product.cpu.abi", shell=True, text=True).strip()}[/dim cyan]'
            T_v = dict(os.environ).get("TERMUX_VERSION")
        except:
            T_v, ram_free, os_ver, threadS, A, B = "Not Termux?!", "?", "?", "?", "[bold red]", "[/bold red]"
            ram = "pkg install procps |"

    termux = f"\nTermux: [dim cyan]{T_v}[/dim cyan]\n" if Android else "\n"

    if python3_8:
        colorama_v = f", (colorama::{version_lib('colorama')})"
        rich_v = f", (rich::{version_lib('rich')})"
        plays_v = f", (playsound::{version_lib('playsound')})"
        urllib3_v = f", (urllib3::{version_lib('urllib3')})"
        folium_v = f", (folium::{version_lib('folium')})" if not Android else ""
        numpy_v = f", (numpy::{version_lib('numpy')})" if not Android else ""
    else:
        urllib3_v = ""
        colorama_v = ""
        folium_v = ""
        numpy_v = ""
        rich_v = ""
        plays_v = ""

    console.print('\n', Panel(f"Program: [dim cyan]{version} {str(platform.architecture(executable=sys.executable, bits='', linkage=''))}" + \
                              "[/dim cyan]\n" + \
                              f"OS: [dim cyan]{os_ver}[/dim cyan]" + termux + \
                              f"Locale: [dim cyan]{locale.setlocale(locale.LC_ALL)}[/dim cyan]\n" + \
                              f"Python: [dim cyan]{platform.python_version()}[/dim cyan]\n" + \
                              f"Key libraries: [dim cyan](requests::{requests.__version__}), (certifi::{certifi.__version__}), " + \
                                             f"(speedtest::{networktest.speedtest.__version__}){rich_v}{plays_v}" + \
                                             f"{folium_v}{numpy_v}{colorama_v}{urllib3_v}[/dim cyan]\n" + \
                              f"CPU(s): [dim cyan]{os.cpu_count()},[/dim cyan] {threadS}\n" + \
                              f"Ram: [dim cyan]{ram} Мб,[/dim cyan] available: {A}{ram_free} Мб{B}",
                              title='[bold cyan]snoop info[/bold cyan]', style=STL(color="cyan")))
    sys.exit()


## ОСНОВА.
def run():
    web_sites = f"{len(BDflag) // 100}00+"
# Назначение опций Snoop.
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     usage="python3 snoop.py [search arguments...] nickname\nor\n" + \
                                            "usage: python3 snoop.py [service arguments | plugins arguments]\n",
                                     description=f"{Fore.CYAN}\nСправка{Style.RESET_ALL}",
                                     epilog=(f"{Fore.CYAN}Snoop {Style.BRIGHT}{Fore.RED}demo version {Style.RESET_ALL}" + \
                                             f"{Fore.CYAN}поддержка: \033[31;1m{flagBS}\033[0m \033[36mWebsites!\n{Fore.CYAN}" + \
                                             f"Snoop \033[36;1mfull version\033[0m \033[36mподдержка: \033[36;1m{web_sites} \033[0m" + \
                                             f"\033[36mWebsites!!!\033[0m\n\n"))
# Service arguments.
    service_group = parser.add_argument_group('\033[36mservice arguments\033[0m')
    service_group.add_argument("--version", "-V", action="store_true",
                               help="\033[36mA\033[0mbout: вывод на печать версий:: OS; Snoop; Python и Лицензии"
                              )
    service_group.add_argument("--list-all", "-l", action="store_true", dest="listing",
                               help="\033[36mВ\033[0mывести на печать детальную информацию о базе данных Snoop"
                              )
    service_group.add_argument("--donate", "-d", action="store_true", dest="donation",
                               help="\033[36mП\033[0mожертвовать на развитие Snoop Project-а, получить/приобрести \
                                     \033[32;1mSnoop full version\033[0m"
                              )
    service_group.add_argument("--autoclean", "-a", action="store_true", dest="autoclean", default=False,
                               help="\033[36mУ\033[0mдалить все отчеты, очистить место"
                              )
    service_group.add_argument("--update", "-U", action="store_true", dest="update",
                               help="\033[36mО\033[0mбновить Snoop"
                              )
# Plugins arguments arguments.
    plugins_group = parser.add_argument_group('\033[36mplugins arguments\033[0m')
    plugins_group.add_argument("--module", "-m", action="store_true", dest="module", default=False,
                               help="\033[36mO\033[0mSINT поиск: задействовать различные плагины Snoop:: IP/GEO/YANDEX"
                              )
# Search arguments.
    search_group = parser.add_argument_group('\033[36msearch arguments\033[0m')
    search_group.add_argument("username", nargs='*', metavar='nickname', action="store", default=None,
                              help="\033[36mН\033[0mикнейм разыскиваемого пользователя. \
                                    Поддерживается поиск одновременно нескольких имен.\
                                    Ник, содержащий в своем имени пробел, заключается в кавычки"
                             )
    search_group.add_argument("--verbose", "-v", action="store_true", dest="verbose", default=False,
                              help="\033[36mВ\033[0mо время поиска 'nickname' выводить на печать подробную вербализацию"
                             )
    search_group.add_argument("--base", "-b <file>", dest="json_file", default="BDdemo", metavar='',
                              #help="\033[36mУ\033[0mказать для поиска 'nickname' другую БД (Локально)/В demo version функция отключена"
                              help=argparse.SUPPRESS
                             )
    search_group.add_argument("--web-base", "-w", action="store_true", dest="web", default=False,
                              help=f"\033[36mП\033[0mодключиться для поиска 'nickname' к динамично-обновляемой web_БД ({web_sites} сайтов).\
                                     В demo version функция отключена"
                             )
    search_group.add_argument("--site", "-s <site_name>", action="append", metavar='', dest="site_list", default=None,
                              help="\033[36mУ\033[0mказать имя сайта из БД '--list-all'. Поиск 'nickname' на одном указанном ресурсе, \
                                    допустимо использовать опцию '-s' несколько раз"
                             )
    search_group.add_argument("--exclude", "-e <country_code>", action="append", metavar='', dest="exclude_country", default=None,
                              help="\033[36mИ\033[0mсключить из поиска выбранный регион, \
                                    допустимо использовать опцию '-e' несколько раз, например, '-e RU -e WR' исключить из поиска Россию и Мир"
                             )
    search_group.add_argument("--include", "-i <country_code>", action="append", metavar='', dest="one_level", default=None,
                              help="\033[36mВ\033[0mключить в поиск только выбранный регион, \
                                    допустимо использовать опцию '-i' несколько раз, например, '-i US -i UA' поиск по США и Украине"
                             )
    search_group.add_argument("--country-sort", "-c", action="store_true", dest="country", default=False,
                              help="\033[36mП\033[0mечать и запись результатов по странам, а не по алфавиту"
                             )
    search_group.add_argument("--time-out", "-t <digit>", action="store", metavar='', dest="timeout", type=timeout_check, default=9,
                              help="\033[36mУ\033[0mстановить выделение макс.времени на ожидание ответа от сервера (секунды).\n"
                                   "Влияет на продолжительность поиска. Влияет на 'Timeout ошибки'.\
                                    Вкл. эту опцию необходимо при медленном интернет соединении (по умолчанию 9с)"
                             )
    search_group.add_argument("--found-print", "-f", action="store_true", dest="print_found_only", default=False,
                              help="\033[36mВ\033[0mыводить на печать только найденные аккаунты"
                             )
    search_group.add_argument("--no-func", "-n", action="store_true", dest="no_func", default=False,
                              help="\033[36m✓\033[0mМонохромный терминал, не использовать цвета в url \
                                    ✓Отключить звук\
                                    ✓Запретить открытие web browser-а\
                                    ✓Отключить вывод на печать флагов стран\
                                    ✓Отключить индикацию и статус прогресса"
                             )
    search_group.add_argument("--userlist", "-u <file>", metavar='', action="store", dest="user", default=False,
                              help="\033[36mУ\033[0mказать файл со списком user-ов. Snoop интеллектуально обработает \
                                    данные и предоставит доп.отчеты"
                             )
    search_group.add_argument("--save-page", "-S", action="store_true", dest="reports", default=False,
                              help="\033[36mС\033[0mохранять найденные странички пользователей в локальные html-файлы"
                             )
    search_group.add_argument("--cert-on", "-C", default=False, action="store_true", dest="cert",
                              help="""\033[36mВ\033[0mкл проверку сертификатов на серверах. По умолчанию проверка сертификатов
                                      на серверах отключена, что позволяет обрабатывать проблемные сайты без ошибок"""
                             )
    search_group.add_argument("--headers", "-H <User-Agent>", metavar='', dest="headerS", nargs=1, default=None,
                              help="""\033[36mЗ\033[0mадать user-agent вручную, агент заключается в кавычки, по умолчанию для каждого сайта
                                      задается случайный либо переопределенный user-agent из БД snoop"""
                             )
    search_group.add_argument("--quick", "-q", action="store_true", dest="norm", default=False,
                              help="""\033[36mБ\033[0mыстрый и агрессивный режим поиска.
                                      Не обрабатывает повторно сбойные ресурсы, в следствие чего, ускоряется поиск, но и повышается Bad_raw.
                                      Не выводит промежуточные результаты на печать. Потребляет больше ресурсов.
                                      Режим эффективен в full version"""
                             )

    args = parser.parse_args()
    # print(args)


## Опции  '-cseo' несовместимы между собой и быстрый режим.
    if args.norm and 'full' in version:
        print(Fore.CYAN + "[+] активирована опция '-q': «быстрый режим поиска»\n")
        args.version, args.listing, args.donation, args.autoclean = False, False, False, False
        args.update, args.module, args.autoclean = False, False, False

        options = []
        options.append(args.site_list)
        options.append(args.country)
        options.append(args.verbose)
        options.append(args.print_found_only)
        options.append(args.no_func)
        options.append(args.reports)
        options.append(args.cert)
        options.append(args.headerS)

        if any(options) or args.timeout != 9:
            snoopbanner.logo(text="⛔️ с quick-режимом ['-q'] совместимы лишь опции ['-w', '-u', '-e', '-i']")
    elif args.norm and 'demo' in version:
        snoopbanner.logo(text="[-] в demo деактивирован переключатель '-q': «режимов SNOOPninja/Quick»")
    elif args.norm is False and args.listing is False and 'full' in version:
        if Linux:
            print(Fore.CYAN + "[+] активирован дефолтный поиск '--': «режим SNOOPninja»")

    k = 0
    for _ in bool(args.site_list), bool(args.country), bool(args.exclude_country), bool(args.one_level):
        if _ is True:
            k += 1
        if k == 2:
            snoopbanner.logo(text="⛔️ опции ['-c', '-e' '-i', '-s'] несовместимы между собой")


## Опция  '-V' не путать с опцией '-v'.
    if args.version:
        license_snoop()


## Опция  '-a'.
    if args.autoclean:
        print(Fore.CYAN + "[+] активирована опция '-a': «удаление накопленных отчетов»\n")
        autoclean()


## Опция  '-H'.
    if args.headerS:
        print(f"{Fore.CYAN}[+] активирована опция '-H': «переопределение user-agent(s)»:" + '\n' + \
              f"    user-agent: '{Style.BRIGHT}{Fore.CYAN}{''.join(args.headerS)}{Style.RESET_ALL}{Fore.CYAN}'")


## Опция  '-m'.
# Информативный вывод.
    if args.module:
        print(Fore.CYAN + "[+] активирована опция '-m': «модульный поиск»")

        def module():
            print(f"\n" + \
                  f"\033[36m╭Выберите плагин или действие из списка\033[0m\n" + \
                  f"\033[36m├──\033[0m\033[36;1m[1] --> GEO_IP/domain\033[0m\n" + \
                  f"\033[36m├──\033[0m\033[36;1m[2] --> Reverse Vgeocoder\033[0m\n" + \
                  f"\033[36m├──\033[0m\033[36;1m[3] --> Yandex_parser\033[0m\n" + \
                  f"\033[36m├──\033[0m\033[32;1m[help] --> Справка\033[0m\n" + \
                  f"\033[36m└──\033[0m\033[31;1m[q] --> Выход\033[0m\n")

            mod = console.input("[cyan]ввод --->  [/cyan]")

            if mod == 'help':
                snoopbanner.help_module_1()
                return module()
            elif mod == '1':
                table = Table(title=Style.BRIGHT + Fore.GREEN + "Выбран плагин" + Style.RESET_ALL, style="green", header_style='green')
                table.add_column("GEO_IP/domain_v0.5", style="green", justify="center")
                table.add_row('Получение информации об ip/domain/url цели или по списку этих данных')
                console.print(table)

                snoopplugins.module1()
            elif mod == '2':
                table = Table(title=Style.BRIGHT + Fore.GREEN + "Выбран плагин" + Style.RESET_ALL, style="green", header_style='green')
                table.add_column("Reverse Vgeocoder_v0.5", style="green", justify="center")
                table.add_row('Визуализация Географических координат')
                console.print(table)

                snoopplugins.module2()
            elif mod == '3':
                table = Table(title=Style.BRIGHT + Fore.GREEN + "Выбран плагин" + Style.RESET_ALL, style="green", header_style='green')
                table.add_column("Yandex_parser_v0.5", style="green", justify="center")
                table.add_row('Яндекс парсер: Я_Отзывы; Я_Кью; Я_Маркет; Я_Музыка; Я_Дзен; Я_Диск; E-mail; Name.')
                console.print(table)

                snoopplugins.module3()
            elif mod == 'q':
                print(Style.BRIGHT + Fore.RED + "└──Выход")
                sys.exit()
            else:
                print(Style.BRIGHT + Fore.RED + "└──Неверный выбор\n" + Style.RESET_ALL)
                return module()

        module()
        sys.exit()


## Опция  '-f' + "-v".
    if args.verbose is True and args.print_found_only is True:
        snoopbanner.logo(text="⛔️ Режим подробной вербализации [опция '-v'] отображает детальную информацию,\n   [опция '-f'] неуместна")


## Опция  '-С'.
    if args.cert:
        print(Fore.CYAN + f"[+] активирована опция '-C': «проверка сертификатов на серверах вкл»")


## Опция  '-w'.
    if args.web:
        print(Fore.CYAN + "[+] активирована опция '-w': «подключение к внешней web_database»")


## Опция  '-S'.
    if args.reports:
        print(Fore.CYAN + "[+] активирована опция '-S': «сохранять странички найденных аккаунтов»")


## Опция  '-n'.
    if args.no_func:
        print(Fore.CYAN + "[+] активирована опция '-n': «отключены:: цвета; звук; флаги; браузер; прогресс»")


## Опция  '-t'.
    try:
        if args.timeout and args.norm is False:
            print(Fore.CYAN + f"[+] активирована опция '-t': «snoop будет ожидать ответа от " + \
                  f"сайта \033[36;1m<= {timeout}_sec\033[0m\033[36m.» \033[0m")
    except Exception:
        pass


## Опция '-f'.
    if args.print_found_only:
        print(Fore.CYAN + "[+] активирована опция '-f': «выводить на печать только найденные аккаунты»")


## Опция '-s'.
    if args.site_list:
        print(f"{Fore.CYAN}[+] активирована опция '-s': «поиск '{Style.BRIGHT}{Fore.CYAN}{', '.join(args.username)}{Style.RESET_ALL}" + \
              f"{Fore.CYAN}' на выбранных website(s)»\n" + \
              f"    допустимо использовать опцию '-s' несколько раз\n" + \
              f"    [опция '-s'] несовместима с [опциями '-с', '-e', '-i']")


## Опция '--list-all'.
    if args.listing:
        print(Fore.CYAN + "[+] активирована опция '-l': «детальная информация о БД snoop»")
        print("\033[36m\nСортировать БД Snoop по странам, по имени сайта или обобщенно ?\n" + \
              "по странам —\033[0m 1 \033[36mпо имени —\033[0m 2 \033[36mall —\033[0m 3\n")
        sortY = console.input("[cyan]Выберите действие: [/cyan]")

# Общий вывод стран (3!).
# Вывод для full/demo version.
        def sort_list_all(DB, fore, version, line=None):
            listfull = []
            if sortY == "3":
                if line == "str_line":
                    console.rule("[cyan]Ok, print All Country:", style="cyan bold")
                print("")
                li = [DB.get(con).get("country_klas") if Windows else DB.get(con).get("country") for con in DB]
                cnt = str(Counter(li))
                try:
                    flag_str_sum = (cnt.split('{')[1]).replace("'", "").replace("}", "").replace(")", "")
                    all_ = str(len(DB))
                except Exception:
                    flag_str_sum = str("БД повреждена.")
                    all_ = "-1"
                table = Table(title=Style.BRIGHT + fore + version + Style.RESET_ALL, header_style='green', style="green")
                table.add_column("Страна:Кол-во websites", style="magenta", justify='full')
                table.add_column("All", style="cyan", justify='full')
                table.add_row(flag_str_sum, all_)
                console.print(table)

# Сортируем по алфавиту для full/demo version (2!).
            elif sortY == "2":
                if line == "str_line":
                    console.rule("[cyan]Ok, сортируем по алфавиту:", style="cyan bold")
                if version == "demo version":
                    console.print('\n', Panel.fit("++База данных++", title=version, style=STL(color="cyan", bgcolor="red")))
                else:
                    console.print('\n', Panel.fit("++База данных++", title=version, style=STL(color="cyan")))
                i = 0
                sorted_dict_v_listtuple = sorted(DB.items(), key=lambda x: x[0].lower())  #сорт.словаря по глав.ключу без учета регистра
                datajson_sort = dict(sorted_dict_v_listtuple)  #преобр.список обратно в словарь (сортированный)

                for con in datajson_sort:
                    S = datajson_sort.get(con).get("country_klas") if Windows else datajson_sort.get(con).get("country")
                    i += 1
                    listfull.append(f"\033[36;2m{i}.\033[0m \033[36m{S}  {con}")
                print("\n================\n".join(listfull))

# Сортируем по странам для full/demo version (1!).
            elif sortY == "1":
                listwindows = []

                if line == "str_line":
                    console.rule("[cyan]Ok, сортируем по странам:", style="cyan bold")

                for con in DB:
                    S = DB.get(con).get("country_klas") if Windows else DB.get(con).get("country")
                    listwindows.append(f"{S}  {con}\n")

                if version == "demo version":
                    console.print('\n', Panel.fit("++База данных++", title=version, style=STL(color="cyan", bgcolor="red")))
                else:
                    console.print('\n', Panel.fit("++База данных++", title=version, style=STL(color="cyan")))

                for i in enumerate(sorted(listwindows, key=str.lower), 1):
                    listfull.append(f"\033[36;2m{i[0]}. \033[0m\033[36m{i[1]}")
                print("================\n".join(listfull))

# Запуск функции '--list-all'.
        if sortY == "1" or sortY == "2":
            sort_list_all(BDflag, Fore.GREEN, "full version", line="str_line")
            sort_list_all(BDdemo, Fore.RED, "demo version")
        elif sortY == "3":
            sort_list_all(BDdemo, Fore.RED, "demo version", line="str_line")
            sort_list_all(BDflag, Fore.GREEN, "full version")
# Действие не выбрано '--list-all'.
        else:
            print(Style.BRIGHT + Fore.RED + "└──Извините, но вы не выбрали действие [1/2/3]\n\nВыход")
        sys.exit()


## Опция донат '-d y'.
    if args.donation:
        print(Fore.CYAN + "[+] активирована опция '-d': «финансовая поддержка проекта»")
        snoopbanner.donate()


## Опция '-u' указания файла-списка разыскиваемых пользователей.
    if args.user:
        userlists, userlists_bad, duble, _duble, short_user = [], [], [], [], []
        flipped, d = {}, {}

        try:
            patchuserlist = ("{}".format(args.user))
            userfile = patchuserlist.split('/')[-1] if not Windows else patchuserlist.split('\\')[-1]
            print(Fore.CYAN + f"[+] активирована опция '-u': «розыск nickname(s) из файла:: \033[36;1m{userfile}\033[0m\033[36m»\033[0m")

            with open(patchuserlist, "r", encoding="utf8") as u1:
                userlist = [(line[0], line[1].strip()) for line in enumerate(u1.read().replace("\ufeff", "").splitlines(), 1)]

                for num, user in userlist:
                    i_for = (num, user)
                    if re.findall(symbol_bad, user):
                        if all(i_for[1] != x[1] for x in userlists_bad):
                            userlists_bad.append(i_for)
                        else:
                            duble.append(i_for)
                        continue
                    elif user == "":
                        continue
                    elif len(user) <= 2:
                        short_user.append(i_for)
                        continue
                    else:
                        if all(i_for[1] != x[1] for x in userlists):
                            userlists.append(i_for)
                        else:
                            duble.append(i_for)

        except Exception:
            print(f"\033[31;1mНе могу найти_прочитать файл: '{userfile}'.\033[0m \033[36m\n " + \
                  f"\nПожалуйста, укажите текстовый файл в кодировке —\033[0m \033[36;1mutf-8.\033[0m\n" + \
                  f"\033[36mПо умолчанию, например, блокнот в OS Windows сохраняет текст в кодировке — ANSI.\033[0m\n" + \
                  f"\033[36mОткройте ваш файл '{userfile}' и измените кодировку [файл ---> сохранить как ---> utf-8].\n" + \
                  f"\033[36mИли удалите из файла нечитаемые спецсимволы.")
            sys.exit()

# good.
        if userlists:
            _userlists = [f"[dim cyan]{num}.[/dim cyan] {v} [{k}]".replace("", "") for num, (k, v) in enumerate(userlists, 1)]
            console.print(Panel.fit("\n".join(_userlists).replace("%20", " "), title=f"valid ({len(userlists)})",
                                    style=STL(color="cyan")))

# duplicate.
        if duble:
            dict_duble = dict(duble)
            for key, value in dict_duble.items():
                if value not in flipped:
                    flipped[value] = [key]
                else:
                    flipped[value].append(key)

            for k,v in flipped.items():
                k=f"{k} ({len(v)})"
                d[k]=v

            for num, (k, v) in enumerate(d.items(), 1):
                str_1 = f"[dim yellow]{num}.[/dim yellow] {k} {v}".replace(" (", " ——> ").replace(")", " шт.")
                str_2 = str_1.replace("——> ", "——> [bold yellow]").replace(" шт.", " шт.[/bold yellow]")
                _duble.append(str_2)

            print(f"\n\033[36mСледующие nickname(s) из '\033[36;1m{userfile}\033[0m\033[36m' содержат " + \
                  f"\033[33mдубли\033[0m\033[36m и будут пропущены:\033[0m")
            console.print(Panel.fit("\n".join(_duble), title=f"duplicate ({len(duble)})", style=STL(color="yellow")))

# bad.
        if userlists_bad:
            _userlists_bad = [f"[dim red]{num}.[/dim red] {v} [{k}]" for num, (k, v) in enumerate(userlists_bad, 1)]
            print(f"\n\033[36mСледующие nickname(s) из '\033[36;1m{userfile}\033[0m\033[36m' содержат " + \
                  f"\033[31;1mN/A-символы\033[0m\033[36m и будут пропущены:\033[0m")
            console.print(Panel.fit("\n".join(_userlists_bad), title=f"invalid_data ({len(userlists_bad)})",
                                    style=STL(color="bright_red")))

# Short.
        if short_user:
            _short_user = [f"[dim red]{num}.[/dim red] {v} [{k}]" for num, (k, v) in enumerate(short_user, 1)]
            print(f"\n\033[36mСледующие nickname(s) из '\033[36;1m{userfile}\033[0m\033[36m'\033[0m " + \
                  f"\033[31;1mкороче 3-х символов\033[0m\033[36m и будут пропущены:\033[0m")
            console.print(Panel.fit("\n".join(_short_user).replace("%20", " "), title=f"short nickname ({len(short_user)})",
                                    style=STL(color="bright_red")))

# Сохранение bad_nickname(s) в результатах txt.
        if short_user or userlists_bad:
            for bad_user1, bad_user2 in itertools.zip_longest(short_user, userlists_bad):
                with open (f"{dirpath}/results/nicknames/bad_nicknames.txt", "a", encoding="utf-8") as bad_nick:
                    if bad_user1:
                        bad_nick.write(f"{time.strftime('%d/%m/%Y_%H:%M:%S', time_date)}  <{userfile}>  '{bad_user1[1]}'\n")
                    if bad_user2:
                        bad_nick.write(f"{time.strftime('%d/%m/%Y_%H:%M:%S', time_date)}  <{userfile}>  '{bad_user2[1]}'\n")


        USERLIST = [i[1] for i in userlists]

        del userlists, duble, userlists_bad, _duble, short_user, flipped, d

        if bool(USERLIST) is False:
            console.print(f"\n⛔️ [bold red]Файл '{patchuserlist}' не содержит ни одного валидного nickname'\n\nВыход\n")
            sys.exit()


## Проверка остальных (в т.ч. повтор) опций.
## Опция '--update y' обновление Snoop.
    if args.update:
        print(Fore.CYAN + "[+] активирована опция '-U': «обновление snoop»")
        update_snoop()


## Опция '-w'.
    if args.web:
        print("\n\033[37m\033[44m{}".format("Функция '-w' доступна только пользователям Snoop full version..."))
        snoopbanner.donate()


## Работа с базой.
# опция '-b'. Проверить, существует ли альтернативная база данных, иначе demo.
    if not os.path.exists(str(args.json_file)):
        print(f"\n\033[31;1mОшибка! Неверно указан путь к файлу: '{str(args.json_file)}'.\033[0m")
        sys.exit()


## Опция  '-c'. Сортировка по странам.
    if args.country is True and args.web is False:
        print(Fore.CYAN + "[+] активирована опция '-c': «сортировка/запись результатов по странам»")
        country_sites = sorted(BDdemo, key=lambda k: ("country" not in k, BDdemo[k].get("country", sys.maxsize)))
        sort_web_BDdemo_new = {}
        for site in country_sites:
            sort_web_BDdemo_new[site] = BDdemo.get(site)


## Функция для опций '-eo'.
    def one_exl(one_exl_, bool_):
        lap = []
        bd_flag = []

        for k, v in BDdemo.items():
            bd_flag.append(v.get('country_klas').lower())
            if all(item.lower() != v.get('country_klas').lower() for item in one_exl_) is bool_:
                BDdemo_new[k] = v

        enter_coun_u = [x.lower() for x in one_exl_]
        lap = list(set(bd_flag) & set(enter_coun_u))
        diff_list = list(set(enter_coun_u) - set(bd_flag))  #вывести уник элем из enter_coun_u иначе set(enter_coun_u)^set(bd_flag)

        if bool(BDdemo_new) is False:
            print(f"\033[31;1m[{str(diff_list).strip('[]')}] все регионы поиска являются невалидными.\033[0m")
            sys.exit()
# Вернуть корректный и bad списки пользовательского ввода в cli.
        return lap, diff_list


## Если опции '-seo' не указаны, то используем БД, как есть.
    BDdemo_new = {}
    if args.site_list is None and args.exclude_country is None and args.one_level is None:
        BDdemo_new = BDdemo


## Опция '-s'.
    elif args.site_list is not None:
# Убедиться, что сайты в базе имеются, создать для проверки сокращенную базу данных сайта(ов).
        for site in args.site_list:
            for site_yes in BDdemo:
                if site.lower() == site_yes.lower():
                    BDdemo_new[site_yes] = BDdemo[site_yes]  #выбираем в словарь найденные сайты из БД
            try:
                diff_k_bd = set(BDflag) ^ set(BDdemo)
            except Exception:
                snoopbanner.logo(text="\nnickname(s) не задан(ы)")
            for site_yes_full_diff in diff_k_bd:
                if site.lower() == site_yes_full_diff.lower():  #если сайт (-s) в БД Full версии
                    print(f"\033[31;1m[?] Пропуск:\033[0m \033[36mсайт из БД \033[36;1mfull-версии\033[0m \033[36mнедоступен в" + \
                          f"\033[0m \033[33;1mdemo-версии\033[0m\033[36m:: '\033[30;1m{site_yes_full_diff}\033[0m\033[36m'\033[0m")

            if not any(site.lower() == site_yes_full.lower() for site_yes_full in BDflag):  #если ни одного совпадения по сайту
                print(f"\033[31;1m[!] Пропуск:\033[0m \033[36mжелаемый сайт отсутствует в БД Snoop:: '" + \
                      f"\033[31;1m{site}\033[0m\033[36m'\033[0m")
# Отмена поиска, если нет ни одного совпадения по БД и '-s'.
        if not BDdemo_new:
            sys.exit()


## Опция '-e'.
# Создать для проверки сокращенную базу данных сайта(ов).
# Создать и добавить в новую БД сайты, аргументы (-e) которых != бук.кодам стран (country_klas).
    elif args.exclude_country is not None:
        lap, diff_list = one_exl(one_exl_=args.exclude_country, bool_=True)

        print(Fore.CYAN + f"[+] активирована опция '-e': «исключить из поиска выбранные регионы»::", end=' ')
        print(Style.BRIGHT + Fore.CYAN + str(lap).strip('[]').upper() + Style.RESET_ALL + " " + Style.BRIGHT + Fore.RED + \
              str(diff_list).strip('[]') + Style.RESET_ALL + Fore.CYAN + "\n" + \
              "    допустимо использовать опцию '-e' несколько раз\n" + \
              "    [опция '-e'] несовместима с [опциями '-s', '-c', '-i']")


## Опция '-i'.
# Создать для проверки сокращенную базу данных сайта(ов).
# Создать и добавить в новую БД сайты, аргументы (-e) которых != бук.кодам стран (country_klas).
    elif args.one_level is not None:
        lap, diff_list = one_exl(one_exl_=args.one_level, bool_=False)

        print(Fore.CYAN + f"[+] активирована опция '-i': «включить в поиск только выбранные регионы»::", end=' ')
        print(Style.BRIGHT + Fore.CYAN + str(lap).strip('[]').upper() + Style.RESET_ALL + " " + Style.BRIGHT + Fore.RED + \
              str(diff_list).strip('[]') + Style.RESET_ALL + Fore.CYAN + "\n" + \
              "    допустимо использовать опцию '-i' несколько раз\n" + \
              "    [опция '-i'] несовместима с [опциями '-s', '-c', 'e']")


## Ник не задан или противоречие опций.
    if bool(args.username) is False and bool(args.user) is False:
        snoopbanner.logo(text="\nпараметры либо nickname(s) не задан(ы)")
    if bool(args.username) is True and bool(args.user) is True:
        print("\n\033[31;1mВыберите для поиска nickname(s) из файла или задайте в cli,\n" + \
              "но не совместное использование nickname(s): из файла и cli.\n\nВыход")
        sys.exit()


## Опция '-v'.
    if args.verbose and bool(args.username) or args.verbose and bool(USERLIST):
        print(Fore.CYAN + "[+] активирована опция '-v': «подробная вербализация в CLI»\n")
        networktest.nettest()


## Опция  '-w' не активна.
    try:
        if args.web is False:
            print(f"\n{Fore.CYAN}загружена локальная база: {Style.BRIGHT}{Fore.CYAN}{len(BDdemo)}_Websites{Style.RESET_ALL}")
    except Exception:
        print("\033[31;1mInvalid загружаемая база данных.\033[0m")


## Крутим user's.
    def starts(SQ):
        kef_user = 0
        ungzip, ungzip_all, find_url_lst, el = [], [], [], []
        exl = "/".join(lap).upper() if args.exclude_country is not None else "нет"  #искл.регионы_valid
        one = "/".join(lap).upper() if args.one_level is not None else "нет"  #вкл.регионы_valid
        for username in SQ:
            kef_user += 1
            sort_sites = sort_web_BDdemo_new if args.country is True else BDdemo_new

            FULL, hardware = snoop(username, sort_sites, country=args.country, user=args.user, verbose=args.verbose, cert=args.cert,
                                   norm=args.norm, reports=args.reports, print_found_only=args.print_found_only, timeout=args.timeout,
                                   color=not args.no_func, headerS=args.headerS)

            exists_counter = 0

            if bool(FULL) is False:
                with open (f"{dirpath}/results/nicknames/bad_nicknames.txt", "a", encoding="utf-8") as bad_nick:
                    bad_nick.write(f"{time.strftime('%d/%m/%Y_%H:%M:%S', time_date)}  <CLI>  '{username}'\n")

                continue

## Запись в txt.
            file_txt = open(f"{dirpath}/results/nicknames/txt/{username}.txt", "w", encoding="utf-8")

            file_txt.write("Адрес | ресурс" + "\n\n")

            for website_name in FULL:
                dictionary = FULL[website_name]
                if type(dictionary.get("session_size")) != str:
                    ungzip.append(dictionary.get("session_size")), ungzip_all.append(dictionary.get("session_size"))
                if dictionary.get("exists") == "найден!":
                    exists_counter += 1
                    find_url_lst.append(exists_counter)
                    file_txt.write(dictionary["url_user"] + " | " + (website_name) + "\n")
# Размер сессии персональный и общий, кроме CSV.
            try:
                sess_size = round(sum(ungzip) / 1024, 2)  #в МБ
                s_size_all = round(sum(ungzip_all) / 1024, 2)  #в МБ
            except Exception:
                sess_size = 0.000_000_000_1
                s_size_all = "Err"
            timefinish = time.time() - timestart - sum(el)
            el.append(timefinish)
            time_all = str(round(time.time() - timestart))

            file_txt.write("\n" f"Запрашиваемый объект: <{nick}> найден: {exists_counter} раз(а).")
            file_txt.write("\n" f"Сессия: {str(round(timefinish))}сек {str(sess_size)}Mb.")
            file_txt.write("\n" f"База Snoop (demo version): {flagBS} Websites.")
            file_txt.write("\n" f"Исключённые регионы: {exl}.")
            file_txt.write("\n" f"Выбор конкретных регионов: {one}.")
            file_txt.write("\n" f"Обновлено: {time.strftime('%d/%m/%Y_%H:%M:%S', time_date)}.")
            file_txt.close()


## Запись в html.
            if Android and re.search("[^\W \da-zA-Z]+", nick):
                username = f"nickname_{time.strftime('%d_%m_%Y_%H-%M-%S')}"

            file_html = open(f"{dirpath}/results/nicknames/html/{username}.html", "w", encoding="utf-8")

            file_html.write("<!DOCTYPE html>\n<head>\n<meta charset='utf-8'>\n<style>\nbody { background: url(../../../web/public.png) " + \
                            "no-repeat 20% 0%; }\n</style>\n<link rel='stylesheet' href='../../../web/style.css'>\n</head>\n<body>\n\n" + \
                            "<div id='particles-js'></div>\n" + \
                            "<div id='report'>\n\n" + \
                            "<h1><a class='GL' href='file://" + f"{dirpath}/results/nicknames/html/'>Главная</a>" + "</h1>\n")
            file_html.write("<h3>Snoop Project (demo version)</h3>\n<p>Нажмите: 'сортировать по странам', возврат: 'F5':</p>\n" + \
                            "<button onclick='sortList()'>Сортировать по странам</button><br><br>\n\n")
            file_html.write("Объект " + "<b>" + (nick) + "</b>" + " найден на нижеперечисленных " + "<b>" + str(exists_counter) + \
                            "</b> ресурсах:\n" + "<br><ol" + " id='id777'>\n")

            li = []
            for website_name in FULL:
                dictionary = FULL[website_name]
                flag_sum = dictionary["flagcountry"]
                if dictionary.get("exists") == "найден!":
                    li.append(flag_sum)
                    file_html.write("<li>" + dictionary["flagcountry"] + "<a target='_blank' href='" + dictionary["url_user"] + "'>" + \
                                    (website_name) + "</a>" + "</li>\n")
            try:
                cnt = str(Counter(li))
                flag_str_sum = (cnt.split('{')[1]).replace("'", "").replace("}", "").replace(")", "").replace(",", "  ↯  ").replace(":", "⇔")
            except Exception:
                flag_str_sum = "0"

            file_html.write("</ol>GEO: " + str(flag_str_sum) + ".\n")
            file_html.write("<br> Запрашиваемый объект < <b>" + str(nick) + "</b> > найден: <b>" + str(exists_counter) + "</b> раз(а).")
            file_html.write("<br> Сессия: " + "<b>" + str(round(timefinish)) + "сек_" + str(sess_size) + "Mb</b>.\n")
            file_html.write("<br> Исключённые регионы: <b>" + str(exl) + "</b>.\n")
            file_html.write("<br> Выбор конкретных регионов: <b>" + str(one) + "</b>.\n")
            file_html.write("<br> База Snoop (demo version): <b>" + str(flagBS) + "</b>" + " Websites.\n")
            file_html.write("<br> Обновлено: " + "<i>" + time.strftime("%d/%m/%Y_%H:%M:%S", time_date) + ".</i><br><br>\n")
            file_html.write("""
<script>
function sortList() {
  var list, i, switching, b, shouldSwitch;
  list = document.getElementById('id777');
  switching = true;
  while (switching) {
    switching = false;
    b = list.getElementsByTagName("LI");
    for (i = 0; i < (b.length - 1); i++) {
      shouldSwitch = false;
      if (b[i].innerHTML.toLowerCase() > b[i + 1].innerHTML.toLowerCase()) {
        shouldSwitch = true;
        break;
      }
    }
    if (shouldSwitch) {
      b[i].parentNode.insertBefore(b[i + 1], b[i]);
      switching = true;
    }
  }
}
</script>

<script src="../../../web/particles.js"></script>
<script src="../../../web/app.js"></script>

<audio controls="controls" autoplay="autoplay" loop="loop">
<source src="../../../web/Megapolis (remix).mp3" type="audio/mpeg">
</audio>

<br>
<audio controls="controls" loop="loop">
<source src="../../../web/for snoop in cyberpunk.mp3" type="audio/mpeg">
</audio>

<br><br>

<a target='_blank' href='https://github.com/snooppr/snoop' class="SnA"><span class="SnSpan">🛠  Source Исходный код</span></a>
<a target='_blank' href='https://drive.google.com/file/d/12DzAQMgTcgeG-zJrfDxpUbFjlXcBq5ih/view' class="DnA"><span class="DnSpan">📖 Doc Документация</span></a>
<a target='_blank' href='https://sobe.ru/na/snoop_project_2020' class="DnA"><span class="DnSpan">💳 Donation Пожертвование</span></a>
<br><br><br><br>

</body>
</html>""")
            file_html.close()


## Запись в csv.
            if rus_windows is False:
                file_csv = open(f"{dirpath}/results/nicknames/csv/{username}.csv", "w", newline='', encoding="utf-8")
            else:
                file_csv = open(f"{dirpath}/results/nicknames/csv/{username}.csv", "w", newline='') #для ru_пользователей

            usernamCSV = re.sub(" ", "_", nick)
            censors_cor = int((censors - recensor) / kef_user)  #err_connection
            censors_timeout_cor = int(censors_timeout / kef_user)  #err time-out
            try:
                flagBS_err = round((censors_cor + censors_timeout_cor) * 100 / (len(BDdemo_new) - len(d_g_l)), 2)
            except ZeroDivisionError:
                flagBS_err = 0

            writer = csv.writer(file_csv)
            if rus_windows or rus_unix or Android:
                writer.writerow(['Никнейм', 'Ресурс', 'Страна', 'Url', 'Ссылка_на_профиль', 'Статус', 'Статус_http',
                                 'Общее_замедление/сек', 'Отклик/сек', 'Общее_время/сек', 'Сессия/Kb'])
            else:
                writer.writerow(['username', 'resource', 'country', 'url', 'url_username', 'status', 'http',
                                 'deceleration/s', 'response/s', 'time/s', 'session/Kb'])

            for site in FULL:
                if FULL[site]['session_size'] == 0:
                    Ssession = "Head"
                elif type(FULL[site]['session_size']) != str:
                    Ssession = str(FULL.get(site).get("session_size")).replace('.', locale.localeconv()['decimal_point'])
                else:
                    Ssession = "Bad"

                writer.writerow([usernamCSV, site, FULL[site]['countryCSV'], FULL[site]['url_main'], FULL[site]['url_user'],
                                 FULL[site]['exists'], FULL[site]['http_status'],
                                 FULL[site]['response_time_site_ms'].replace('.', locale.localeconv()['decimal_point']),
                                 FULL[site]['check_time_ms'].replace('.', locale.localeconv()['decimal_point']),
                                 FULL[site]['response_time_ms'].replace('.', locale.localeconv()['decimal_point']),
                                 Ssession])

            writer.writerow(['«' + '-'*30, '-'*8, '-'*4, '-'*35, '-'*56, '-'*13, '-'*17, '-'*32, '-'*13, '-'*23, '-'*16 + '»'])
            writer.writerow([f'БД_(demoversion)={flagBS}_Websites'])
            writer.writerow('')
            writer.writerow([f'Исключённые_регионы={exl}'])
            writer.writerow([f'Выбор_конкретных_регионов={one}'])
            writer.writerow([f"Bad_raw:_{flagBS_err}%_БД" if flagBS_err >= 2 else ''])
            writer.writerow('')
            writer.writerow(['Дата'])
            writer.writerow([time.strftime("%d/%m/%Y_%H:%M:%S", time_date)])

            file_csv.close()

            ungzip.clear()
            d_g_l.clear()


## Финишный вывод.
        if bool(FULL) is True:
            recomend = "       \033[36m├─используйте \033[36;1mVPN\033[0m \033[36m\n       └─или увеличьте значение опции" + \
                           "'\033[36;1m-t\033[0m\033[36m'\033[0m\n"

            direct_results = f"{dirpath}/nicknames/results/*" if not Windows else f"{dirpath}\\results\\*"

            print(f"{Fore.CYAN}├─Результаты:{Style.RESET_ALL} найдено --> {len(find_url_lst)} url (сессия: {time_all} сек_{s_size_all}Mb)")
            print(f"{Fore.CYAN}├──Сохранено в:{Style.RESET_ALL} {direct_results}")
            if flagBS_err >= 2:  #perc_%
                print(f"{Fore.CYAN}├───Дата поиска:{Style.RESET_ALL} {time.strftime('%d/%m/%Y_%H:%M:%S', time_date)}")
                print(f"{Fore.CYAN}└────\033[31;1mВнимание! Bad_raw: {flagBS_err}% БД\033[0m")
                print(f"{Fore.CYAN}     └─нестабильное соединение или I_Censorship")
                print(recomend)
            else:
                print(f"{Fore.CYAN}└───Дата поиска:{Style.RESET_ALL} {time.strftime('%d/%m/%Y_%H:%M:%S', time_date)}\n")
            console.print(Panel(f"{e_mail} до {Do}", title=license, style=STL(color="white", bgcolor="blue")))


## Музыка.
            try:
                if args.no_func is False: playsound('end.wav')
            except Exception:
                pass


## Открывать/нет браузер с результатами поиска.
            if args.no_func is False and exists_counter >= 1:
                try:
                    if not Android:
                        webbrowser.open(f"file://{dirpath}/results/nicknames/html/{username}.html")
                    else:
                        install_service = Style.DIM + Fore.CYAN + \
                                              "\nДля авто-открытия результатов во внешнем браузере на Android у пользователя " + \
                                              "должна быть настроена среда, код:" + Style.RESET_ALL + Fore.CYAN + \
                                              "\ncd && pkg install termux-tools; echo 'allow-external-apps=true' >>" + \
                                              ".termux/termux.properties" + Style.RESET_ALL + \
                                              Style.DIM + Fore.CYAN + "\n\nИ перезапустить терминал."

                        termux_sv = False
                        if os.path.exists("/data/data/com.termux/files/usr/bin/termux-open"):
                            with open("/data/data/com.termux/files/home/.termux/termux.properties", "r", encoding="utf-8") as f:
                                for line in f:
                                    if ("allow-external-apps" in line and "#" not in line) and line.split("=")[1].strip().lower() == "true":
                                        termux_sv = True

                            if termux_sv is True:
                                subprocess.run(f"termux-open {dirpath}/results/nicknames/html/{username}.html", shell=True)
                            else:
                                print(install_service)

                        else:
                            print(install_service)
                except Exception:
                    print(f"\n\033[31;1mНе удалось открыть результаты\033[0m")
        try:
            hardware.shutdown()
        except Exception:
            console.log(snoopbanner.err_all(err_="low"))
            pass

## поиск по выбранным пользователям.
    starts(args.username) if args.user is False else starts(USERLIST)

## Arbeiten...
if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        console.print(f"\n[bold red]Прерывание [italic](высвобождение ресурсов, ждите...)[/bold red]")
        if Windows:
            os.kill(os.getpid(), signal.SIGBREAK)
        elif lame_workhorse:
            os.kill(os.getpid(), signal.SIGKILL)
        else:
            for child in active_children():
                child.terminate()
                time.sleep(0.1)

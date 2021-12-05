#! /usr/bin/env python3
# Copyright (c) 2020 Snoop Project <snoopproject@protonmail.com>

import argparse
import base64
import csv
import glob
try:
    import psutil
except:
    print("ВНИМАНИЕ! Обновите lib python:\ncd ~/snoop && python3 -m pip install -r requirements.txt")
import json
import locale
import networktest
import os
import platform
import random
import re
import requests
import shutil
import snoopplugins
import subprocess
import sys
import time
import webbrowser

from collections import Counter
from colorama import Fore, Style, init
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from playsound import playsound
from requests_futures.sessions import FuturesSession
from rich.progress import (track,BarColumn,TimeRemainingColumn,SpinnerColumn,TimeElapsedColumn,Progress)
from rich.panel import Panel
from rich.style import Style as STL
from rich.console import Console
from rich.table import Table

locale.setlocale(locale.LC_ALL, '')
init(autoreset=True)
console = Console()

vers = 'v1.3.2C'
print (f"""\033[36m
  ___|                          
\___ \  __ \   _ \   _ \  __ \  
      | |   | (   | (   | |   | 
_____/ _|  _|\___/ \___/  .__/  
                         _|    \033[0m \033[37m{vers}\033[34;1m_rus_\033[31;1mSource Demo\033[0m
""")
version = f"{vers}_rus Snoop (Source demo)"

print (Fore.CYAN + "#Примеры:" + Style.RESET_ALL)
if sys.platform == 'win32':
    print (Fore.CYAN + " cd с:\<path>\snoop")
    print (Fore.CYAN + " python snoop.py --help" + Style.RESET_ALL, "#справка")
    print (Fore.CYAN + " python snoop.py nickname" + Style.RESET_ALL, "#поиск user-a")
    print (Fore.CYAN + " python snoop.py --module" + Style.RESET_ALL, "#задействовать плагины")
else:
    print (Fore.CYAN + " cd ~/snoop")
    print (Fore.CYAN + " python3 snoop.py --help" + Style.RESET_ALL, "#справка")
    print (Fore.CYAN + " python3 snoop.py nickname" + Style.RESET_ALL, "#поиск user-a")
    print (Fore.CYAN + " python3 snoop.py --module" + Style.RESET_ALL, "#задействовать плагины")
console.rule(characters = '=', style="cyan")
print("")

timestart = time.time()
time_date = time.localtime()
censors = 0
censors_timeout = 0
recensor = 0

## date +%s конвертер
e_mail = 'Demo: snoopproject@protonmail.com'
## лицензия: год/месяц/число:
license = 'лицензия'
ts = (2022, 11, 11, 3, 0, 0, 0, 0, 0)
date_up = int(time.mktime(ts)) #дата в секундах с начала эпохи
up1 = time.gmtime(date_up)
Do = (f"{up1.tm_mday}/{up1.tm_mon}/{up1.tm_year}") #в UTC (-3 часа)

if time.time() > int(date_up):
    print(Style.BRIGHT + Fore.RED + "Версия Snoop " + version + " деактивирована согласно лицензии.")
    sys.exit()

def ravno():
    console.rule(characters = '=', style="cyan bold")

def DB(db_base):
    try:
        with open(db_base, "r", encoding="utf8") as f_r:
            db = f_r.read()
            db = db.encode("UTF-8")
            db = base64.b64decode(db)
            db = db[::-1]
            db = base64.b64decode(db)
            trinity = json.loads(db.decode("UTF-8"))
            return trinity
    except:
        print(Style.BRIGHT + Fore.RED + "Упс, что-то пошло не так..." + Style.RESET_ALL)
        sys.exit()

## Получаем результаты и в будущем везде используем, сокращая вызовы функций.
BDdemo = DB('BDdemo')
BDflag = DB('BDflag')
## Флаг БС.
flagBS = len(BDdemo)

## Создание директорий результатов.
dirresults = os.getcwd()
dirhome = os.environ['HOME'] + "/snoop" if sys.platform != 'win32' else os.environ['LOCALAPPDATA'] + "\snoop"
dirpath = dirresults if 'Source' in version else dirhome
os.makedirs(f"{dirpath}/results", exist_ok=True)
os.makedirs(f"{dirpath}/results/nicknames/html", exist_ok=True)
os.makedirs(f"{dirpath}/results/nicknames/txt", exist_ok=True)
os.makedirs(f"{dirpath}/results/nicknames/csv", exist_ok=True)
os.makedirs(f"{dirpath}/results/nicknames/save reports", exist_ok=True)
os.makedirs(f"{dirpath}/results/plugins/ReverseVgeocoder", exist_ok=True)
os.makedirs(f"{dirpath}/results/plugins/Yandex_parser", exist_ok=True)
os.makedirs(f"{dirpath}/results/plugins/domain", exist_ok=True)

################################################################################
class ElapsedFuturesSession(FuturesSession):
    """test_metrica: API:: https://pypi.org/project/requests-futures/"""
    def request(self, method, url, *args, **kwargs):
        """test"""
        return super(ElapsedFuturesSession, self).request(method, url, *args, **kwargs)

## Вывести на печать инфостроку.
def print_info(title, info, color=True):
    if color:
        print(Fore.GREEN + "[" + Fore.YELLOW + "*" + Fore.GREEN + f"] {title}" + Fore.RED + " <" + Fore.WHITE + f" {info}" +
        Fore.RED + " >" + Style.RESET_ALL)
    else:
        print(f"\n[*] {title} {info}:")

## Вывести на печать ошибки в режиме обычного поиска.
def print_error(err, errstr, var, verbose=False, color=True):
    if color:
        print(Style.RESET_ALL + Fore.CYAN + "[" + Style.BRIGHT + Fore.RED + "-" + Style.RESET_ALL + Fore.CYAN + "]" + Style.BRIGHT +
        Fore.RED + f" {errstr}" + Style.BRIGHT + Fore.YELLOW + f" {var}" + f" {err if verbose else ''}")
        try:
            playsound('err.wav')
        except:
            pass
    else:
        print(f"[-] {errstr} {var} {err if verbose else ''}")

## Вывод на печать на разных платформах, индикация.
## Вывести на печать аккаунт найден.
def print_found_country(websites_names, url, country_Emoj_Code, response_time=False, verbose=False, color=True):
    if color and sys.platform == 'win32':
        print(Style.RESET_ALL + Style.BRIGHT + Fore.CYAN + f" {country_Emoj_Code}" + Fore.GREEN + f" {websites_names}:", Style.RESET_ALL +
        Fore.GREEN + f"{url}")
    elif color and not sys.platform == 'win32':
        print(country_Emoj_Code, (Style.BRIGHT + Fore.GREEN + f" {websites_names}:"), Style.RESET_ALL + Fore.GREEN + f"{url}")
    else:
        print(f"[+] {websites_names}: {url}")

## Вывести на печать аккаунт не найден.
def print_not_found(websites_names, response_time, verbose=False, color=True):
    if color:
        print(Style.RESET_ALL + Fore.CYAN + "[" + Style.BRIGHT + Fore.RED + "-" + Style.RESET_ALL + Fore.CYAN + "]" +
        Style.BRIGHT + Fore.GREEN + f" {websites_names}:" + Style.BRIGHT + Fore.YELLOW + " Увы!")
    else:
        print(f"[-] {websites_names}: Увы!")

## Вывести на печать пропуск сайтов по блок. маске в имени username и пропуск по проблеме с openssl.
def print_invalid(mes, websites_names, message, color=True):
    """Ошибка вывода результата"""
    if color:
        print(Style.RESET_ALL + Fore.RED + "[" + Style.BRIGHT + Fore.RED + "-" + Style.RESET_ALL + Fore.RED + "]" +
        Style.BRIGHT + Fore.GREEN + f" {websites_names}:" + Style.RESET_ALL + Fore.YELLOW + f" {message}")
    else:
        print(f"[-] {websites_names}: {message}")

## Вернуть результат future for2.
def get_response(request_future, error_type, websites_names, print_found_only=False, verbose=False, color=True):
    try:
        res = request_future.result()
        if res.status_code:
            return res, error_type, res.elapsed
    except requests.exceptions.HTTPError as err1:
        if print_found_only==False:
            print_error(err1, "HTTP Error:", websites_names, verbose, color)
    except requests.exceptions.ConnectionError as err2:
        global censors
        censors +=1
        if print_found_only==False:
            print_error(err2, "Ошибка соединения:", websites_names, verbose, color)
    except requests.exceptions.Timeout as err3:
        global censors_timeout
        censors_timeout +=1
        if print_found_only==False:
            print_error(err3, "Timeout ошибка:", websites_names, verbose, color)
    except requests.exceptions.RequestException as err4:
        if print_found_only==False:
            print_error(err4, "Непредвиденная ошибка", websites_names, verbose, color)
    return None, "", -1

## Сохранение отчетов опция (-S).
def sreports(url, headers,session2,error_type, username,websites_names,r):
    os.makedirs(f"{dirpath}/results/nicknames/save reports/{username}", exist_ok=True)
# Сохранять отчеты для метода: redirection.
    if error_type == "redirection":
        try:
            future2 = session2.get(url=url, headers=headers, allow_redirects=True, timeout=4)
            response = future2.result()
            session_size = len(response.content) #подсчет извлеченных данных.
            with open(f"{dirpath}/results/nicknames/save reports/{username}/{websites_names}.html", 'w', encoding=r.encoding) as repre:
                repre.write(response.text)
        except requests.exceptions.ConnectionError:
            time.sleep(1)
            try:
                future2 = session2.get(url=url, headers=headers, allow_redirects=True, timeout=2)
                response = future2.result()
                session_size = len(response.content) #подсчет извлеченных данных.
                with open(f"{dirpath}/results/nicknames/save reports/{username}/{websites_names}.html", 'w', encoding=r.encoding) as repre:
                    repre.write(response.text)
            except:
                session_size = 'Err' #подсчет извлеченных данных.
        return session_size
# Сохранять отчеты для всех остальных методов: status; response; message со стандартными параметрами.
    else:
        with open(f"{dirpath}/results/nicknames/save reports/{username}/{websites_names}.html", 'w', encoding=r.encoding) as rep:
            rep.write(r.text)


## Основная функция.
def snoop(username, BDdemo_new, verbose=False, norm=False, reports=False, user=False, country=False, print_found_only=False, timeout=None, color=True, cert=False, quickly=False, headerS=None):
## Печать первой инфостроки.
    if '%20' in username:
        username_space = re.sub("%20", " ", username)
        print_info("разыскиваем:", username_space, color)
    else:
        print_info("разыскиваем:", username, color)

    username = re.sub(" ", "%20", username)

## Результаты анализа всех сайтов.
    dic_snoop_full = {}

## Предотвращение 'DDoS' из-за невалидных логинов; номеров телефонов, ошибок поиска из-за спецсимволов.
    with open('domainlist.txt', 'r', encoding="utf-8") as err:
        username_bad = username.rsplit(sep='@', maxsplit=1)
        username_bad = '@bro'.join(username_bad).lower()

        ermail = err.read().splitlines()
        if any(ermail_iter.lower() in username.lower() for ermail_iter in ermail):
            username = username.rsplit(sep='@', maxsplit=1)[0]
            print(f"\n{Fore.CYAN}Обнаружен E-mail адрес, извлекаем nickname: '{Style.BRIGHT}{Fore.CYAN}{username}{Style.RESET_ALL}" + \
                  f"{Fore.CYAN}'\nsnoop способен отличать e-mail от логина, например, поиск '{username_bad}'\n" + \
                  f"не является валидной электропочтой, но может существовать как nickname, следовательно — не будет обрезан\n")
        del ermail

    with open('specialcharacters', 'r', encoding="utf-8") as errspec:
        my_list_bad = list(errspec.read())
        if any(symbol_bad in username for symbol_bad in my_list_bad):
            console.print(f"[bold red]недопустимые символы в username: '{username}'\n\nВыход")
            sys.exit()

    ernumber=['79', '89', "38", "37"]
    if any(ernumber in username[0:2] for ernumber in ernumber):
        if len(username) >= 10 and len(username) <= 13 and username.isdigit() == True:
            print(Style.BRIGHT + Fore.RED + "\nSnoop выслеживает учётки пользователей, но не номера телефонов...")
            sys.exit()
    elif username[0] == "+" or username[0] == ".":
        print (Style.BRIGHT + Fore.RED + "\nПубличный логин, начинающийся с такого символа, практически всегда невалидный...")
        sys.exit()
    elif username[0] == "9" and len(username) == 10 and username.isdigit() == True:
        print (Style.BRIGHT + Fore.RED + "\nSnoop выслеживает учётки пользователей, но не номера телефонов...")
        sys.exit()
    global nick
    nick = username
## Создать много_поточный/процессный сеанс для всех запросов.
    requests.packages.urllib3.disable_warnings() #блокировка предупреждений о сертификате.
    my_session = requests.Session()
    if cert == False:
        my_session.verify = False
        requests.packages.urllib3.disable_warnings()

    if not sys.platform == 'win32':
        if "arm" in platform.platform(aliased=True, terse=0) or "aarch64" in platform.platform(aliased=True, terse=0):
            session1 = ElapsedFuturesSession(executor=ThreadPoolExecutor(max_workers=10), session=my_session)
        else:
            if norm == False:
                session1 = ElapsedFuturesSession(executor=ProcessPoolExecutor(max_workers=26), session=my_session)
            else:
                session1 = ElapsedFuturesSession(executor=ThreadPoolExecutor(max_workers=16), session=my_session)
    else:
        session1 = ElapsedFuturesSession(executor=ThreadPoolExecutor(max_workers=15), session=my_session)

    if reports:
        session2 = FuturesSession(max_workers=1, session=my_session)
    if norm == False:
        session3 = ElapsedFuturesSession(executor=ThreadPoolExecutor(max_workers=1), session=my_session)

### Создание futures на все запросы. Это позволит распараллетить запросы.
    for websites_names, param_websites in BDdemo_new.items():
        results_site = {}

        param_websites.pop('usernameON', None)
        param_websites.pop('usernameOFF', None)
        param_websites.pop('comments', None)

## Запись URL основного сайта и флага страны (сопоставление в БД).
        results_site['flagcountry'] = param_websites.get("country")
        results_site['flagcountryklas'] = param_websites.get("country_klas")
        results_site['url_main'] = param_websites.get("urlMain")

## Пользовательский user-agent браузера (рандомно на каждый сайт), а при сбое постоянный с расширенным заголовком.
        majR = random.choice(range(73, 94, 1))
        minR = random.choice(range(2683, 4606, 13))
        patR = random.choice(range(52, 99, 1))
        RandHead=([f"{{'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) " + \
                   f"Chrome/{majR}.0.{minR}.{patR} Safari/537.36'}}",
                   f"{{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) "+ \
                   f"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{majR}.0.{minR}.{patR} Safari/537.36'}}"])
        RH = random.choice(RandHead)
        headers = json.loads(RH.replace("'",'"'))

        if "headers" in param_websites:
## Переопределить/добавить любые дополнительные заголовки, необходимые для данного сайта.
            headers.update(param_websites["headers"])
        if headerS is not None:
            headers.update({"User-Agent":''.join(headerS)})
        #console.print(headers) #проверка u-агентов.
## Пропуск временно-отключенного сайта и не делать запрос, если имя пользователя не подходит для сайта.
        exclusionYES = param_websites.get("exclusion")
        if exclusionYES and re.search(exclusionYES, username) or param_websites.get("bad_site") == 1:
            if exclusionYES and re.search(exclusionYES, username) and not print_found_only:
                print_invalid("", websites_names, f"недопустимый ник '{username}' для данного сайта", color)
            results_site["exists"] = "invalid_nick"
            results_site["url_user"] = '*'*56
            results_site['countryCSV'] = "****"
            results_site['http_status'] = '*'*10
            results_site['session_size'] = ""
            results_site['check_time_ms'] = '*'*15
            results_site['response_time_ms'] = '*'*15
            results_site['response_time_site_ms'] = '*'*25
            if param_websites.get("bad_site") == 1 and verbose == True and not print_found_only:
                print_invalid("", websites_names, f"**Пропуск. Dynamic gray_list", color)
                results_site["exists"] = "gray_list"
        else:
## URL пользователя на сайте (если он существует).
            #global url
            url = param_websites["url"].format(username)
            results_site["url_user"] = url
            url_API = param_websites.get("urlProbe")
            if url_API is None:
## URL-адрес — является обычным, который видят люди в Интернете.
                url_API = url
            else:
## Существует специальный URL (обычно о нем мы не догадываемся/api) для проверки существования отдельно юзера.
                url_API = url_API.format(username)

## Если нужен только статус кода, не загружать тело страницы, экономими память для status/redirect методов.
            if reports == True or param_websites["errorTypе"] == 'message' or param_websites["errorTypе"] == 'response_url':
                request_method = session1.get
            else:
                request_method = session1.head

## Сайт перенаправляет запрос на другой URL.
            if param_websites["errorTypе"] == "response_url" or param_websites["errorTypе"] == "redirection":
## Имя найдено. Запретить перенаправление чтобы захватить статус кода из первоначального url.
                allow_redirects = False
            else:
## Разрешить любой редирект, который хочет сделать сайт.
## Окончательным результатом запроса будет то, что доступно.
                allow_redirects = True

## Отправить все запросы и сохранить future in data для последующего доступа.
            future = request_method(url=url_API, headers=headers, allow_redirects=allow_redirects, timeout=timeout)
            param_websites["request_future"] = future

## Добавлять флаги/url-s в будущий-окончательный словарь с будущими всеми другими результатами.
        dic_snoop_full[websites_names] = results_site

    li_time = [0]
    if verbose == False:
# Прогресс.
        if sys.platform != 'win32':
            progress = Progress(TimeElapsedColumn(), SpinnerColumn(spinner_name=random.choice(["dots", "dots12"])),
            "[progress.percentage]{task.percentage:>1.0f}%", BarColumn(bar_width=None, complete_style='cyan', finished_style='cyan bold'),
            refresh_per_second = 3.0)#auto_refresh=False) #transient=True) #исчезает прогресс
        else:
            progress = Progress(TimeElapsedColumn(), "[progress.percentage]{task.percentage:>1.0f}%", BarColumn(bar_width=None,
            complete_style='cyan', finished_style='cyan bold'), refresh_per_second = 3.0)#,auto_refresh=False)#transient=True) #исчезает прогресс
    else:
        progress = Progress(TimeElapsedColumn(), "[progress.percentage]{task.percentage:>1.0f}%", auto_refresh=False)#,refresh_per_second = 3.0)#
# Панель вербализации.
        if not "arm" in platform.platform(aliased=True, terse=0) and not "aarch64" in platform.platform(aliased=True, terse=0):
            if color == True:
                console.print(Panel("[yellow]об.время[/yellow] | [magenta]об.% выполн.[/magenta] | [bold cyan]отклик сайта[/bold cyan] " + \
                                    "| [bold red]цвет.[bold cyan]об[/bold cyan].скор.[/bold red] | [bold cyan]разм.расп.данных[/bold cyan]",
                                    title="Обозначение", style=STL(color="cyan")))
            else:
                console.print(Panel("об.время | об.% выполн. | отклик сайта | цвет.об.время | разм.расп.данных" , title="Обозначение"))
        else:
            if color == True:
                console.print(Panel("[yellow]time[/yellow] | [magenta]perc.[/magenta] | [bold cyan]response [/bold cyan] " + \
                                    "| [bold red]joint[bold cyan].[/bold cyan]rate[/bold red] | [bold cyan]data[/bold cyan]",
                                    title="Designation", style=STL(color="cyan")))
            else:
                console.print(Panel("time | perc. | response | joint.rate | data" , title="Designation"))

### Получить результаты и пройтись по массиву future.
    with progress:
        task0 = progress.add_task("", total=len(BDdemo_new.items())) if color == True else None
        for websites_names, param_websites in BDdemo_new.items():# БД:-скоррект.Сайт--> флаг,эмодзи,url, url_сайта, gray_lst, запрос-future.
            progress.update(task0, advance=1, refresh=True) if color == True else "" #\nprogress.refresh()
## Получить другую информацию сайта снова.
            url = dic_snoop_full.get(websites_names).get("url_user")
            country_emojis = dic_snoop_full.get(websites_names).get("flagcountry")
            country_code = dic_snoop_full.get(websites_names).get("flagcountryklas")
            country_Emoj_Code = country_emojis if sys.platform != 'win32' else country_code
## Пропустить запрещенный никнейм или пропуск сайта из gray-list.
            if dic_snoop_full.get(websites_names).get("exists") is not None:
                continue
## Получить ожидаемый тип данных 4 методов.
            error_type = param_websites["errorTypе"]
## Получить future и убедиться, что оно закончено.
            r, error_type, response_time = get_response(request_future=param_websites["request_future"], error_type=error_type,
                                                        websites_names=websites_names, print_found_only=print_found_only,
                                                        verbose=verbose, color=color
                                                        )
## Повторное соединение через новую сессию быстрее, чем через adapter - timeout*2=дольше.
            if norm == False and quickly == False and r is None and 'raised ConnectionError' in str(future):
                #print(future)
                head_duble = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                              'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                              'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)' + \
                                            'Chrome/76.0.3809.100 Safari/537.36'}

                for _ in range(3):
                    global recensor
                    recensor += 1
                    future_rec = session3.get(url=url, headers=head_duble, allow_redirects=allow_redirects, timeout=1.5)
                    if color and print_found_only == False:
                        print(Style.RESET_ALL + Fore.CYAN + "[" + Style.BRIGHT + Fore.RED + "-" + Style.RESET_ALL + Fore.CYAN + "]" +
                        Style.BRIGHT + Fore.GREEN + "    └──повторное соединение" + Style.RESET_ALL)
                    else:
                        print("повторное соединение") if print_found_only==False else ""
                        #time.sleep(0.1)
                    r, error_type, response_time = get_response(request_future=future_rec, error_type=param_websites.get("errorTypе"),
                                                                websites_names=websites_names, print_found_only=print_found_only,
                                                                verbose=verbose, color=color)
                    if r is not None:
                        break

## Проверка, 4 методов; #1.
# Ответы message (разные локации).
            if error_type == "message":
                error = param_websites.get("errorMsg")
                error2 = param_websites.get("errоrMsg2")
                error3 = param_websites.get("errorMsg3") if param_websites.get("errorMsg3") is not None else "NoneNoneNone"
                if param_websites.get("errorMsg2"):
                    sys.exit()
#                print(r.text) #проверка ответа (+- '-S')
#                print(r.status_code) #Проверка ответа
                if error2 in r.text or error in r.text or error3 in r.text:
                    if not print_found_only:
                        print_not_found(websites_names, response_time, verbose, color)
                    exists = "увы"
                else:
                    print_found_country(websites_names, url, country_Emoj_Code, response_time, verbose, color)
                    exists = "найден!"
                    if reports:
                        sreports(url, headers,session2,error_type, username,websites_names,r)

## Проверка, 4 методов; #2.
# Проверка username при статусе 301 и 303 (перенаправление и соль).
            elif error_type == "redirection":
#                print(r.text) #проверка ответа (+- '-S')
#                print(r.status_code) #Проверка ответа
                if r.status_code == 301 or r.status_code == 303:
                    print_found_country(websites_names, url, country_Emoj_Code, response_time, verbose, color)
                    exists = "найден!"
                    if reports:
                        session_size = sreports(url, headers,session2,error_type, username, websites_names,r)
                else:
                    if not print_found_only:
                        print_not_found(websites_names, response_time, verbose, color)
                        session_size = len(str(r.content))
                    exists = "увы"

## Проверка, 4 методов; #3.
# Проверяет, является ли код состояния ответа 2..
            elif error_type == "status_code":
#                print(r.text) #проверка ответа (+- '-S')
#                print(r.status_code) #Проверка ответа
                if not r.status_code >= 300 or r.status_code < 200:
                    print_found_country(websites_names, url, country_Emoj_Code, response_time, verbose, color)
                    if reports:
                        sreports(url, headers,session2,error_type, username, websites_names,r)
                    exists = "найден!"
                else:
                    if not print_found_only:
                        print_not_found(websites_names, response_time, verbose, color)
                    exists = "увы"

## Проверка, 4 методов; #4
# Перенаправление.
            elif error_type == "response_url":
#                print(r.text) #проверка ответа (+- '-S')
#                print(r.status_code) #Проверка ответа
                if 200 <= r.status_code < 300:
                    print_found_country(websites_names, url, country_Emoj_Code, response_time, verbose, color)
                    if reports:
                        sreports(url, headers,session1,error_type, username, websites_names,r)
                    exists = "найден!"
                else:
                    if not print_found_only:
                        print_not_found(websites_names, response_time, verbose, color)
                    exists = "увы"

## Если все 4 метода не сработали, например, из-за ошибки доступа (красный) или из-за каптчи (желтый).
            else:
                print_invalid("", websites_names, "*ПРОПУСК", color) if not print_found_only else ""
                exists = "блок"

## Попытка получить информацию запроса запись в CSV служебной информации).
            try:
                http_status = r.status_code #запрос статус-кода.
            except:
                http_status = "сбой"
            try:
                response_text = r.text.encode(r.encoding) #запрос данных.
            except:
                response_text = ""
            try:# сессия в КБ.
                if reports == True:
                    session_size = session_size if error_type == 'redirection' else len(str(r.content))
                else:
                    session_size = len(str(r.content))

                if session_size >= 555:
                    session_size = round(session_size/1024)
                elif session_size <= 555:
                    session_size = round((session_size/1024), 2)
            except:
                session_size = "Err"
## Считать 2x-тайминги с приемлемой точностью.
# Реакция.
            ello_time = round(float(time.time() - timestart), 2)#текущее.
            li_time.append(ello_time)
            dif_time = round(li_time[-1] - li_time[-2], 2)#разница.
# Отклик.
            try:
                site_time = str(response_time).rsplit(sep=':', maxsplit=1)[1]
                site_time=round(float(site_time), 2)#реальный ответ.
            except:
                site_time = str("-")

## Опция '-v'.
            if verbose == True:
                if session_size == 0 or session_size is None:
                    Ssession_size = "Head"
                elif session_size == "Err":
                    Ssession_size = "Нет"
                else:
                    Ssession_size = str(session_size) + " Kb"

                if color == True:
                    if dif_time > 2.7 and dif_time != ello_time: #задержка в общем времени
                        console.print(f"[cyan] [*{site_time} s T] >>", f"[bold red][*{ello_time} s t]", f"[cyan][*{Ssession_size}]")
                        console.rule("", style="bold red")
                    else:
                        console.print(f"[cyan] [*{site_time} s T] >>", f"[cyan][*{ello_time} s t]", f"[cyan][*{Ssession_size}]")
                        console.rule("", style="bold blue")
                else:
                    console.print(f" [*{site_time} s T] >>", f"[*{ello_time} s t]", f"[*{Ssession_size}]", highlight=False)
                    console.rule(style="color")

## Служебная информация для CSV.
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

## Добавление результатов этого сайта в окончательный словарь со всеми другими результатами.
            dic_snoop_full[websites_names] = dic_snoop_full.get(websites_names)
# Вернуть словарь со всеми данными на запрос функции snoop.
        return dic_snoop_full

## Опция '-t'.
def timeout_check(value):
    try:
        global timeout
        timeout = int(value)
    except:
        raise argparse.ArgumentTypeError(f"\n\033[31;1mTimeout '{value}' Err,\033[0m \033[36mукажите время в 'секундах'. \033[0m")
    if timeout <= 0:
        raise argparse.ArgumentTypeError(f"\033[31;1mTimeout '{value}' Err,\033[0m \033[36mукажите время > 0sec. \033[0m")
    return timeout

## Обновление Snoop.
def update_snoop():
    print(
"""\033[36m\nВы действительно хотите:
                    __             _  
   ._  _| _._|_ _  (_ ._  _  _ ._   ) 
|_||_)(_|(_| |_(/_ __)| |(_)(_)|_) o  
   |                           |    
нажмите\033[0m 'y' """)
    upd = str(input())

    if upd == "y":
        print(Fore.CYAN + "Функция обновления Snoop требует установки < Git >")
        os.startfile("update.bat") if sys.platform == 'win32' else os.system("./update.sh")
    print(Style.BRIGHT + Fore.RED + "\nВыход")
    sys.exit()

## Удаление отчетов.
def autoclean():
# Определение директорий.
    path_build_del = "/results" if sys.platform != 'win32' else "\\results"
    rm = dirpath + path_build_del
# Подсчет файлов и размера удаляемого каталога 'results'.
    total_size = 0
    delfiles=[]
    for total_file in glob.iglob(rm + '/**/*', recursive=True):
        total_size += os.path.getsize(total_file)
        delfiles.append(total_file) if os.path.isfile(total_file) else ""
# Удаление каталога 'results'.
    try:
        shutil.rmtree(rm, ignore_errors=True)
        print(f"\033[31;1mdeleted --> {rm}\033[0m\033[36m {len(delfiles)} files, {round(total_size/1024/1024, 2)} Mb\033[0m")
    except:
        console.log("[red]Ошибка")
    sys.exit()

## Лого.
def logo(text):
    if sys.platform != 'win32':
        with console.screen():
            console.print("""[cyan]
 ____                                      
/\  _`\                                    
\ \,\L\_\    ___     ___     ___   _____   
 \/_\__ \  /' _ `\  / __`\  / __`\/\ '__`\\
   /\ \L\ \/\ \/\ \/\ \_\ \/\ \_\ \ \ \L\ \\
   \ `\____\ \_\ \_\ \____/\ \____/\ \ ,__/
    \/_____/\/_/\/_/\/___/  \/___/  \ \ \/ 
                                     \ \_\\
      __                              \/_/ 
     /\ \                              
     \_\ \     __    ___ ___     ___   
     /'_` \  /'__`\/' __` __`\  / __`\\
    /\ \_\ \/\  __//\ \/\ \/\ \/\ \_\ \\
    \ \___,_\ \____\ \_\ \_\ \_\ \____/
     \/__,_ /\/____/\/_/\/_/\/_/\/___/ 
""")
            time.sleep(1.4)
    for i in text:
        time.sleep(0.04)
        print(f"\033[31;1m{i}", end='', flush=True)
    print("\033[31;1m\n\nВыход")
    sys.exit()

## Пожертвование.
def donate():
    print("")
    console.print(Panel("""[cyan]
╭donate/Buy:
├──Яндекс.Деньги (Юmoney):: [white]4100111364257544[/white]
├──Visa:: [white]4274320047338002[/white]
├──PayPal:: [white]snoopproject@protonmail.com[/white]
└──Bitcoin (только Donate)::[/cyan] [white]1Ae5uUrmUnTjRzYEJ1KkvEY51r4hDGgNd8[/white]

[bold green]Если вас заинтересовала [red]Snoop Demo Version[/red], Вы можете официально приобрести
[cyan]Snoop Full Version[/cyan], поддержав развитие проекта[/bold green] [bold cyan]20$[/bold cyan] [bold green]или[/bold green] [bold cyan]1400р.[/bold cyan]
[bold green]При пожертвовании/покупке в сообщении укажите информацию в таком порядке:[/bold green]

    [cyan]"Пожертвование на развитие Snoop Project: 20$ ваш e-mail
    Full Version for Windows RU или Full Version for Linux RU,
    статус пользователя: Физ.лицо; ИП; Юр.лицо (если покупка ПО)"[/cyan]

[bold green]В ближайшее время на email пользователя придёт чек и ссылка для скачивания
Snoop Full Version готовой сборки то есть исполняемого файла,
для Windows — это 'snoop.exe', для GNU/Linux — 'snoop'.

Snoop в исполняемом виде (бинарник) предоставляется по лицензии, с которой пользователь должен ознакомиться перед покупкой ПО.
Лицензия (RU/EN) для Snoop Project в исполняемом виде находится в rar-архивах демо версий Snoop по ссылке: [/bold green]
[cyan]https://github.com/snooppr/snoop/releases[/cyan][bold green], а так же лицензия доступна по команде '[/bold green][cyan]snoop -V[/cyan][bold green]' или '[/bold green][cyan]snoop.exe -V[/cyan][bold green]' у исполняемого файла.

Если Snoop требуется вам для служебных или образовательных задач,
напишите письмо на e-mail разработчика в свободной форме.
Студентам по направлению ИБ/Криминалистика Snoop ПО Full Version может быть
предоставлено на безвозмездной основе.

Snoop Full Version: плагины без ограничений; 2200+ Websites;
поддержка и обновление Database Snoop.
Подключение к Web_Database Snoop (online), которая расширяется/обновляется.[/bold green]
[bold red]Ограничения Demo Version: Websites (Database Snoop сокращена в > 15 раз);
отключены некоторые опции/плагины; необновляемая Database_Snoop.[/bold red]

[bold green]Email:[/bold green] [cyan]snoopproject@protonmail.com[/cyan]
[bold green]Исходный код:[/bold green] [cyan]https://github.com/snooppr/snoop[/cyan]""", title="[bold red]Demo: (Публичная оферта)",
border_style="bold blue"))# ,style="bold green"))
    webbrowser.open("https://sobe.ru/na/snoop_project_2020")
    print(Style.BRIGHT + Fore.RED + "Выход")
    sys.exit()

## Лицензия/версия.
def license_snoop():
    with open('COPYRIGHT', 'r', encoding="utf8") as copyright:
        cop = copyright.read().replace("\ufeffSnoop", "Snoop")
        console.print(Panel(cop, title='COPYRIGHT', style=STL(color="white", bgcolor="blue")))

    threadS = int(psutil.cpu_count() / psutil.cpu_count(logical=False))
    console.print('\n',
Panel(f"""Snoop: {platform.architecture(executable=sys.executable, bits='', linkage='')}
Source: {version}
OS: {platform.platform(aliased=True, terse=0)}
Locale: {locale.setlocale(locale.LC_ALL)}
Python: {platform.python_version()}
CPU(s): {psutil.cpu_count()}, threads(s): {threadS}
Ram: {int(psutil.virtual_memory().total/1024/1024)} Мб, доступно: {int(psutil.virtual_memory().available/1024/1024)} Мб""",
title='snoop info', style=STL(color="cyan")))
    sys.exit()
#    print(repr(cop))

### ОСНОВА.
def run():
## Назначение опций Snoop.
    parser = argparse.ArgumentParser(formatter_class = argparse.RawDescriptionHelpFormatter,
                            usage = 'python3 %(prog)s [options] nickname\nor\nusage: python3 %(prog)s nickname [options]\n ',
                            description = Fore.CYAN + "Справка" + Style.RESET_ALL,
                            epilog = (Fore.CYAN + f"Snoop " + Style.BRIGHT + Fore.RED + f"Demo Version " + Style.RESET_ALL + \
                            Fore.CYAN + f"поддержка: \033[31;1m{flagBS}\033[0m  \033[36mWebsites!\n"  + Fore.CYAN +
                            f"Snoop \033[36;1mFull Version\033[0m \033[36mподдержка: \033[36;1m2200+\033[0m \033[36mWebsites!!!\033[0m\n" +\
                            f" \033[32;1mEnglish version — see release (available 'old build Snoop EN version')\033[0m\n\n"))
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
                               \033[32;1mSnoop Full Version\033[0m"
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
                               help="\033[36mO\033[0mSINT поиск: задействовать различные плагины Snoop:: IP/GEO/YANDEX \
                               (список плагинов будет пополняться)"
                              )
# Search arguments.
    search_group = parser.add_argument_group('\033[36msearch arguments\033[0m')
    search_group.add_argument("username", nargs='*', metavar='nickname', action="store", default=None,
                              help="\033[36mН\033[0mикнейм разыскиваемого пользователя. \
                              Поддерживается поиск одновременно нескольких имён.\
                              Ник, содержащий в своем имени пробел, заключается в кавычки"
                             )
    search_group.add_argument("--verbose", "-v", action="store_true", dest="verbose", default=False,
                              help="\033[36mВ\033[0mо время поиска 'username' выводить на печать подробную вербализацию"
                             )
    search_group.add_argument("--base", "-b <path>", dest="json_file", default="BDdemo", metavar='',
                              help="\033[36mУ\033[0mказать для поиска 'username' другую БД (Локально)/В demo version функция отключена"
                             )
    search_group.add_argument("--web-base", "-w", action="store_true", dest="web", default=False,
                              help="\033[36mП\033[0mодключиться для поиска 'username' к обновляемой web_БД (Онлайн)/\
                              В demo version функция отключена"
                             )
    search_group.add_argument("--site", "-s chess", action="append", metavar='', dest="site_list",  default=None,
                              help="\033[36mУ\033[0mказать имя сайта из БД '--list-all'. Поиск 'username' на одном указанном ресурсе, \
                              допустимо использовать опцию '-s' несколько раз"
                             )
    search_group.add_argument("--exclude", "-e RU", action="append", metavar='', dest="exclude_country",  default=None,
                              help="\033[36mИ\033[0mсключить из поиска выбранный регион, \
                              допустимо использовать опцию '-e' несколько раз, например, '-e ru -e wr' исключить из поиска Россию и Мир"
                             )
    search_group.add_argument("--one-level", "-o UA", action="append", metavar='', dest="one_level",  default=None,
                              help="\033[36mВ\033[0mлючить в поиск только выбранный регион, \
                              допустимо использовать опцию '-o' несколько раз, например, '-o us -o ua' поиск по США и Украине"
                             )
    search_group.add_argument("--country", "-c", action="store_true", dest="country", default=False,
                              help="\033[36mС\033[0mортировка 'печать/запись_результатов' по странам, а не по алфавиту"
                             )
    search_group.add_argument("--time-out", "-t 9", action="store", metavar='', dest="timeout", type=timeout_check, default=5,
                              help="\033[36mУ\033[0mстановить выделение макс.времени на ожидание ответа от сервера (секунды).\n"
                              "Влияет на продолжительность поиска. Влияет на 'Timeout ошибки:'"
                              "Вкл. эту опцию необходимо при медленном \
                              интернет соединении, чтобы избежать длительных зависаний \
                              при неполадках в сети (по умолчанию значение выставлено 5с)"
                             )
    search_group.add_argument("--found-print", "-f", action="store_true", dest="print_found_only", default=False,
                              help="\033[36mВ\033[0mыводить на печать только найденные аккаунты"
                             )
    search_group.add_argument("--no-func", "-n", action="store_true", dest="no_func", default=False,
                              help="\033[36m✓\033[0mМонохромный терминал, не использовать цвета в url\
                              ✓Отключить звук\
                              ✓Запретить открытие web browser-а\
                              ✓Отключить вывод на печать флагов стран\
                              ✓Отключить индикацию и статус прогресса.\
                              Экономит ресурсы системы и ускоряет поиск"
                             )
    search_group.add_argument("--userlist", "-u <path>", metavar='', action="store", dest="user", default=False,
                              help="\033[36mУ\033[0mказать файл со списком user-ов. \
                              Пример_Linux: 'python3 snoop.py -u ~/users.txt'.\
                              Пример_Windows: 'python snoop.py -u c:\\User\\User\Documents\\users.txt'"
                             )
    search_group.add_argument("--save-page", "-S", action="store_true", dest="reports", default=False,
                              help="\033[36mС\033[0mохранять найденные странички пользователей в локальные файлы"
                             )
    search_group.add_argument("--cert-on", "-C", default=False, action="store_true", dest="cert",
                              help="""\033[36mВ\033[0mкл проверку сертификатов на серверах. По умолчанию проверка сертификатов
                              на серверах отключена, что даёт меньше ошибок и больше положительных результатов
                              при поиске nickname"""
                             )
    search_group.add_argument("--headers", "-H <name>", action="append", metavar='', dest="headerS",  default=None,
                              help="""\033[36mЗ\033[0mадать user-agent вручную, агент заключается в кавычки, по умолчанию для каждого сайта
                               задаётся случайный либо переопреденный user-agent из БД snoop. https://юзерагент.рф/"""
                             )
    search_group.add_argument("--normal-mode", "-N", action="store_false", dest="norm", default=True,
                              help="""\033[36mП\033[0mереключатель режимов: SNOOPninja > нормальный режим > SNOOPninja.
                              По_умолчанию (GNU/Linux Full Version) вкл 'режим SNOOPninja':
                              ускорение поиска ~25pct, экономия ОЗУ ~50pct, повторное 'гибкое' соединение на сбойных ресурсах.
                              Режим SNOOPninja эффективен только для Snoop for GNU/Linux Full Version.
                              По_умолчанию (в Windows) вкл 'нормальный режим'. В Demo Version переключатель режимов деактивирован"""
                             )
    search_group.add_argument("--quick-mode ", "-q", default=False, action="store_true", dest="quickly",
                              help="""\033[36mВ\033[0mкл  тихий режим поиска. Промежуточные результаты не выводятся на печать.
                              Повторные гибкие соединения на сбойных ресурсах без замедления ПО.
                              Самый прогрессивный режим поиска (в разработке - не использовать)"""
                             )

    args = parser.parse_args()
    logo(text="🛠 новая функциональность — в разработке") if args.quickly else ""
#    print(args)
## Опции  '-cseo' несовместимы между собой.
    k=0
    for _ in bool(args.site_list), bool(args.country), bool(args.exclude_country), bool(args.one_level):
        if _ == True:
            k += 1
        if k == 2:
            logo(text="⛔️ опциии ['-c', '-e' '-o', '-s'] несовместимы между собой")
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
            print("""\n
\033[36m╭Выберите плагин или действие из списка\033[0m
\033[36m├──\033[0m\033[36;1m[1] --> GEO_IP/domain\033[0m
\033[36m├──\033[0m\033[36;1m[2] --> Reverse Vgeocoder\033[0m
\033[36m├──\033[0m\033[36;1m[3] --> Yandex_parser\033[0m
\033[36m├──\033[0m\033[32;1m[help] --> Справка\033[0m
\033[36m└──\033[0m\033[31;1m[q] --> Выход\033[0m\n""")
            mod = console.input("[cyan]Я выбираю: [/cyan]")

            if mod == 'help':
                print("""\033[32;1m└──[Справка]\033[0m

\033[32;1m========================
| Плагин GEO_IP/domain |
========================\033[0m \033[32m\n
1) Реализует онлайн одиночный поиск цели по IP/url/domain и предоставляет статистическую информацию:
IPv4/v6; GEO-координаты/ссылку; локация
    (лёгкий ограниченный поиск).

2) Реализует онлайн поиск цели по списку данных: и предоставляет статистическую и визуализированную информацию:
IPv4/v6; GEO-координаты/ссылки; страны/города; отчеты в CLI/txt/csv форматах; предоставляет визуализированный отчет на картах OSM
    (умеренный не быстрый поиск: ограничения запросов:: 15к/час; не предоставляет информацию о провайдерах).

3) Реализует офлайн поиск цели по списку данных, используя БД: и предоставляет статистическую и визуализированную информацию:
IPv4/v6; GEO-координаты/ссылки; локации; провайдеры; отчеты в CLI/txt/csv форматах; предоставляет визуализированный отчет на картах OSM
    (сильный и быстрый поиск).

Результаты по 1 и 2 методу могут отличаться и быть неполными - зависит от персональных настроек DNS/IPv6 пользователя.
Список данных — текстовый файл (в кодировке utf-8), который пользователь указывает в качестве цели, и который содержит ip, domain или url (или их комбинации).

\033[32;1m============================
| Плагин Reverse Vgeocoder |
============================\033[0m\n
\033[32mОбратный геокодер для визуализации координат на карте OSM и статистическим анализом в csv/txt форматах.
Плагин реализует оффлайн поиск цели по заданным геокоординатам и предоставляет статистическую и визуализированную информацию.
С помощью данного плагина пользователь способен получить и проанализировать информацию о тысячах геокоординат за несколько секунд.
Предназначение плагина — CTF.\033[0m

\033[32;1m========================
| Плагин Yandex_parser |
========================\033[0m\n
\033[32mПлагин позволяет получить информацию о пользователе/пользователях сервисов Яндекс:
Я_Отзывы; Я_Кью; Я_Маркет; Я_Музыка; Я_Дзен; Я_Диск; E-mail, Name.
И связать полученные данные между собой с высокой скоростью и масштабно.
Предназначение — OSINT.

Плагин разработан на идее и материалах уязвимости, отчёты былы отправлены Яндексу в рамках программы «Охота за ошибками».
Попал в зал славы, получил финансовое вознаграждение, а Яндекс исправил 'ошибки' по своему усмотрению.

Подробнее о плагинах (скриншоты примеров) см. документацию Snoop Project.\033[0m""")

                console.rule("[bold red]Конец справки")
                module()
            elif mod == '1':
                table = Table(title = Style.BRIGHT + Fore.GREEN + "Выбран плагин" + Style.RESET_ALL, style="green")
                table.add_column("GEO_IP/domain_v0.2", style="green")
                table.add_row('Получение информации об ip/domain/url цели или по списку этих данных')
                console.print(table)
                snoopplugins.module1()
            elif mod == '2':
                table = Table(title = Style.BRIGHT + Fore.GREEN + "Выбран плагин" + Style.RESET_ALL, style="green")
                table.add_column("Reverse Vgeocoder_v0.4", style="green")
                table.add_row('Визуализация Географических координат')
                console.print(table)
                snoopplugins.module2()
            elif mod == '3':
                table = Table(title = Style.BRIGHT + Fore.GREEN + "Выбран плагин" + Style.RESET_ALL, style="green")
                table.add_column("Yandex_parser_v0.5", style="green")
                table.add_row('Яндекс парсер: Я_Отзывы; Я_Кью; Я_Маркет; Я_Музыка; Я_Дзен; Я_Диск; E-mail; Name.')
                console.print(table)
                snoopplugins.module3()
            elif mod == 'q':
                print(Style.BRIGHT + Fore.RED + "└──Выход")
                sys.exit()
            else:
                print(Style.BRIGHT + Fore.RED + "└──Неверный выбор\n" + Style.RESET_ALL)
                module()
        module()
        sys.exit()

## Опция  '-f' + "-v".
    if args.verbose and args.print_found_only:
        logo(text="⛔️ Режим подробной вербализации [опция '-v'] отображает детальную информацию,\n   [опция '-f'] неуместна")
## Опция  '-С'.
    if args.cert:
        print(Fore.CYAN + "[+] активирована опция '-C': «проверка сертификатов на серверах вкл»")
## Опция режима SNOOPnina > < нормальный режим.
    if args.norm == False:
        logo(text="[-] в demo деактивирован переключатель '--': «режимов SNOOPninja/Normal»")
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
        if args.timeout:
            print(Fore.CYAN + f"[+] активирована опция '-t': «snoop будет ожидать ответа от сайта \033[36;1m<= {timeout}_sec\033[0m\033[36m.» \033[0m")
    except:
        pass
## Опция '-f'.
    if args.print_found_only:
        print(Fore.CYAN + "[+] активирована опция '-f': «выводить на печать только найденные аккаунты»")
## Опция '-s'.
    if args.site_list:
        print(f"{Fore.CYAN}[+] активирована опция '-s': «поиск '{Style.BRIGHT}{Fore.CYAN}{', '.join(args.username)}{Style.RESET_ALL}" + \
              f"{Fore.CYAN}' на выбранных website(s)»\n"
        "    допустимо использовать опцию '-s' несколько раз\n"
        "    [опция '-s'] несовместима с [опциями '-с', '-e', 'o']")
## Опция '-v'.
    if args.verbose and bool(args.username):
        print(Fore.CYAN + "[+] активирована опция '-v': «подробная вербализация в CLI»\n")
        with console.status("[cyan]Ожидайте, идёт самотестирование сети..."):
            networktest.nettest()
            console.log("[cyan]--> тест сети")
## Опция '--list-all'.
    if args.listing:
        print(Fore.CYAN + "[+] активирована опция '-l': «детальная информация о БД snoop»")
        print("\033[36m\nСортировать БД Snoop по странам, по имени сайта или обобщенно ?\n" + \
              "по странам —\033[0m 1 \033[36mпо имени —\033[0m 2 \033[36mall —\033[0m 3\n")
        sortY = console.input("[cyan]Выберите действие: [/cyan]")

# Общий вывод стран (3!).
# Вывод для Full/Demo Version.
        def sort_list_all(DB, fore, version, line=None):
            if sortY == "3":
                console.rule("[cyan]Ok, print All Country:", style="cyan bold") if line == "str_line" else ""
                print("")
                li = [DB.get(con).get("country_klas") if sys.platform == 'win32' else DB.get(con).get("country") for con in DB]
                cnt = str(Counter(li))
                try:
                    flag_str_sum = (cnt.split('{')[1]).replace("'", "").replace("}", "").replace(")", "")
                    all_= str(len(DB))
                    #raise Exception("")
                except:
                    flag_str_sum = str("БД повреждена.")
                    all_= "-1"
                table = Table(title = Style.BRIGHT + fore + version + Style.RESET_ALL, style="green")
                table.add_column("Страна:Кол-во websites", style="magenta")
                table.add_column("All", style="cyan", justify='full')
                table.add_row(flag_str_sum, all_)
                console.print(table)

# Сортируем по алфавиту для Full/Demo Version (2!).
            elif sortY == "2":
                console.rule("[cyan]Ok, сортируем по алфавиту:",style="cyan bold") if line == "str_line" else ""
                if version == "Demo Version":
                    console.print('\n', Panel.fit("++База данных++", title=version, style=STL(color="cyan", bgcolor="red")))
                else:
                    console.print('\n', Panel.fit("++База данных++", title=version, style=STL(color="cyan")))
                i = 0
                sorted_dict_v_listtuple = sorted(DB.items(), key=lambda x: x[0].lower()) # сорт.словаря по глав.ключу без учета регистра
                datajson_sort = dict(sorted_dict_v_listtuple) #преобр.список обратно в словарь (сортированный)

                for con in datajson_sort:
                    S = datajson_sort.get(con).get("country_klas") if sys.platform == 'win32' else datajson_sort.get(con).get("country")
                    i += 1
                    print(f"{Style.BRIGHT}{Fore.GREEN}{i}. {Style.RESET_ALL}{Fore.CYAN}{S}  {con}\n================")

# Сортируем по странам для Full/Demo Version (1!).
            elif sortY == "1":
                console.rule("[cyan]Ok, сортируем по странам:",style="cyan bold") if line == "str_line" else ""
                listwindows = []

                for con in DB:
                    S = DB.get(con).get("country_klas") if sys.platform == 'win32' else DB.get(con).get("country")
                    listwindows.append(f"{S}  {con}\n")

                if version == "Demo Version":
                    console.print('\n', Panel.fit("++База данных++", title=version, style=STL(color="cyan", bgcolor="red")))
                else:
                    console.print('\n', Panel.fit("++База данных++", title=version, style=STL(color="cyan")))

                for i in enumerate(sorted(listwindows, key=str.lower), 1):
                    print(f"{Style.BRIGHT}{Fore.GREEN}{i[0]}. {Style.RESET_ALL}{Fore.CYAN}{i[1]}", end = '')

# Действие не выбрано --list-all.
            else:
                print(Style.BRIGHT + Fore.RED + "└──Извините, но вы не выбрали действие [1/2/3]\n\nвыход")
                sys.exit()
# Запуск функции '--list-all'.
        if sortY != "3":
            sort_list_all(BDflag, Fore.GREEN, "Full Version", line = "str_line")
            sort_list_all(BDdemo, Fore.RED, "Demo Version")
        else:
            sort_list_all(BDdemo, Fore.RED, "Demo Version", line = "str_line")
            sort_list_all(BDflag, Fore.GREEN, "Full Version")
        sys.exit()

## Опция донат '-d y'.
    if args.donation:
        print(Fore.CYAN + "[+] активирована опция '-d': «финансовая поддержка проекта»")
        donate()
## Опция '-u' указания файла-списка разыскиваемых пользователей.
    if args.user:
        userlists=[]
        userlists_bad=[]
        with open('specialcharacters', 'r', encoding="utf-8") as errspec:
            my_list_bad = list(errspec.read())
        try:
            patchuserlist = ("{}".format(args.user))
            userfile = patchuserlist.split('/')[-1] if sys.platform != 'win32' else patchuserlist.split('\\')[-1]
            with open(patchuserlist, "r", encoding="utf8") as u1:
                userlist=[line.strip() for line in u1.read().splitlines()]
                for i in userlist:
                    if any(D in i for D in my_list_bad):
                        userlists_bad.append(i)
                        continue
                    elif any(' ' in i for i in i):
                        g11 = " ".join(i.split())
                        userlists.append(g11) if g11 not in userlist else ""
                    elif i == "":
                        continue
                    else:
                        userlists.append(i)
            print(Fore.CYAN + f"[+] активирована опция '-u': «розыск nickname(s) из файла: \033[36;1m{userfile}\033[0m\033[36m»::\033[0m")
            console.print(Panel.fit("\n".join(userlists), title='valid', style=STL(color="cyan")))
        except:
            print(f"\033[31;1mНе могу найти_прочитать файл: '{userfile}'.\033[0m \033[36m " + \
                   "\nПожалуйста, укажите текстовый файл в кодировке —\033[0m \033[36;1mutf-8.\033[0m\n")
            print("\033[36mПо умолчанию, например, блокнот в OS Windows сохраняет текст в кодировке — ANSI.\033[0m")
            print("\033[36mОткройте ваш список пользователей и измените кодировку [файл ---> сохранить как ---> utf-8].")
            print("\033[36mИли удалите из файла нечитаемые спецсимволы.")
            sys.exit()
        if userlists_bad:
            print(f"\n\033[36mСледующие [nickname(s)] из '\033[36;1m{userfile}\033[0m\033[36m' содержат " + \
                   "\033[31;1mN/A-символы\033[0m\033[36m и будут пропущены:\033[0m")
            console.print(Panel.fit("\n".join(userlists_bad), title='invalid', style=STL(color="bright_red")))
        sys.exit() if bool(userlists) == False else ""

## Проверка остальных (в т.ч. повтор) опций.
## Опция '--update y' обновление Snoop.
    if args.update:
        print(Fore.CYAN + "[+] активирована опция '-U': «Обновление Snoop»")
        update_snoop()
## Опция '-w'.
    if args.web:
        print("\n\033[37m\033[44m{}".format("Функция '-w' доступна только пользователям Snoop Full Version..."))
        donate()
## Работа с базой.
# Проверить, существует ли альтернативная база данных, иначе demo.
    if not os.path.exists(str(args.json_file)):
        print(f"\033[31;1mОшибка! Неверно указан путь к файлу: '{str(args.json_file)}'.\033[0m")
        sys.exit()

## Опция  '-c'. Сортировка по странам.
    if args.country:
        print(Fore.CYAN + "[+] активирована опция '-c': «сортировка/запись результатов по странам»")
        country_sites = sorted(BDdemo, key=lambda k: ("country" not in k, BDdemo[k].get("country", sys.maxsize)))
        sort_web_BDdemo_new = {}
        for site in country_sites:
            sort_web_BDdemo_new[site] = BDdemo.get(site)

## Функция для опций '-eo'
    def one_exl(one_exl_, bool_):
        lap = []
        bd_flag = []

        for k,v in BDdemo.items():
            bd_flag.append(v.get('country_klas').lower())
            if all(item.lower() != v.get('country_klas').lower() for item in one_exl_) == bool_:
                BDdemo_new[k] = v

        enter_coun_u=[x.lower() for x in one_exl_]
        lap=list(set(bd_flag) & set(enter_coun_u))
        diff_list=list(set(enter_coun_u) - set(bd_flag)) # вывести уникальные элементы только из enter_coun_u иначе set(enter_coun_u)^set(bd_flag)

        if bool(BDdemo_new) == False:
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
# Пользователь выборочно запускает запросы к подмножеству списку сайтов из БД.
# Убедиться, что сайты в базе имеются, создать для проверки сокращенную базу данных сайта(ов).
        for site in args.site_list:
            for site_yes in BDdemo:
                if site.lower() == site_yes.lower():
                    BDdemo_new[site_yes] = BDdemo[site_yes] #выбираем в словарь найденные сайты из БД

            diff_k_bd = set(BDflag) ^ set(BDdemo)
            for site_yes_full_diff in diff_k_bd:
                if site.lower() == site_yes_full_diff.lower(): #если сайт (-s) в БД Full версии.
                    print(f"\033[31;1m[?] Пропуск:\033[0m \033[36mсайт из БД \033[36;1mFull-версии\033[0m \033[36mнедоступен в" +
                          f"\033[0m \033[33;1mDemo-версии\033[0m\033[36m:: '\033[30;1m{site_yes_full_diff}\033[0m\033[36m'\033[0m")

            if not any(site.lower() == site_yes_full.lower() for site_yes_full in BDflag): #если ни одного совпадения по сайту
                print(f"\033[31;1m[!] Пропуск:\033[0m \033[36mжелаемый сайт отсутствует в БД Snoop:: '" +
                      f"\033[31;1m{site}\033[0m\033[36m'\033[0m")

## Отмена поиска, если нет ни одного совпадения по БД и '-s'.
        if not BDdemo_new:
            sys.exit()

## Опция '-e'.
# Создать для проверки сокращенную базу данных сайта(ов).
# Создать и добавить в новую БД сайты, аргументы (-e) которых != бук.кодам стран (country_klas).
    elif args.exclude_country is not None:
        lap, diff_list = one_exl(one_exl_ = args.exclude_country, bool_=True)

        print(Fore.CYAN + f"[+] активирована опция '-e': «исключить из поиска выбранные регионы»::", end=' ')
        print(Style.BRIGHT + Fore.CYAN + str(lap).strip('[]').upper() + Style.RESET_ALL + " " + Style.BRIGHT + Fore.RED + \
        str(diff_list).strip('[]') + Style.RESET_ALL + Fore.CYAN + "\n" + \
        "    допустимо использовать опцию '-e' несколько раз\n"
        "    [опция '-e'] несовместима с [опциями '-s', '-c', 'o']")

## Опция '-o'.
# Создать для проверки сокращенную базу данных сайта(ов).
# Создать и добавить в новую БД сайты, аргументы (-e) которых != бук.кодам стран (country_klas).
    elif args.one_level is not None:
        lap, diff_list = one_exl(one_exl_ = args.one_level, bool_=False)

        print(Fore.CYAN + f"[+] активирована опция '-o': «включить в поиск только выбранные регионы»::", end=' ')
        print(Style.BRIGHT + Fore.CYAN + str(lap).strip('[]').upper() + Style.RESET_ALL + " " + Style.BRIGHT + Fore.RED + \
        str(diff_list).strip('[]') + Style.RESET_ALL + Fore.CYAN + "\n" + \
        "    допустимо использовать опцию '-o' несколько раз\n"
        "    [опция '-o'] несовместима с [опциями '-s', '-c', 'e']")

## Ник не задан или противоречие.
    if bool(args.username) == False and bool(args.user) == False:
        logo(text="параметры либо nickname(s) не задан(ы)")
    if bool(args.username) == True and bool(args.user) == True:
        print("\n\033[31;1mВыберите для поиска nickname(s) из файла или задайте в cli,\n" + \
              "но не совместное использование nickname(s): из файла и cli.\n\nВыход")
        sys.exit()
## Опция  '-w' не активна.
    try:
        if args.web == False:
            print(f"\n{Fore.CYAN}загружена локальная база: {Style.BRIGHT}{Fore.CYAN}{len(BDdemo)}_Websites{Style.RESET_ALL}")
    except:
        print("\033[31;1mInvalid загружаемая база данных.\033[0m")


## Крутим user's.
    def starts(SQ):
        kef_user=0
        ungzip, ungzip_all, find_url_lst, el =[],[],[],[]
        exl = "/".join(lap).upper() if args.exclude_country is not None else "нет" #искл.регионы_valid.
        one = "/".join(lap).upper() if args.one_level is not None else "нет" #вкл.регионы_valid.
        for username in SQ:
            kef_user+=1
            sort_sites = sort_web_BDdemo_new if args.country == True else BDdemo_new
            FULL = snoop(username, sort_sites, country=args.country, user=args.user, verbose=args.verbose, cert=args.cert,
                        norm=args.norm, reports=args.reports, print_found_only=args.print_found_only, timeout=args.timeout,
                        color=not args.no_func, quickly=args.quickly, headerS = args.headerS)

            if args.quickly:
                print(FULL)

            exists_counter = 0

## Запись в txt.
            try:
                file_txt = open(f"{dirpath}/results/nicknames/txt/{username}.txt", "w", encoding="utf-8")
                #raise Exception("")
            except:
                file_txt = open(f"{dirpath}/results/nicknames/txt/username{time.strftime('%d_%m_%Y_%H_%M_%S', time_date)}.txt", "w", encoding="utf-8")

            file_txt.write("Адрес | ресурс" + "\n\n")

            for website_name in FULL:
                dictionary = FULL[website_name]
                if type(dictionary.get("session_size")) != str:
                    ungzip.append(dictionary.get("session_size")), ungzip_all.append(dictionary.get("session_size"))
                if dictionary.get("exists") == "найден!":
                    exists_counter += 1
                    find_url_lst.append(exists_counter)
                    file_txt.write(dictionary ["url_user"] + " | " + (website_name)+"\n")
# Размер сессии персональный и общий, кроме CSV.
            try:
                sess_size=round(sum(ungzip)/1024 , 2)#в МБ
                s_size_all=round(sum(ungzip_all)/1024 , 2)#в МБ
            except:
                sess_size=0.00000000001
                s_size_all="Err"
            timefinish = time.time() - timestart - sum(el)
            el.append(timefinish)
            time_all = str(round(time.time() - timestart))

            file_txt.write("\n" f"Запрашиваемый объект: <{nick}> найден: {exists_counter} раз(а).")
            file_txt.write("\n" f"Сессия: {str(round(timefinish))}сек {str(sess_size)}Mb.")
            file_txt.write("\n" f"База Snoop (Demo Version): {flagBS} Websites.")
            file_txt.write("\n" f"Исключённые регионы: {exl}.")
            file_txt.write("\n" f"Выбор конкретных регионов: {one}.")
            file_txt.write("\n" f"Обновлено: {time.strftime('%d/%m/%Y_%H:%M:%S', time_date)}.")
            file_txt.close()

## Запись в html.
            try:
                file_html = open(f"{dirpath}/results/nicknames/html/{username}.html", "w", encoding="utf-8")
                #raise Exception("")
            except:
                file_html = open(f"{dirpath}/results/nicknames/html/username" + time.strftime("%d_%m_%Y_%H_%M_%S", time_date) + ".html", "w",
                                  encoding="utf-8")

            file_html.write("<!DOCTYPE html>\n<head>\n<meta charset='utf-8'>\n<style>\nbody { background: url(../../../web/public.png) " + \
            "no-repeat 20% 0%; }\n</style>\n<link rel='stylesheet' href='../../../web/style.css'>\n</head>\n<body>\n\n" + \
            "<div id='particles-js'></div>\n" + \
            "<div id='report'>\n\n" + \
            "<h1><a class='GL' href='file://" + f"{dirpath}/results/nicknames/html/'>Главная</a>" + "</h1>\n")
            file_html.write("<h3>Snoop Project (Demo Version)</h3>\n<p>Нажмите: 'сортировать по странам', возврат: 'F5':</p>\n" + \
            "<button onclick='sortList()'>Сортировать по странам</button><br><br>\n\n")
            file_html.write("Объект " + "<b>" + (nick) + "</b>" + " найден на нижеперечисленных " + "<b>" + str(exists_counter) +
            "</b> ресурсах:\n" + "<br><ol" + " id='id777'>\n")

            li = []            
            for website_name in FULL:
                dictionary = FULL[website_name]
                flag_sum=dictionary["flagcountry"]
                if dictionary.get("exists") == "найден!":
                    li.append(flag_sum)
                    file_html.write("<li>" + dictionary["flagcountry"] + "<a target='_blank' href='" + dictionary ["url_user"] + "'>" +
                    (website_name) + "</a>" + "</li>\n")
            try:
                cnt = str(Counter(li))
                flag_str_sum = (cnt.split('{')[1]).replace("'", "").replace("}", "").replace(")", "").replace(",", "  ↯  ").replace(":", "⇔")
            except:
                flag_str_sum = "0"

            file_html.write("</ol>GEO: " + str(flag_str_sum) + ".\n")
            file_html.write("<br> Запрашиваемый объект < <b>" + str(nick) + "</b> > найден: <b>" + str(exists_counter) + "</b> раз(а).")
            file_html.write("<br> Сессия: " + "<b>" + str(round(timefinish)) + "сек_" + str(sess_size) + "Mb</b>.\n")
            file_html.write("<br> Исключённые регионы: <b>" + str(exl) + ".</b>\n")
            file_html.write("<br> Выбор конкретных регионов: <b>" + str(one) + ".</b>\n")
            file_html.write("<br> База Snoop (Demo Version): <b>" + str(flagBS) + "</b>" + " Websites.\n")
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

<a target='_blank' href='https://github.com/snooppr/snoop' class="SnA"><span class="SnSpan">💊 Source Исходный код</span></a>
<a target='_blank' href='https://sobe.ru/na/snoop_project_2020' class="DnA"><span class="DnSpan">💊 Donation Пожертвование</span></a>
<br><br><br><br>

</body>
</html>""")
            file_html.close()

## Запись в csv.
            try:
                file_csv = open(f"{dirpath}/results/nicknames/csv/{username}.csv", "w", newline='')#, encoding="utf-8")
                #raise Exception("")
            except:
                file_csv = open(f"{dirpath}/results/nicknames/csv/username {time.strftime('%d_%m_%Y_%H_%M_%S', time_date)}.csv",
                                "w", newline='')

            usernamCSV = re.sub(" ", "_", nick)
            censors_cor = int((censors - recensor)/kef_user) #err_connection
            censors_timeout_cor = int(censors_timeout/kef_user) #err time-out
            flagBS_err = round((censors_cor + censors_timeout_cor)*100/flagBS, 3)

            writer = csv.writer(file_csv)
            writer.writerow(['Никнейм', 'Ресурс', 'Страна', 'Url', 'Ссылка_на_профиль', 'Статус', 'Статус_http', 'Общее_замедление/сек',
                             'Отклик/сек', 'Общее_время/сек', 'Сессия/Kb'])

            for site in FULL:
                if FULL[site]['session_size'] == 0:
                    Ssession = "Head"
                elif type(FULL[site]['session_size']) != str:
                    Ssession = str(FULL.get(site).get("session_size")).replace('.',locale.localeconv()['decimal_point'])
                else:
                    Ssession = "Bad"

                writer.writerow([usernamCSV, site, FULL[site]['countryCSV'], FULL[site]['url_main'], FULL[site]['url_user'],
                                 FULL[site]['exists'], FULL[site]['http_status'],
                                 FULL[site]['response_time_site_ms'].replace('.',locale.localeconv()['decimal_point']),
                                 FULL[site]['check_time_ms'].replace('.',locale.localeconv()['decimal_point']),
                                 FULL[site]['response_time_ms'].replace('.',locale.localeconv()['decimal_point']),
                                 Ssession])

            writer.writerow(['«' + "-"*30, '-'*8, '-'*4, '-'*35, '-'*56, '-'*13, '-'*17, '-'*32,'-'*13, '-'*23, '-'*16 + '»'])
            writer.writerow([f'БД_(DemoVersion)={flagBS}_Websites'])
            writer.writerow('')
            writer.writerow([f'Исключённые_регионы={exl}'])
            writer.writerow([f'Выбор_конкретных_регионов={one}'])
            writer.writerow([f"Bad_raw:_{flagBS_err}%_БД" if flagBS_err >= 2 else ''])
            writer.writerow('')
            writer.writerow(['Дата'])
            writer.writerow([time.strftime("%d/%m/%Y_%H:%M:%S", time_date)])
            file_csv.close()

            ungzip.clear()
            #print(exists_counter) if 'exists_counter' in locals() else ""
## Финишный вывод.
        direct_results = f"{dirpath}/nicknames/results/*/{username}.*" if sys.platform != 'win32' else f"{dirpath}\\results\\*\\{username}.*"
        print(f"{Fore.CYAN}├─Результаты:{Style.RESET_ALL} найдено --> {len(find_url_lst)} url (сессия: {time_all} сек_{s_size_all}Mb)")
        print(f"{Fore.CYAN}├──Cохранено в:{Style.RESET_ALL} {direct_results}")
        if flagBS_err >= 2:#perc
            print(f"{Fore.CYAN}├───Дата поиска:{Style.RESET_ALL} {time.strftime('%d/%m/%Y_%H:%M:%S', time_date)}")
            print(f"{Fore.CYAN}└────\033[31;1mВнимание! Bad_raw: {flagBS_err}% БД\033[0m")
            print(f"{Fore.CYAN}     └─нестабильное соединение или Internet Censorship")
            print("       \033[36m└─используйте \033[36;1mVPN\033[0m \033[36mили увеличьте значение опции" + \
                  " '\033[36;1m-t\033[0m\033[36m'\033[0m\n")
        else:
            print(f"{Fore.CYAN}└───Дата поиска:{Style.RESET_ALL} {time.strftime('%d/%m/%Y_%H:%M:%S', time_date)}\n")
        console.print(Panel(f"{e_mail} до {Do}",title=license, style=STL(color="white", bgcolor="blue")))

## Музыка.
        try:
            if args.no_func==False:
                playsound('end.wav')
        except:
            pass

## Открывать/нет браузер с результатами поиска.
        if args.no_func==False and exists_counter >= 1:
            if not "arm" in platform.platform(aliased=True, terse=0) and not "aarch64" in platform.platform(aliased=True, terse=0):
                try:
                    webbrowser.open(f"file://{dirpath}/results/nicknames/html/{username}.html")
                except:
                    pass
## поиск по выбранным пользователям.
    starts(args.username) if args.user==False else starts(userlists)
## Arbeiten...
run() #snoop(...) --> def(..) --> starts(.).

#! /usr/bin/env python3
# Copyright (c) 2020 Snoop Project <snoopproject@protonmail.com>

import base64
import csv
import glob
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

from argparse import ArgumentTypeError
from argparse import ArgumentParser, RawDescriptionHelpFormatter
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

if sys.platform == 'win32':
    locale.setlocale(locale.LC_ALL, '')

init(autoreset=True)
console = Console()

print ("""\033[36m
  ___|                          
\___ \  __ \   _ \   _ \  __ \  
      | |   | (   | (   | |   | 
_____/ _|  _|\___/ \___/  .__/  
                         _|    \033[0m \033[37mv1.3.2\033[34;1m_rus_\033[31;1mSource Demo\033[0m
""")

print (Fore.CYAN + "#Примеры:" + Style.RESET_ALL)
if sys.platform == 'win32':
    print (Fore.CYAN + " cd с:\<path>\snoop" + Style.RESET_ALL)
    print (Fore.CYAN + " python snoop.py --help" + Style.RESET_ALL, "#справка")
    print (Fore.CYAN + " python snoop.py nickname" + Style.RESET_ALL, "#поиск user-a")
    print (Fore.CYAN + " python snoop.py --module y" + Style.RESET_ALL, "#задействовать плагины")
else:
    print (Fore.CYAN + " cd ~/snoop" + Style.RESET_ALL)
    print (Fore.CYAN + " python3 snoop.py --help" + Style.RESET_ALL, "#справка")
    print (Fore.CYAN + " python3 snoop.py nickname" + Style.RESET_ALL, "#поиск user-a")
    print (Fore.CYAN + " python3 snoop.py --module y" + Style.RESET_ALL, "#задействовать плагины")
console.rule(characters = '=', style="cyan")
print("")

module_name = (Fore.CYAN + "Snoop: поиск никнейма по всем фронтам!" + Style.RESET_ALL)
version = "v1.3.2_rus Snoop (Source demo)"

dirresults = os.getcwd()
dirhome = os.environ['HOME'] + "/snoop" if sys.platform != 'win32' else os.environ['LOCALAPPDATA'] + "\snoop"
timestart = time.time()
time_data = time.localtime()
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

## Флаг БС.
def baza():
    BS = DB('BDdemo')
    return BS
flagBS = len(baza())

## Создание директорий результатов.
dirpath = dirresults if 'Source' in version else dirhome
try:
    os.makedirs(f"{dirpath}/results")
except:
    pass
try:
    os.makedirs(f"{dirpath}/results/html")
except:
    pass
try:
    os.makedirs(f"{dirpath}/results/txt")
except:
    pass
try:
    os.makedirs(f"{dirpath}/results/csv")
except:
    pass
try:
    os.makedirs(f"{dirpath}/results/save reports")
except:
    pass
try:
    os.makedirs(f"{dirpath}/results/ReverseVgeocoder")
except:
    pass
try:
    os.makedirs(f"{dirpath}/results/Yandex_parser")
except:
    pass
try:
    os.makedirs(f"{dirpath}/results/domain")
except:
    pass
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
def print_found_country(social_network, url, countryAB, response_time=False, verbose=False, color=True):
    if color and sys.platform == 'win32':
        print(Style.RESET_ALL + Style.BRIGHT + Fore.CYAN + f" {countryAB}" + Fore.GREEN + f" {social_network}:", Style.RESET_ALL +
        Fore.GREEN + f"{url}")
    elif color and not sys.platform == 'win32':
        print(countryAB, (Style.BRIGHT + Fore.GREEN + f" {social_network}:"), Style.RESET_ALL + Fore.GREEN + f"{url}")
    else:
        print(f"[+] {social_network}: {url}")

## Вывести на печать аккаунт не найден.
def print_not_found(social_network, response_time, verbose=False, color=True):
    if color:
        print(Style.RESET_ALL + Fore.CYAN + "[" + Style.BRIGHT + Fore.RED + "-" + Style.RESET_ALL + Fore.CYAN + "]" +
        Style.BRIGHT + Fore.GREEN + f" {social_network}:" + Style.BRIGHT + Fore.YELLOW + " Увы!")
    else:
        print(f"[-] {social_network}: Увы!")

## Вывести на печать пропуск сайтов по блок. маске в имени username и пропуск по проблеме с openssl.
def print_invalid(mes, social_network, message, color=True):
    """Ошибка вывода результата"""
    if color:
        print(Style.RESET_ALL + Fore.RED + "[" + Style.BRIGHT + Fore.RED + "-" + Style.RESET_ALL + Fore.RED + "]" +
        Style.BRIGHT + Fore.GREEN + f" {social_network}:" + Style.RESET_ALL + Fore.YELLOW + f" {message}")
    else:
        print(f"[-] {social_network}: {message}")

## Вернуть результат future for2.
def get_response(request_future, error_type, social_network, print_found_only=False, verbose=False, color=True):
    try:
        res = request_future.result()
        if res.status_code:
            return res, error_type, res.elapsed
    except requests.exceptions.HTTPError as err1:
        if print_found_only==False:
            print_error(err1, "HTTP Error:", social_network, verbose, color)
    except requests.exceptions.ConnectionError as err2:
        global censors
        censors +=1
        if print_found_only==False:
            print_error(err2, "Ошибка соединения:", social_network, verbose, color)
    except requests.exceptions.Timeout as err3:
        global censors_timeout
        censors_timeout +=1
        if print_found_only==False:
            print_error(err3, "Timeout ошибка:", social_network, verbose, color)
    except requests.exceptions.RequestException as err4:
        if print_found_only==False:
            print_error(err4, "Непредвиденная ошибка", social_network, verbose, color)
    return None, "", -1

## Сохранение отчетов опция (-S).
def sreports(url, headers,session2,error_type, username,social_network,r):
    try:
        os.makedirs(f"{dirpath}/results/save reports/{username}")
    except:
        pass
# Сохранять отчеты для метода: redirection.
    if error_type == "redirection":
        try:
            future2 = session2.get(url=url, headers=headers, allow_redirects=True, timeout=4)
            response = future2.result()
            try:
                with open(f"{dirpath}/results/save reports/{username}/{social_network}.html", 'w', encoding=r.encoding) as repre:
                    repre.write(response.text)
            except:
                pass
        except requests.exceptions.ConnectionError:
            time.sleep(1)
            try:
                future2 = session2.get(url=url, headers=headers, allow_redirects=True, timeout=2)
                response = future2.result()
                try:
                    with open(f"{dirpath}/results/save reports/{username}/{social_network}.html", 'w', encoding=r.encoding) as repre:
                        repre.write(response.text)
                except:
                    pass
            except:
                pass
# Сохранять отчеты для всех остальных методов: status; response; message со стандартными параметрами.
    else:
        try:
            with open(f"{dirpath}/results/save reports/{username}/{social_network}.html", 'w', encoding=r.encoding) as rep:
                rep.write(r.text)
        except:
            pass

## Основная функция.
def snoop(username, site_data, verbose=False, norm=False, reports=False, user=False, country=False, print_found_only=False, timeout=None, color=True, cert=False):
    username = re.sub(" ", "%20", username)

## Предотвращение 'DDoS' из-за невалидных логинов; номеров телефонов, ошибок поиска из-за спецсимволов.
    with open('domainlist.txt', 'r', encoding="utf-8") as err:
        ermail = err.read().splitlines()
    if any(ermail in username for ermail in ermail):
        print(Style.BRIGHT + Fore.RED + "\nE-mail адрес будет обрезан до валидного состояния")
        username = username.rsplit(sep='@', maxsplit=1)[0]

    with open('specialcharacters', 'r', encoding="utf-8") as errspec:
        my_list_bad = list(errspec.read())
        if any(my_list_bad in username for my_list_bad in my_list_bad):
            print(Style.BRIGHT + Fore.RED + f"недопустимые символы в username: {username}")
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

## Печать первой инфостроки.
    if '%20' in username:
        username_space = re.sub("%20", " ", username)
        print_info("разыскиваем:", username_space, color)
    else:
        print_info("разыскиваем:", username, color)

## Создать много_поточный/процессный сеанс для всех запросов.
    requests.packages.urllib3.disable_warnings() #блокировка предупреждений о сертификате.
    my_session = requests.Session()
    if cert == False:
        my_session.verify = False
        requests.packages.urllib3.disable_warnings()
    session0 = ElapsedFuturesSession(executor=ThreadPoolExecutor(max_workers=16), session=my_session)
    if not sys.platform == 'win32':
        if "arm" in platform.platform(aliased=True, terse=0) or "aarch64" in platform.platform(aliased=True, terse=0):
            session1 = ElapsedFuturesSession(executor=ThreadPoolExecutor(max_workers=10), session=my_session)
        else:
            session1 = ElapsedFuturesSession(executor=ProcessPoolExecutor(max_workers=30), session=my_session)
    else:
        session1 = ElapsedFuturesSession(executor=ThreadPoolExecutor(max_workers=16), session=my_session)
    session2 = FuturesSession(max_workers=4, session=my_session)
    session3 = ElapsedFuturesSession(executor=ThreadPoolExecutor(max_workers=4), session=my_session)

## Результаты анализа всех сайтов.
    results_total = {}

### Создание futures на все запросы. Это позволит распараллетить запросы.
    for social_network, net_info in site_data.items():
        results_site = {}

## Запись URL основного сайта и флага страны (сопоставление в БД).
        results_site['flagcountry'] = net_info.get("country")
        results_site['flagcountryklas'] = net_info.get("country_klas")
        results_site['url_main'] = net_info.get("urlMain")

## Пользовательский user-agent браузера (рандомно на каждый сайт).
        RandHead = ([
        "{'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}",
        "{'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}",
        "{'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36 OPR/60.0.3255.109'}",
        "{'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/89.0'}",
        "{'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'}",
        "{'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.58 Safari/537.36'}",
        "{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4701.0 Safari/537.36'}"
        ])
        RH = random.choice(RandHead)
        headers = json.loads(RH.replace("'",'"'))

        if "headers" in net_info:
## Переопределить/добавить любые дополнительные заголовки, необходимые для данного сайта.
            headers.update(net_info["headers"])

## Пропуск временно-отключенного сайта и Не делать запрос, если имя пользователя не подходит для сайта.
        exclusionYES = net_info.get("exclusion")
        if exclusionYES and re.search(exclusionYES, username) or net_info.get("bad_site") == 1:
## Не нужно делать проверку на сайте: если это имя пользователя не допускается.
            if exclusionYES and re.search(exclusionYES, username):
                if not print_found_only:
                    print_invalid("", social_network, f"Недопустимый формат имени для данного сайта", color)
            results_site["exists"] = "invalid_nick"
            results_site["url_user"] = '*'*56
            results_site['countryCSV'] = "****"
            results_site['http_status'] = '*'*10
            results_site['session_size'] = ""
            results_site['check_time_ms'] = '*'*15
            results_site['response_time_ms'] = '*'*15
            results_site['response_time_site_ms'] = '*'*25
            if net_info.get("bad_site") == 1 and verbose == True and not print_found_only:
                print_invalid("", social_network, f"**Пропуск. Dynamic gray_list", color)
                results_site["exists"] = "gray_list"
        else:
## URL пользователя на сайте (если он существует).
            #global url
            url = net_info["url"].format(username)
            results_site["url_user"] = url
            url_API = net_info.get("urlProbe")
            if url_API is None:
## URL-адрес — является обычным, который видят люди в Интернете.
                url_API = url
            else:
## Существует специальный URL (обычно о нем мы не догадываемся/api) для проверки существования отдельно юзера.
                url_API = url_API.format(username)

## Если нужен только статус кода, не загружать тело страницы.
            if norm == False:
                if reports == True or net_info["errorTypе"] == 'message' or net_info["errorTypе"] == 'response_url':
                    request_method = session1.get
                else:
                    request_method = session1.head
            else:
                if reports == True or net_info["errorTypе"] == 'message' or net_info["errorTypе"] == 'response_url':
                    request_method = session0.get
                else:
                    request_method = session0.head

            if net_info["errorTypе"] == "response_url" or net_info["errorTypе"] == "redirection":
## Сайт перенаправляет запрос на другой URL, если имя пользователя не существует.
## Имя найдено. Запретить перенаправление чтобы захватить статус кода из первоначального url.
                allow_redirects = False
            else:
## Разрешить любой редирект, который хочет сделать сайт.
## Окончательным результатом запроса будет то, что доступно.
                allow_redirects = True

            future = request_method(url=url_API, headers=headers, allow_redirects=allow_redirects, timeout=timeout)

## Сохранить future in data для последующего доступа.
            net_info["request_future"] = future

## Добавлять имя сайта 'results_total[social_network]' в окончательный словарь со всеми другими результатами.
        results_total[social_network] = results_site

# print(results_site) # Проверка записи на успех.
    li_time = []
    if verbose == False:
        if sys.platform != 'win32':
            progress = Progress(TimeElapsedColumn(), SpinnerColumn(spinner_name=random.choice(["dots", "dots12"])),
            "[progress.percentage]{task.percentage:>1.0f}%", BarColumn(bar_width=None, complete_style='cyan', finished_style='cyan bold'),
            auto_refresh=False)#transient=True) #исчезает прогресс
        else:
            progress = Progress(TimeElapsedColumn(), "[progress.percentage]{task.percentage:>1.0f}%",
            BarColumn(bar_width=None, complete_style='cyan', finished_style='cyan bold'),
            auto_refresh=False)#transient=True) #исчезает прогресс
    else:
        progress = Progress(TimeElapsedColumn(), "[progress.percentage]{task.percentage:>1.0f}%", auto_refresh=False)

### Получить результаты и пройтись по массиву future.
    with progress:
        if color == True:
            task0 = progress.add_task("", total=len(site_data.items()))
        for social_network, net_info in site_data.items():
            if color == True:
                progress.update(task0, advance=1)
                progress.refresh()
            results_site = results_total.get(social_network)
## Получить другую информацию сайта снова.
            url = results_site.get("url_user")
            countryA = results_site.get("flagcountry")
            countryB = results_site.get("flagcountryklas")
            countryAB = countryA if not sys.platform == 'win32' else countryB
## Пропустить запрещенный никнейм или пропуск сайта из gray-list.
            if results_site.get("exists") is not None:
                continue
## Получить ожидаемый тип данных 4 методов.
            error_type = net_info["errorTypе"]
## Данные по умолчанию в случае каких-либо сбоев в выполнении запроса.
            http_status = "сбой"
            response_text = ""
            session_size = "Err"
## Получить future и убедиться, что оно закончено.
            future = net_info["request_future"]
            r, error_type, response_time = get_response(request_future=future,
                                                        error_type=error_type,
                                                        social_network=social_network,
                                                        print_found_only=print_found_only,
                                                        verbose=verbose,
                                                        color=color)
## Повторное соединение через новую сессию быстрее, чем через adapter - timeout*2=дольше.
            if norm == False:
                #print(future)
                head1 = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 9; Redmi 8 Build/QQ3A.200805.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/88.0.4324.152 Mobile Safari/537.36',
                'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'}
                A1 = str(future)
                if r is None and 'raised ConnectionError' in A1:
                    for _ in range(3):
                        global recensor
                        recensor += 1
                        if color:
                            if print_found_only==False:
                                print(Style.RESET_ALL + Fore.CYAN + "[" + Style.BRIGHT + Fore.RED + "-" + Style.RESET_ALL + Fore.CYAN + "]" +
                                Style.BRIGHT + Fore.GREEN + "    └──повторное соединение" + Style.RESET_ALL)
                        else:
                            if print_found_only==False:
                                print("повторное соединение")
                            #time.sleep(0.1)
                        future1 = session3.get(url=url, headers=head1, allow_redirects=allow_redirects,
                        timeout=1.5)
                        r, error_type, response_time = get_response(request_future=future1,
                                                                    error_type=net_info.get("errorTypе"),
                                                                    social_network=social_network,
                                                                    print_found_only=print_found_only,
                                                                    verbose=verbose,
                                                                    color=color)
                        if r is not None:
                            break
## Попытка получить информацию запроса.
            try:
                http_status = r.status_code #запрос статус-кода.
            except:
                pass
            try:
                response_text = r.text.encode(r.encoding) #запрос данных.
            except:
                pass
            try:
                session_size = len(r.content) #подсчет извлеченных данных.
            except:
                pass
## Проверка, 4 методов; #1.
# Ответы message (разные локации).
            if error_type == "message":
                error = net_info.get("errorMsg")
                error2 = net_info.get("errоrMsg2")
                if net_info.get("errorMsg2"):
                    sys.exit()
#                print(r.text) #проверка ответа (+- '-S')
#                print(r.status_code) #Проверка ответа
                if error2 in r.text or error in r.text:
                    if not print_found_only:
                        print_not_found(social_network, response_time, verbose, color)
                    exists = "увы"
                else:
                    print_found_country(social_network, url, countryAB, response_time, verbose, color)
                    exists = "найден!"
                    if reports:
                        sreports(url, headers,session2,error_type, username,social_network,r)

## Проверка, 4 методов; #2.
# Проверка username при статусе 301 и 303 (перенаправление и соль).
            elif error_type == "redirection":
#                print(r.text) #проверка ответа (+- '-S')
#                print(r.status_code) #Проверка ответа
                if r.status_code == 301 or r.status_code == 303:
                    print_found_country(social_network, url, countryAB, response_time, verbose, color)
                    exists = "найден!"
                    if reports:
                        sreports(url, headers,session2,error_type, username, social_network,r)
                else:
                    if not print_found_only:
                        print_not_found(social_network, response_time, verbose, color)
                    exists = "увы"

## Проверка, 4 методов; #3.
# Проверяет, является ли код состояния ответа 2..
            elif error_type == "status_code":
#                print(r.text) #проверка ответа (+- '-S')
#                print(r.status_code) #Проверка ответа
                if not r.status_code >= 300 or r.status_code < 200:
                    print_found_country(social_network, url, countryAB, response_time, verbose, color)
                    if reports:
                        sreports(url, headers,session2,error_type, username, social_network,r)
                    exists = "найден!"
                else:
                    if not print_found_only:
                        print_not_found(social_network, response_time, verbose, color)
                    exists = "увы"

## Проверка, 4 методов; #4
# Перенаправление.
            elif error_type == "response_url":
#                print(r.text) #проверка ответа (+- '-S')
#                print(r.status_code) #Проверка ответа
                if 200 <= r.status_code < 300:
                    print_found_country(social_network, url, countryAB, response_time, verbose, color)
                    if reports:
                        sreports(url, headers,session1,error_type, username, social_network,r)
                    exists = "найден!"
                else:
                    if not print_found_only:
                        print_not_found(social_network, response_time, verbose, color)
                    exists = "увы"

## Если все 4 метода не сработали, например, из-за ошибки доступа (красный) или из-за каптчи (желтый).
            else:
                if not print_found_only:
                    print_invalid("", social_network, "*ПРОПУСК", color)
                exists = "блок"

## Считать тайминги приближенно.
            ello = float(time.time() - timestart)
            li_time.append(ello)
            dif_time = []

## Считать тайминги с повышенной точностью.
            try:
                time_site = str(response_time).rsplit(sep=':', maxsplit=1)[1]
                time_site=round(float(time_site)*1000)
            except:
                time_site = str("-")

            for i in (li_time[-2:-1]):
                i
                for i1 in (li_time[-1:]):
                    i1
                dif = (i1-i)
                dif_time.append(dif)

## Опция '-v'.
                if verbose == True:
                    if session_size == 0 or session_size is None:
                        Ssession_size = "Head"
                    elif session_size == "Err":
                        Ssession_size = "Нет"
                    else:
                        Ssession_size = str(round(session_size/1024)) + " Kb"

                    time_ello=("%.0f" % float(ello*1000))
                    if color == True:
                        if dif > 5: #задержка в общем времени
                            console.print(f"[cyan][*{time_site} ms T] -->", f"[bold red][*{time_ello} ms t]", f"[cyan][*{Ssession_size}]")
                            console.rule("", style="bold red")
                        else:
                            console.print(f"[cyan][*{time_site} ms T] -->", f"[cyan][*{time_ello} ms t]", f"[cyan][*{Ssession_size}]")
                            console.rule("", style="bold blue")
                    else:
                        console.print(f"[*{time_site} ms T] -->", f"[*{time_ello} ms t]", f"[*{Ssession_size}]", highlight=False)
                        console.rule(style="color")

## Служебная информация для CSV.
            response_time_site_ms = 0
            for response_time_site_ms in dif_time:
                response_time_site_ms

## Сохранить сущ.флаги.
            results_site['exists'] = exists
            results_site['session_size'] = session_size
            results_site['countryCSV'] = countryB
            results_site['http_status'] = http_status
            results_site['check_time_ms'] = time_site
            results_site['response_time_ms'] = round(float(ello*1000))
            if response_time_site_ms*1000 < 250:
                results_site['response_time_site_ms'] = "нет"
            else:
                results_site['response_time_site_ms'] = round(float(response_time_site_ms*1000))
## Добавление результатов этого сайта в окончательный словарь со всеми другими результатами.
            results_total[social_network] = results_site
# Вернуть словарь со всеми данными.
        return results_total

## Опция '-t'.
def timeout_check(value):
    try:
        global timeout
        timeout = int(value)
    except:
        raise ArgumentTypeError(f"\n\033[31;1mTimeout '{value}' Err,\033[0m \033[36mукажите время в 'секундах'. \033[0m")
    if timeout <= 0:
        raise ArgumentTypeError(f"\033[31;1mTimeout '{value}' Err,\033[0m \033[36mукажите время > 0sec. \033[0m")
    return timeout

## Обновление Snoop.
def update_snoop():
    print(
"""\033[36mВы действительно хотите:
                    __             _  
   ._  _| _._|_ _  (_ ._  _  _ ._   ) 
|_||_)(_|(_| |_(/_ __)| |(_)(_)|_) o  
   |                           |    
нажмите\033[0m 'y' """)
    upd = str(input())

    if upd == "y":
        print(Style.BRIGHT + Fore.RED + "Функция обновления Snoop требует установки <Git>")
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

### ОСНОВА.
def run():
## Лицензия.
    with open('COPYRIGHT', 'r', encoding="utf8") as copyright:
        cop = copyright.read()

    version_snoop = f"\033[37m{cop}\033[0m\n" + \
                    f"\033[36mSnoop: {platform.architecture(executable=sys.executable, bits='', linkage='')}\033[36m\n" + \
                    f"\033[36mSource: {version}\033[36m\n" +  \
                    f"\033[36mOS: {platform.platform(aliased=True, terse=0)}\033[36m\n" + \
                    f"\033[36mPython: {platform.python_version()}\033[36m\n\n"

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

Snoop в исполняемом виде (бинарник) предоставляется по лицензии, с которой пользователь
должен ознакомиться перед покупкой ПО. Лицензия (RU/EN) для Snoop Project в
исполняемом виде находится в rar-архивах демо версий Snoop по ссылке[/bold green]
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

## Функция выбор регионов для поиска.
    def onelevel_or_exclude(exl_onelevel):
        lap = []
        bd_flag = []
        for k,v in DB('BDdemo').items():
            bd_flag.append(v.get('country_klas').lower())

        enter_coun_u=[x.lower() for x in exl_onelevel]
        lap=list(set(bd_flag) & set(enter_coun_u))
        diff_list=list(set(enter_coun_u) - set(bd_flag)) # вывести уникальные элементы только из enter_coun_u иначе set(enter_coun_u)^set(bd_flag)
# Вернуть корректный и bad списки пользовательского ввода в cli.
        return lap, diff_list

## Назначение опций Snoop.
    parser = ArgumentParser(formatter_class = RawDescriptionHelpFormatter,
                            usage = 'python3 %(prog)s [options] nickname\nor\nusage: python3 %(prog)s nickname [options]\n ',
                            description = Fore.CYAN + "Справка" + Style.RESET_ALL,
                            epilog = (Fore.CYAN + f"Snoop " + Style.BRIGHT + Fore.RED + f"Demo Version " + Style.RESET_ALL + \
                            Fore.CYAN + f"поддержка: \033[31;1m{flagBS}\033[0m  \033[36mWebsites!\n"  + Fore.CYAN +
                            f"Snoop \033[36;1mFull Version\033[0m \033[36mподдержка: \033[36;1m2200+\033[0m \033[36mWebsites!!!\033[0m\n\
 \033[32;1mEnglish version — of Snoop see release (available 'Snoop EN version')\033[0m\n\n")
                           )
# Service arguments.
    service_group = parser.add_argument_group('\033[36mservice arguments\033[0m')
    service_group.add_argument("--version", "-V", action="version",  version=(version_snoop),
                               help="\033[36mA\033[0mbout: вывод на печать версий:: OS; Snoop; Python и Лицензии"
                              )
    service_group.add_argument("--list all", "-l y", action="store_true", dest="listing",
                               help="\033[36mВ\033[0mывести на печать детальную информацию о базе данных Snoop"
                              )
    service_group.add_argument("--donate y", "-d y", action="store_true", dest="donation",
                               help="\033[36mП\033[0mожертвовать на развитие Snoop Project-а, получить/приобрести \
                               \033[32;1mSnoop Full Version\033[0m"
                              )
    service_group.add_argument("--autoclean y", "-a y", action="store_true", dest="autoclean", default=False,
                               help="\033[36mУ\033[0mдалить все отчеты, очистить место"
                              )
    service_group.add_argument("--update y", "-U y", action="store_true", dest="update",
                               help="\033[36mО\033[0mбновить Snoop"
                              )
# Plugins arguments arguments.
    plugins_group = parser.add_argument_group('\033[36mplugins arguments\033[0m')
    plugins_group.add_argument("--module y", "-m y", action="store_true", dest="module", default=False,
                               help="\033[36mO\033[0mSINT поиск: задействовать различные плагины Snoop:: IP/GEO/YANDEX \
                               (список плагинов будет пополняться)"
                              )
# Search arguments.
    search_group = parser.add_argument_group('\033[36msearch arguments\033[0m')
    search_group.add_argument("username", nargs='+', metavar='nickname', action="store",
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
                              help="\033[36mУ\033[0mказать имя сайта из БД '--list all'. Поиск 'username' на одном указанном ресурсе, \
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
                              help="\033[36mС\033[0mортировка 'вывода на печать/запись_результатов' по странам, а не по алфавиту"
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
    search_group.add_argument("--userload", "-u", metavar='', action="store", dest="user", default=False,
                              help="\033[36mУ\033[0mказать файл со списком user-ов. \
                              Пример_Linux: 'python3 snoop.py -u ~/listusers.txt start'.\
                              Пример_Windows: 'python snoop.py -u c:\\User\\User\Documents\\listusers.txt start'"
                             )
    search_group.add_argument("--save-page", "-S", action="store_true", dest="reports", default=False,
                              help="\033[36mС\033[0mохранять найденные странички пользователей в локальные файлы"
                             )
    search_group.add_argument("--cert-on", "-C", default=False, action="store_true", dest="cert",
                              help="""\033[36mВ\033[0mкл проверку сертификатов на серверах. По умолчанию проверка сертификатов
                              на серверах отключена, что даёт меньше ошибок и больше положительных результатов
                              при поиске nickname"""
                             )
    search_group.add_argument("--normal", "-N", action="store_true", dest="norm", default=True,
                              help="""\033[36mП\033[0mереключатель режимов: SNOOPninja > нормальный режим > SNOOPninja.
                              По_умолчанию (GNU/Linux Full Version) вкл 'режим SNOOPninja':
                              ускорение поиска ~25pct, экономия ОЗУ ~50pct, повторное 'гибкое' соединение на сбойных ресурсах.
                              Режим SNOOPninja эффективен только для Snoop for GNU/Linux Full Version.
                              По_умолчанию (Windows) вкл 'нормальный режим'. В Demo Version переключатель режимов деактивирован"""
                             )

    args = parser.parse_args()

## Опции  '-cseo' несовместимы между собой.
    list_cseo = []

    list_cseo.append(bool(args.site_list))
    list_cseo.append(bool(args.country))
    list_cseo.append(bool(args.exclude_country))
    list_cseo.append(bool(args.one_level))

    k=0
    for _ in list_cseo:
        if _ == True:
            k += 1
        if k == 2:
            print(Style.BRIGHT + Fore.RED + "опциии ['-c', '-e' '-o', '-s'] несовместимы между собой")
            sys.exit()
## Опция  '-a'.
    if args.autoclean:
        print(Fore.CYAN + "[+] активирована опция '-a': «удаление накопленных отчетов»\n")
        autoclean()
        sys.exit()
## Информативный вывод.
    if args.module:
        print(Fore.CYAN + "[+] активирована опция '-m': «модульный поиск»")
        def module():
            print("""\n
\033[36m╭Выберите плагин из списка\033[0m
\033[36m├──\033[0m\033[36;1m[1] --> GEO_IP/domain\033[0m
\033[36m├──\033[0m\033[36;1m[2] --> Reverse Vgeocoder\033[0m
\033[36m├──\033[0m\033[36;1m[3] --> Yandex_parser\033[0m
\033[36m├──\033[0m\033[32;1m[help] --> Справка\033[0m
\033[36m└──\033[0m\033[31;1m[q] --> Выход\033[0m\n""")
            mod = input()

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
Я_Отзывы; Я_Кью; Я_Маркет; Я_Музыка; Я_Дзен; Я_Коллекции; Я_Диск; E-mail, Name.
И связать полученные данные между собой с высокой скоростью и масштабно.
Предназначение — OSINT.

Плагин разработан на идее и материалах уязвимости, отчёт был отправлен Яндексу в рамках программы «Охота за ошибками».
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
                table.add_column("Yandex_parser_v0.4", style="green")
                table.add_row('Яндекс парсер: Я_Отзывы; Я_Кью; Я_Маркет; Я_Музыка; Я_Дзен; Я_Коллекции; Я_Диск; E-mail; Name.')
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
        console.print(f"[yellow bold]Режим подробной вербализации [опция '-v'] отображает детальную информацию,\n\
[опция '-f'] неуместна", f"\n\n[red bold]Выход")
        sys.exit()
## Опция  '-С'.
    if args.cert:
        print(Fore.CYAN + "[+] активирована опция '-C': «проверка сертификатов на серверах вкл»")
## Опция режима SNOOPnina > < нормальный режим.
    if args.norm == False:
        sys.exit()
        print(Fore.CYAN + "[+] активирована опция '--': «режим SNOOPninja»")
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
## Опция  '-c'. Сортировка по странам.
    if args.country:
        patchjson = ("{}".format(args.json_file))
        jsonjson = DB('BDdemo')
        print(Fore.CYAN + "[+] активирована опция '-c': «сортировка/запись в HTML результатов по странам»")
        country_sites = sorted(jsonjson, key=lambda k: ("country" not in k, jsonjson[k].get("country", sys.maxsize)))
        sort_web = {}
        for site in country_sites:
            sort_web[site] = jsonjson.get(site)
## Опция '-f'.
    if args.print_found_only:
        print(Fore.CYAN + "[+] активирована опция '-f': «выводить на печать только найденные аккаунты»")
## Опция '-s'.
    if args.site_list:
        print(Fore.CYAN + "[+] активирована опция '-s': «будет произведён поиск user-a на 1-м выбранном website»\n"
        "    допустимо использовать опцию '-s' несколько раз\n"
        "    [опция '-s'] несовместима с [опциями '-с', '-e', 'o']")
## Опция '-e'.
    if args.exclude_country:
        lap, diff_list = onelevel_or_exclude(args.exclude_country)

        print(Fore.CYAN + f"[+] активирована опция '-e': «исключить из поиска выбранные регионы»::", end=' ')
        print(Style.BRIGHT + Fore.CYAN + str(lap).strip('[]').upper() + Style.RESET_ALL + " " + Style.BRIGHT + Fore.RED + \
        str(diff_list).strip('[]') + Style.RESET_ALL + Fore.CYAN + "\n" + \
        "    допустимо использовать опцию '-e' несколько раз\n"
        "    [опция '-e'] несовместима с [опциями '-s', '-c', 'o']")
## Опция '-o'.
    if args.one_level:
        lap, diff_list = onelevel_or_exclude(args.one_level)

        print(Fore.CYAN + f"[+] активирована опция '-o': «включить в поиск только выбранные регионы»::", end=' ')
        print(Style.BRIGHT + Fore.CYAN + str(lap).strip('[]').upper() + Style.RESET_ALL + " " + Style.BRIGHT + Fore.RED + \
        str(diff_list).strip('[]') + Style.RESET_ALL + Fore.CYAN + "\n" + \
        "    допустимо использовать опцию '-o' несколько раз\n"
        "    [опция '-o'] несовместима с [опциями '-s', '-c', 'e']")
## Опция '-v'.
    if args.verbose:
        print(Fore.CYAN + "[+] активирована опция '-v': «подробная вербализация в CLI»\n")
        with console.status("[cyan]Ожидайте, идёт самотестирование сети..."):
            networktest.nettest()
            console.log("[cyan]--> тест сети")
## Опция '--list all'.
    if args.listing:
        print(
"\033[36m\nСортировать БД Snoop по странам, по имени сайта или обобщенно ?\n" + \
"по странам —\033[0m 1 \033[36mпо имени —\033[0m 2 \033[36mall —\033[0m 3\n" + \
"\033[36mВыберите действие...\033[0m\n")
        sortY = str(input())

# Общий вывод стран (3!).
# Вывод для Demo Version.
        if sortY == "3":
            console.rule("[cyan]Ok, print All Country:",style="cyan bold")
            def sortY3(DB, fore, version):
                print("")
                datajson = DB
                cnt = Counter()
                li = []
                for con in datajson:
                    S = datajson.get(con).get("country_klas") if sys.platform == 'win32' else datajson.get(con).get("country")
                    li.append(S)
                for word in li:
                    cnt[word] += 1
                flag_str=str(cnt)
                try:
                    flag_str_sum = (flag_str.split('{')[1]).replace("'", "").replace("}", "").replace(")", "")
                except:
                    pass
                table = Table(title = Style.BRIGHT + fore + version + Style.RESET_ALL, style="green")
                table.add_column("Страна:Кол-во websites", style="magenta")
                table.add_column("All", style="cyan", justify='full')
                table.add_row(flag_str_sum, str(len(datajson)))
                console.print(table)

            sortY3(DB('BDdemo'), Fore.RED, "Demo Version")
# Вывод для full Version.
            sortY3(DB('BDflag'), Fore.GREEN, "Full Version")
            sys.exit()

# Сортируем по алфавиту для Full Version (2!).
        elif sortY == "2":
            console.rule("[cyan]Ok, сортируем по алфавиту:",style="cyan bold")
            def sortY2(DB, version):
                print(Fore.GREEN + f"\n++Белый список {version}++")
                datajson = DB
                i = 0
                sorted_dict_v_listtuple = sorted(datajson.items(), key=lambda x: x[0].lower()) # сорт.словаря по глав.ключу без учета регистра
                datajson_sort = dict(sorted_dict_v_listtuple) #преобр.список обратно в словарь (сортированный)
                for con in datajson_sort:
                    S = datajson_sort.get(con).get("country_klas") if sys.platform == 'win32' else datajson_sort.get(con).get("country")
                    i += 1
                    print(Style.BRIGHT + Fore.GREEN + f"{i}.", Fore.CYAN + f"{S}  {con}")
                    print(Fore.CYAN + "================")

            sortY2(DB('BDflag'), "Full Version")
# Сортировка по алфавиту для Demo Version (2!).
            sortY2(DB('BDdemo'), "Demo Version")
            sys.exit()

# Сортируем по странам для Full Version (1!).
        elif sortY == "1":
            console.rule("[cyan]Ok, сортируем по странам:",style="cyan bold")
            def sortY1(DB, version):
                listwindows = []
                datajson = DB
                for con in datajson:
                    S = datajson.get(con).get("country_klas") if sys.platform == 'win32' else datajson.get(con).get("country")
                    listwindows.append(f"{S}  {con}\n")
                print(Fore.GREEN + f"\n++Белый список {version}++")
                for i in enumerate(sorted(listwindows, key=str.lower), 1):
                    print(Style.BRIGHT + Fore.GREEN + str(i[0]) + '.', Fore.CYAN + str(i[1]) ,end = '')
                    print(Fore.CYAN + "================")

            sortY1(DB('BDflag'), "Full Version")
# Сортировка по странам для Demo Version (1!).
            sortY1(DB('BDdemo'), "Demo Version")
            sys.exit()

# Действие не выбрано --list all.
        else:
            print(Style.BRIGHT + Fore.RED + "Извините, но вы не выбрали действие\nвыход")
            sys.exit()

## Опция донат '-d y'.
    if args.donation:
        donate()
## Опция '-u' указания файла-списка разыскиваемых пользователей.
    if args.user:
        userlists=[]
        userlists_bad=[]
        with open('specialcharacters', 'r', encoding="utf-8") as errspec:
            my_list_bad = list(errspec.read())
        try:
            patchuserlist = ("{}".format(args.user))
            if sys.platform != 'win32':
                userfile=patchuserlist.split('/')[-1]
            else:
                userfile=patchuserlist.split('\\')[-1]
            with open(patchuserlist, "r", encoding="utf8") as u1:
                userlist=[line.strip() for line in u1.read().splitlines()]
                for i in userlist:
                    if any(D in i for D in my_list_bad):
                        userlists_bad.append(i)
                        continue
                    elif any(' ' in i for i in i):
                        g1=i.split()
                        g11 = " ".join(g1)
                        if g11 not in userlist:
                            userlists.append(g11)
                    elif i == "":
                        continue
                    else:
                        userlists.append(i)
            if userlists_bad:
                print(Style.RESET_ALL + Style.BRIGHT + Fore.RED + f"Следующие [username] из '{userfile}' содержат ошибки и будут пропущены:")
                print(Style.BRIGHT + Fore.RED + f"{userlists_bad}" + Style.RESET_ALL)
        except:
            print(f"\033[31;1mНе могу найти_прочитать '{userfile}'!\033[0m \033[36mПожалуйста, укажите текстовый файл в кодировке —\033[0m \033[36;1mutf-8.\033[0m\n")
            print("\033[36mПо умолчанию блокнот в OS Windows сохраняет текст в кодировке — ANSI\033[0m")
            print("\033[36mОткройте ваш список пользователей и измените кодировку [файл ---> сохранить как ---> utf-8]")
            print("\033[36mИли удалите из файла нечитаемые символы.")
            sys.exit()
        print(Fore.CYAN + f"[+] активирована опция '-u': «розыск user-ов из файла: \033[36;1m{userfile}\033[0m\033[36m»\033[0m")
        print(Fore.CYAN + "    Будем искать:" + f" {userlists[:3]}" + " и других..." + Style.RESET_ALL)

## Опция '--update y' обновление Snoop.
    if args.update:
        update_snoop()

## Проверка остальных опций.
    site_data_all = None
    baseput = ("{}".format(args.json_file))
    #print(baseput) #проверка пути базы.
## Работа с базой.
    if site_data_all is None:
# Проверить, существует ли альтернативная база данных, иначе выход.
        if not os.path.exists(baseput):
            print("\033[31;1mФайла базы не существует.\033[0m")
            sys.exit()
        else:
            try:
                a1 = DB('BDdemo')
            except:
                print("\033[31;1mНеподдерживаемый формат базы данных\033[0m")
        try:
            if args.web == False:
                site_data_all = a1
                print(Fore.CYAN + f"\nзагружена локальная база: " +
                Style.BRIGHT + Fore.CYAN + f"{len(site_data_all)}" + "_Websites" + Style.RESET_ALL)
        except:
            print("\033[31;1mInvalid загружаемая база данных.\033[0m")

## Функция для опций '-eo'
    def one_exl(one_exl, bool_):
        for k,v in site_data_all.items():
            if all(item.lower() != v.get('country_klas').lower() for item in one_exl) == bool_:
                site_data[k] = v

## Опция '-w'.
    if args.web:
        print("\n\033[37m\033[44m{}".format("Функция '-w' доступна только пользователям Snoop Full Version..."))
        donate()

## Если опции '-seo' не указаны, то используем БД, как есть.
    site_data = {}
    if args.site_list is None and args.exclude_country is None and args.one_level is None:
        site_data = site_data_all
## Опция '-s'.
    elif args.site_list is not None:
# Пользователь выборочно запускает запросы к подмножеству списку сайтов из БД.
# Убедиться, что сайты в базе имеются, создать для проверки сокращенную базу данных сайта(ов).
        for site in args.site_list:
            for site_yes in site_data_all:
                if site.lower() == site_yes.lower():
                    site_data[site_yes] = site_data_all[site_yes] #выбираем в словарь найденные сайты из БД

            diff_k_bd = set(DB('BDflag')) ^ set(DB('BDdemo'))
            for site_yes_full_diff in diff_k_bd:
                if site.lower() == site_yes_full_diff.lower(): #если сайт (-s) в БД Full версии.
                    print(f"\033[31;1m[?] Пропуск:\033[0m \033[36mсайт из БД \033[36;1mFull-версии\033[0m \033[36mнедоступен в" +
                    f"\033[0m \033[33;1mDemo-версии\033[0m\033[36m:: '\033[30;1m{site_yes_full_diff}\033[0m\033[36m'\033[0m")

            if not any(site.lower() == site_yes_full.lower() for site_yes_full in DB('BDflag')): #если ни одного совпадения по сайту
                print(f"\033[31;1m[!] Пропуск:\033[0m \033[36mжелаемый сайт отсутствует в БД Snoop:: '\033[31;1m{site}\033[0m\033[36m'\033[0m")

## Отмена поиска, если нет ни одного совпадения по БД и '-s'.
        if not site_data:
            sys.exit()
## Опция '-e'.
# Создать для проверки сокращенную базу данных сайта(ов).
# Создать и добавить в новую БД сайты, аргументы (-e) которых != бук.кодам стран (country_klas).
    elif args.exclude_country is not None:
        one_exl(args.exclude_country, True)
## Опция '-o'.
# Создать для проверки сокращенную базу данных сайта(ов).
# Создать и добавить в новую БД сайты, аргументы (-e) которых != бук.кодам стран (country_klas).
    elif args.one_level is not None:
        one_exl(args.one_level, False)

## Крутим user's.
    def starts(SQ):
        kef_user=0
        ungzip = []
        find_url_lst=[]
        exl = "/".join(lap).upper() if args.exclude_country is not None else "нет" #искл.регионы_valid.
        one = "/".join(lap).upper() if args.one_level is not None else "нет" #вкл.регионы_valid.
        for username in SQ:
            kef_user+=1
            sort_sites = sort_web if args.country == True else site_data
            FULL = snoop(username, sort_sites, country=args.country, user=args.user, verbose=args.verbose, cert=args.cert,
                        norm=args.norm, reports=args.reports, print_found_only=args.print_found_only, timeout=args.timeout,
                        color=not args.no_func)

            exists_counter = 0
            try:
                file_txt = open(f"{dirpath}/results/txt/{username}.txt", "w", encoding="utf-8")
                #raise Exception("")
            except:
                file_txt = open(f"{dirpath}/results/txt/username" + str(time.strftime("%d_%m_%Y_%H_%M_%S", time_data)) + ".txt",
                "w", encoding="utf-8")
            file_txt.write("Адрес | ресурс" + "\n\n")
            for website_name in FULL:
                timefinish = time.time() - timestart
                dictionary = FULL[website_name]
                if type(dictionary.get("session_size")) != str:
                    ungzip.append(dictionary.get("session_size"))
                if dictionary.get("exists") == "найден!":
                    exists_counter += 1
                    find_url_lst.append(exists_counter)
                    file_txt.write(dictionary ["url_user"] + " | " + (website_name)+"\n")
            file_txt.write("\n" f"Запрашиваемый объект: <{username}> найден: {exists_counter} раз(а).")
            file_txt.write("\n" f"База Snoop (Demo Version): {flagBS} Websites.")
            file_txt.write("\n" f"Исключённые регионы: {exl}.")
            file_txt.write("\n" f"Выбор конкретных регионов: {one}.")
            file_txt.write("\n" f"Обновлено: " + time.strftime("%d/%m/%Y_%H:%M:%S", time_data) + ".")
            file_txt.close()
## Размер сесии.
            try:
                sess_size=round(sum(ungzip)/1024/1024 , 2)
            except:
                sess_size=0.00000000001
## Запись в html.
            try:
                file_html = open(f"{dirpath}/results/html/{username}.html", "w", encoding="utf-8")
                #raise Exception("")
            except:
                file_html = open(f"{dirpath}/results/html/username" + time.strftime("%d_%m_%Y_%H_%M_%S", time_data) + ".html", "w",
                encoding="utf-8")
            file_html.write("<!DOCTYPE html>\n<head>\n<meta charset='utf-8'>\n<style>\nbody { background: url(../../web/public.png) \
            no-repeat 20% 0%; }\n</style>\n<link rel='stylesheet' href='../../web/style.css'>\n</head>\n<body>\n\n\
            <div id='particles-js'></div>\n\
            <div id='report'>\n\n\
            <h1><a class='GL' href='file://" + f"{dirpath}/results/html/'>Главная</a>" + "</h1>\n")
            file_html.write("""\t\t\t<h3>Snoop Project (Demo Version)</h3>
            <p>Нажмите: 'сортировать по странам', возврат: 'F5':</p>
            <button onclick="sortList()">Сортировать по странам</button><br><br>\n\n""")
            file_html.write("Объект " + "<b>" + (username) + "</b>" + " найден на нижеперечисленных " + "<b>" + str(exists_counter) +
            "</b> ресурсах:\n" + "<br><ol" + " id='id777'>\n")

            cnt = Counter()
            for website_name in FULL:
                dictionary = FULL[website_name]
                flag_sum=dictionary["flagcountry"]
                if dictionary.get("exists") == "найден!":
                    li = []
                    li.append(flag_sum)
                    exists_counter += 0
                    for word in li:
                        cnt[word] += 1
                    file_html.write("<li>" + dictionary["flagcountry"]+ "<a target='_blank' href='" + dictionary ["url_user"] + "'>"+
                    (website_name) + "</a>" + "</li>\n")
            flag_str=str(cnt)
            try:
                flag_str_sum = (flag_str.split('{')[1]).replace("'", "").replace("}", "").replace(")", "").replace(",", "  ↯  ").replace(":", "⇔")
                file_html.write("</ol>GEO: " + str(flag_str_sum) + ".\n")
            except:
                pass
            file_html.write("<br> Запрашиваемый объект < <b>" + str(username) + "</b> > найден: <b>" + str(exists_counter) + "</b> раз(а).")
            file_html.write("<br> Затраченное время на сессию: " + "<b>" + "(%.0f" % float(timefinish) + "сек_ %.2f" % float(sess_size) + "Mb)</b>.\n")
            file_html.write("<br> Исключённые регионы: <b>" + str(exl) + ".</b>\n")
            file_html.write("<br> Выбор конкретных регионов: <b>" + str(one) + ".</b>\n")
            file_html.write("<br> База Snoop (Demo Version): <b>" + str(flagBS) + "</b>" + " Websites.\n")
            file_html.write("<br> Обновлено: " + "<i>" + time.strftime("%d/%m/%Y_%H:%M:%S", time_data) + ".</i><br><br>\n")
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

<script src="../../web/particles.js"></script>
<script src="../../web/app.js"></script>

<audio controls="controls" autoplay="autoplay" loop="loop">
<source src="../../web/Megapolis (remix).mp3" type="audio/mpeg">
</audio>

<br>
<audio controls="controls" loop="loop">
<source src="../../web/for snoop in cyberpunk.mp3" type="audio/mpeg">
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
                file_csv = open(f"{dirpath}/results/csv/{username}.csv", "w", newline='')#, encoding="utf-8")
                #raise Exception("")
            except:
                file_csv = open(f"{dirpath}/results/csv/username" + time.strftime("%d_%m_%Y_%H_%M_%S", time_data) + ".csv", "w", newline='')#, encoding="utf-8")
            usernamCSV = re.sub(" ", "_", username)
            censors_cor = int((censors - recensor)/kef_user) #err_connection
            censors_timeout_cor = int(censors_timeout/kef_user) #err time-out
            flagBS_err = round((censors_cor + censors_timeout_cor)*100/flagBS, 3)
            czr_csv = ''
            if flagBS_err >= 2:#perc
                czr_csv = 'Внимание!_Поиск_проходил_при_нестабильном_интернет_соединении_или_Internet-Censorship. Результаты_могут_быть_неполные.'
            writer = csv.writer(file_csv)
            writer.writerow(['Никнейм',
                             'Ресурс',
                             'Страна',
                             'Url',
                             'Ссылка_на_профиль',
                             'Статус',
                             'Статус_http',
                             'Общее_замедление/мс',
                             'Отклик/мс',
                             'Общее_время/мс',
                             'Сессия/Kb',
                             czr_csv
                             ])
            for site in FULL:
                if FULL[site]['session_size'] == 0:
                    Ssession = "Head"
                elif type(FULL[site]['session_size']) != str:
                    Ssession = round((FULL.get(site).get("session_size")/1024))
                else:
                    Ssession = "Bad"
                writer.writerow([usernamCSV,
                                 site,
                                 FULL[site]['countryCSV'],
                                 FULL[site]['url_main'],
                                 FULL[site]['url_user'],
                                 FULL[site]['exists'],
                                 FULL[site]['http_status'],
                                 FULL[site]['response_time_site_ms'],
                                 FULL[site]['check_time_ms'],
                                 FULL[site]['response_time_ms'],
                                 Ssession])
            writer.writerow(['«' + "-"*30, '-'*8, '-'*4, '-'*35, '-'*56, '-'*13, '-'*17, '-'*32,'-'*13, '-'*23, '-'*16 + '»'])
            writer.writerow(['БД_(DemoVersion)=' + str(flagBS) + '_Websites'])
            writer.writerow('')
            writer.writerow(['Исключённые_регионы=' + str(exl)])
            writer.writerow(['Выбор_конкретных_регионов=' + str(one)])
            writer.writerow('')
            writer.writerow(['Дата'])
            writer.writerow([time.strftime("%d/%m/%Y_%H:%M:%S", time_data)])
            file_csv.close()

## Финишный вывод.
        direct_results = f"{dirpath}/results/*/{username}.*" if sys.platform != 'win32' else f"{dirpath}\\results\\*\\{username}.*"
        print(Fore.CYAN + "├─Результаты поиска:", "найдено -->", len(find_url_lst), "url (сессия: %.0f" % float(timefinish) + f"сек_{sess_size}Mb)")
        print(Fore.CYAN + "├──Результаты сохранены в: " + Style.RESET_ALL + direct_results)
        if flagBS_err >= 2:#perc
            print(Fore.CYAN + "├───Дата поискового запроса:", time.strftime("%d/%m/%Y_%H:%M:%S", time_data))
            print(Fore.CYAN + f"└────\033[31;1mВнимание! Bad_raw: {flagBS_err}% БД\033[0m")
            print(Fore.CYAN + "     └─нестабильное соединение или Internet Censorship")
            print("       \033[36m└─используйте \033[36;1mVPN\033[0m \033[36mили увеличьте значение опции'\033[36;1m-t\033[0m\033[36m'\033[0m\n")
        else:
            print(Fore.CYAN + "└───Дата поискового запроса:", time.strftime("%d/%m/%Y_%H:%M:%S", time_data), "\n")
        console.print(Panel(f"{e_mail} до {Do}",title=license, style=STL(color="white", bgcolor="blue")))
## Музыка.
        try:
            if args.no_func==False:
                playsound('end.wav')
        except:
            pass

## Открывать/нет браузер с результатами поиска.
        if args.no_func==False and exists_counter >= 1:
            if "arm" in platform.platform(aliased=True, terse=0) or "aarch64" in platform.platform(aliased=True, terse=0):
                pass
            else:
                try:
                    webbrowser.open(f"file://{dirpath}/results/html/{username}.html")
                except:
                    pass
## Arbeiten...
    starts(args.username) if args.user==False else starts(userlists)
run()

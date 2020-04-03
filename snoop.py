#! /usr/bin/env python3
#Copyright (c) 2020 Snoop Project <snoopproject@protonmail.com> 

import certifi
import csv
import json
import locale
import os
import platform
import re
import requests
import sortirovka
import subprocess
import sys
import time
import webbrowser

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from collections import Counter
from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor
from playsound import playsound
from requests_futures.sessions import FuturesSession


if sys.platform == 'win32':
    locale.setlocale(locale.LC_ALL, '')

init(autoreset=True)

print ("""\033[36m
  ___|                          
\___ \  __ \   _ \   _ \  __ \  
      | |   | (   | (   | |   | 
_____/ _|  _|\___/ \___/  .__/  
                         _|    \033[0m \033[37mv1.\033[34;1m1.7\033[31;1m_rus\033[0m
""")

if sys.platform == 'win32':
	print (Fore.CYAN + "#Пример:" + Style.RESET_ALL)
	print (Fore.CYAN + " cd с:\snoop" + Style.RESET_ALL)	
	print (Fore.CYAN + " python snoop.py -h" + Style.RESET_ALL, "#справка 'как начать'")
	print (Fore.CYAN + " python snoop.py -t 9 username" + Style.RESET_ALL, "#поиск user-a")
	print (Fore.CYAN + "============================================\n" + Style.RESET_ALL)
else:
	print (Fore.CYAN + "#Пример:" + Style.RESET_ALL)
	print (Fore.CYAN + " cd ~/snoop" + Style.RESET_ALL)
	print (Fore.CYAN + " python3 snoop.py -h" + Style.RESET_ALL, "#справка по функциям ПО")
	print (Fore.CYAN + " python3 snoop.py -t 9 username" + Style.RESET_ALL, "#поиск user-a")
	print (Fore.CYAN + "=============================================\n" + Style.RESET_ALL)

module_name = (Fore.CYAN + "Snoop: поиск никнейма по всем фронтам!" + Style.RESET_ALL)
__version__ = "1.1.7_rus Ветка Snoop Desktop"

dirresults = os.getcwd()
timestart = time.time()
time_data = time.localtime()
censor = 0

#Создание директорий результатов
try:
    os.makedirs(str(dirresults + "/results"))
except:
    pass
try:    
    os.mkdir(str(dirresults + "/results/html"))
except:        
    pass
try:    
    os.mkdir(str(dirresults + "/results/txt"))
except:            
    pass
try:    
    os.mkdir(str(dirresults + "/results/csv"))
except:            
    pass

################################################################################
class ElapsedFuturesSession(FuturesSession):
    """
    Расширяет 'FutureSession' для добавления метрики времени ответа к каждому запросу.

    https://github.com/ross/requests-futures#working-in-the-background
    """

    def request(self, method, url, hooks={}, *args, **kwargs):
        start = time.time()

        def timing(r, *args, **kwargs):
            elapsed_sec = time.time() - start
            r.elapsed = round(elapsed_sec * 1000)

        try:
            if isinstance(hooks['response'], (list, tuple)):
# должен быть первым, поэтому мы не рассчитываем время выполнения других hooks.
                hooks['response'].insert(0, timing)
            else:
                hooks['response'] = [timing, hooks['response']]
        except KeyError:
            hooks['response'] = timing

        return super(ElapsedFuturesSession, self).request(method, url, hooks=hooks, *args, **kwargs)


def print_info(title, info, color=True):
    if color:
        print(Fore.GREEN + "[" +
            Fore.YELLOW + "*" +
            Fore.GREEN + f"] {title}" +
            Fore.RED + "\033[5m <\033[0m" +
            Fore.WHITE + f" {info}" +
            Fore.RED + "\033[5m >\033[0m")
    else:
        print(f"[*] {title} {info}:")


def print_error(err, errstr, var, verbose=False, color=True):
    if color:
        print(Fore.CYAN + "[" +
            Style.BRIGHT + Fore.RED + "-" + Style.RESET_ALL +
            Fore.CYAN + "]" +
            Style.BRIGHT + Fore.RED + f" {errstr}" +
            Style.BRIGHT + Fore.YELLOW + f" {err if verbose else var}")
        playsound('err.wav')
    else:
        print(f"[-] {errstr} {err if verbose else var}")


def format_response_time(response_time, verbose):
    return " [{} ms]".format(response_time) if verbose else ""

# Вывод на печать на разных платформах.
if sys.platform == 'win32':
    def print_found_country(social_network, url, countryB, response_time=False, verbose=False, color=True):
        if color:
            print(Style.BRIGHT + Fore.CYAN + f" {countryB}" + 
                format_response_time(response_time, verbose) +
                Fore.GREEN + f" {social_network}:", url)
        else:
            print(f"[+]{format_response_time(response_time, verbose)} {social_network}: {url}")
else:            
    def print_found_country(social_network, url, countryA, response_time=False, verbose=False, color=True):
        if color:
            print(countryA, (Style.BRIGHT +
                format_response_time(response_time, verbose) +
                Fore.GREEN + f" {social_network}:"), url)
        else:
            print(f"[+]{format_response_time(response_time, verbose)} {social_network}: {url}")

def print_not_found(social_network, response_time, verbose=False, color=True):
    if color:
        print((Fore.CYAN + "[" +
            Style.BRIGHT + Fore.RED + "-" + Style.RESET_ALL +
            Fore.CYAN + "]" +
            format_response_time(response_time, verbose) +
            Style.BRIGHT + Fore.GREEN + f" {social_network}:" +
            Style.BRIGHT + Fore.YELLOW + " Увы!"))
    else:
        print(f"[-]{format_response_time(response_time, verbose)} {social_network}: Увы!")

def print_invalid(social_network, msg, color=True):
    """Ошибка вывода результата"""
    if color:
        print((Fore.CYAN + "[" +
            Style.BRIGHT + Fore.RED + "-" + Style.RESET_ALL +
            Fore.CYAN + "]" +
            Style.BRIGHT + Fore.GREEN + f" {social_network}:" +
            Style.BRIGHT + Fore.YELLOW + f" {msg}"))
    else:
        print(f"[-] {social_network} {msg}")


def get_response(request_future, error_type, social_network, verbose=False, retry_no=None, color=True):
    
    try:
        rsp = request_future.result()
        if rsp.status_code:
            return rsp, error_type, rsp.elapsed
    except requests.exceptions.HTTPError as errh:
        print_error(errh, "HTTP Error:", social_network, verbose, color)

    except requests.exceptions.ConnectionError as errc:
        def gebb():
            global censor
            censor +=1
            print_error(errc, "Ошибка соединения:", social_network, verbose, color)
        gebb()            
    except requests.exceptions.Timeout as errt:
        print_error(errt, "Timeout ошибка:", social_network, verbose, color)
    except requests.exceptions.RequestException as err:
        print_error(err, "Ошибка раскладки\nклавиатуры/*символов", social_network, verbose, color)
    return None, "", -1


def snoop(username, site_data, verbose=False, user=False, country=False, print_found_only=False, timeout=None, color=True):

    """Snoop Аналитика.

    Snoop ищет никнеймы на различных интернет-ресурсах.

    Аргументы:
    username               -- Разыскиваемый никнейм.
    site_data              -- Snoop БД поддерживваемых сайтов 
    verbose/debug          -- Подробная вербализация
    timeoutout             -- Ограничение времени на ожидание ответа от сайта
    color                  -- Монохромный/раскрашиваемый терминал
    country                -- Страны
    sort                   -- Сортировка по алфавиту внутри баз данных: (data.json; bad_data.json; sites.md; bad_site.md) 
    listing                -- Вывод на печать БС и ЧС
    update                 -- Обновление ПО Snoop
    donation               -- Финансовая поддержка Snoop

    Возвращаемые значения:
    Словарь, содержащий результаты из отчета. Ключом словаря является название
    сайта из БД .json, значением — вложенный словарь со следующими ключами::
        flagcountry:               Флаг государства (расположение страны/локация).
        url_main:                  URL основного сайта.
        url_user:                  URL ведущий на пользователя (если такой аккаунт найден).
        exists/статус:             Указание результатов теста на наличие аккаунта.
        http_status/статус кода:   HTTP status code ответа сайта.
        response_text:             Текст, который вернулся запрос-ответ от сайта (при ошибке соединения может отсутствовать).
    """

    print_info("разыскиваем:", username, color)

# Создать сеанс на основе методологии запроса.
    underlying_session = requests.session()
    underlying_request = requests.Request()

# Рабочий лимит 20+
    if len(site_data) >= 20:
        max_workers=20
    else:
        max_workers=len(site_data)

# Создать многопоточный сеанс для всех запросов.
    session = ElapsedFuturesSession(max_workers=max_workers, session=underlying_session)

# Результаты анализа всех сайтов.
    results_total = {}


# Создание futures на все запросы. Это позволит распараллетить запросы.
#    global countryA
    for social_network, net_info in site_data.items():
#        print([iz for iz in site_data]) #Тест вывода ключей
#        print(social_network)
        # Результаты анализа конкретного сайта.
        results_site = {}

# Запись URL основного сайта и флага страные (сопоставление с data.json)
        results_site['flagcountry'] = net_info.get("country")
        results_site['flagcountryklas'] = net_info.get("country_klas")
        results_site['url_main'] = net_info.get("urlMain")


# Пользовательский user-agent браузера, некоторые сайты от этого зависят напрямую.
# Временно поставил самый популярный, чтобы не думали, что запросы идут от ботов.
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }

        if "headers" in net_info:
# Переопределить / добавить любые дополнительные заголовки, необходимые для данного сайта.
            headers.update(net_info["headers"])

# Не делать запрос, если имя пользователя не подходит для сайта.
        regex_check = net_info.get("regexCheck")
        if regex_check and re.search(regex_check, username) is None:
# Не нужно делать проверку на сайте: если это имя пользователя не допускается.
            if not print_found_only:
                print_invalid(social_network, "Недопустимый формат имени для данного сайта", color)

            results_site["exists"] = "прочерк"
            results_site["url_user"] = ""
            results_site['http_status'] = ""
            results_site['response_text'] = ""
            results_site['response_time_ms'] = ""
        else:
# URL пользователя на сайте (если он существует).
            url = net_info["url"].format(username)
            results_site["url_user"] = url
            url_probe = net_info.get("urlProbe")
            if url_probe is None:
# URL-адрес — является обычным, который видят люди в Интернете.
                url_probe = url
            else:
# Существует специальный URL (обычно о нем мы не догадываемся) для проверки существования отдельно юзера.
                url_probe = url_probe.format(username)

# Если нужен только статус кода, не загружать код страницы.
            if net_info["errоrTypе"] == 'status_code':
                request_method = session.head
            else:
                request_method = session.get

            if net_info["errоrTypе"] == "response_url":
# Сайт перенаправляет запрос на другой URL, если имя пользователя не существует.
# Имя найдено. Запретить перенаправление чтобы захватить статус кода из первоначального url.
                allow_redirects = False
            else:
# Разрешить любой редирект, который хочет сделать сайт.
# Окончательным результатом запроса будет то, что доступно.
                allow_redirects = True


            future = request_method(url=url_probe, headers=headers,
                                    allow_redirects=allow_redirects,
                                    timeout=timeout
                                    )

# Сохранить future in data для последующего доступа.
            net_info["request_future"] = future

# Добавлять результаты этого сайта в окончательный словарь со всеми другими результатами.
        results_total[social_network] = results_site

# Открыть файл, содержащий ссылки на аккаунт.
# Основная логика: если текущие запросов, сделайте их. Если многопоточные запросы, дождаться ответов.

# print(results_site) # Проверка записи на успех.
    for social_network, net_info in site_data.items():

# Получить результаты снова.
        results_site = results_total.get(social_network)

# Получить другую информацию сайта снова.
        url = results_site.get("url_user")
        countryA = results_site.get("flagcountry")
        countryB = results_site.get("flagcountryklas")        
        exists = results_site.get("exists")

        if exists is not None:
# Мы уже определили, что пользователь не существует здесь.
            continue

# Получить ожидаемый тип ошибки.
        error_type = net_info["errоrTypе"]

# Данные по умолчанию в случае каких-либо сбоев в выполнении запроса.
        http_status = "?"
        response_text = ""

# Получить future и убедиться, что оно закончено.
        future = net_info["request_future"]
        r, error_type, response_time = get_response(request_future=future,
                                                    error_type=error_type,
                                                    social_network=social_network,
                                                    verbose=verbose,
                                                    retry_no=3,
                                                    color=color)

# Попытка получить информацию запроса.
        try:
            http_status = r.status_code
        except:
            pass
        try:
            response_text = r.text.encode(r.encoding)
        except:
            pass

# Ответы message (разные локации).
        if "message" == "errorMsg":
            print("errorMsg")
        if error_type == "message":
            error = net_info.get("errorMsg") 
            error2 = net_info.get("errorMsg2")
            if error2 in r.text:
                if not print_found_only:
                    print_not_found(social_network, response_time, verbose, color)
                exists = "увы"
            elif error in r.text:
                if not print_found_only:
                    print_not_found(social_network, response_time, verbose, color)
                exists = "увы"
                
            else:
                if sys.platform == 'win32':
                    print_found_country(social_network, url, countryB, response_time, verbose, color)
                else:
                    print_found_country(social_network, url, countryA, response_time, verbose, color)
                exists = "найден!"

        elif error_type == "status_code":
# Проверяет, является ли код состояния ответа 2..
            if not r.status_code >= 300 or r.status_code < 200:
                if sys.platform == 'win32':
                    print_found_country(social_network, url, countryB, response_time, verbose, color)
                else:
                    print_found_country(social_network, url, countryA, response_time, verbose, color)
                exists = "найден!"
            else:
                if not print_found_only:
                    print_not_found(social_network, response_time, verbose, color)
                exists = "увы"

        elif error_type == "response_url":

# Для этого метода обнаружения мы отключили перенаправление.
# Таким образом, нет необходимости проверять URL-адрес ответа: он всегда будет соответствовать запросу. 
# Вместо этого мы обеспечим, чтобы статус кода указывал, что запрос был успешным (тоесть не 404 или перенаправлен.
        
            if 200 <= r.status_code < 300:
                if sys.platform == 'win32':
                    print_found_country(social_network, url, countryB, response_time, verbose, color)
                else:
                    print_found_country(social_network, url, countryA, response_time, verbose, color)
                exists = "найден!"
            else:
                if not print_found_only:
                    print_not_found(social_network, response_time, verbose, color)
                exists = "увы"

        elif error_type == "":
            if not print_found_only:
                print_invalid(social_network, "*Пропуск", color)
            exists = "блок"

# Сохранить сущ.флаг.
        results_site['exists'] = exists

# Сохранить результаты из запроса.
        results_site['http_status'] = http_status
        results_site['response_text'] = response_text
        results_site['response_time_ms'] = response_time

# Добавьление результатов этого сайта в окончательный словарь со всеми другими результатами.
        results_total[social_network] = results_site
    return results_total


def timeout_check(value):
    """Проверка: время ожидания ответа сайта.

    Проверка опцией "--timeoutout" на достоверность.

    Аргумент - указание в секундах.

    Возвращаемое значение - число в секундах, которое используется для timeoutout-а.

    Примечание:  Возникает исключение в случае, если время ожидания...
    """
    from argparse import ArgumentTypeError
    
    try:
        global timeout
        timeout = int(value)
    except:
        raise ArgumentTypeError(f"\033[36mTimeout '{value}' Err, укажите время в 'секундах'. \033[0m")
    if timeout <= 0:
        raise ArgumentTypeError(f"\033[36mTimeout '{value}' Err, укажите время > 0 c. \033[0m")
    return timeout

# Обновление Snoop.
def update_snoop():
    if sys.platform == 'win32':
        upd = str(input("""Вы действительно хотите:
                    __             _  
   ._  _| _._|_ _  (_ ._  _  _ ._   ) 
|_||_)(_|(_| |_(/_ __)| |(_)(_)|_) o  
   |                           |    
нажмите 'y' """))
    else:
        upd = str(input("""\033[36mВы действительно хотите:
                    __             _  
   ._  _| _._|_ _  (_ ._  _  _ ._   ) 
|_||_)(_|(_| |_(/_ __)| |(_)(_)|_) o  
   |                           |    
нажмите\033[0m 'y' """))

    if upd == "y":
        if sys.platform == 'win32':
            print(Fore.RED + "Функция обновления Snoop требует установки <Git> на OS Windows")
            os.startfile("update.bat")
        else:
            print(Fore.RED + "Функция обновления Snoop требует установки <Git> на OS GNU/Linux")
            os.system("./update.sh")


def main():
# Запрос лицензии.
    with open('COPYRIGHT', 'r', encoding="utf8") as copyright:
        cop = copyright.read()

    version_snoop = f"\033[36m%(prog)s: {__version__}\033[36m\n" +  \
                     f"\033[36mOS: {platform.platform(aliased=True, terse=0)}\033[36m\n" + \
                     f"\033[36mPython: {platform.python_version()}\033[36m\n\n" + \
                     f"\033[37m{cop}\033[0m\n"


# Пожертвование.
    donate = ("""
\033[36m╭donate:\033[0m
\033[36m├──BTC_BHC:\033[0m \033[37m1EXoQj1rd5oi54k9yynVLsR4kG61e4s8g3\033[0m
\033[36m├──Яндекс.Деньги:\033[0m \033[37m4100111364257544\033[0m  
\033[36m└──PayPal:\033[0m \033[37msnoopproject@protonmail.com\033[0m    
\n\033[36mИсходный код:\033[0m \033[37mhttps://github.com/snooppr/snoop\033[0m """)
              
# Флаг БС
    with open("data.json", "r", encoding="utf8") as flag:
        BS = json.load(flag)
        flagBS = len(BS)                
                
# Назначение опций Snoop.
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                            description=f"{module_name} (Version {__version__})",
                            epilog=(f"\033[36mSnoop поддержка: \033[36;1m{flagBS}\033[0m \033[36mWebsites!!!\033[0m\n\n{donate} ")
                            )
    parser.add_argument("--donate Y", "-d Y",
                        action="store_true", dest="donation",
                        help="Пожертвовать на развитие Snoop project-а"
                        )
    parser.add_argument("--sort Y",
                        action="store_true", dest="sort", default=False,
                        help="Обновление/сортировка черного и белого списков (.json) сайтов БД Snoop.\n"
                             "Если вы не разработчик, не используйте эту опцию"
                        )
    parser.add_argument("--version", "--about", "-V",
                        action="version",  version=(version_snoop),
                        help="Вывод на печать версий: OS; Snoop; Python и Лицензии"
                        )
    parser.add_argument("--verbose", "-v",
                        action="store_true",  dest="verbose", default=False,
                        help="Во время поиска 'username' выводить на печать подробную вербализацию"
                        )
    parser.add_argument("--csv",
                        action="store_true",  dest="csv", default=False,
                        help="По завершению поиска 'username' сохранить файл в формате таблицы 'username.CSV' с расширенным анализом"
                        )
    parser.add_argument("--json", "-j",
                        dest="json_file", default="data.json", metavar='',
                        help="""Указать для поиска 'username' другую БД в формате 'json',
                              например, 'example_data.json'. Если у вас нет такой БД, не используйте эту опцию"""
                        )
    parser.add_argument("--site", "-s",
                        action="append", metavar='', 
                        dest="site_list",  default=None, 
                        help="Указать имя сайта из БС '--list all'. Поиск 'username' на одном указанном ресурсе"
                        )
    parser.add_argument("--time", "-t 9",
                        action="store", metavar='',
                        dest="timeout", type=timeout_check, default=None,
                        help="Установить выделение макс.времени на ожидание ответа от сервера (секунды).\n"
                             "Влияет на продолжительность поиска. Влияет на 'Timeout ошибки:'"
                             "Оптимальное значение при хорошем интернет соединении = 9с.\n"
                             "\033[31;1mВкл. эту опцию необходимо практически всегда\033[0m, \
                              чтобы избежать длительных зависаний при Internet Censorship"
                        )
    parser.add_argument("--found-print", "-f", 
                        action="store_true", dest="print_found_only", default=False,
                        help="Выводить на печать только найденные аккаунты"
                        )
    parser.add_argument("--no-func", "-n",
                        action="store_true", dest="no_func", default=False,
                        help="""✓Монохромный терминал, не использовать цвета в url\n
                                ✓Отключить звук\n
                                ✓Запретить открытие web browser-а\n
                                ✓Отключить вывод на печать для флагов стран"""
                        )
    parser.add_argument("username",
                        nargs='+', metavar='USERNAMES',
                        action="store",
                        help="Никнейм разыскиваемого пользователя, поддерживается несколько имён"
                        )
    parser.add_argument("--userload", "-u", metavar='',
                        action="store", dest="user", default=False,
                        help="Указать файл со списком user-ов. Пример_Linux: 'python3 snoop.py -u ~/list.txt start'\n"
                             "Пример для Windows: 'python snoop.py -u c:\snoop\list.txt start'"
                        )                        
    parser.add_argument("--list all",
                        action="store_true", dest="listing",
                        help="Вывод на печать БД (БС+ЧС) поддерживаемых сайтов"
                        )
    parser.add_argument("--country", "-c",
                        action="store_true", dest="country", default=False,
                        help="Сортировка 'вывода на печать/запись в html' результатов по странам, а не по алфавиту"
                        )                        
    parser.add_argument("--update Y",
                        action="store_true", dest="update",
                        help="Обновить Snoop"
                        )   

    args = parser.parse_args()

    if args.csv:
        print(Fore.CYAN + "[+] активирована опция '--csv': «будет создан дополнительный подробный отчёт»")

    if args.no_func:
        print(Fore.CYAN + "[+] активирована опция '-n': «отключены:: цвета; звук; флаги; браузер»")

    if args.timeout:
        print(Fore.CYAN + f"[+] активирована опция '-t': «snoop будет ожидать ответа от сайта \033[36;1m<= {timeout}_sec\033[0m\033[36m.» \033[0m")

    if args.verbose:
        print(Fore.CYAN + "[+] активирована опция '-v': «подробная вербализация в CLI»")

# Сортировка по странам
    if args.country:
        patchjson = ("{}".format(args.json_file))
        raw = open(patchjson, "r", encoding="utf-8")
        jsonjson = json.load(raw)        
        print(Fore.CYAN + "[+] активирована опция '-c': «сортировка/запись в HTML результатов по странам»")
        site_country = dict(jsonjson)
        country_sites = sorted(jsonjson, key=lambda k: ("country" not in k, jsonjson[k].get("country", sys.maxsize)))
        s = {}
        for site in country_sites:
            s[site] = site_country.get(site)

# Информативный вывод -f
    if args.print_found_only:
        print(Fore.CYAN + "[+] активирована опция '-f': «выводить на печать только найденные аккаунты»")

    if args.site_list:
        print(Fore.CYAN + "[+] активирована опция '-s': «будет произведён поиск user-a на 1-м выбранном website»\n"
        "    допустимо использовать опцию '-s' несколько раз\n"
        "    опция '-s' несовместима с опцией '-с'")        

# Опция сортировки
    if args.sort:
        sortirovka.sorts()
        sys.exit(0)

# Опция list all
# Сортируем по алфавиту (2!)
#Сортировка для ОС Win
    if args.listing:
        if sys.platform == 'win32':
            sortY = str(input("Сортировать БС Snoop по странам или по имени сайта ?\nпо странам — 1 по имени — 2\n"))
        else:       
            sortY = str(input("\033[36mСортировать БС Snoop по странам или по имени сайта ?\n" + \
            "по странам —\033[0m 1 \033[36mпо имени —\033[0m 2\n"))

        if sortY == "2":
            if sys.platform == 'win32':
                print(Fore.CYAN + "========================\nOk, сортируем по алфавиту:\n")
                print(Fore.GREEN + "++Белый список++")
                with open("data.json", "r", encoding="utf8") as contry:
                    datajson = json.load(contry)
                    i = 0
                    for con in datajson:
                        aaa = datajson.get(con).get("country_klas")
                        i += 1
                        print(f"{i}.", Fore.CYAN + f"{aaa}  {con}")
#Общий результат БС Win                        
                listallsortFlag = []
                with open('sites.md', "r", encoding="utf8") as listyes:
                    for site in listyes.readlines():
                        patch = (site.split('[')[0]).replace(" ", "")
                        patch1 = str(patch.split('.')[1:2]).replace("[", "").replace("]", " ").replace("'", "")
                        listallsortFlag.append(patch1)
                        goba = sorted(listallsortFlag)
                    print(Fore.CYAN + "================\n")
                    print(Fore.CYAN + "Wr =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🌎 ')}", Fore.CYAN + "сайт(а/ов)!")
                    print(Fore.CYAN + "RU =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🇷🇺 ')}", Fore.CYAN + "сайт(а/ов)!")
                    print(Fore.CYAN + "US =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🇺🇸 ')}", Fore.CYAN + "сайт(а/ов)!")
                    print(Fore.CYAN + "Kb =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🏁 ')}", Fore.CYAN + "сайт(а/ов)!")
                    print(Fore.CYAN + "GB =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🇬🇧 ')}", Fore.CYAN + "сайт(а/ов)!")
                    print(Fore.CYAN + "DE =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🇩🇪 ')}", Fore.CYAN + "сайт(а/ов)!")
                    print(Fore.CYAN + "AU =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🇦🇺 ')}", Fore.CYAN + "сайт(а/ов)!")
                    print(Fore.CYAN + "CZ =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🇨🇿 ')}", Fore.CYAN + "сайт(а/ов)!")
                    print(Fore.CYAN + "CA =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🇨🇦 ')}", Fore.CYAN + "сайт(а/ов)!")
                    print(Fore.CYAN + "FR =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🇫🇷 ')}", Fore.CYAN + "сайт(а/ов)!")
                    print(Fore.CYAN + "...")
                    sys.exit(0)
#Сортировка для ОС GNU   
            else:
                print(Fore.CYAN + "========================\nOk, сортируем по алфавиту:\n")
                print(Fore.GREEN + "++Белый список++")                
                listall = []
                with open('sites.md', "r", encoding="utf8") as listyes:
                    for site in listyes.readlines():
                        patch = (site.split(']')[0]).replace("[", " ")
                        listall.append(patch)

                    narezka=listall[1:]
                    for zzz in (narezka):
                        print(Fore.CYAN + str(zzz))

                listallsortFlag = []
                with open('sites.md', "r", encoding="utf8") as listyes:
                    for site in listyes.readlines():
                        patch = (site.split('[')[0]).replace(" ", "")
                        patch1 = str(patch.split('.')[1:2]).replace("[", "").replace("]", " ").replace("'", "")
                        listallsortFlag.append(patch1)
                        goba = sorted(listallsortFlag)

                listall_bad = []
                with open('bad_site.md', "r", encoding="utf8") as listbad:
                    for site_bad in listbad.readlines():
                        patch_bad = (site_bad.split(']')[0]).replace("[", " ")
                        listall_bad.append(patch_bad)
                    print(Fore.RED + "\n--Чёрный список--", *listall_bad[1:], sep = "\n")

                print("================\n")
                print(Fore.CYAN + "🌎 =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🌎 ')}", Fore.CYAN + "сайт(а/ов)!")
                print(Fore.CYAN + "🇷🇺 =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🇷🇺 ')}", Fore.CYAN + "сайт(а/ов)!")
                print(Fore.CYAN + "🇺🇸 =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🇺🇸 ')}", Fore.CYAN + "сайт(а/ов)!")
                print(Fore.CYAN + "🏁 =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🏁 ')}", Fore.CYAN + "сайт(а/ов)!")
                print(Fore.CYAN + "🇬🇧 =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🇬🇧 ')}", Fore.CYAN + "сайт(а/ов)!")
                print(Fore.CYAN + "🇩🇪 =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🇩🇪 ')}", Fore.CYAN + "сайт(а/ов)!")
                print(Fore.CYAN + "🇦🇺 =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🇦🇺 ')}", Fore.CYAN + "сайт(а/ов)!")
                print(Fore.CYAN + "🇨🇿 =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🇨🇿 ')}", Fore.CYAN + "сайт(а/ов)!")
                print(Fore.CYAN + "🇨🇦 =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🇨🇦 ')}", Fore.CYAN + "сайт(а/ов)!")
                print(Fore.CYAN + "🇫🇷 =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🇫🇷 ')}", Fore.CYAN + "сайт(а/ов)!")
                print(Fore.CYAN + "...")
                sys.exit(0)

# Сортируем по странам (1!)
#Сортировка для ОС Win
        elif sortY == "1":
            if sys.platform == 'win32':
                listwindows = []
                with open("data.json", "r", encoding="utf8") as contry:
                    datajson = json.load(contry)
                    for con in datajson:
                        aaa = (datajson.get(con).get("country_klas"))
                        listwindows.append(f"{aaa}  {con}\n")
                    sort_spisok=sorted(listwindows)
                    print(Fore.CYAN + "========================\nOk, сортируем по странам:\n")
                    print(Fore.GREEN + "++Белый список++")
                    for i, numerlist in enumerate(sort_spisok):
                        fd=(i + 1)
                        print(f"{fd}.", Fore.CYAN + f"{numerlist}",end = '')
#Общий результат БС Win
                listallsortFlag = []
                with open('sites.md', "r", encoding="utf8") as listyes:
                    for site in listyes.readlines():
                        patch = (site.split('[')[0]).replace(" ", "")
                        patch1 = str(patch.split('.')[1:2]).replace("[", "").replace("]", " ").replace("'", "")
                        listallsortFlag.append(patch1)
                        goba = sorted(listallsortFlag)
                    print(Fore.CYAN + "================\n")
                    print(Fore.CYAN + "Wr =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🌎 ')}", Fore.CYAN + "сайт(а/ов)!")
                    print(Fore.CYAN + "RU =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🇷🇺 ')}", Fore.CYAN + "сайт(а/ов)!")
                    print(Fore.CYAN + "US =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🇺🇸 ')}", Fore.CYAN + "сайт(а/ов)!")
                    print(Fore.CYAN + "Kb =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🏁 ')}", Fore.CYAN + "сайт(а/ов)!")
                    print(Fore.CYAN + "GB =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🇬🇧 ')}", Fore.CYAN + "сайт(а/ов)!")
                    print(Fore.CYAN + "DE =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🇩🇪 ')}", Fore.CYAN + "сайт(а/ов)!")
                    print(Fore.CYAN + "AU =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🇦🇺 ')}", Fore.CYAN + "сайт(а/ов)!")
                    print(Fore.CYAN + "CZ =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🇨🇿 ')}", Fore.CYAN + "сайт(а/ов)!")
                    print(Fore.CYAN + "CA =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🇨🇦 ')}", Fore.CYAN + "сайт(а/ов)!")
                    print(Fore.CYAN + "FR =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🇫🇷 ')}", Fore.CYAN + "сайт(а/ов)!")
                    print(Fore.CYAN + "...")
                    sys.exit(0)
#Сортировка для ОС GNU
            else:
                print(Fore.CYAN + "========================\nOk, сортируем по странам:\n")
                listall = []
                with open('sites.md', "r", encoding="utf8") as listyes:
                    for site in listyes.readlines():
                        patch = (site.split(']')[0]).replace("[", " ")
                        patch1 = str(patch.split('.')[1:]).replace("[", "").replace("]", " ").replace("'", "")
                        listall.append(patch1)
                        sortlistall = sorted(listall)
                    print(Fore.GREEN + "++Белый список++")

                    narezka=sortlistall[1:]
                    for i, numerlist in enumerate(narezka):
                        fd=(i + 1)
                        print(Fore.CYAN + str(fd) + str(numerlist))

                listallsortFlag = []
                with open('sites.md', "r", encoding="utf8") as listyes:
                    for site in listyes.readlines():
                        patch = (site.split('[')[0]).replace(" ", "")
                        patch1 = str(patch.split('.')[1:2]).replace("[", "").replace("]", " ").replace("'", "")
                        listallsortFlag.append(patch1)
                        goba = sorted(listallsortFlag)

                listall_bad = []
                with open('bad_site.md', "r", encoding="utf8") as listbad:
                    for site_bad in listbad.readlines():
                        patch_bad = (site_bad.split(']')[0]).replace("[", " ")
                        listall_bad.append(patch_bad)
                    print(Fore.RED + "\n--Чёрный список--", *listall_bad[1:], sep = "\n")

                print("================\n")
                print(Fore.CYAN + "🌎 =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🌎 ')}", Fore.CYAN + "сайт(а/ов)!")
                print(Fore.CYAN + "🇷🇺 =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🇷🇺 ')}", Fore.CYAN + "сайт(а/ов)!")
                print(Fore.CYAN + "🇺🇸 =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🇺🇸 ')}", Fore.CYAN + "сайт(а/ов)!")
                print(Fore.CYAN + "🏁 =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🏁 ')}", Fore.CYAN + "сайт(а/ов)!")
                print(Fore.CYAN + "🇬🇧 =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🇬🇧 ')}", Fore.CYAN + "сайт(а/ов)!")
                print(Fore.CYAN + "🇩🇪 =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🇩🇪 ')}", Fore.CYAN + "сайт(а/ов)!")
                print(Fore.CYAN + "🇦🇺 =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🇦🇺 ')}", Fore.CYAN + "сайт(а/ов)!")
                print(Fore.CYAN + "🇨🇿 =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🇨🇿 ')}", Fore.CYAN + "сайт(а/ов)!")
                print(Fore.CYAN + "🇨🇦 =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🇨🇦 ')}", Fore.CYAN + "сайт(а/ов)!")
                print(Fore.CYAN + "🇫🇷 =", Style.BRIGHT + Fore.GREEN + f"{goba.count('🇫🇷 ')}", Fore.CYAN + "сайт(а/ов)!")
                print(Fore.CYAN + "...")
                sys.exit(0)

        else:
            print(Style.BRIGHT + Fore.RED + "Извините, но вы не выбрали действие\nвыход")
            sys.exit(0)
# Опция донат.
    if args.donation:
        print(donate)
        webbrowser.open("https://yasobe.ru/na/snoop_project")
        print(Style.BRIGHT + Fore.RED + "Выход")
        sys.exit(0)



# Опция указания списка разыскиваемых пользователей
    if args.user:
        userlist = []
        patchuserlist = ("{}".format(args.user))
        userfile=patchuserlist.split('/')[-1]
        with open(patchuserlist, "r", encoding="utf8") as u1:
            try:
                for lineuserlist in u1.readlines():
                    lineuserlist.strip()
                    userlist.append(lineuserlist)
                userlist=[line.rstrip() for line in userlist]
            except:
                print("\033[31;1mНе могу найти_прочитать!\033[0m \033[36mПожалуйста, укажите текстовый файл в кодировке —\033[0m \033[36;1mutf-8.\033[0m\n")
                print("\033[36mПо умолчанию блокнот в OS Windows сохраняет текст в кодировке — ANSI\033[0m")
                print("\033[36mОткройте ваш список пользователей и измените кодировку [файл ---> сохранить как ---> utf-8]")
                print("\033[36mИли удалите из словаря нечитаемые символы, в т.ч. и кириллицу.")
                sys.exit(0)
        print(Fore.CYAN + f"[+] активирована опция '-u': «розыск user-ов из файла: \033[36;1m{userfile}\033[0m\033[36m»\033[0m")
        print(Fore.CYAN + "    Будем искать:" + f" {userlist[:3]}" + " и других..." + Style.RESET_ALL)

# Завершение обновления Snoop.
    if args.update:
        print("\033[36m=======================\033[0m")
        update_snoop()
        print("\033[36m=======================\n", Style.BRIGHT + Fore.RED +"\nВыход")
        sys.exit(0)

# Проверка остальных опций.

    response_json_online = None
    site_data_all = None

    data_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), args.json_file)
    altjson = ("{}".format(args.json_file))
# Этого не будет, если в запросе отсутствовала Shema.
    if site_data_all is None:
# Проверьте, существует ли файл, иначе выход.
        if not os.path.exists(data_file_path):
            print("\033[36mJSON file не существует.\033[0m")
            print(
                "\033[36mВы не добавили .json файл\033[0m")
            sys.exit(1)
        else:
            raw = open(data_file_path, "r", encoding="utf-8")
            try:
                site_data_all = json.load(raw)
                print(Fore.CYAN + f"\nзагружена база: {altjson}:: " + 
                Style.BRIGHT + Fore.CYAN + f"{len(site_data_all)}" + "_Websites" + Style.RESET_ALL)
            except:
                print("\033[36mInvalid загружаемый JSON file.\033[0m")

    if args.site_list is None:
# Не желательно смотреть на подмножество сайтов.
        site_data = site_data_all
    else:
# Пользователь желает выборочно запускать запросы к подмножеству списку сайтов.

# Убедиться, что сайты поддерживаются, создать сокращенную базу данных сайта.
        site_data = {}
        site_missing = []
        for site in args.site_list:
            for existing_site in site_data_all:
                if site.lower() == existing_site.lower():
                    site_data[existing_site] = site_data_all[existing_site]
            if not site_data:
# Создать список сайтов, которые не поддерживаются для будущего сообщения об ошибке.
                site_missing.append(f"'{site}'")

        if site_missing:
            print(
                f"\033[36mОшибка: желаемый сайт не найден в базе Snoop:: {', '.join(site_missing)}\n"
                "Или вы пропустили знак '-' в опции '--csv' \033[0m")
            sys.exit(1)


# Крутим список юзеров  
    if args.user:
        kef_user=0
        for username in userlist:
            kef_user +=1
            file = open("results/txt/" + username + ".txt", "w", encoding="utf-8")
            try:
                file = open("results/txt/" + username + ".txt", "w", encoding="utf-8")
            except (SyntaxError, ValueError):
                pass

            try:
                results = snoop(username,
                               s,
                               country=args.country,
                               user=args.user,
                               verbose=args.verbose,
                               print_found_only=args.print_found_only,
                               timeout=args.timeout,
                               color=not args.no_func)
            except:
                results = snoop(username,
                               site_data,
                               country=args.country,
                               user=args.user,
                               verbose=args.verbose,
                               print_found_only=args.print_found_only,
                               timeout=args.timeout,
                               color=not args.no_func)

            exists_counter = 0
            file.write("Адрес | ресурс" + "\n\n")
            for website_name in results:
                timefinish = time.time() - timestart            
                dictionary = results[website_name]
                if dictionary.get("exists") == "найден!":
                    exists_counter += 1
                    file.write(dictionary ["url_user"] + " | " + (website_name)+"\n")
            file.write("\n" f"Запрашиваемый объект: <{username}> найден: {exists_counter} раз(а).")
            file.write("\n" f"База Snoop: " + str(flagBS) + " Websites.")
            file.write("\n" f"Обновлено: " + time.strftime("%m/%d/%Y_%H:%M:%S", time_data) + ".")      
            print(Fore.CYAN + "├─Результаты поиска:", "найдено -->", exists_counter, "url (%.0f" % float(timefinish) +"sec)")

    # Запись в html.
            file = open("results/html/" + username + ".html", "w", encoding="utf-8")
            try:
                file = open("results/html/" + username + ".html", "w", encoding="utf-8")
            except (SyntaxError, ValueError):
                pass
            file.write("<!DOCTYPE html>\n\n<h1>" + "<a href='file://" + str(dirresults) + "/results/html/'>Главная</a>" + "</h1>")
            file.write("""<h3>Snoop Project</h3> <p>Нажмите: 'сортировать по странам', возврат: 'F5':</p>\n
            <button onclick="sortList()">Сортировать по странам</button><br><br>\n\n""")
            file.write("Объект " + "<b>" + (username) + "</b>" + " найден на нижеперечисленных " + "<b>" + str(exists_counter) + 
            "</b> ресурсах:\n" + "<br><ol" + " id='id777'>\n")
            
            cnt = Counter()
            for website_name in results:
                dictionary = results[website_name]
                flag_sum=dictionary["flagcountry"]
                if dictionary.get("exists") == "найден!":
                    li = []
                    li.append(flag_sum)
                    exists_counter += 0
                    for word in li:
                        cnt[word] += 1
                    file.write("<li>" + dictionary["flagcountry"]+ "<a href='" + dictionary ["url_user"] + "'>"+ 
                    (website_name) + "</a>" + "</li>\n")
            flag_str=str(cnt)
            flag_str_sum = (flag_str.split('{')[1]).replace("'", "").replace("}", "").replace(")", "").replace(",", "  ↯  ").replace(":", "⇔")

            file.write("</ol>GEO: " + str(flag_str_sum) + ".\n")
            file.write("<br> Запрашиваемый объект < <b>" + str(username) + "</b> > найден: <b>" + str(exists_counter) + "</b> раз(а).")
            file.write("<br> Затраченное время на создание отчёта: " + "<b>" + "%.0f" % float(timefinish) + "</b>" + " c.\n")
            file.write("<br> База Snoop: <b>" + str(flagBS) + "</b>" + " Websites.\n")
            file.write("<br> Обновлено: " + "<i>" + time.strftime("%m/%d/%Y_%H:%M:%S", time_data) + ".</i>\n")
            file.write("<br><br><a href='https://github.com/snooppr/snoop'>🌎Snoop/Исходный код</a>\n")
            file.write("""
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
    </script>""")
            file.close()

    #+CSV вывод на печать информации
            if args.csv == True:
                print(Fore.CYAN + "├──Результаты сохранены в: " + Style.RESET_ALL +
                "results/*/" + str(username) + ".*")
                print(Fore.CYAN + "├──Расширенный анализ сохранён в: " + Style.RESET_ALL + "results/csv/" + str(username) + ".csv")
            else:        
                print(Fore.CYAN + "├──Результаты сохранены в: " + Style.RESET_ALL +
                "results/*/" + str(username) + ".*")
            file.close()

    # Запись в csv.
            if args.csv == True:
                with open("results/csv/" + username + ".csv", "w", newline='', encoding="utf-8") as csv_report:
                    if censor >= 9 * kef_user:
                        writer = csv.writer(csv_report)
                        writer.writerow(['Объект',
                                         'Ресурс',
                                         'Url',
                                         'Url_username',
                                         'Статус',
                                         'Статус_кода',
                                         'Время/мс',
                                         'Внимание!_Поиск_проходил_при_слабом_интернет_соединении_или_Internet-Censorship. '
                                         'Результаты_могут_быть_неполные.'
                                         ])
                    else:
                        writer = csv.writer(csv_report)
                        writer.writerow(['Объект',
                                         'Ресурс',
                                         'Url',
                                         'Url_username',
                                         'Статус',
                                         'Статус_кода',
                                         'Время/мс',
                                         ])
                    for site in results:
                        writer.writerow([username,
                                         site,
                                         results[site]['url_main'],
                                         results[site]['url_user'],
                                         results[site]['exists'],
                                         results[site]['http_status'],
                                         results[site]['response_time_ms']
                                         ])
                    writer.writerow(['«---------------------------------------',
                                     '--------', '----------------------------------',
                                     '--------------------------------------------------',
                                     '-------------', '-----------------', '--------------»'])
                    writer.writerow(['База_Snoop=' + str(flagBS) + '_Websites'])
                    writer.writerow('')
                    writer.writerow(['Дата'])
                    writer.writerow([time.strftime("%m/%d/%Y_%H:%M:%S", time_data)])
                    file.close()

# Финишный вывод.
        if censor >= 9 * int(kef_user):
            print(Fore.CYAN + "├───Дата поискового запроса:", time.strftime("%m/%d/%Y_%H:%M:%S", time_data))
            print(Fore.CYAN + "└────\033[31;1mВнимание!\033[0m", Fore.CYAN + "Cлабое соединение или Internet Censorship:", 
                              "*используйте VPN")
            print("\n\033[37m\033[44m{}".format("Лицензия: авторская"))
        else:
            print(Fore.CYAN + "└───Дата поискового запроса:", time.strftime("%m/%d/%Y_%H:%M:%S", time_data))
            print("\n\033[37m\033[44m{}".format("Лицензия: авторская"))

# Поиск по умолчанию (без опции -u)
    else:
        for username in args.username:
            
            file = open("results/txt/" + username + ".txt", "w", encoding="utf-8")
            try:
                file = open("results/txt/" + username + ".txt", "w", encoding="utf-8")
            except (SyntaxError, ValueError):
                pass
            try:
                results = snoop(username,
                               s,
                               country=args.country,
                               user=args.user,
                               verbose=args.verbose,
                               print_found_only=args.print_found_only,
                               timeout=args.timeout,
                               color=not args.no_func)
            except:
                results = snoop(username,
                               site_data,
                               country=args.country,
                               user=args.user,
                               verbose=args.verbose,
                               print_found_only=args.print_found_only,
                               timeout=args.timeout,
                               color=not args.no_func)                
            exists_counter = 0
            file.write("Адрес | ресурс" + "\n\n")
            for website_name in results:
                timefinish = time.time() - timestart            
                dictionary = results[website_name]
                if dictionary.get("exists") == "найден!":
                    exists_counter += 1
                    file.write(dictionary ["url_user"] + " | " + (website_name)+"\n")
            file.write("\n" f"Запрашиваемый объект: <{username}> найден: {exists_counter} раз(а).")
            file.write("\n" f"База Snoop: " + str(flagBS) + " Websites.")
            file.write("\n" f"Обновлено: " + time.strftime("%m/%d/%Y_%H:%M:%S", time_data) + ".")
            print(Fore.CYAN + "├─Результаты поиска:", "найдено -->", exists_counter, "url (%.0f" % float(timefinish) +"sec)")


    # Запись в html.
            file = open("results/html/" + username + ".html", "w", encoding="utf-8")
            try:
                file = open("results/html/" + username + ".html", "w", encoding="utf-8")
            except (SyntaxError, ValueError):
                pass
            file.write("<!DOCTYPE html>\n\n<h1>" + "<a href='file://" + str(dirresults) + "/results/html/'>Главная</a>" + "</h1>")
            file.write("""<h3>Snoop Project</h3> <p>Нажмите: 'сортировать по странам', возврат: 'F5':</p>\n
            <button onclick="sortList()">Сортировать по странам</button><br><br>\n\n""")
            file.write("Объект " + "<b>" + (username) + "</b>" + " найден на нижеперечисленных " + "<b>" + str(exists_counter) + 
            "</b> ресурсах:\n" + "<br><ol" + " id='id777'>\n")
            
            cnt = Counter()
            for website_name in results:
                dictionary = results[website_name]
                flag_sum=dictionary["flagcountry"]
                if dictionary.get("exists") == "найден!":
                    li = []
                    li.append(flag_sum)
                    exists_counter += 0
                    for word in li:
                        cnt[word] += 1
                    file.write("<li>" + dictionary["flagcountry"]+ "<a href='" + dictionary ["url_user"] + "'>"+ 
                    (website_name) + "</a>" + "</li>\n")
            flag_str=str(cnt)
            try:            
                flag_str_sum = (flag_str.split('{')[1]).replace("'", "").replace("}", "").replace(")", "").replace(",", "  ↯  ").replace(":", "⇔")
                file.write("</ol>GEO: " + str(flag_str_sum) + ".\n")
            except:
                pass
            file.write("<br> Запрашиваемый объект < <b>" + str(username) + "</b> > найден: <b>" + str(exists_counter) + "</b> раз(а).")
            file.write("<br> Затраченное время на создание отчёта: " + "<b>" + "%.0f" % float(timefinish) + "</b>" + " c.\n")
            file.write("<br> База Snoop: <b>" + str(flagBS) + "</b>" + " Websites.\n")
            file.write("<br> Обновлено: " + "<i>" + time.strftime("%m/%d/%Y_%H:%M:%S", time_data) + ".</i>\n")
            file.write("<br><br><a href='https://github.com/snooppr/snoop'>🌎Snoop/Исходный код</a>\n")
            file.write("""
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
    </script>""")
            file.close()

    #+CSV вывод на печать информации
            if args.csv == True:
                print(Fore.CYAN + "├──Результаты сохранены в: " + Style.RESET_ALL +
                "results/*/" + str(username) + ".*")
                print(Fore.CYAN + "├──Расширенный анализ сохранён в: " + Style.RESET_ALL + "results/csv/" + str(username) + ".csv")
            else:
                print(Fore.CYAN + "├──Результаты сохранены в: " + Style.RESET_ALL +
                "results/*/" + str(username) + ".*")
            file.close()

    # Запись в csv.
            if args.csv == True:
                with open("results/csv/" + username + ".csv", "w", newline='', encoding="utf-8") as csv_report:
                    if censor >= 9:            
                        writer = csv.writer(csv_report)
                        writer.writerow(['Объект',
                                         'Ресурс',
                                         'Url',
                                         'Url_username',
                                         'Статус',
                                         'Статус_кода',
                                         'Время/мс',
                                         'Внимание!_Поиск_проходил_при_слабом_интернет_соединении_или_Internet-Censorship. '
                                         'Результаты_могут_быть_неполные.'
                                         ])
                    else:
                        writer = csv.writer(csv_report)
                        writer.writerow(['Объект',
                                         'Ресурс',
                                         'Url',
                                         'Url_username',
                                         'Статус',
                                         'Статус_кода',
                                         'Время/мс'
                                         ])
                    for site in results:
                        writer.writerow([username,
                                         site,
                                         results[site]['url_main'],
                                         results[site]['url_user'],
                                         results[site]['exists'],
                                         results[site]['http_status'],
                                         results[site]['response_time_ms']
                                         ])
                    writer.writerow(['«---------------------------------------',
                                     '--------', '----------------------------------',
                                     '--------------------------------------------------',
                                     '-------------', '-----------------', '--------------»'])
                    writer.writerow(['База_Snoop=' + str(flagBS) + '_Websites'])
                    writer.writerow('')
                    writer.writerow(['Дата'])
                    writer.writerow([time.strftime("%m/%d/%Y_%H:%M:%S", time_data)])
                    file.close()

# Финишный вывод.
        if censor >= 9:
            print(Fore.CYAN + "├───Дата поискового запроса:", time.strftime("%m/%d/%Y_%H:%M:%S", time_data))
            print(Fore.CYAN + "└────\033[31;1mВнимание!\033[0m", Fore.CYAN + "Cлабое соединение или Internet Censorship:", "*используйте VPN")
            print("\n\033[37m\033[44m{}".format("Лицензия: авторская"))
        else:
            print(Fore.CYAN + "└───Дата поискового запроса:", time.strftime("%m/%d/%Y_%H:%M:%S", time_data))
            print("\n\033[37m\033[44m{}".format("Лицензия: авторская"))


# Открывать/нет браузер с результатами поиска.
    if args.no_func==False:
        if exists_counter >= 1:
            webbrowser.open(str("file://" + str(dirresults) + "/results/html/" + str(username) + ".html"))
# Музыка.
        playsound('end.wav')

if __name__ == "__main__":
    main()

#! /usr/bin/env python3

import csv  
import json
import locale
import os
import platform
import random
import re
import requests
import subprocess
import sys
import time
import webbrowser


from argparse import ArgumentParser, RawDescriptionHelpFormatter
from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor
from load_proxies import load_proxies_from_csv, check_proxy_list
from pathlib import Path
from playsound import playsound
from requests_futures.sessions import FuturesSession
from torrequest import TorRequest


if sys.platform == 'win32':
    locale.setlocale(locale.LC_ALL, '')

init(autoreset=True)

print ("""
  ___|                          
\___ \  __ \   _ \   _ \  __ \  
      | |   | (   | (   | |   | 
_____/ _|  _|\___/ \___/  .__/  
                         _|     \033[37mv1.\033[34m1.2\033[31m_rus\033[0m\n
""")

print ("#Пример:\n cd ~/snoop\n python3 snoop.py -h \033[37m#справка по всем функциям ПО\033[0m\n" + 
" python3 snoop.py --time 9 user \033[37m#поиск user-a, ожидание ответа от сайта ≤ 9с.\033[0m\n" + 
" открыть 'snoop/results/*/user.[txt.html.csv]' \033[37m#изучить сохранённые результаты поиска\033[0m\n")


module_name = "Snoop: поиск никнейма по всем фронтам!"
__version__ = "1.1.2_rus Ветка GNU/Linux"


dirresults = Path.cwd()

timestart = time.time()

global proxy_list

proxy_list = []

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
        print(Style.BRIGHT + Fore.WHITE + "[" +
            Fore.RED + "-" +
            Fore.WHITE + "]" +
            Fore.RED + f" {errstr}" +
            Fore.YELLOW + f" {err if verbose else var}")
        playsound('err.wav')
    else:
        print(f"[-] {errstr} {err if verbose else var}")


def format_response_time(response_time, verbose):
    return " [{} ms]".format(response_time) if verbose else ""


def print_found(social_network, url, response_time, verbose=False, color=True):
    if color:
        print((Style.BRIGHT + Fore.WHITE + "[" +
            Fore.GREEN + "+" +
            Fore.WHITE + "]" +
            format_response_time(response_time, verbose) +
            Fore.GREEN + f" {social_network}:"), url)
    else:
        print(f"[+]{format_response_time(response_time, verbose)} {social_network}: {url}")

def print_not_found(social_network, response_time, verbose=False, color=True):
    if color:
        print((Style.BRIGHT + Fore.WHITE + "[" +
            Fore.RED + "-" +
            Fore.WHITE + "]" +
            format_response_time(response_time, verbose) +
            Fore.GREEN + f" {social_network}:" +
            Fore.YELLOW + " Увы!"))
    else:
        print(f"[-]{format_response_time(response_time, verbose)} {social_network}: Увы!")

def print_invalid(social_network, msg, color=True):
    """Ошибка вывода результата"""
    if color:
        print((Style.BRIGHT + Fore.WHITE + "[" +
            Fore.RED + "-" +
            Fore.WHITE + "]" +
            Fore.GREEN + f" {social_network}:" +
            Fore.YELLOW + f" {msg}"))
    else:
        print(f"[-] {social_network} {msg}")


def get_response(request_future, error_type, social_network, verbose=False, retry_no=None, color=True):

    
    global proxy_list
    
    try:
        rsp = request_future.result()
        if rsp.status_code:
            return rsp, error_type, rsp.elapsed
    except requests.exceptions.HTTPError as errh:
        print_error(errh, "HTTP Error:", social_network, verbose, color)

# Сбой с прокси, дубль попытка.
    except requests.exceptions.ProxyError as errp:
        if retry_no>0 and len(proxy_list)>0:
# Выбор нового прокси.
            new_proxy = random.choice(proxy_list)
            new_proxy = f'{new_proxy.protocol}://{new_proxy.ip}:{new_proxy.port}'
            print(f'Retrying with {new_proxy}')
            request_future.proxy = {'http':new_proxy,'https':new_proxy}
            get_response(request_future,error_type, social_network, verbose,retry_no=retry_no-1, color=color)
        else:
            print_error(errp, "Proxy error:", social_network, verbose, color)
    except requests.exceptions.ConnectionError as errc:
        print_error(errc, "Ошибка соединения:", social_network, verbose, color)
    except requests.exceptions.Timeout as errt:
        print_error(errt, "Timeout ошибка:", social_network, verbose, color)
    except requests.exceptions.RequestException as err:
        print_error(err, "Ошибка раскладки\nклавиатуры/*символов", social_network, verbose, color)
    return None, "", -1


def snoop(username, site_data, verbose=False, tor=False, unique_tor=False,
             proxy=None, print_found_only=False, timeout=None, color=True):

    """Snoop Аналитика.

    Snoop ищет никнеймы на различных интернет-ресурсах.

    Аргументы:
    username               -- Разыскиваемый никнейм.
    site_data              -- Snoop БД поддерживваемых сайтов 
    verbose                -- Подробная вербализация
    tor                    -- Служба Tor
    unique_tor             -- Опция Tor: новая цепочка при поиске для каждого сайта
    proxy                  -- Указание своего proxy
    timeoutout                -- Ограничение времени на ожидание ответа сайта
    color                  -- Монохромный/раскрашиваемый терминал

    Возвращаемые значения:
    Словарь, содержащий результаты из отчета. Ключом словаря является название
    сайта из БД, и значение другого словаря со следующими ключами::
        url_main:                  URL основного сайта.
        url_user:                  URL ведущий на пользователя (если такой аккаунт найден).
        exists/статус:             Указание результатов теста на наличие аккаунта.
        http_status/статус кода:   HTTP status code ответа сайта.
        response_text:    Текст, который вернулся запрос-ответ от сайта (при ошибке соединения может отсутствовать)
    """

    print_info("разыскиваем:", username, color)

# Создать сеанс на основе методологии запроса.
    if tor or unique_tor:
# Requests Tor.
        underlying_request = TorRequest()
        underlying_session = underlying_request.session
    else:
# Normal requests.
        underlying_session = requests.session()
        underlying_request = requests.Request()

# Рабочий лимит 20+
    if len(site_data) >= 20:
        max_workers=20
    else:
        max_workers=len(site_data)

# Создать многопоточный сеанс для всех запросов.
    session = ElapsedFuturesSession(max_workers=max_workers,
                                    session=underlying_session)

# Результаты анализа всех сайтов.
    results_total = {}

# Создание futures на все запросы. Это позволит распараллетить запросы.
    for social_network, net_info in site_data.items():

        # Результаты анализа конкретного сайта.
        results_site = {}

# Запись URL основного сайта.
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

            results_site["exists"] = "illegal"
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

#Если нужен только статус кода, не загружать код страницы.
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

# запуск запрос в новом потоке, не блокирует основной поток.
            if proxy != None:
                proxies = {"http": proxy, "https": proxy}
                future = request_method(url=url_probe, headers=headers,
                                        proxies=proxies,
                                        allow_redirects=allow_redirects,
                                        timeout=timeout
                                        )
            else:
                future = request_method(url=url_probe, headers=headers,
                                        allow_redirects=allow_redirects,
                                        timeout=timeout
                                        )

# Сохранить future in data для последующего доступа.
            net_info["request_future"] = future

# Сброс идентифкатора Tor (при необходимости).
            if unique_tor:
                underlying_request.reset_identity()

# Добавлять результаты этого сайта в окончательный словарь со всеми другими результатами.
        results_total[social_network] = results_site

# Открыть файл, содержащий ссылки на аккаунт.
# Основная логика: если текущие запросов, сделайте их. Если многопоточные запросы, дождаться ответов.
    for social_network, net_info in site_data.items():

# Получить результаты снова.
        results_site = results_total.get(social_network)

# Получить другую информацию сайта снова.
        url = results_site.get("url_user")
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

        if error_type == "message":
            error = net_info.get("errorMsg")
# Проверяет, есть ли сообщение об ошибке в HTML.
            if not error in r.text:
                print_found(social_network, url, response_time, verbose, color)
                exists = "yes"
            else:
                if not print_found_only:
                    print_not_found(social_network, response_time, verbose, color)
                exists = "no"

        elif error_type == "status_code":
# Проверяет, является ли код состояния ответа 2..
            if not r.status_code >= 300 or r.status_code < 200:
                print_found(social_network, url, response_time, verbose, color)
                exists = "yes"
            else:
                if not print_found_only:
                    print_not_found(social_network, response_time, verbose, color)
                exists = "no"

        elif error_type == "response_url":

# Для этого метода обнаружения мы отключили перенаправление.
# Таким образом, нет необходимости проверять URL-адрес ответа: он всегда будет соответствовать запросу. 
# Вместо этого мы обеспечим, чтобы статус кода указывал, что запрос был успешным (тоесть не 404 или перенаправлен.
        
            if 200 <= r.status_code < 300:
                #
                print_found(social_network, url, response_time, verbose, color)
                exists = "yes"
            else:
                if not print_found_only:
                    print_not_found(social_network, response_time, verbose, color)
                exists = "no"

        elif error_type == "":
            if not print_found_only:
                print_invalid(social_network, "*Пропуск", color)
            exists = "error"

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
        timeout = float(value)
    except:
        raise ArgumentTypeError(f"Timeout '{value}' must be a number.")
    if timeout <= 0:
        raise ArgumentTypeError(f"Timeout '{value}' must be greater than 0.0s.")
    return timeout

# Обновление Snoop.
def update_snoop():
    upd = str(input("""Вы действительно хотите:
                    __             _  
   ._  _| _._|_ _  (_ ._  _  _ ._   ) 
|_||_)(_|(_| |_(/_ __)| |(_)(_)|_) o  
   |                           |    
нажмите 'y' """))
    if upd == "y":
        if sys.platform == 'win32':
            print(Fore.RED + "Функция обновления Snoop требует установки <Git> на OS Windows")
            os.startfile("update.bat")
        else:
            print(Fore.RED + "Функция обновления Snoop требует установки <Git> на OS GNU/Linux")
            os.system("./update.sh")

# Запрос лицензии.
def main():

    with open('COPYRIGHT', 'r', encoding="utf8") as copyright:
        cop = copyright.read()

    version_snoop = f"%(prog)s: {__version__}\n" +  \
                     f"{requests.__description__}:  {requests.__version__}\n" + \
                     f"Python:  {platform.python_version()}\n\n" + \
                     f"\033[37m{cop}\033[0m\n"


    with open('sites.md', 'r', encoding="utf8") as support:
        sup = support.read()
    sup_color = f"\033[37m{sup}\033[0m"

# Пожертование.
    donate = ("""
╭donate:
├──BTC_BHC: \033[37m1EXoQj1rd5oi54k9yynVLsR4kG61e4s8g3\033[0m
├──Яндекс.Деньги: \033[37m4100111364257544\033[0m  
└──PayPal: \033[37msnoopproject@protonmail.com\033[0m    
\nИсходный код: \033[37mhttps://github.com/snooppr/snoop\033[0m """)
              
                
                
# Назначение опций Snoop.
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                            description=f"{module_name} (Version {__version__})",
                            epilog=donate
                            )
    parser.add_argument("--donate Y",
                        action="store_true", dest="donation",
                        help="Пожертвовать на развитие Snoop project-а"
                        )
    parser.add_argument("--sort Y",
                        action="store_true", dest="sort",
                        help="Обновление/сортировка черного и белого списков (.json) сайтов БД Snoop"
                        )
    parser.add_argument("--version", "-V",
                        action="version",  version=(version_snoop),
                        help="Вывод на дисплей: версий Snoop, Python; Сублицензии"
                        )
    parser.add_argument("--verbose", "-v", "-d", "--debug",
                        action="store_true",  dest="verbose", default=False,
                        help="Вывод на дисплей отладочной информации и подробная её вербализация"
                        )
    parser.add_argument("--folderoutput", "-fo", dest="folderoutput",
                        help="Указать каталог отличный от стандартного, куда будут сохранены результаты поиска при разовом поиске нескольких имён"
                        )
    parser.add_argument("--output", "-o", dest="output",
                        help="Указать отличный от стандартного файл с сохранением результатов. По умолчанию файл для сохранения результатов — переменное username.txt"
                        )
    parser.add_argument("--tor", "-t",
                        action="store_true", dest="tor", default=False,
                        help="Делать запросы через Tor-службу; требуется чтобы Tor был установлен по системному стандартному пути и не модифицирован torrc")
    parser.add_argument("--unique-tor", "-u",
                        action="store_true", dest="unique_tor", default=False,
                        help="Делать запросы через Tor-службу с новой цепочкой Tor после каждого запроса; увеличивает время выполнения; требуется чтобы Tor был установлен по системному стандартному пути")
    parser.add_argument("--proxy", "-p", metavar='PROXY_URL',
                        action="store", dest="proxy", default=None,
                        help="Делать запросы через прокси, например, socks5://127.0.0.1:9070"
                        )
    parser.add_argument("--proxy_list", "-pl", metavar='PROXY_LIST',
                        action="store", dest="proxy_list", default=None,
                        help="Поиск 'username' через случайный прокси, указать file.csv с прокси"
                        )
    parser.add_argument("--check_proxies", "-cp", metavar='CHECK_PROXY',
                        action="store", dest="check_prox", default=None,
                        help="Связка с параметром '--proxy_list'. "
                             "Скрипт проверяет рабочие ли предоставленные прокси из file.csv, являются ли они анонимными. "
                             "Установите '0' для безлимитного количества успешно-проверенных прокси, установите > '1' для ограничения"
                        )
    parser.add_argument("--csv",
                        action="store_true",  dest="csv", default=False,
                        help="Сохранить файл в формате (nickname.CSV) с расширенным анализом"
                        )
    parser.add_argument("--json", "-j", metavar="JSON_FILE",
                        dest="json_file", default="data.json",
                        help="Указать для поиска 'username' другую БД сайтов в формате file.json"              )                        
    parser.add_argument("--site",
                        action="append", metavar='SITE_NAME',
                        dest="site_list",  default=None, 
                        help="Указать имя сайта из БД (data.json). Ограничение поиска 'username' до одного ресурса"
                        )
    parser.add_argument("--timeout",
                        action="store", metavar='--time 9',
                        dest="timeout", type=timeout_check, default=None,
                        help="Выделение макс.времени на ожидание ответа от сервера\n"
                             "Влияет на продолжительность поиска. Оптимальное значение при хорошем интернет соединении и нескольких 'упавших' сайтов = 9с."
                        )
    parser.add_argument("--print-found", 
                        action="store_true", dest="print_found_only", default=False,
                        help="Выводить на печать только найденные аккаунты"
                        )
    parser.add_argument("--no-func", "-n",
                        action="store_true", dest="no_color", default=False,
                        help="""✓Монохромный терминал, не использовать цвета в url\n
                                ✓Отключить звук\n
                                ✓Запретить открытие web browser-a"""
                        )
    parser.add_argument("username",
                        nargs='+', metavar='USERNAMES',
                        action="store",
                        help="Никнейм разыскиваемого пользователя, поддерживается несколько имён"
                        )
    parser.add_argument("--list all",
                        action="store_true", dest="listing",
                        help="Вывод на дисплей БД (БС+ЧС) поддерживаемых сайтов"
                        )
    parser.add_argument("--update Y",
                        action="store_true", dest="update",
                        help="Обновить Snoop"
                        )            

    args = parser.parse_args()

# Опция сортировки.
    if args.sort:
        if sys.platform == 'win32':
            subprocess.run(["python", "site_list.py"])
        else:
            subprocess.run(["python3", "site_list.py"])
        exit(0)

    if args.listing:
        listall = []
        with open('sites.md', "r", encoding="utf8") as listyes:
            for site in listyes.readlines():
                patch = (site.split(']')[0]).replace("[", "  ")
                listall.append(patch)
            print(Fore.GREEN + "++Белый список++", *listall, sep = "\n")

    if args.listing:
        listall_bad = []
        with open('bad_site.md', "r", encoding="utf8") as listbad:
            for site_bad in listbad.readlines():
                patch_bad = (site_bad.split(']')[0]).replace("[", "  ")
                listall_bad.append(patch_bad)
            print(Fore.RED + "\n\n--Чёрный список--", *listall_bad, sep = "\n")
        sys.exit(0)

# Опция донат.
    if args.donation:
        print(donate)
        webbrowser.open("https://yasobe.ru/na/snoop_project")
        print("Выход")
        sys.exit(0)

# Завершение обновления Snoop.
    if args.update:
        print("=======================")
        update_snoop()
        print("=======================\nВыход")
        sys.exit(0)
    
# Проверка остальных аргументов.
# Проверка регулярных выражений TODO на args.proxy.
    if args.tor and (args.proxy != None or args.proxy_list != None):
        raise Exception("Tor и Proxy не могут быть запущены одновременно.")

# Проверка аргументов прокси.
# Не обязательно генерировать ошибку, так как мы могли бы объединить один прокси с теми, которые были сгенерированы из .csv,
# но в настоящее время это кажется излишне сложным.
    if args.proxy != None and args.proxy_list != None:
        raise Exception("Один прокси не может использоваться вместе со списком прокси.")

# Делать подсказку.
    if args.proxy != None:
        print("Using the proxy: " + args.proxy)

    global proxy_list

    if args.proxy_list != None:
        print_info("Loading proxies from", args.proxy_list, not args.color)

        proxy_list = load_proxies_from_csv(args.proxy_list)

# Анонимность? Должны ли проки проверяться на анонимность.
    if args.check_prox != None and args.proxy_list != None:
        try:
            limit = int(args.check_prox)
            if limit == 0:
                proxy_list = check_proxy_list(proxy_list)
            elif limit > 0:
                proxy_list = check_proxy_list(proxy_list, limit)
            else:
                raise ValueError
        except ValueError:
            raise Exception("Parameter --check_proxies/-cp must be a positive integer.")

    if args.tor or args.unique_tor:
        print(Fore.RED + "Внимание запущена экспериментальная функция!'Snoop попытается работать через луковую сеть Tor'.\n\
Ваши запросы могут посылаться НЕ анонимно!\n\
Также многие сайты могут блокировать выходные_ноды_Tor, что приведёт к 'ошибкам соединения' на этих сайтах.")

# Проверка, введены ли оба метода вывода в качестве ввода.
    if args.output is not None and args.folderoutput is not None:
        print("Вы можете использовать только один метода выхода.")
        sys.exit(1)

# Проверка правильность вывода одного из имен username.
    if args.output is not None and len(args.username) != 1:
        print("Вы можете использовать данный флаг только с одним username")
        sys.exit(1)

    response_json_online = None
    site_data_all = None

# Попробовать загрузить JSON с веб-сайта.
    try:
        response_json_online = requests.get(url=args.json_file)
    except requests.exceptions.MissingSchema:  # В случае если Shema неверная (не может быть на сайте).
        pass

# Проверка на соответствие ответа.
    if response_json_online is not None and response_json_online.status_code == 200:
# Поскольку мы получили данные с веб-сайта, попробовать загрузить json и выйти, если синтаксический анализ завершился ошибкой.
        try:
            site_data_all = response_json_online.json()
        except ValueError:
            print("Invalid JSON website!")
            sys.exit(1)
            pass

    data_file_path = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), args.json_file)
# Этого не будет, если в запросе отсутствовала Shema.
    if site_data_all is None:
# Проверьте, существует ли файл, иначе выход.
        if not os.path.exists(data_file_path):
            print("JSON file не существует.")
            print(
                "Вы не добавили .json файл или убедитесь, что сделали запрос http:// или https://...")
            sys.exit(1)
        else:
            raw = open(data_file_path, "r", encoding="utf-8")
            try:
                site_data_all = json.load(raw)
            except:
                print("Invalid загружаемый JSON file.")

    if args.site_list is None:
# Не желательно смотреть на подмножество сайтов.
        site_data = site_data_all
    else:
# Пользователь желает выборочно запускать запросы к подмножеству списку сайтов.

# Убедится, что сайты поддерживаются, создать сокращенную базу данных сайта.
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
                f"Ошибка: желаемые сайты не найдены: {', '.join(site_missing)}.")
            sys.exit(1)


#Запись в txt.
    for username in args.username:
        print()
        
        if args.output:
            file = open(args.output, "w", encoding="utf-8")
        elif args.folderoutput:  
# В случае, если мы обрабатываем несколько имен пользователей в целевой папке. Если папка не существует, сначала создать её.
            if not os.path.isdir(args.folderoutput):
                os.mkdir(args.folderoutput)
            file = open(os.path.join(args.folderoutput,
                                     username + ".txt"), "w", encoding="utf-8")
        else:
            file = open("results/txt/" + username + ".txt", "w", encoding="utf-8")
            try:
                file = open("results/txt/" + username + ".txt", "w", encoding="utf-8")
            except (SyntaxError, ValueError):
                pass
# Попытаться объявить случайный 'proxy_list' в качестве прокси запроса.
# Если мы не можем получить доступ к списку или он пуст, мы используем 'args.proxy' в качестве прокси.
        try:
            random_proxy = random.choice(proxy_list)
            proxy = f'{random_proxy.protocol}://{random_proxy.ip}:{random_proxy.port}'
        except (NameError, IndexError):
            proxy = args.proxy

        results = snoop(username,
                           site_data,
                           verbose=args.verbose,
                           tor=args.tor,
                           unique_tor=args.unique_tor,
                           proxy=args.proxy,
                           print_found_only=args.print_found_only,
                           timeout=args.timeout,
                           color=not args.no_color)

        exists_counter = 0
        file.write("Адрес | ресурс" + "\n\n")
        for website_name in results:
            dictionary = results[website_name]
            if dictionary.get("exists") == "yes":
                exists_counter += 1
                file.write(dictionary ["url_user"] + " | " + (website_name)+"\n")
        file.write("\n" f"Запрашиваемый объект: <{username}> найден: {exists_counter} раз(а)")
        file.write("\n" f"Обновлено: " + time.ctime())      
        print(Fore.WHITE + "├─Результаты поиска:", "всего найдено —", exists_counter, "url")


#Запись в html.
        timefinish = time.time() - timestart
        file = open("results/html/" + username + ".html", "w", encoding="utf-8")

        try:
            file = open("results/html/" + username + ".html", "w", encoding="utf-8")
        except (SyntaxError, ValueError):
            pass
        file.write("<h1>" + "<a href='file://" + str(dirresults) + "/results/html/'>Главная</a>" + "</h1>")    
        file.write("<h3>" + "Snoop Project" + "</h3>" + "Объект" + " " + 
        "<b>" + (username) + "</b>" + " " + "найден на нижеперечисленных" + "<b> " + str(exists_counter) + 
        "</b> ресурсах: " + "<br><ol>")
        for website_name in results:
            dictionary = results[website_name]
            if dictionary.get("exists") == "yes":
                exists_counter += 0
                file.write("<li>" + "<a href='" + dictionary ["url_user"] + "'>"+ (website_name)+"</a>" + "</li>")
        file.write("</ol>Запрашиваемый объект < <b>" + str(username) + "</b> > найден: <b>" + str(exists_counter) + "</b> раз(а).")
        file.write("<br> Затраченное время на создание отчёта: " + "%.0f" % float(timefinish) + " c.")      
        file.write("<br> Обновлено: " + "<i>" + time.ctime() + "</i>")      
        file.write("<br><br><a href='https://github.com/snooppr/snoop'>Snoop/Исходный код</a>")      
        file.close()


        if args.csv == True:
            print(Fore.WHITE + "├───Положительные результаты сохранены в: " + Style.RESET_ALL +
            "~/snoop/results/*/" + str(username) + "[.txt.html]")
            print(Fore.WHITE + "├───Расширенный анализ:" +
            Fore.RED + "\033[5m <\033[0m" +
            Fore.GREEN + f"{username}" +
            Fore.RED + "\033[5m>\033[0m",           
            "сохранён в ~/snoop/results/csv/" + str(username) + ".csv")
        else:        
            print(Fore.WHITE + "├───Положительные результаты сохранены в: " + Style.RESET_ALL +
            "~/snoop/results/*/" + str(username) + "[.txt.html]")
        file.close()

#Запись в csv.
        if args.csv == True:
            with open("results/csv/" + username + ".csv", "w", newline='', encoding="utf-8") as csv_report:
                            
                writer = csv.writer(csv_report)
                writer.writerow(['Объект',
                                 'Ресурс',
                                 'url_main',
                                 'url_user',
                                 'статус',
                                 'статус_кода',
                                 'время/мс'
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
                writer.writerow("")
                writer.writerow(['Дата'])
                writer.writerow([time.ctime()])

# Открыть/нет браузер с результатами поиска.
    if args.no_color==False:
        if exists_counter >= 1:
            webbrowser.open(str("file://" + str(dirresults) + "/results/html/" + str(username) + ".html"))
# Музыка.
        playsound('end.wav')

if __name__ == "__main__":
    main()

# Финишный вывод.
print(Fore.WHITE + "└────╼Дата выполнения этого поискового запроса:", time.ctime())
print("\n\033[37m\033[44m{}".format("Сублицензия: авторская"))

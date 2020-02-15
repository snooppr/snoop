#! /usr/bin/env python3

print ("""
  ___|                          
\___ \  __ \   _ \   _ \  __ \  
      | |   | (   | (   | |   | 
_____/ _|  _|\___/ \___/  .__/  
                         _|     \033[37mv1.\033[34m0.1\033[31m_rus\033[0m\n
""")

print ("#Пример:\n cd ~/snoop\n python3 snoop.py -h \033[37m#справка по всем функциям ПО\033[0m\n python3 snoop.py --time 9 user \033[37m#поиск user-a, ожидание ответа от сайта ≤ 9с.\033[0m\n nano user.txt\n")

import datetime
import csv  
import subprocess
import webbrowser
import json
import os
import platform
import re
import sys
import random
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from concurrent.futures import ThreadPoolExecutor
from time import time

import requests
from colorama import Fore, Style, init

from requests_futures.sessions import FuturesSession
from torrequest import TorRequest
from load_proxies import load_proxies_from_csv, check_proxy_list

module_name = "Snoop: поиск никнейма по всем фронтам!"
__version__ = "1.0.1_rus"

date = datetime.datetime.today()

global proxy_list

proxy_list = []

class ElapsedFuturesSession(FuturesSession):
    """
    Расширяет 'FutureSession' для добавления метрики времени ответа к каждому запросу.

    https://github.com/ross/requests-futures#working-in-the-background
    """

    def request(self, method, url, hooks={}, *args, **kwargs):
        start = time()

        def timing(r, *args, **kwargs):
            elapsed_sec = time() - start
            r.elapsed = round(elapsed_sec * 1000)

        try:
            if isinstance(hooks['response'], (list, tuple)):
                # needs to be first so we don't time other hooks execution
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

    # In case our proxy fails, we retry with another proxy.
    except requests.exceptions.ProxyError as errp:
        if retry_no>0 and len(proxy_list)>0:
            #Selecting the new proxy.
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
        url_main:      URL основного сайта.
        url_user:      URL ведущий на пользователя (если такой аккаунт найден).
        exists:        Указание результатов теста на наличие аккаунта.
        http_status:   HTTP status code ответа сайта.
        response_text: Текст, который вернулся запрос-ответ от сайта (при ошибке соединения может отсутствовать)
    """

    print_info("разыскиваем:", username, color)

    # Create session based on request methodology
    if tor or unique_tor:
        #Requests using Tor obfuscation
        underlying_request = TorRequest()
        underlying_session = underlying_request.session
    else:
        #Normal requests
        underlying_session = requests.session()
        underlying_request = requests.Request()

    #Limit number of workers to 20.
    #This is probably vastly overkill.
    if len(site_data) >= 20:
        max_workers=20
    else:
        max_workers=len(site_data)

    #Create multi-threaded session for all requests.
    session = ElapsedFuturesSession(max_workers=max_workers,
                                    session=underlying_session)

    # Results from analysis of all sites
    results_total = {}

    # First create futures for all requests. This allows for the requests to run in parallel
    for social_network, net_info in site_data.items():

        # Results from analysis of this specific site
        results_site = {}

        # Record URL of main site
        results_site['url_main'] = net_info.get("urlMain")

        # A user agent is needed because some sites don't return the correct
        # information since they think that we are bots (Which we actually are...)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }

        if "headers" in net_info:
            # Override/append any extra headers required by a given site.
            headers.update(net_info["headers"])

        # Don't make request if username is invalid for the site
        regex_check = net_info.get("regexCheck")
        if regex_check and re.search(regex_check, username) is None:
            # No need to do the check at the site: this user name is not allowed.
            if not print_found_only:
                print_invalid(social_network, "Недопустимый формат имени для данного сайта", color)

            results_site["exists"] = "illegal"
            results_site["url_user"] = ""
            results_site['http_status'] = ""
            results_site['response_text'] = ""
            results_site['response_time_ms'] = ""
        else:
            # URL of user on site (if it exists)
            url = net_info["url"].format(username)
            results_site["url_user"] = url
            url_probe = net_info.get("urlProbe")
            if url_probe is None:
                # Probe URL is normal one seen by people out on the web.
                url_probe = url
            else:
                # There is a special URL for probing existence separate
                # from where the user profile normally can be found.
                url_probe = url_probe.format(username)

            #If only the status_code is needed don't download the body
            if net_info["errorType"] == 'status_code':
                request_method = session.head
            else:
                request_method = session.get

            if net_info["errorType"] == "response_url":
                # Site forwards request to a different URL if username not
                # found.  Disallow the redirect so we can capture the
                # http status from the original URL request.
                allow_redirects = False
            else:
                # Allow whatever redirect that the site wants to do.
                # The final result of the request will be what is available.
                allow_redirects = True

            # This future starts running the request in a new thread, doesn't block the main thread
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

            # Store future in data for access later
            net_info["request_future"] = future

            # Reset identify for tor (if needed)
            if unique_tor:
                underlying_request.reset_identity()

        # Add this site's results into final dictionary with all of the other results.
        results_total[social_network] = results_site

    # Open the file containing account links
    # Core logic: If tor requests, make them here. If multi-threaded requests, wait for responses
    for social_network, net_info in site_data.items():

        # Retrieve results again
        results_site = results_total.get(social_network)

        # Retrieve other site information again
        url = results_site.get("url_user")
        exists = results_site.get("exists")
        if exists is not None:
            # We have already determined the user doesn't exist here
            continue

        # Get the expected error type
        error_type = net_info["errorType"]

        # Default data in case there are any failures in doing a request.
        http_status = "?"
        response_text = ""

        # Retrieve future and ensure it has finished
        future = net_info["request_future"]
        r, error_type, response_time = get_response(request_future=future,
                                                    error_type=error_type,
                                                    social_network=social_network,
                                                    verbose=verbose,
                                                    retry_no=3,
                                                    color=color)

        # Attempt to get request information
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
            # Checks if the error message is in the HTML
            if not error in r.text:
                print_found(social_network, url, response_time, verbose, color)
                exists = "yes"
            else:
                if not print_found_only:
                    print_not_found(social_network, response_time, verbose, color)
                exists = "no"

        elif error_type == "status_code":
            # Checks if the status code of the response is 2XX
            if not r.status_code >= 300 or r.status_code < 200:
                print_found(social_network, url, response_time, verbose, color)
                exists = "yes"
            else:
                if not print_found_only:
                    print_not_found(social_network, response_time, verbose, color)
                exists = "no"

        elif error_type == "response_url":
            # For this detection method, we have turned off the redirect.
            # So, there is no need to check the response URL: it will always
            # match the request.  Instead, we will ensure that the response
            # code indicates that the request was successful (i.e. no 404, or
            # forward to some odd redirect).
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

        # Save exists flag
        results_site['exists'] = exists

        # Save results from request
        results_site['http_status'] = http_status
        results_site['response_text'] = response_text
        results_site['response_time_ms'] = response_time

        # Add this site's results into final dictionary with all of the other results.
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

#Обновление Snoop
def update_snoop():
    upd = str(input("""Вы действительно хотите: 
                    __             _  
   ._  _| _._|_ _  (_ ._  _  _ ._   ) 
|_||_)(_|(_| |_(/_ __)| |(_)(_)|_) o  
   |                           |    
нажмите 'y' """))
    if upd == "y":
        os.system("./update.sh")

               
def main():
    # Colorama module's initialization.
    init(autoreset=True)
    
    with open('COPYRIGHT', 'r') as copyright:
        cop = copyright.read()

    version_snoop = f"%(prog)s: {__version__}\n" +  \
                     f"{requests.__description__}:  {requests.__version__}\n" + \
                     f"Python:  {platform.python_version()}\n\n" + \
                     f"\033[37m{cop}\033[0m\n"


    with open('sites.md', 'r') as support:
        sup = support.read()
    sup_color = f"\033[37m{sup}\033[0m"
    
    donate = ("""
╭donate:
├──BTC_BHC: \033[37m1EXoQj1rd5oi54k9yynVLsR4kG61e4s8g3\033[0m
├──Яндекс.Деньги: \033[37m4100111364257544\033[0m  
└──PayPal: \033[37msnoopproject@protonmail.com\033[0m    
\nИсходный код: \033[37mhttps://github.com/snooppr/snoop\033[0m                """)
              
                
                
                
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
   # parser.add_argument("--rank", "-r",
    #                    action="store_true", dest="rank", default=False,
     #                   help="Результаты поиска сортируются не по алфавиту, а по полуярности рейтинга Alexa #опция временно отключена")
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
    parser.add_argument("--no-color",
                        action="store_true", dest="no_color", default=False,
                        help="Монохромный терминал, не использовать цвета в url"
                        )                        
    parser.add_argument("username",
                        nargs='+', metavar='USERNAMES',
                        action="store",
                        help="Никнейм разыскиваемого пользователя, поддерживается несколько имён"
                        )
    parser.add_argument("--list all", 
                        action="store_true", dest="listing",
                        help="Вывод на дисплей БД поддерживаемых сайтов"
                        )                        
    parser.add_argument("--update Y",
                        action="store_true", dest="update", 
                        help="Обновить Snoop"
                        )            

    args = parser.parse_args()
    
    if args.sort: 
        subprocess.run(["python3", "site_list.py"])
        exit(0)
    
    if args.listing:
        listall = []
        with open('sites.md') as listyes:
            for site in listyes.readlines():
                patch = (site.split(']')[0]).replace("[", "  ") 
                listall.append(patch)
            print(Fore.GREEN + "++Белый список++", *listall, sep = "\n")    

    if args.listing:
        listall_bad = []                
        with open('bad_site.md') as listbad:
            for site_bad in listbad.readlines():
                patch_bad = (site_bad.split(']')[0]).replace("[", "  ") 
                listall_bad.append(patch_bad)
            print(Fore.RED + "\n\n--Чёрный список--", *listall_bad, sep = "\n")                    
        sys.exit(0)                                        
        
    if args.donation:
        print(donate)
        webbrowser.open("https://yasobe.ru/na/snoop_project")
        print("Выход")
        sys.exit(0)
          
    if args.update:
        print("=======================")
        update_snoop() 
        print("=======================\nВыход")
        sys.exit(0)
    
    # Argument check
    # TODO regex check on args.proxy
    if args.tor and (args.proxy != None or args.proxy_list != None):
        raise Exception("Tor и Proxy не могут быть запущены одновременно.")

    # Proxy argument check.
    # Does not necessarily need to throw an error,
    # since we could join the single proxy with the ones generated from the .csv,
    # but it seems unnecessarily complex at this time.
    if args.proxy != None and args.proxy_list != None:
        raise Exception("Один прокси не может использоваться вместе со списком прокси.")

    # Make prompts
    if args.proxy != None:
        print("Using the proxy: " + args.proxy)

    global proxy_list

    if args.proxy_list != None:
        print_info("Loading proxies from", args.proxy_list, not args.color)

        proxy_list = load_proxies_from_csv(args.proxy_list)

    # Checking if proxies should be checked for anonymity.
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
        print("\033[31mВнимание запущена экспериментальная функция! 'Snoop попытается работать через луковую сеть Tor'.\nВаши запросы могут посылаться НЕ анонимно!\033[0m\nТакже многие сайты могут блокировать выходные_ноды_Tor, что приведёт к 'ошибкам соединения' на этих сайтах.")

    # Check if both output methods are entered as input.
    if args.output is not None and args.folderoutput is not None:
        print("Вы можете использовать только один метода выхода.")
        sys.exit(1)

    # Check validity for single username output.
    if args.output is not None and len(args.username) != 1:
        print("Вы можете использовать флаг --output только с одним username")
        sys.exit(1)

    response_json_online = None
    site_data_all = None

    # Try to load json from website.
    try:
        response_json_online = requests.get(url=args.json_file)
    except requests.exceptions.MissingSchema:  # In case the schema is wrong it's because it may not be a website
        pass

    # Check if the response is appropriate.
    if response_json_online is not None and response_json_online.status_code == 200:
        # Since we got data from a website, try to load json and exit if parsing fails.
        try:
            site_data_all = response_json_online.json()
        except ValueError:
            print("Invalid JSON website!")
            sys.exit(1)
            pass

    data_file_path = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), args.json_file)
    # This will be none if the request had a missing schema
    if site_data_all is None:
        # Check if the file exists otherwise exit.
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
        # Not desired to look at a sub-set of sites
        site_data = site_data_all
    else:
        # User desires to selectively run queries on a sub-set of the site list.

        # Make sure that the sites are supported & build up pruned site database.
        site_data = {}
        site_missing = []
        for site in args.site_list:
            for existing_site in site_data_all:
                if site.lower() == existing_site.lower():
                    site_data[existing_site] = site_data_all[existing_site]
            if not site_data:
                # Build up list of sites not supported for future error message.
                site_missing.append(f"'{site}'")

        if site_missing:
            print(
                f"Ошибка: желаемые сайты не найдены: {', '.join(site_missing)}.")
            sys.exit(1)

#rak опция временно отключена
    #if args.rank:
        # Sort data by rank
        #site_dataCpy = dict(site_data)
        #ranked_sites = sorted(site_data, key=lambda k: ("rank" not in k, site_data[k].get("rank", sys.maxsize)))
        #site_data = {}
        #for site in ranked_sites:
            #site_data[site] = site_dataCpy.get(site)

    # Run report on all specified users.
    for username in args.username:
        print()

        if args.output:
            file = open(args.output, "w", encoding="utf-8")
        elif args.folderoutput:  # In case we handle multiple usernames at a targetted folder.
            # If the folder doesnt exist, create it first
            if not os.path.isdir(args.folderoutput):
                os.mkdir(args.folderoutput)
            file = open(os.path.join(args.folderoutput,
                                     username + ".txt"), "w", encoding="utf-8")
        else:
            file = open(username + ".txt", "w", encoding="utf-8")

        # We try to ad a random member of the 'proxy_list' var as the proxy of the request.
        # If we can't access the list or it is empty, we proceed with args.proxy as the proxy.
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
        for website_name in results:
            dictionary = results[website_name]
            if dictionary.get("exists") == "yes":
                exists_counter += 1
                file.write(dictionary["url_user"] + "\n")
        file.write("\n" f"Запрашиваемый объект: <")
        file.write(username)
        file.write(f"> найден: {exists_counter} раз(а)")
        file.write("\n" f"Обновлено: ")      
        file.write(date.strftime("%d/%m/%Yг. в %Hч.%Mм.%Sс."))   
        print(Fore.WHITE + "├─Результаты поиска:", "всего найдено —", exists_counter, "url")
        file.close()

        if args.csv == True:
            with open(username + ".csv", "w", newline='', encoding="utf-8") as csv_report:
                writer = csv.writer(csv_report)
                writer.writerow(['username',
                                 'name',
                                 'url_main',
                                 'url_user',
                                 'exists',
                                 'http_status',
                                 'response_time_ms'
                                 ]
                                )
                for site in results:
                    writer.writerow([username,
                                     site,
                                     results[site]['url_main'],
                                     results[site]['url_user'],
                                     results[site]['exists'],
                                     results[site]['http_status'],
                                     results[site]['response_time_ms']
                                     ]
                                    )


if __name__ == "__main__":
    main()
    

print(Fore.WHITE + "└──╼Дата выполнения этого поискового запроса:", 
date.strftime("%d/%m/%Yг. в %Hч.%Mм.%Sс.\n"))   
print("\033[37m\033[44m{}".format("Сублицензия: The MIT License"))




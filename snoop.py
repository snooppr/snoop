#! /usr/bin/env python3
# Copyright (c) 2020 Snoop Project <snoopproject@protonmail.com>

import argparse
import certifi
import csv
import glob
import itertools
import json
import locale
import os
import platform
import psutil
import random
import re
import requests
import shutil
import signal
import ssl
import subprocess
import sys
import textwrap
import time
import webbrowser

from charset_normalizer import detect as char_detect
from collections import Counter
from colorama import Fore, init, Style
from concurrent.futures import as_completed, ProcessPoolExecutor, ThreadPoolExecutor, TimeoutError
from multiprocessing import active_children
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TimeElapsedColumn
from rich.style import Style as STL
from rich.table import Table

import snoopbanner
import snoopnetworktest
import snoopplugins

if int(platform.python_version_tuple()[1]) >= 8:
    from importlib.metadata import version as version_lib
    PYTHON_3_8_PLUS = True
else:
    PYTHON_3_8_PLUS = False


locale.setlocale(locale.LC_ALL, '')
init(autoreset=True)
console = Console()


## Баннер и версия ПО.
def version_snoop(vers, vers_code, demo_full):
    print(f"""\033[36m
  ___|
\\___ \\  __ \\   _ \\   _ \\  __ \\ 
      | |   | (   | (   | |   | 
_____/ _|  _|\\___/ \\___/  .__/  
                         _|    \033[0m \033[37m\033[44m{vers}\033[0m
""")

    sb = "build" if vers_code == 'b' else "source"
    _sb = "demo" if demo_full == 'd' else "full"

    if WINDOWS: OS_ = f"ru Snoop for Windows {sb} {_sb}"
    elif ANDROID: OS_ = f"ru Snoop for Termux {sb} {_sb}"
    elif LINUX: OS_ = f"ru Snoop for GNU/Linux {sb} {_sb}"

    console.print("[dim cyan]Примеры:[dim cyan]")
    console.print(f"[dim cyan] $ [/dim cyan]" + \
                  f"[cyan]{'cd C:' + chr(92) + 'path' + chr(92) + 'snoop' if WINDOWS else 'cd ~/snoop'}[/cyan]")
    console.print(f"[dim cyan] $ [/dim cyan][cyan]{'python' if WINDOWS else 'python3'} snoop.py --help[/cyan] #справка")
    console.print(f"[dim cyan] $ [/dim cyan][cyan]{'python' if WINDOWS else 'python3'} snoop.py --module[/cyan] #плагины")
    console.print(f"[dim cyan] $ [/dim cyan][cyan]{'python' if WINDOWS else 'python3'} snoop.py nickname[/cyan] #поиск user-a")
    console.rule(characters="=", style="cyan")
    print("")

    return f"{vers}_{OS_}"


## Создание директорий результатов.
def mkdir_path():
    if WINDOWS:
        dirhome = os.environ['LOCALAPPDATA'] + "\\snoop"
    elif ANDROID:
        try:
            dirhome = "/data/data/com.termux/files/home/storage/shared/snoop"
        except Exception:
            dirhome = os.environ['HOME'] + "/snoop"
    elif LINUX:
        dirhome = os.environ['HOME'] + "/snoop"

    dirpath = os.getcwd() if 'source' in VERSION and not ANDROID else dirhome

    os.makedirs(f"{dirpath}/results", exist_ok=True)
    os.makedirs(f"{dirpath}/results/nicknames/html", exist_ok=True)
    os.makedirs(f"{dirpath}/results/nicknames/txt", exist_ok=True)
    os.makedirs(f"{dirpath}/results/nicknames/csv", exist_ok=True)
    os.makedirs(f"{dirpath}/results/nicknames/save reports", exist_ok=True)
    os.makedirs(f"{dirpath}/results/plugins/ReverseVgeocoder", exist_ok=True)
    os.makedirs(f"{dirpath}/results/plugins/Yandex_parser", exist_ok=True)
    os.makedirs(f"{dirpath}/results/plugins/domain", exist_ok=True)

    return dirpath


# Константы.
ANDROID = True if hasattr(sys, 'getandroidapilevel') else False
WINDOWS = True if sys.platform == 'win32' else False
LINUX = True if ANDROID is False and WINDOWS is False else False

E_MAIL = 'demo: snoopproject@protonmail.com'
END_OF_LICENSE = (2025, 9, 10, 3, 0, 0, 0, 0, 0) #формат даты согласно международному стандарту ISO 8601, год-месяц-день.
VERSION = version_snoop('v1.4.1h', "s", "d")
DIRPATH = mkdir_path()
TIME_START = time.time()
TIME_DATE = time.localtime()


dic_binding = {"symbol_bad": re.compile("[^a-zA-Zа-яА-Я\\_\\s\\d\\%\\@\\-\\.\\+]"),
               "badraw": [], "badzone": [],
               "censors": 0, "android_lame_workhorse": False}


# Создание web-каталога и его контроль, но не файлов внутри + раздача верных прав "-x -R" после компиляции двоичных данных [.mp3].
def web_path_copy():
    try:
        if "build" in VERSION and os.path.exists(f"{DIRPATH}/web") is False:
            shutil.copytree(web_path, f"{DIRPATH}/web")
            if LINUX: # и 'build' in 'VERSION'
                os.chmod(f"{DIRPATH}/web", 0o755)
                for total_file_path in glob.iglob(f"{DIRPATH}/web/**/*", recursive=True):
                    if os.path.isfile(total_file_path) == True:
                        os.chmod(total_file_path, 0o644)
                    else:
                        os.chmod(total_file_path, 0o755)
        elif "source" in VERSION and ANDROID and os.path.exists("/data/data/com.termux/files/home/storage/shared/snoop/web") is False:
            shutil.copytree(f"{os.getcwd()}/web", "/data/data/com.termux/files/home/storage/shared/snoop/web")
    except Exception as e:
        print(f"ERR: {e}")


# Действие лицензии.
def license():
    date_up = int(time.mktime(END_OF_LICENSE))  #дата в секундах с начала эпохи
    End = time.strftime('%Y-%m-%d', time.gmtime(date_up))

    if time.time() > date_up:
        snoopbanner.logo(text=f"ПО {VERSION} деактивировано согласно лицензии.")
        sys.exit()

    return End


## Расход памяти.
def mem_test():
    try:
        return round(psutil.virtual_memory().available / 1024 / 1024)
    except Exception:
        if not WINDOWS:
            console.print(f"{' ' * 17} [bold red]ERR Psutil lib[/bold red]")
            return int(subprocess.check_output("free -m", shell=True, text=True).splitlines()[1].split()[-1])
        else:
            return -1


## Вывести на печать инфостроку.
def info_str(infostr, nick, color=True):
    if color is True:
        print(f"{Fore.GREEN}[{Fore.YELLOW}*{Fore.GREEN}] {infostr}{Fore.RED} <{Fore.WHITE} {nick} {Fore.RED}>{Style.RESET_ALL}")
    else:
        print(f"\n[*] {infostr} < {nick} >")


## Bad_raw, bad_zone.
def bad_raw(flagBS_err, bad_zone, nick, lst_options):
    print(f"{Fore.CYAN}├───Дата поиска:{Style.RESET_ALL} {time.strftime('%Y-%m-%d__%H:%M:%S', TIME_DATE)}")

    if any(lst_options):
        print(f"{Fore.CYAN}└────\033[31;1mBad_raw: {flagBS_err}% БД, bad_zone {bad_zone}\033[0m\n")
    else:
        if 4 >= flagBS_err >= 2:
            print(f"{Fore.CYAN}└────\033[33;1mВнимание! Bad_raw: {flagBS_err}% БД, bad_zone {bad_zone}\033[0m")
        elif 12 >= flagBS_err > 4:
            print(f"{Fore.CYAN}└────\033[31;1mВнимание!! Bad_raw: {flagBS_err}% БД, bad_zone {bad_zone}\033[0m")
        elif flagBS_err > 12:
            print(f"{Fore.CYAN}└────\033[30m\033[41mВнимание!!! Bad_raw: {flagBS_err}% БД, критический уровень, " + \
                  f"bad_zone {bad_zone}\033[0m")

    if not any(lst_options):
        print(Fore.CYAN + "     └─нестабильное соединение или I_Censorship")
        print(f"       \033[36m{'├' if 'full' in VERSION else '└'}─используйте \033[36;1mVPN\033[0m\033[36m/'\033[0m" + \
              f"\033[36;1m--web-base\033[0m\033[36m'\033[0m ", end='' if 'full' in VERSION else '\n\n')
        if "full" in VERSION:
            nick = f"'{nick}'" if nick.count(" ") > 0 else nick
            print(f"\033[36m\n       └─или исключите из поиска bad_zone: '\033[36;1m" + \
                  f"{bad_zone.split('/')[0].replace('~', '')}\033[0m" + \
                  f"\033[36m'\n         └─$ {os.path.basename(sys.argv[0])} --exclude " + \
                  f"{bad_zone.split('/')[0].replace('~', '')} {nick}\033[0m\n")


## Форматирование, отступы.
def format_txt(text, k=False, m=False):
    gal = " • " if WINDOWS else " ✔ "
    indent_end = "" if k else " " * 3
    gal = gal if k and not m else ""

    try:
        return textwrap.fill(f"{gal}{text}", width=os.get_terminal_size()[0], subsequent_indent=" " * 3, initial_indent=indent_end)
    except OSError:
        return "ERR"


## Вывести на печать ошибки.
def print_error(websites_names, errstr, country_code, errX, verbose=False, color=True):
    """Вывести на печать разного рода ошибки сети."""
    if color is True:
        print(f"{Style.RESET_ALL}{Fore.RED}[{Style.BRIGHT}{Fore.RED}-{Style.RESET_ALL}{Fore.RED}]{Style.BRIGHT}" \
              f"{Fore.GREEN} {websites_names}: {Style.BRIGHT}{Fore.RED}{errstr}{country_code}" \
              f"{Fore.YELLOW} {errX if verbose else ''} {Style.RESET_ALL}")
    else:
        print(f"[!] {websites_names}: {errstr}{country_code} {errX if verbose else ''}")


## Вывод на печать на разных платформах, индикация.
def print_found_country(websites_names, url, country_Emoj_Code, verbose=False, color=True):
    """Вывести на печать аккаунт найден."""
    if color is True and WINDOWS:
        print(f"{Style.RESET_ALL}{Style.BRIGHT}{Fore.CYAN}{country_Emoj_Code}" \
              f"{Fore.GREEN}  {websites_names}:{Style.RESET_ALL}{Fore.GREEN} {url}{Style.RESET_ALL}")
    elif color is True and not WINDOWS:
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


## Вывести на печать пропуск сайтов по блок. маске в имени username, gray_list.
def print_invalid(websites_names, message, color=True):
    if color is True:
        return f"{Style.RESET_ALL}{Fore.RED}[{Style.BRIGHT}{Fore.RED}-{Style.RESET_ALL}{Fore.RED}]" \
               f"{Style.BRIGHT}{Fore.GREEN} {websites_names}: {Style.RESET_ALL}{Fore.YELLOW}{message}{Style.RESET_ALL}\n"
    else:
        return f"[-] {websites_names}: {message}\n"


## Вывести предупреждение об устаревших версиях библиотек.
def warning_lib():
    if int(requests.urllib3.__version__.split(".")[0]) < 2 or int("".join(requests.__version__.split("."))) < 2282:
        console.log("[yellow]Внимание! \n\nВ Requests > v2.28.2 / Urllib3 v2 разработчики отказались от поддержки старых шифров. " + \
                    "Некоторые, немногочисленные, устаревшие сайты из БД, работающие по старой технологии, будут продолжать " + \
                    "коннектиться без ошибок (Snoop будет стремиться обеспечивать режим совместимости с любыми старыми версиями " + \
                    "Requests / Urllib3).[/yellow]\n\n[bold green]Все же рекомендуется обновить зависимости: \n" + \
                    "$ python -m pip install requests urllib3 -U[/bold green]", highlight=False)
        console.rule(characters="=", style="cyan")


## Сеть.
def r_session(cert=False, connect=0, speed=False, norm = False, method="get",
              url=None, headers="", allow_redirects=True, timeout=9):
    """
    Объект сессии нужен для расширения пула сетевых соединений, существенный минус (многопоточноть/OS Windows):
    с течением времени происходит утечка процессорного времени. Обходное решение: создавать временную сессию
    на каждое соединение без кэширования, прирост производительности (Windows) ~25-30%.
    Кроме того, в версии urllib3 > 2 при multiprocessing (Linux) необходимо вручную мариновать объект SSL.
    """

    if speed:
        connections = (speed + 20) if speed >= 60 else (70 if not WINDOWS else 50)
    elif speed is False:
        connections = 200 if LINUX else (70 if WINDOWS else 40) #L/W/A.

    if "test" in VERSION:
        total = False if norm else None
        retry = requests.urllib3.util.Retry(total=total, connect=connect, read=0, status=0, other=1, backoff_factor=0.1)
        adapter = requests.adapters.HTTPAdapter(max_retries=retry)
    else:
        adapter = requests.adapters.HTTPAdapter()

    try: #urllib3 > 2
        cert_reqs = ssl.CERT_NONE if cert is False else ssl.CERT_REQUIRED
        ciphers = 'ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:ECDH+AESGCM:DH+AESGCM\
                   :ECDH+AES:DH+AES:RSA+AESGCM:RSA+AES:!aNULL:!eNULL:!MD5:!DSS:HIGH:!DH'
        ctx = requests.urllib3.util.create_urllib3_context(ciphers=ciphers, cert_reqs=cert_reqs)
        adapter.init_poolmanager(connections=connections, maxsize=40 if ANDROID else 20, block=False,
                                 ssl_minimum_version=ssl.TLSVersion.TLSv1, ssl_context=ctx)
    except Exception: #urllib3 < 2, перенастраивать процессы не требуется
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
        adapter.init_poolmanager(connections=connections, maxsize=20, block=False)

    requests.packages.urllib3.disable_warnings()
    r_session = requests.Session()
    r_session.max_redirects = 6 if ANDROID else 9
    r_session.verify = False if cert is False else certifi.where()
    r_session.mount('http://', adapter)
    r_session.mount('https://', adapter)

    if method == "get":
        req_session = r_session.get
    elif method == "head":
        req_session = r_session.head

    return req_session(url=url, headers=headers, allow_redirects=allow_redirects, timeout=timeout)


# Вернуть результат future for2.
# Логика: возврат ответа и дублирующего метода (из 4-х) в случае успеха/повтора.
def r_results(request_future, error_type, websites_names, timeout=None, norm=False,
              print_found_only=False, verbose=False, color=True, country_code=''):
    try:
        res = request_future.result(timeout=timeout + 10)
        if res.status_code:
            return res, error_type, str(round(res.elapsed.total_seconds(), 2))
    except requests.exceptions.HTTPError as err1:
        if norm is False and print_found_only is False:
            print_error(websites_names, "HTTP Error ", country_code, err1, verbose, color)
    except requests.exceptions.ConnectionError as err2:
        if norm is False and ('aborted' in str(err2) or 'None: None' in str(err2) or
                              'SSLZeroReturnError' in str(err2) or 'Failed' in str(err2) or 'None' == str(err2)):
            dic_binding.update({'censors': dic_binding.get('censors') + 1})
            if print_found_only is False:
                print_error(websites_names, "Ошибка соединения ", country_code, err2, verbose, color)
            return "FakeNone", "", "-"
        else:
            if norm is False and print_found_only is False:
                print_error(websites_names, "Censorship | TLS ", country_code, err2, verbose, color)
    except (requests.exceptions.Timeout, TimeoutError) as err3:
        if norm is False and print_found_only is False:
            print_error(websites_names, "Timeout ошибка ", country_code, err3, verbose, color)
        if len(str(repr(err3))) == 14:
            dic_binding.update({'censors': dic_binding.get('censors') + 1})
            return "FakeStuck", "", "-"
    except requests.exceptions.RequestException as err4:
        if norm is False and print_found_only is False:
            print_error(websites_names, "Непредвиденная ошибка ", country_code, err4, verbose, color)
    except Exception as err5:
        if norm is False and print_found_only is False:
            print_error(websites_names, "Network Pool Crash ", country_code, err5, verbose, color)

    dic_binding.update({'censors': dic_binding.get('censors') + 1})

    return None, "Great Snoop returns None", "-"


## Сохранение отчетов, опция (-S).
def new_session(url, headers, error_type, username, websites_names, r, t):
    """
    Если nickname найден, но актуальная html-страница находится дальше по редиректу,
    поднимаем новое соединение и двигаемся по редиректу чтобы ее захватить и сохранить.
    """

    response = r_session(url=url, headers=headers, allow_redirects=True, timeout=t)

# Ловушка на некот.сайтах (if response.content is not None ≠ if response.content).
    if response.content is not None and response.encoding == 'ISO-8859-1':
        try:
            response.encoding = char_detect(response.content).get("encoding")
            if response.encoding is None:
                response.encoding = "utf-8"
        except Exception:
            response.encoding = "utf-8"

    try:
        session_size = len(response.content)  #подсчет извлеченных данных
    except UnicodeEncodeError:
        session_size = None
    return response, session_size

def sreports(url, headers, error_type, username, websites_names, r):
    os.makedirs(f"{DIRPATH}/results/nicknames/save reports/{username}", exist_ok=True)
# Сохранять отчеты для метода: redirection.
    if error_type == "redirection":
        try:
            response, session_size = new_session(url, headers, error_type,
                                                 username, websites_names, r, t=6)
        except requests.exceptions.ConnectionError:
            time.sleep(0.02)
            try:
                response, session_size = new_session(url, error_type, username,
                                                     websites_names, r, headers="", t=3)
            except Exception:
                session_size = 'Err'  #подсчет извлеченных данных
        except Exception:
            session_size = 'Err'
# Сохранять отчеты для всех остальных методов: status; response; message со стандартными параметрами.
    try:
        with open(f"{DIRPATH}/results/nicknames/save reports/{username}/{websites_names}.html", 'w', encoding=r.encoding) as rep:
            if 'response' in locals():
                rep.write(response.text)
            elif error_type == "redirection" and 'response' not in locals():
                rep.write("❌ Snoop Project bad_save, timeout")
            else:
                rep.write(r.text)
    except Exception:
        console.log(snoopbanner.err_all(err_="low"), f"\nlog --> [{websites_names}:[bold red] {r.encoding} | response?[/bold red]]")

    if error_type == "redirection":
        return session_size


## Snoop функция.
def snoop(username, BDdemo_new, verbose=False, norm=False, reports=False, user=False, country=False,
          speed=False, print_found_only=False, timeout=None, color=True, cert=False, header_custom=None):
## Печать инфострок.
    еasteregg = ['Snoop', 'snoop', 'SNOOP',
                 'Snoop Project', 'snoop project', 'SNOOP PROJECT',
                 'Snoop_Project', 'snoop_project', 'SNOOP_PROJECT',
                 'Snoop-Project', 'snoop-project', 'SNOOP-PROJECT',
                 'Snooppr', 'snooppr', 'SNOOPPR']

    nick = username.replace("%20", " ")  #username 2-переменные (args/info)
    info_str("разыскиваем:", nick, color)

    if len(username) < 3:
        print(Style.BRIGHT + Fore.RED + format_txt("⛔️ nickname не может быть короче 3-х символов",
                                                   k=True, m=True) + "\n   пропуск\n")
        return False, False, nick
    elif username in еasteregg:
        with console.status("[bold blue] 💡 Обнаружена пасхалка...", spinner='noise'):
            try:
                r_east = r_session(url="https://raw.githubusercontent.com/snooppr/snoop/master/changelog.txt", timeout=timeout)
                r_repo = r_session(url='https://api.github.com/repos/snooppr/snoop', timeout=timeout).json()
                r_latestvers = r_session(url='https://api.github.com/repos/snooppr/snoop/tags', timeout=timeout).json()

                console.print(Panel(Markdown(r_east.text.replace("=" * 83, "")),
                                    subtitle="[bold blue]журнал snoop-версий[/bold blue]", style=STL(color="cyan")))
                console.print(Panel(f"[bold cyan]Дата создания проекта:[/bold cyan] 2020-02-14 " + \
                                    f"({round((time.time() - 1581638400) / 86400)}_дней).\n" + \
                                    f"[bold cyan]Последнее обновление репозитория:[/bold cyan] " + \
                                    f"{'_'.join(r_repo.get('pushed_at')[0:-4].split('T'))} (UTC).\n" + \
                                    f"[bold cyan]Размер репозитория:[/bold cyan] {round(int(r_repo.get('size')) / 1024, 1)} Мб.\n" + \
                                    f"[bold cyan]Github-рейтинг:[/bold cyan] {r_repo.get('watchers')} звёзд.\n" + \
                                    f"[bold cyan]Скрытые опции:[/bold cyan]\n'--headers/-H':: Задать user-agent вручную, агент " + \
                                                              f"заключается в кавычки, по умолчанию для каждого сайта задается " + \
                                                              f"случайный либо переопределенный user-agent из БД snoop.\n" + \
                                                              f"'--cert-on/-C':: Включить проверку сертификатов на серверах, " + \
                                                              f"по умолчанию проверка сертификатов на серверах " + \
                                                              f"отключена, что позволяет обрабатывать проблемные сайты без ошибок.\n"
                                    f"[bold cyan]Последняя версия snoop:[/bold cyan] {r_latestvers[0].get('name')}.",
                                    style=STL(color="cyan"), subtitle="[bold blue]ключевые показатели[/bold blue]", expand=False))
            except Exception:
                console.log(snoopbanner.err_all(err_="high"))
        sys.exit()

    username = re.sub(" ", "%20", username)


## Предотвращение 'DoS' из-за невалидных логинов; номеров телефонов, ошибок поиска из-за спецсимволов.
    with open('domainlist.txt', 'r', encoding="utf-8") as err:
        ermail = err.read().splitlines()

        username_bad = username.rsplit(sep='@', maxsplit=1)
        username_bad = '@bro'.join(username_bad).lower()

        for ermail_iter in ermail:
            if ermail_iter.lower() == username.lower():
                print("\n" + Style.BRIGHT + Fore.RED + format_txt("⛔️ bad nickname: '{0}' (обнаружен чистый домен)"
                                                                  .format(ermail_iter), k=True, m=True) + "\n   пропуск\n")
                return False, False, nick
            elif ermail_iter.lower() in username.lower():
                usernameR = username.rsplit(sep=ermail_iter.lower(), maxsplit=1)[1]
                username = username.rsplit(sep='@', maxsplit=1)[0]

                if len(username) == 0:
                    username = usernameR
                print(f"\n{Fore.CYAN}Обнаружен E-mail адрес, извлекаем nickname: " + \
                      f"'{Style.BRIGHT}{Fore.CYAN}{username}{Style.RESET_ALL}" + \
                      f"{Fore.CYAN}'\nSnoop способен отличать e-mail от логина, например, поиск '{username_bad}'\n" + \
                      f"не является валидной электропочтой, но может существовать как nickname, следовательно — не будет обрезан\n")

                if len(username) == 0 and len(usernameR) == 0:
                    print("\n" + Style.BRIGHT + Fore.RED + format_txt("⛔️ bad nickname: '{0}' (обнаружен чистый домен)"\
                                                                      .format(ermail_iter), k=True, m=True) + "\n   пропуск\n")
                    return False, False, nick
                elif len(username) != 0 and len(username) < 3:
                    print(Style.BRIGHT + Fore.RED + format_txt("⛔️ nickname не может быть короче 3-х символов",
                                                               k=True, m=True) + "\n   пропуск\n")
                    return False, False, nick
        del ermail


    err_nick = re.findall(dic_binding.get("symbol_bad"), username)
    if err_nick:
        print(Style.BRIGHT + Fore.RED + format_txt("⛔️ недопустимые символы в nickname: " + \
                                                   "{0}{1}{2}{3}{4}".format(Style.RESET_ALL, Fore.RED, err_nick,
                                                                            Style.RESET_ALL, Style.BRIGHT + Fore.RED),
                                                   k=True, m=True) + "\n   пропуск\n")
        return False, False, nick


    ernumber = ['76', '77', '78', '79', '89', "38", "37", "9", "+"]
    if any(ernumber in username[0:2] for ernumber in ernumber):
        if len(username) >= 10 and len(username) <= 13 and username[1:].isdigit() is True:
            print(Style.BRIGHT + Fore.RED + format_txt("⛔️ snoop выслеживает учётки пользователей, " + \
                                                       "но не номера телефонов...", k=True, m=True) + "\n   пропуск\n")
            return False, False, nick
    elif '.' in username and '@' not in username:
        print(Style.BRIGHT + Fore.RED + format_txt("⛔️ nickname, содержащий [.] и не являющийся email, " + \
                                                   "невалидный...", k=True, m=True) + "\n   пропуск\n")
        return False, False, nick


## Создать многопоточный/процессный сеанс для всех запросов.
    if ANDROID:
        try:
            proc_ = len(BDdemo_new) if len(BDdemo_new) < 17 else 17
            executor1 = ProcessPoolExecutor(max_workers=proc_ if not speed else speed)
        except Exception:
            console.log(snoopbanner.err_all(err_="high"))
            dic_binding.update({'android_lame_workhorse': True})
            executor1 = ThreadPoolExecutor(max_workers=10 if not speed else speed)
    elif WINDOWS:
        cpu = 1 if psutil.cpu_count(logical=False) == None else psutil.cpu_count(logical=False)
        if norm is False:
            thread__ = len(BDdemo_new) if len(BDdemo_new) < (cpu * 5) else (18 if cpu < 4 else 30)
        else:
            thread__ = len(BDdemo_new) if len(BDdemo_new) < (os.cpu_count() * 5) else (20 if cpu < 4 else 40)
        executor1 = ThreadPoolExecutor(max_workers=thread__ if not speed else speed)
    elif LINUX:
        if norm is False:
            proc_ = len(BDdemo_new) if len(BDdemo_new) < 70 else (50 if len(os.sched_getaffinity(0)) < 4 else 140)
        else:
            proc_ = len(BDdemo_new) if len(BDdemo_new) < 70 else (60 if len(os.sched_getaffinity(0)) < 4 else 180)
        executor1 = ProcessPoolExecutor(max_workers=proc_ if not speed else speed)

    if norm is False:
        executor2 = ThreadPoolExecutor(max_workers=1)


## Анализ всех сайтов.
    dic_snoop_full = {}
    BDdemo_new_quick = {}
    lst_invalid = []
## Создание futures на все запросы. Это позволит распараллелить запросы с прерываниями.
    for websites_names, param_websites in BDdemo_new.items():
        results_site = {}
        results_site['flagcountry'] = param_websites.get("country")
        results_site['flagcountryklas'] = param_websites.get("country_klas")
        results_site['url_main'] = param_websites.get("urlMain")
        # username = param_websites.get("usernameON")

# Пользовательский user-agent браузера (рандомно на каждый сайт), а при сбое — постоянный с расширенным заголовком.
        majR = random.choice(range(101, 124, 1))
        RandHead=([f'{{"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ' + \
                   f'Chrome/{majR}.0.0.0 Safari/537.36"}}',
                   f'{{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' + \
                   f'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{majR}.0.0.0 Safari/537.36"}}'])
        headers = json.loads(random.choice(RandHead))

# Переопределить/добавить любые дополнительные заголовки необходимые для сайта из БД, или задать U-A из CLI.
        if header_custom is not None:
            headers.update({"User-Agent": ''.join(header_custom)})
        elif "headers" in param_websites:
            headers.update(param_websites["headers"])
        # console.print(headers, websites_names)  #проверка u-агентов

# Пропуск временно-отключенного сайта, не делать запрос если имя пользователя не подходит для сайта.
        exclusionYES = param_websites.get("exclusion")
        if exclusionYES and re.search(exclusionYES, username) or param_websites.get("bad_site") == 1:
            if exclusionYES and re.search(exclusionYES, username) and not print_found_only and not norm:
                lst_invalid.append(print_invalid(websites_names, f"#недопустимый ник '{nick}' для данного сайта", color))
            results_site["exists"] = "invalid_nick"
            results_site["url_user"] = '*' * 56
            results_site['countryCSV'] = "****"
            results_site['http_status'] = '*' * 10
            results_site['session_size'] = ""
            results_site['check_time_ms'] = '*' * 15
            results_site['response_time_ms'] = '*' * 15
            results_site['response_time_site_ms'] = '*' * 25
            if param_websites.get("bad_site") == 1 and verbose and not print_found_only and not norm:
                lst_invalid.append(print_invalid(websites_names, f"*ПРОПУСК. DYNAMIC GRAY_LIST", color))
            if param_websites.get("bad_site") == 1:
                dic_binding.get("badraw").append(websites_names)
                results_site["exists"] = "gray_list"
        else:
# URL пользователя на сайте (если он существует).
            url = param_websites["url"].format(username)
            results_site["url_user"] = url
            url_API = param_websites.get("urlProbe")
# Использование api/nickname.
            url_API = url if url_API is None else url_API.format(username)
# Повторы.
            connect = 1 if param_websites.get("country_klas") == "UA" else 2
# Если нужен только статус кода, не загружать тело страницы, экономия памяти, и многие сайты с защитой предпочитают Head.
            if param_websites["errorTypе"] != 'status_code' or reports:
                method = "get"
            else:
                method = "head"
# Сайт перенаправляет запрос.
# Запретить перенаправление чтобы захватить статус кода из первоначального url.
            if param_websites["errorTypе"] == "response_url" or param_websites["errorTypе"] == "redirection":
                allow_redirects = False
# Разрешить любой редирект, который хочет сделать сайт и захватить тело и статус ответа.
            else:
                allow_redirects = True

# Дергаем объект сессии не по прямому назначению, спасаем CPU/Windows/Многопоточность на длинной дистанции.
# Кроме того SSL замариновать при multiprocessing.
# Отправить параллельно все запросы и сохранить future для последующего доступа.
            try:
                future_ = executor1.submit(r_session, cert=cert, speed=speed, norm=norm, connect=connect, method=method,
                                           url=url_API, headers=headers, allow_redirects=allow_redirects, timeout=timeout)

                if norm: #quick режим
                    BDdemo_new_quick.update({future_:{websites_names:param_websites}})
                else: #последовательный режим
                    param_websites["request_future"] = future_
            except Exception:
                continue

# Добавлять во вложенный словарь future со всеми другими результатами.
        dic_snoop_full[websites_names] = results_site


# Вывести на печать invalid_data.
    if bool(lst_invalid) is True:
        print("".join(lst_invalid))


## Прогресс_описание.
    if not verbose:
        refresh = False
        refresh_per_second = 4.0 if "demo" in VERSION else (2.0 if not WINDOWS else 1.0)
        if not WINDOWS:
            spin_emoj = 'arrow3' if norm else random.choice(["dots", "dots12"])
            progress = Progress(TimeElapsedColumn(), SpinnerColumn(spinner_name=spin_emoj),
                                "[progress.percentage]{task.percentage:>1.0f}%", BarColumn(bar_width=None, complete_style='cyan',
                                finished_style='cyan bold'), refresh_per_second=refresh_per_second)
        else:
            progress = Progress(TimeElapsedColumn(), "[progress.percentage]{task.percentage:>1.0f}%", BarColumn(bar_width=None,
                                complete_style='cyan', finished_style='cyan bold'), refresh_per_second=refresh_per_second)
    else:
        refresh = True
        progress = Progress(TimeElapsedColumn(), "[progress.percentage]{task.percentage:>1.0f}%", auto_refresh=False)

## Панель вербализации.
        if not ANDROID:
            if color:
                console.print(Panel("[yellow]время[/yellow] | [magenta]выпол.[/magenta] | [bold cyan]отклик (t=s)[/bold cyan] " + \
                                    "| [bold red]общ.[bold cyan]время (T=s)[/bold cyan][/bold red] | " + \
                                    "[bold cyan]разм.данных[/bold cyan] | [bold cyan]дост.память[/bold cyan]",
                                    title="Обозначение", style=STL(color="cyan")))
            else:
                console.print(Panel("отклик сайта (t=s) | общ.время (T=s) | разм.данных | дост.память", title="Обозначение"))
        else:
            if color:
                console.print(Panel("[yellow]time[/yellow] | [magenta]perc.[/magenta] | [bold cyan]response (t=s)[/bold cyan] " + \
                                    "| [bold red]total [bold cyan]time (T=s)[/bold cyan][/bold red] | [bold cyan]data [/bold cyan]" + \
                                    "| [bold cyan]avail.ram[/bold cyan]",
                                    title="Designation", style=STL(color="cyan")))
            else:
                console.print(Panel("time | perc. | response (t=s) | total time (T=s) | data | avail.ram", title="Designation"))


## Пройтись по массиву future и получить результаты.
    li_time = [0]
    with progress:
        if color is True:
            task0 = progress.add_task("", total=len(BDdemo_new_quick)) if norm else progress.add_task("", total=len(BDdemo_new))
        iterator_future = iter(as_completed(BDdemo_new_quick)) if norm else iter(BDdemo_new.items())
        for future in iterator_future:
            if norm:
                websites_names = [*BDdemo_new_quick.get(future).keys()][0]
                param_websites = [*BDdemo_new_quick.get(future).values()][0]
            else:
                websites_names = future[0]
                param_websites = future[1]
            if color is True:
                progress.update(task0, advance=1, refresh=refresh)  #progress.refresh()
# Пропустить запрещенный никнейм или пропуск сайта из gray-list.
            if dic_snoop_full.get(websites_names).get("exists") is not None:
                continue
# Получить метаинформацию сайта, снова.
            url = dic_snoop_full.get(websites_names).get("url_user")
            country_emojis = dic_snoop_full.get(websites_names).get("flagcountry")
            country_code = dic_snoop_full.get(websites_names).get("flagcountryklas")
            country_Emoj_Code = country_emojis if not WINDOWS else country_code
# Получить ожидаемый тип данных 4-х методов.
            error_type = param_websites["errorTypе"]
# Результат ответа от сервера.
            request_future = future if norm else param_websites["request_future"]
            r, error_type, response_time = r_results(request_future=request_future, norm=norm,
                                                     error_type=error_type, websites_names=websites_names,
                                                     print_found_only=print_found_only, verbose=verbose,
                                                     color=color, timeout=timeout, country_code=f" ~{country_code}")


# Повторный запрос на сбойное соединение результативнее, чем через Adapter.
            if norm is False and r == "FakeNone":
                head_duble = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                              'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' + \
                                            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}

                for num, _ in enumerate(range(3), 1):
                    dic_binding.update({'censors': dic_binding.get('censors') - 1})
                    if num > 2:
                        head_duble = ""
                    r_retry = executor2.submit(r_session, url=url, headers=head_duble,
                                               allow_redirects=allow_redirects, timeout=4)
                    if color is True and print_found_only is False:
                        print(f"{Style.RESET_ALL}{Fore.CYAN}[{Style.BRIGHT}{Fore.RED}-{Style.RESET_ALL}{Fore.CYAN}]" \
                              f"{Style.DIM}{Fore.GREEN} ┌──└──повторное соединение{Style.RESET_ALL}")
                    else:
                        if print_found_only is False:
                            print("    ┌──└──повторное соединение")

                    r, error_type, response_time = r_results(request_future=r_retry, error_type=param_websites.get("errorTypе"),
                                                             websites_names=websites_names, print_found_only=print_found_only,
                                                             verbose=verbose, color=color, timeout=4.5,
                                                             country_code=f" ~{country_code}")

                    if r != "FakeNone":
                        break

                del r_retry

# Сбор сбойной локации bad_zone.
            if r == None or r == "FakeNone" or r == "FakeStuck":
                dic_binding.get("badzone").append(country_code)
## Проверка, 4 методов; #1.
# Автодетектирование кодировки при устаревшей специфике либы requests/ISO-8859-1, или ее смена вручную через БД.
            try:
                if r is not None and r != "FakeNone" and r != "FakeStuck":
                    if r.content and r.encoding == 'ISO-8859-1': #ловушка (if r is not None ≠ if r)
                        r.encoding = char_detect(r.content).get("encoding")
                        if r.encoding is None: r.encoding = "utf-8"
                    elif r.content and r.encoding != 'ISO-8859-1' and r.encoding.lower() != 'utf-8':
                        if r.encoding == "cp-1251": r.encoding = "cp1251"
                        elif r.encoding == "cp-1252": r.encoding = "cp1252"
                        elif r.encoding == "windows1251": r.encoding = "windows-1251"
                        elif r.encoding == "windows1252": r.encoding = "windows-1252"
            except Exception:
                r.encoding = "utf-8"

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

                try:
                    if r.status_code > 200 and param_websites.get("ignore_status_code") is None \
                                                                 or error in r.text or error2 in r.text or error3 in r.text:
                        if not print_found_only and not norm:
                            print_not_found(websites_names, verbose, color)
                        exists = "увы"
                    else:
                        if not norm:
                            print_found_country(websites_names, url, country_Emoj_Code, verbose, color)
                        exists = "найден!"
                        if reports:
                            sreports(url, headers, error_type, username, websites_names, r)
                except UnicodeEncodeError:
                    exists = "увы"
## Проверка, 4 методов; #2.
# Проверка username при статусе 301 и 303 (перенаправление и соль).
            elif error_type == "redirection":
                if r.status_code == 301 or r.status_code == 303:
                    if not norm:
                        print_found_country(websites_names, url, country_Emoj_Code, verbose, color)
                    exists = "найден!"
                    if reports:
                        session_size = sreports(url, headers, error_type, username, websites_names, r)
                else:
                    if not print_found_only and not norm:
                        print_not_found(websites_names, verbose, color)
                        session_size = len(str(r.content))
                    exists = "увы"
## Проверка, 4 методов; #3.
# Проверяет, является ли код состояния ответа 2..
            elif error_type == "status_code":
                if not r.status_code >= 300 or r.status_code < 200:
                    if not norm:
                        print_found_country(websites_names, url, country_Emoj_Code, verbose, color)
                    if reports:
                        sreports(url, headers, error_type, username, websites_names, r)
                    exists = "найден!"
                else:
                    if not print_found_only and not norm:
                        print_not_found(websites_names, verbose, color)
                    exists = "увы"
## Проверка, 4 методов; #4.
# Перенаправление.
            elif error_type == "response_url":
                if 200 <= r.status_code < 300:
                    if not norm:
                        print_found_country(websites_names, url, country_Emoj_Code, verbose, color)
                    if reports:
                        sreports(url, headers, error_type, username, websites_names, r)
                    exists = "найден!"
                else:
                    if not print_found_only and not norm:
                        print_not_found(websites_names, verbose, color)
                    exists = "увы"
## Если все 4 метода не сработали, например, из-за ошибки доступа (красный) или из-за неизвестной ошибки.
            else:
                exists = "блок"


## Попытка получить информацию из запроса, пишем в csv.
            try:
                http_status = r.status_code
            except Exception:
                http_status = "сбой" if r != "FakeStuck" else "завис"

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


## Считать тайминги с приемлемой точностью.
# Реакция.
            ello_time = round(float(time.time() - TIME_START), 2)  #текущее
            li_time.append(ello_time)
            dif_time = round(li_time[-1] - li_time[-2], 2)  #разница


## Опция '-v'.
            if verbose is True:
                ram_free = mem_test()
                ram_free_color = "[cyan]" if ram_free > 100 else "[red]"
                R = "[red]" if dif_time > 2.7 and dif_time != ello_time else "[cyan]"  #задержка в общем времени, цвет
                R1 = "bold red" if dif_time > 2.7 and dif_time != ello_time else "bold blue"

                if session_size == 0 or session_size is None:
                    Ssession_size = "Head"
                elif session_size == "Err":
                    Ssession_size = "Нет"
                else:
                    Ssession_size = str(session_size) + " Kb"

                if color is True:
                    console.print(f"[cyan] [*{response_time} s] {R}[*{ello_time} s] [cyan][*{Ssession_size}]",
                                  f"{ram_free_color}[*{ram_free} Мб]")
                    console.rule("", style=R1)
                else:
                    console.print(f" [*{response_time} s T] >>", f"[*{ello_time} s t]", f"[*{Ssession_size}]",
                                  f"[*{ram_free} Мб]", highlight=False)
                    console.rule(style="color")


## Служебная информация/CSV, обновление словаря с финальными результатами.
            if dif_time > 2.7 and dif_time != ello_time:
                dic_snoop_full.get(websites_names)['response_time_site_ms'] = str(dif_time)
            else:
                dic_snoop_full.get(websites_names)['response_time_site_ms'] = "нет"
            dic_snoop_full.get(websites_names)['exists'] = exists
            dic_snoop_full.get(websites_names)['session_size'] = session_size
            dic_snoop_full.get(websites_names)['countryCSV'] = country_code
            dic_snoop_full.get(websites_names)['http_status'] = http_status
            dic_snoop_full.get(websites_names)['check_time_ms'] = response_time
            dic_snoop_full.get(websites_names)['response_time_ms'] = str(ello_time)
# Добавление результатов этого сайта в окончательный словарь со всеми другими результатами.
            dic_snoop_full[websites_names] = dic_snoop_full.get(websites_names)
# не удерживать ресурсы соединения с сервером; предотвратить утечку памяти: del future.
            if r != "FakeStuck":
                if norm:
                    BDdemo_new_quick.pop(future, None)
                else:
                    param_websites.pop("request_future", None)

# Высвободить незначительную часть ресурсов.
        try:
            if 'executor2' in locals():
                executor2.shutdown()
        except Exception:
            console.log(snoopbanner.err_all(err_="low"))
# Вернуть словарь со всеми данными на запрос функции snoop и пробросить удерживаемые ресурсы (позже, закрыть в фоне).
        return dic_snoop_full, executor1, nick


## Опция '-t'.
def set_timeout(value):
    try:
        timeout = int(value)
    except Exception:
        raise argparse.ArgumentTypeError(f"\n\033[31;1mTimeout '{value}' Err,\033[0m \033[36m" + \
                                         f"укажите время целым числом в секундах.\n \033[0m")
    if timeout <= 0:
        raise argparse.ArgumentTypeError(f"\n\033[31;1mTimeout '{value}' Err,\033[0m \033[36m" + \
                                         f"укажите время > 0 sec.\n \033[0m")
    return timeout


## Опция '-p'.
def speed_snoop(speed):
    try:
        speed = int(speed)
        if WINDOWS and (speed <= 0 or speed > 60):
            raise Exception("")
        elif speed <= 0 or speed > 300:
            raise Exception("")
        return speed
    except Exception:
        if not WINDOWS:
            raise argparse.ArgumentTypeError(f"\n\033[31;1mMax. workers proc = '{speed}' Err,\033[0m" + \
                                              " \033[36m рабочий диапазон от '1' до '300' целым числом.\n \033[0m")
        else:
            snoopbanner.logo(text=format_txt(f" !  Задана слишком высокая многопоточноть: '{speed} поток' не имеет смысла, " + \
                                             f"уменьшите значение '--pool/-p <= 60'. Обратите внимание, что, например, " + \
                                             f"в OS GNU/Linux используется иная технология, которую имеет смысл разгонять.",
                                             k=True, m=True) + "\n\n", exit=False)
            sys.exit()


## Обновление исходного кода Snoop Project.
def update_snoop():
    print("""
\033[36mВы действительно хотите:
                    __             _  
   ._  _| _._|_ _  (_ ._  _  _ ._   ) 
|_||_)(_|(_| |_(/_ __)| |(_)(_)|_) o  
   |                           |    \033[0m""")

    while True:
        print("\033[36mВыберите действие:\033[0m [y/n] ", end='')
        upd = input().lower()
        if upd == "y":
            print("\033[36mПримечание: функция обновления Snoop работает при помощи утилиты < Git >\033[0m")
            os.startfile("update.bat") if WINDOWS else os.system("./update.sh")
            break
        elif upd == "n":
            print(Style.BRIGHT + Fore.RED + "\nОбновление отклонено\nВыход")
            break
        else:
            print(Style.BRIGHT + Fore.RED + format_txt("{0}└──False, [Y/N] ?", k=True, m=True).format(' ' * 25))
    sys.exit()


## Удаление отчетов.
def autoclean():
    print("""
\033[36mВы действительно хотите:\033[0m \033[31;1m
               _                _  
 _| _ |  _.|| |_) _ ._  _ .-_|_  ) 
(_|(/_| (_||| | \\(/_|_)(_)|  |_ o  
                    |             \033[0m""")

    while True:
        print("\033[36mВыберите действие:\033[0m [y/n] ", end='')
        del_all = input().lower()
        if del_all == "y":
            try:
# Определение директорий.
                path_build_del = "/results" if not WINDOWS else "\\results"
                if 'source' in VERSION and not ANDROID:
                    rm = DIRPATH + path_build_del
                    reports = rm
                else:
                    rm = DIRPATH
                    reports = rm + path_build_del
# Подсчет файлов и размера удаляемого каталога 'results'.
                total_size = 0
                delfiles = []
                for total_file in glob.iglob(reports + '/**/*', recursive=True):
                    total_size += os.path.getsize(total_file)
                    if os.path.isfile(total_file): delfiles.append(total_file)
# Сброс кэша и удаление каталога 'results'.
                shutil.rmtree(rm, ignore_errors=True)
                print(f"\n\033[31;1mdeleted --> '{rm}'\033[0m\033[36m {len(delfiles)} files, " + \
                      f"{round(total_size/1024/1024, 2)} Mb\033[0m")
            except Exception:
                console.log("[red]Ошибка")
            break
        elif del_all == "n":
            print(Style.BRIGHT + Fore.RED + "\nОтмена действия\nВыход")
            break
        else:
            print(Style.BRIGHT + Fore.RED + format_txt("{0}└──False, [Y/N] ?", k=True, m=True).format(' ' * 25))
    sys.exit()


## Лицензия/системная информация.
def license_snoop():
    with open('COPYRIGHT', 'r', encoding="utf8") as copyright:
        wl = 4
        if WINDOWS and int(platform.win32_ver()[0]) < 10:
            wl = 5

        cop = copyright.read().replace("\ufeffSnoop", "Snoop", 1)
        cop = cop.replace('=' * 80, "~" * (os.get_terminal_size()[0] - wl)).strip()
        console.print(Panel(cop, title='[bold white]COPYRIGHT[/bold white]', style=STL(color="white", bgcolor="blue")))

    if not ANDROID:
        cpu = 2 if psutil.cpu_count(logical=False) == None else psutil.cpu_count(logical=False)
        pool_ = str(cpu * 7 if WINDOWS else (os.cpu_count() * 40)) + \
                f" {'threads (~600_MB_Ram = 50_Threads = 5_Mbit/s)' if WINDOWS else 'process (~1.2_GB_Ram = 100_Process = 10_Mbit/s)'}"

        if WINDOWS and 'full' in VERSION:
            ram_av = 800
        elif WINDOWS and 'demo' in VERSION:
            ram_av = 500

        if LINUX and 'full' in VERSION:
            ram_av = 3000 if os.cpu_count() > 4 else 700
        elif LINUX and 'demo' in VERSION:
            ram_av = 200

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
            console.print(f"\n[bold red]Используемая версия Snoop: '{VERSION}' разработана для платформы Android, " + \
                          f"но кажется используется что-то другое 💻\n\nВыход")
            sys.exit()
    elif ANDROID:
        pool_ = str(os.cpu_count() * 3) + f" process, (~300_MB_Ram = 25_Process = 4_Mbit/s)"

        try:
            ram = subprocess.check_output("free -m", shell=True, text=True).splitlines()[1].split()[1]
            ram_free = int(subprocess.check_output("free -m", shell=True, text=True).splitlines()[1].split()[-1])
            if ram_free <= 200:
                A, B = "[bold red]", "[/bold red]"
            else:
                A, B = "[dim cyan]", "[/dim cyan]"
            os_ver = 'Android ' + subprocess.check_output("getprop ro.build.version.release", shell=True, text=True).strip()
            threadS = f'model: [dim cyan]{subprocess.check_output("getprop ro.product.cpu.abi", shell=True, text=True).strip()}' + \
                      f'[/dim cyan]'
            T_v = dict(os.environ).get("TERMUX_VERSION")
        except Exception:
            T_v, ram_free, os_ver, threadS, A, B = "Not Termux?!", "?", "?", "?", "[bold red]", "[/bold red]"
            ram = "pkg install procps |"

    termux = f"\nTermux: [dim cyan]{T_v}[/dim cyan]\n" if ANDROID else "\n"

    light_v = True if not 'snoopplugins' in globals() else False
    if PYTHON_3_8_PLUS:
        colorama_v = f", (colorama::{version_lib('colorama')})"
        rich_v = f", (rich::{version_lib('rich')})"
        urllib3_v = f", (urllib3::{version_lib('urllib3')})"
        psutil_v = f", (psutil::{version_lib('psutil')})"
        char_v = f", (charset_normalizer::{version_lib('charset_normalizer')})"
    else:
        urllib3_v = ""
        colorama_v = ""
        rich_v = ""
        psutil_v = ""
        char_v = ""

    console.print('\n', Panel(f"Program: [blue bold]{'light ' if light_v else ''}[/blue bold][dim cyan]{VERSION}" + \
                                       f"{str(platform.architecture(executable=sys.executable, bits='', linkage=''))}[/dim cyan]\n" + \
                              f"OS: [dim cyan]{os_ver}[/dim cyan]" + termux + \
                              f"Locale: [dim cyan]{locale.setlocale(locale.LC_ALL)}[/dim cyan]\n" + \
                              f"Python: [dim cyan]{platform.python_version()}[/dim cyan]\n" + \
                              f"Key libraries: [dim cyan](requests::{requests.__version__}), (certifi::{certifi.__version__}), " + \
                                             f"(speedtest::{snoopnetworktest.speedtest.__version__}){rich_v}{psutil_v}" + \
                                             f"{colorama_v}{urllib3_v}{char_v}[/dim cyan]\n" + \
                              f"CPU(s): [dim cyan]{os.cpu_count()},[/dim cyan] {threadS}\n" + \
                              f"Ram: [dim cyan]{ram} MB,[/dim cyan] available: {A}{ram_free} MB{B}\n" + \
                              f"Recommended pool: [dim cyan]{pool_}[/dim cyan]",
                              title='[bold cyan]snoop info[/bold cyan]', style=STL(color="cyan")))
    sys.exit()


## ОСНОВА.
def main_cli():
    web_path_copy()
    date_off = license()
    BDdemo = snoopbanner.DB('BDdemo')
    BDflag = snoopbanner.DB('BDflag')
    flagBS = len(BDdemo)
    web_sites = f"{len(BDflag) // 100}00+"

# Назначение опций Snoop.
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     usage="python3 snoop.py [search arguments...] nickname\nor\n" + \
                                           "usage: python3 snoop.py [service arguments | plugins arguments]\n",
                                     description=f"{Fore.CYAN}\nСправка{Style.RESET_ALL}",
                                     epilog=(f"{Fore.CYAN}Snoop {Style.BRIGHT}{Fore.RED}demo version {Style.RESET_ALL}" + \
                                             f"{Fore.CYAN}поддержка: \033[31;1m{flagBS}\033[0m \033[36mWebsites!\n{Fore.CYAN}" + \
                                             f"Snoop \033[36;1mfull version\033[0m \033[36mподдержка: " + \
                                             f"\033[36;1m{web_sites} \033[0m\033[36mWebsites!!!\033[0m\n\n"))
# Service arguments.
    service_group = parser.add_argument_group('\033[36mservice arguments\033[0m')
    service_group.add_argument("--version", "-V", action="store_true",
                               help="\033[36mA\033[0mbout: вывод на печать версии ПО, snoop info и Лицензии")
    service_group.add_argument("--list-all", "-l", action="store_true", dest="listing",
                               help="\033[36mВ\033[0mывести на печать детальную информацию о базе данных Snoop")
    service_group.add_argument("--donate", "-d", action="store_true", dest="donation",
                               help="\033[36mП\033[0mожертвовать на развитие Snoop Project-а, получить/приобрести \
                                     \033[32;1mSnoop full version\033[0m")
    service_group.add_argument("--autoclean", "-a", action="store_true", dest="autoclean", default=False,
                               help="\033[36mУ\033[0mдалить все отчеты, очистить кэш")
    service_group.add_argument("--update", "-U", action="store_true", dest="update",
                               help="\033[36mО\033[0mбновить Snoop")
# Plugins arguments.
    plugins_group = parser.add_argument_group('\033[36mplugins arguments\033[0m')
    plugins_group.add_argument("--module", "-m", action="store_true", dest="module", default=False,
                               help="\033[36mO\033[0mSINT поиск: задействовать различные плагины Snoop:: IP/GEO/YANDEX")
# Search arguments.
    search_group = parser.add_argument_group('\033[36msearch arguments\033[0m')
    search_group.add_argument("username", nargs='*', metavar='nickname', action="store", default=None,
                              help="\033[36mН\033[0mикнейм разыскиваемого пользователя. \
                                    Поддерживается поиск одновременно нескольких имен.\
                                    Ник, содержащий в своем имени пробел, заключается в кавычки")
    search_group.add_argument("--base", "-b <file>", dest="json_file", default="BDdemo", metavar='',
                              help=argparse.SUPPRESS if "demo" in VERSION else "\033[36mУ\033[0mказать для поиска 'nickname' \
                                                                                другую БД (Локально)")
    search_group.add_argument("--web-base", "-w", action="store_true", dest="web", default=False,
                              help=f"\033[36mП\033[0mодключиться для поиска 'nickname' к динамично-обновляемой web_БД \
                                    ({web_sites} сайтов)")
    search_group.add_argument("--site", "-s <site_name>", action="append", metavar='', dest="site_list", default=None,
                              help="\033[36mУ\033[0mказать имя сайта из БД '--list-all'. Поиск 'nickname' на одном указанном ресурсе, \
                                    допустимо использовать опцию '-s' несколько раз")
    search_group.add_argument("--exclude", "-e <country_code>", action="append", metavar='', dest="exclude_country", default=None,
                              help="\033[36mИ\033[0mсключить из поиска выбранный регион, допустимо использовать опцию '-e' \
                                    несколько раз, например, '-e RU -e WR' исключить из поиска Россию и Мир")
    search_group.add_argument("--include", "-i <country_code>", action="append", metavar='', dest="one_level", default=None,
                              help="\033[36mВ\033[0mключить в поиск только выбранный регион, \
                                    допустимо использовать опцию '-i' несколько раз, например, '-i US -i UA' поиск по США и Украине")
    search_group.add_argument("--time-out", "-t <digit>", action="store", metavar='', dest="timeout", type=set_timeout, default=8.9,
                              help="\033[36mУ\033[0mстановить max время ожидания ответа от сервера (секунды).\n"
                                   "Влияет на продолжительность поиска и 'timeout ошибки', по умолчанию задано 9 сек")
    search_group.add_argument("--country-sort", "-c", action="store_true", dest="country", default=False,
                              help="\033[36mП\033[0mечать и запись результатов по странам, а не по алфавиту")
    search_group.add_argument("--no-func", "-n", action="store_true", dest="no_func", default=False,
                              help="\033[36m✓\033[0mМонохромный терминал, не использовать цвета в url \
                                    ✓Запретить открытие web browser-а\
                                    ✓Отключить вывод на печать флагов стран\
                                    ✓Отключить индикацию и статус прогресса")
    search_group.add_argument("--found-print", "-f", action="store_true", dest="print_found_only", default=False,
                              help="\033[36mВ\033[0mыводить на печать только найденные аккаунты")
    search_group.add_argument("--verbose", "-v", action="store_true", dest="verbose", default=False,
                              help="\033[36mВ\033[0mо время поиска 'nickname' выводить на печать подробную вербализацию")
    search_group.add_argument("--userlist", "-u <file>", metavar='', action="store", dest="user", default=False,
                              help="\033[36mУ\033[0mказать файл со списком user-ов. Snoop интеллектуально обработает \
                                    данные и предоставит доп.отчеты")
    search_group.add_argument("--save-page", "-S", action="store_true", dest="reports", default=False,
                              help="\033[36mС\033[0mохранять найденные странички пользователей в локальные html-файлы,\
                              медленный режим")
    search_group.add_argument("--cert-on", "-C", default=False, action="store_true", dest="cert",
                              help=argparse.SUPPRESS)
    search_group.add_argument("--headers", "-H <User-Agent>", metavar='', dest="header_custom", nargs=1, default=None,
                              help=argparse.SUPPRESS)
    _val = "60 макс. рабочих потоков." if WINDOWS else "300 макс. процессов."
    search_group.add_argument("--pool", "-p <digit>", metavar='', dest="speed", type=speed_snoop, default=False,
                              help=
                              f"""
                               \033[36mО\033[0mтключить автооптимизацию и задать вручную скорость поиска от 1 до {_val}
                               По умолчанию используется высокая нагрузка на ресурсы ЭВМ в Quick-режиме, в остальных режимах
                               используется умеренное потребление мощностей. Слишком низкое или высокое значение может существенно
                               замедлить работу ПО. ~Расчетное оптимальное значение для данного устройства выводится в 'snoop info',
                               параметр 'Recommended pool', опция [--version/-V]. Данную опцию предлагается задействовать
                               1) если пользователь имеет многоядерную ЭВМ и запас ОЗУ или наоборот слабую, арендованную VPS 
                               2) ускорять, замедлять поиск рекомендуется в тандеме с опцией [--found-print/-f']
                               """)
    search_group.add_argument("--quick", "-q", action="store_true", dest="norm", default=False,
                              help=
                              """
                              \033[36mБ\033[0mыстрый и агрессивный режим поиска.
                              Не обрабатывает повторно сбойные ресурсы, вследствие чего ускоряется поиск,
                              но и немного повышается Bad_raw. Quick-режим подстраивается под мощность ПК,
                              не выводит промежуточные результаты на печать,
                              эффективен и предназначен для Snoop full version
                              """)

    args = parser.parse_args()

## Опции  '-csei' несовместимы между собой и quick-режим.
    if args.norm and 'full' in VERSION:
        print(Fore.CYAN + format_txt("активирована опция '-q': «быстрый режим поиска»", k=True))
        args.version, args.listing, args.donation, args.timeout = False, False, False, 8
        args.update, args.module, args.autoclean = False, False, False

        options = []
        options.extend([args.site_list, args.country, args.verbose, args.print_found_only,
                        args.no_func, args.reports, args.cert, args.header_custom, args.speed])

        if any(options) or args.timeout != 8:
            snoopbanner.logo(text=format_txt("⛔️ с quick-режимом ['-q'] совместимы лишь опции ['-w', '-u', '-e', '-i']",
                             k=True, m=True))
    elif args.norm and 'demo' in VERSION:
        snoopbanner.logo("в demo деактивирован переключатель '-q': «режим SNOOPninja/Quick»...",
                         color="\033[37m\033[44m", exit=False)
        snoopbanner.donate()
    elif args.norm is False and args.listing is False and args.speed is False and 'full' in VERSION:
        if LINUX:
            print(Fore.CYAN + format_txt("активирован дефолтный поиск '--': «режим SNOOPninja»", k=True))

    if [args.country, bool(args.site_list), bool(args.exclude_country), bool(args.one_level)].count(True) >= 2:
        snoopbanner.logo(text=format_txt("⛔️ опции ['-c', '-e' '-i', '-s'] несовместимы между собой", k=True, m=True))


## Опция  '-p'.
    if args.speed and 'full' in VERSION:
        thread_proc = "потоков" if WINDOWS else "процессов"
        print(Fore.CYAN + format_txt(f"активирована опция '-p': «макс. рабочих {thread_proc} =" + \
                                     "{0}{1} {2}{3}{4}» {5}".format(Style.BRIGHT, Fore.CYAN, args.speed,
                                                                    Style.RESET_ALL, Fore.CYAN,
                                                                    Style.RESET_ALL), k=True))
    elif args.speed and 'demo' in VERSION:
        snoopbanner.logo("Функция '-p' настройка ускорения/замедления поиска доступна пользователям Snoop full version...",
                         color="\033[37m\033[44m", exit=False)
        snoopbanner.donate()


## Опция  '-V' не путать с опцией '-v'.
    if args.version:
        license_snoop()


## Опция  '-a'.
    if args.autoclean:
        print(Fore.CYAN + format_txt("активирована опция '-a': «удаление накопленных отчетов»", k=True))
        autoclean()


## Опция  '-H'.
    if args.header_custom:
        print(Fore.CYAN + format_txt("активирована скрытая опция '-H': «переопределение user-agent(s)»", k=True), '\n',
              Fore.CYAN + format_txt("User-Agent: '{0}{1}{2}{3}{4}'".format(Style.BRIGHT, Fore.CYAN, ''.join(args.header_custom),
                                                                            Style.RESET_ALL, Fore.CYAN)), sep='')


## Опция  '-m'.
# Информативный вывод.
    if args.module:
        if not 'snoopplugins' in globals():
            snoopbanner.logo(text=f"\nTHIS IS THE LIGHT VERSION OF SNOOP PROJECT WITH PLUGINS DISABLED\n$ " + \
                                  f"{os.path.basename(sys.argv[0])} --version/-V")
            sys.exit()
        if 'full' in VERSION:
            with console.status("[cyan] проверка параметров..."):
                meta()

        print(Fore.CYAN + format_txt("активирована опция '-m': «модульный поиск»", k=True))

        def module():
            print(f"\n" + \
                  f"\033[36m╭Выберите плагин или действие из списка\033[0m\n" + \
                  f"\033[36m├──\033[0m\033[36;1m[1] --> GEO_IP/domain\033[0m\n" + \
                  f"\033[36m├──\033[0m\033[36;1m[2] --> Reverse Vgeocoder\033[0m\n" + \
                  f"\033[36m├──\033[0m\033[36;1m[3] --> \033[30;1mYandex_parser\033[0m\n" + \
                  f"\033[36m├──\033[0m\033[32;1m[help] --> Справка\033[0m\n" + \
                  f"\033[36m└──\033[0m\033[31;1m[q] --> Выход\033[0m\n")

            mod = console.input("[cyan]ввод --->  [/cyan]")

            if mod == 'help':
                snoopbanner.help_module_1()
                return module()
            elif mod == '1':
                table = Table(title=Style.BRIGHT + Fore.GREEN + "Выбран плагин" + Style.RESET_ALL, style="green", header_style='green')
                table.add_column("GEO_IP/domain_v0.6", style="green", justify="center")
                table.add_row('Получение информации об ip/domain/url цели или по списку этих данных')
                console.print(table)

                snoopplugins.module1()
            elif mod == '2':
                table = Table(title=Style.BRIGHT + Fore.GREEN + "Выбран плагин" + Style.RESET_ALL, style="green", header_style='green')
                table.add_column("Reverse Vgeocoder_v0.6", style="green", justify="center")
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


## Опции  '-f' + "-v".
    if args.verbose is True and args.print_found_only is True:
        snoopbanner.logo(text=format_txt("⛔️ режим подробной вербализации [опция '-v'] отображает детальную информацию " + \
                                         "[опция '-f'] неуместна", k=True, m=True))


## Опция  '-С'.
    if args.cert:
        print(Fore.CYAN + format_txt("активирована скрытая опция '-C': «проверка сертификатов на серверах вкл»", k=True))


## Опция  '-w'.
    if args.web:
        print(Fore.CYAN + format_txt("активирована опция '-w': «подключение к внешней web_database»", k=True))


## Опция  '-S'.
    if args.reports:
        print(Fore.CYAN + format_txt("активирована опция '-S': «сохранять странички найденных аккаунтов»", k=True))


## Опция  '-n'.
    if args.no_func:
        print(Fore.CYAN + format_txt("активирована опция '-n': «отключены:: цвета; флаги; браузер; прогресс»", k=True))


## Опция  '-t'.
    if args.timeout != 8.9 and args.norm is False:
        print(Fore.CYAN + format_txt("активирована опция '-t': ожидание ответа от " + \
                                     "сайта до{0}{1} {2} {3}{4}с.» {5}".format(Style.BRIGHT, Fore.CYAN, args.timeout,
                                                                               Style.RESET_ALL, Fore.CYAN,
                                                                               Style.RESET_ALL), k=True))
    if args.timeout == 8.9:
        args.timeout = 9


## Опция '-f'.
    if args.print_found_only:
        print(Fore.CYAN + format_txt("активирована опция '-f': «выводить на печать только найденные аккаунты»", k=True))


## Опция '-s'.
    if args.site_list:
        print(Fore.CYAN + format_txt(f"активирована опция '-s': «поиск{Style.BRIGHT}{Fore.CYAN} {', '.join(args.username)}" + \
                                     f"{Style.RESET_ALL} {Fore.CYAN}на выбранных website(s)»", k=True), '\n',
              Fore.CYAN + format_txt("допустимо использовать опцию '-s' несколько раз"), "\n",
              Fore.CYAN + format_txt("[опция '-s'] несовместима с [опциями '-с', '-e', '-i']"), sep="")


## Опция '--list-all'.
    if args.listing:
        print(Fore.CYAN + format_txt("активирована опция '-l': «детальная информация о БД Snoop»", k=True))
        print("\033[36m\nСортировать БД Snoop по странам, по имени сайта или обобщенно ?\n" + \
              "по странам —\033[0m 1 \033[36mпо имени —\033[0m 2 \033[36mall —\033[0m 3\n")

# Общий вывод стран (3!).
# Вывод для full/demo version.
        def sort_list_all(DB, fore, version, line=False):
            listfull = []
            if sortY == "3":
                if line:
                    console.rule("[cyan]Ok, print All Country", style="cyan bold")
                print("")
                li = [DB.get(con).get("country_klas") if WINDOWS else DB.get(con).get("country") for con in DB]
                cnt = str(Counter(li))
                try:
                    flag_str_sum = (cnt.split('{')[1]).replace("'", "").replace("}", "").replace(")", "")
                    all_ = str(len(DB))
                except Exception:
                    flag_str_sum = str("БД повреждена.")
                    all_ = "-1"
                table = Table(title=Style.BRIGHT + fore + version + Style.RESET_ALL, header_style='green', style="green")
                table.add_column("Геолокация: Кол-во websites", style="magenta", justify='full')
                table.add_column("All", style="cyan", justify='full')
                table.add_row(flag_str_sum, all_)
                console.print(table)

# Сортируем по алфавиту для full/demo version (2!).
            elif sortY == "2":
                if line:
                    console.rule("[cyan]Ok, сортируем по алфавиту", style="cyan bold")
                if version == "demo version":
                    console.print('\n', Panel.fit("++База данных++", title=version, style=STL(color="cyan", bgcolor="red")))
                else:
                    console.print('\n', Panel.fit("++База данных++", title=version, style=STL(color="cyan")))
                i = 0
                sorted_dict_v_listtuple = sorted(DB.items(), key=lambda x: x[0].lower())  #сорт.слов. по глав.ключу без уч. регистра
                datajson_sort = dict(sorted_dict_v_listtuple)  #преобр обратно в словарь (отсортированный)

                for con in datajson_sort:
                    S = datajson_sort.get(con).get("country_klas") if WINDOWS else datajson_sort.get(con).get("country")
                    i += 1
                    listfull.append(f"\033[36;2m{i}.\033[0m \033[36m{S}  {con}")
                print("\n~~~~~~~~~~~~~~~~\n".join(listfull), "\n")

# Сортируем по странам для full/demo version (1!).
            elif sortY == "1":
                listwindows = []

                if line:
                    console.rule("[cyan]Ok, сортируем по странам", style="cyan bold")

                for con in DB:
                    S = DB.get(con).get("country_klas") if WINDOWS else DB.get(con).get("country")
                    listwindows.append(f"{S}  {con}\n")

                if version == "demo version":
                    console.print('\n', Panel.fit("++База данных++", title=version, style=STL(color="cyan", bgcolor="red")))
                else:
                    console.print('\n', Panel.fit("++База данных++", title=version, style=STL(color="cyan")))

                for i in enumerate(sorted(listwindows, key=str.lower), 1):
                    listfull.append(f"\033[36;2m{i[0]}. \033[0m\033[36m{i[1]}")
                print("~~~~~~~~~~~~~~~~\n".join(listfull))

# Запуск функции '--list-all'.
        while True:
            sortY = console.input("[cyan]Выберите действие: [/cyan]")
            if sortY == "1" or sortY == "2":
                sort_list_all(BDflag, Fore.GREEN, "full version", line=True)
                sort_list_all(BDdemo, Fore.RED, "demo version")
                break
            elif sortY == "3":
                sort_list_all(BDdemo, Fore.RED, "demo version", line=True)
                sort_list_all(BDflag, Fore.GREEN, "full version")
                break
# Действие не выбрано '--list-all'.
            else:
                print(Style.BRIGHT + Fore.RED + format_txt("{0}└──False, [1/2/3] ?", k=True, m=True).format(' ' * 19))
        sys.exit()


## Опция донат '-d'.
    if args.donation:
        print(Fore.CYAN + format_txt("активирована опция '-d': «финансовая поддержка проекта»", k=True))
        snoopbanner.donate()


## Опция '-u' указание файла-списка разыскиваемых пользователей.
    if args.user:
        userlists, userlists_bad, duble, _duble, short_user = [], [], [], [], []
        flipped, d = {}, {}

        try:
            patchuserlist = ("{}".format(args.user))
            userfile = os.path.basename(patchuserlist)
            print(Fore.CYAN + format_txt("активирована опция '-u': «розыск nickname(s) из файла:: {0}{1}{2}{3}{4}» {5}",
                                         k=True).format(Style.BRIGHT, Fore.CYAN, userfile,
                                                        Style.RESET_ALL, Fore.CYAN, Style.RESET_ALL))

            with open(patchuserlist, "r", encoding="utf8") as u1:
                userlist = [(line[0], line[1].strip()) for line in enumerate(u1.read().replace("\ufeff", "").splitlines(), 1)]

                for num, user in userlist:
                    i_for = (num, user)
                    if re.findall(dic_binding.get("symbol_bad"), user):
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
            print(f"\n\033[31;1mНе могу найти_прочитать файл: '{userfile}'.\033[0m \033[36m\n " + \
                  f"\nПожалуйста, укажите текстовый файл в кодировке —\033[0m \033[36;1mutf-8.\033[0m\n" + \
                  f"\033[36mПо умолчанию, например, блокнот в OS Windows сохраняет текст в кодировке — ANSI.\033[0m\n" + \
                  f"\033[36mОткройте ваш файл '{userfile}' и измените кодировку [файл ---> сохранить как ---> utf-8].\n" + \
                  f"\033[36mИли удалите из файла нечитаемые спецсимволы.")
            sys.exit()

# good user.
        if userlists:
            _userlists = [f"[dim cyan]{num}.[/dim cyan] {v} [{k}]".replace("", "") for num, (k, v) in enumerate(userlists, 1)]
            console.print(Panel.fit("\n".join(_userlists).replace("%20", " "), title=f"valid ({len(userlists)})",
                                    style=STL(color="cyan")))

# duplicate user.
        if duble:
            dict_duble = dict(duble)
            for key, value in dict_duble.items():
                if value not in flipped:
                    flipped[value] = [key]
                else:
                    flipped[value].append(key)

            for k,v in flipped.items():
                k = f"{k} ({len(v)})"
                d[k] = v

            for num, (k, v) in enumerate(d.items(), 1):
                str_1 = f"[dim yellow]{num}.[/dim yellow] {k} {v}".replace(" (", " ——> ").replace(")", " шт.")
                str_2 = str_1.replace("——> ", "——> [bold yellow]").replace(" шт.", " шт.[/bold yellow]")
                _duble.append(str_2)

            print(f"\n\033[36mследующие nickname(s) из '\033[36;1m{userfile}\033[0m\033[36m' содержат " + \
                  f"\033[33mдубли\033[0m\033[36m и будут пропущены:\033[0m")
            console.print(Panel.fit("\n".join(_duble), title=f"duplicate ({len(duble)})", style=STL(color="yellow")))

# bad user.
        if userlists_bad:
            _userlists_bad = [f"[dim red]{num}.[/dim red] {v} [{k}]" for num, (k, v) in enumerate(userlists_bad, 1)]
            print(f"\n\033[36mследующие nickname(s) из '\033[36;1m{userfile}\033[0m\033[36m' содержат " + \
                  f"\033[31;1mN/A-символы\033[0m\033[36m и будут пропущены:\033[0m")
            console.print(Panel.fit("\n".join(_userlists_bad), title=f"invalid_data ({len(userlists_bad)})",
                                    style=STL(color="bright_red")))

# Short user.
        if short_user:
            _short_user = [f"[dim red]{num}.[/dim red] {v} [{k}]" for num, (k, v) in enumerate(short_user, 1)]
            print(f"\n\033[36mследующие nickname(s) из '\033[36;1m{userfile}\033[0m\033[36m'\033[0m " + \
                  f"\033[31;1mкороче 3-х символов\033[0m\033[36m и будут пропущены:\033[0m")
            console.print(Panel.fit("\n".join(_short_user).replace("%20", " "), title=f"short nickname ({len(short_user)})",
                                    style=STL(color="bright_red")))

# Сохранение bad_nickname(s) в отдельном txt файле.
        if short_user or userlists_bad:
            for bad_user1, bad_user2 in itertools.zip_longest(short_user, userlists_bad):
                with open (f"{DIRPATH}/results/nicknames/bad_nicknames.txt", "a", encoding="utf-8") as bad_nick:
                    if bad_user1:
                        bad_nick.write(f"{time.strftime('%Y-%m-%d_%H:%M:%S', TIME_DATE)}  <FILE: {userfile}>  '{bad_user1[1]}'\n")
                    if bad_user2:
                        bad_nick.write(f"{time.strftime('%Y-%m-%d_%H:%M:%S', TIME_DATE)}  <FILE: {userfile}>  '{bad_user2[1]}'\n")


        USERLIST = [i[1] for i in userlists]

        del userlists, duble, userlists_bad, _duble, short_user, flipped, d

        if bool(USERLIST) is False:
            print("\n", Style.BRIGHT + Fore.RED + format_txt("⛔️ Файл '{0}' не содержит ни одного валидного nickname".format(userfile),
                                                             k=True, m=True), "\n\n\033[31;1mВыход\033[0m\n", sep="")
            sys.exit()


## Проверка остальных (в т.ч. повтор) опций.
## Опция '--update' обновление Snoop.
    if args.update:
        print(Fore.CYAN + format_txt("активирована опция '-U': «обновление snoop»", k=True))
        update_snoop()


## Опция '-w'.
    if args.web:
        print("")
        snoopbanner.logo("Функция '-w' доступна только пользователям Snoop full version...",
                         color="\033[37m\033[44m", exit=False)
        snoopbanner.donate()


## Опция '-b'. Проверить, существует ли альтернативная база данных, иначе default.
    if not os.path.exists(str(args.json_file)):
        print(f"\n\033[31;1mОшибка! Неверно указан путь к файлу: '{str(args.json_file)}'.\033[0m")
        sys.exit()


## Опция  '-c'. Сортировка по странам.
    if args.country is True and args.web is False:
        print(Fore.CYAN + format_txt("активирована опция '-c': «сортировка/запись результатов по странам»", k=True))
        country_sites = sorted(BDdemo, key=lambda k: ("country" not in k, BDdemo[k].get("country", sys.maxsize)))
        sort_web_BDdemo_new = {}
        for site in country_sites:
            sort_web_BDdemo_new[site] = BDdemo.get(site)


## Функция для опций '-ei'.
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
            print('\n', format_txt(f"⛔️ \033[31;1m[{str(diff_list).strip('[]')}] пожалуйста проверьте ввод, " + \
                                   f"т.к. все указанные регионы для поиска являются невалидными.\033[0m", k=True, m=True), sep='')
            sys.exit()
# Вернуть корректный и bad списки пользовательского ввода в CLI.
        return lap, diff_list


## Если опции '-sei' не указаны, то используем БД, как есть.
    BDdemo_new = {}
    if args.site_list is None and args.exclude_country is None and args.one_level is None:
        BDdemo_new = BDdemo if len(BDdemo) < 404 else sys.exit()


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
                    print(format_txt("{0}⛔️ пропуск:{2} {3}сайт из БД {4}full-версии{5} {6}недоступен в{7} " + \
                                     "{8}demo-версии{9}{10}:: '{11}{1}{12}{13}'{14}",
                                     k=True, m=True).format(Style.BRIGHT + Fore.RED, site_yes_full_diff,
                                                            Style.RESET_ALL, Fore.CYAN, Style.BRIGHT + Fore.CYAN,
                                                            Style.RESET_ALL, Fore.CYAN, Style.RESET_ALL,
                                                            Style.BRIGHT + Fore.YELLOW, Style.RESET_ALL,
                                                            Fore.CYAN, Style.BRIGHT + Fore.BLACK,
                                                            Style.RESET_ALL, Fore.CYAN, Style.RESET_ALL))

            if not any(site.lower() == site_yes_full.lower() for site_yes_full in BDflag):  #если ни одного совпадения по сайту
                print(format_txt("{0}⛔️ пропуск:{1} {2}желаемый сайт отсутствует в БД Snoop:: '" + \
                                 "{3}{4}{5}' {6}", k=True, m=True).format(Style.BRIGHT + Fore.RED, Style.RESET_ALL, Fore.CYAN,
                                                                          Style.BRIGHT + Fore.RED, site,
                                                                          Style.RESET_ALL + Fore.CYAN, Style.RESET_ALL))
# Отмена поиска, если нет ни одного совпадения по БД и '-s'.
        if not BDdemo_new:
            sys.exit()


## Опция '-e'.
# Создать для проверки сокращенную базу данных сайта(ов).
# Создать и добавить в новую БД сайты, аргументы (-e) которых != бук.кодам стран (country_klas).
    elif args.exclude_country is not None:
        lap, diff_list = one_exl(one_exl_=args.exclude_country, bool_=True)
        str_e = "активирована опция '-e': «исключить из поиска выбранные регионы»::" + \
                                     "{0} {1} {2} {3} {4} {5}".format(Fore.CYAN, str(lap).strip('[]').upper(),
                                                                      Style.RESET_ALL, Style.BRIGHT + Fore.RED,
                                                                      str(diff_list).strip('[]'), Style.RESET_ALL)
        print(Fore.CYAN + format_txt(str_e, k=True), '\n',
              Fore.CYAN + format_txt("допустимо использовать опцию '-e' несколько раз", m=True), '\n',
              Fore.CYAN + format_txt("[опция '-e'] несовместима с [опциями '-s', '-c', '-i']", m=True), sep='')


## Опция '-i'.
# Создать для проверки сокращенную базу данных сайта(ов).
# Создать и добавить в новую БД сайты, аргументы (-e) которых != бук.кодам стран (country_klas).
    elif args.one_level is not None:
        lap, diff_list = one_exl(one_exl_=args.one_level, bool_=False)
        str_i = "активирована опция '-i': «включить в поиск только выбранные регионы»::" + \
                                     "{0} {1} {2} {3} {4} {5}".format(Fore.CYAN, str(lap).strip('[]').upper(),
                                                                      Style.RESET_ALL, Style.BRIGHT + Fore.RED,
                                                                      str(diff_list).strip('[]'), Style.RESET_ALL)
        print(Fore.CYAN + format_txt(str_i, k=True), '\n',
              Fore.CYAN + format_txt("допустимо использовать опцию '-i' несколько раз", m=True), '\n',
              Fore.CYAN + format_txt("[опция '-i'] несовместима с [опциями '-s', '-c', 'e']", m=True), sep='')


## Ник не задан или противоречие опций.
    if bool(args.username) is False and bool(args.user) is False:
        snoopbanner.logo(text="\nпараметры либо nickname(s) не задан(ы)")
    if bool(args.username) is True and bool(args.user) is True:
        print('\n⛔️' + format_txt("\033[31;1m выберите для поиска nickname(s) из файла или задайте в CLI,\n" + \
              "но не совместное использование nickname(s): из файла и CLI", k=True, m=True), "\033[31;1m\n\nВыход\033[0m")
        sys.exit()


## Опция '-v'.
    if args.verbose and bool(args.username) or args.verbose and bool(USERLIST):
        print(Fore.CYAN + format_txt("активирована опция '-v': «подробная вербализация в CLI»\n", k=True))
        snoopnetworktest.nettest()


## Опция  '-w' активна/не активна.
    try:
        if args.web is False:
            _DB = f"_[_{len(BDdemo_new)}_]" if len(BDdemo_new) != len(BDdemo) else ""
            print(f"\n{Fore.CYAN}загружена локальная база: {Style.BRIGHT}{Fore.CYAN}{len(BDdemo)}_Websites{_DB}{Style.RESET_ALL}")
    except Exception:
        print("\033[31;1mInvalid загружаемая база данных.\033[0m")


## Проверка версий lib: 'requests/urllib3'.
    warning_lib()


## Крутим user's.
    def starts(SQ):
# Метаинформация.
        if 'full' in VERSION:
            meta()

# Выбор корректной кодировки для CSV с учетом OS/геолокации.
        try:
            if os.environ.get('LANG') is not None and 'ru' in os.environ.get('LANG'):
                rus_unix = True
            else:
                rus_unix = False
            if WINDOWS and "1251" in locale.setlocale(locale.LC_ALL):
                rus_windows = True
            else:
                rus_windows = False
        except Exception:
            rus_unix = False
            rus_windows = False

        kef_user = 0
        ungzip, ungzip_all, find_url_lst, el = [], [], [], []
        exl = "/".join(lap).upper() if args.exclude_country is not None else "нет"  #искл.регионы_valid
        one = "/".join(lap).upper() if args.one_level is not None else "нет"  #вкл.регионы_valid
        for username in SQ:
            kef_user += 1
            sort_sites = sort_web_BDdemo_new if args.country is True else BDdemo_new

            FULL, hardware, nick = snoop(username, sort_sites, country=args.country, user=args.user, verbose=args.verbose,
                                         cert=args.cert, norm=args.norm, reports=args.reports,
                                         print_found_only=args.print_found_only, timeout=args.timeout,
                                         color=not args.no_func, header_custom=args.header_custom, speed=args.speed)

            exists_counter = 0

            if bool(FULL) is False:
                kef_user -= 1
                cli_file = " <CLI>       " if args.user is False else f" <FILE: {userfile}>"
                with open (f"{DIRPATH}/results/nicknames/bad_nicknames.txt", "a", encoding="utf-8") as bad_nick:
                    bad_nick.write(f"{time.strftime('%Y-%m-%d_%H:%M:%S', TIME_DATE)} {cli_file}  '{username}'\n")

                continue


## Запись в txt отчет.
            file_txt = open(f"{DIRPATH}/results/nicknames/txt/{username}.txt", "w", encoding="utf-8")

            file_txt.write(f"Гео | Ресурс {' ' * 18} | Адрес" + "\n\n")

            for website_name in FULL:
                dictionary = FULL[website_name]
                if type(dictionary.get("session_size")) != str:
                    ungzip.append(dictionary.get("session_size")), ungzip_all.append(dictionary.get("session_size"))
                if dictionary.get("exists") == "найден!":
                    exists_counter += 1
                    find_url_lst.append(exists_counter)
                    txt_str = f"{dictionary['flagcountryklas']}  |  {(website_name)}"
                    kef_indent = 30 - (len(txt_str))
                    file_txt.write(f"{txt_str} {' ' * kef_indent} |  {dictionary['url_user']}\n")
# Размер сессии персональный и общий, кроме CSV.
            try:
                sess_size = round(sum(ungzip) / 1024, 2)  #в МБ
                s_size_all = round(sum(ungzip_all) / 1024, 2)  #в МБ
            except Exception:
                sess_size = 0.000_000_000_1
                s_size_all = "Err"

            timefinish = time.time() - TIME_START - sum(el)
            el.append(timefinish)
            time_all = str(round(time.time() - TIME_START))
            

            file_txt.write("\n" f"Запрашиваемый объект: <{nick}> найден: {exists_counter} раз(а).")
            file_txt.write("\n" f"Сессия: {str(round(timefinish))}сек {str(sess_size)}Mb.")
            file_txt.write("\n" f"База Snoop (demo version): {flagBS} Websites.")
            file_txt.write("\n" f"Исключённые регионы: {exl}.")
            file_txt.write("\n" f"Выбор конкретных регионов: {one}.")
            file_txt.write("\n" f"Обновлено: {time.strftime('%Y-%m-%d_%H:%M:%S', TIME_DATE)}.\n")
            file_txt.write("\n" f"©2020-{time.localtime().tm_year} «Snoop Project» (demo version).")
            file_txt.close()


## Запись в html отчет.
            if ANDROID and re.search("[^\\W \\da-zA-Z]+", nick):
                username = f"nickname_{time.strftime('%Y-%m-%d_%H-%M-%S')}"

            file_html = open(f"{DIRPATH}/results/nicknames/html/{username}.html", "w", encoding="utf-8")

            path_ = DIRPATH if not ANDROID else "/storage/emulated/0/snoop"
            file_html.write("<!DOCTYPE html>\n<html lang='ru'>\n\n<head>\n<title>◕ Snoop HTML-отчет</title>\n" + \
                            "<meta charset='utf-8'>\n<style>\nbody {background: url(../../../web/public.png) " + \
                            "no-repeat 20% 0%}\n.str1{text-shadow: 0px 0px 20px #333333}\n.shad{display: inline-block}\n" + \
                            ".shad:hover{text-shadow: 0px 0px 14px #6495ED; transform: scale(1.1); transition: transform 0.15s}\n" + \
                            "</style>\n<link rel='stylesheet' href='../../../web/style.css'>\n</head>\n\n<body id='snoop'>\n\n" + \
                            "<div id='particles-js'></div>\n\n" + \
                            "<h1><a class='GL' href='file://" + f"{path_}/results/nicknames/html/'>open file</a>" + "</h1>\n")
            file_html.write("<h3>Snoop Project (demo version)</h3>\n<p>Нажмите: 'сортировать по странам', возврат:" + \
                            "'<span style='text-shadow: 0px 0px 13px #40E0D0'>F5'</span></p>\n<div id='report'>\n" + \
                            "<button onclick='sortList()'>Сортировать по странам ↓↑</button><br>\n<ol" + " id='id777'>\n")

            li = []
            for website_name in FULL:
                dictionary = FULL[website_name]
                flag_sum = dictionary["flagcountry"]
                if dictionary.get("exists") == "найден!":
                    li.append(flag_sum)
                    file_html.write("<li><span class='shad'>" + dictionary["flagcountry"] + \
                                    "<a target='_blank' href='" + dictionary["url_user"] + "'>" + \
                                    (website_name) + "</a></span></li>\n")
            try:
                cnt = []
                for k, v in sorted(Counter(li).items(), key=lambda x: x[1], reverse=True):
                    cnt.append(f"【{k} ⇔ {v}】")
                flag_str_sum = "; ".join(cnt)
            except Exception:
                flag_str_sum = "-1"

            file_html.write("</ol>\n</div>\n\n<br>\n\n<div id='meta'>GEO:" + flag_str_sum + ".\n")
            file_html.write("<br> Запрашиваемый объект &lt; <b>" + str(nick) + "</b> &gt; найден: <b>" + \
                            str(exists_counter) + "</b> раз(а).")
            file_html.write("<br> Сессия: " + "<b>" + str(round(timefinish)) + "сек_" + str(sess_size) + "Mb</b>.\n")
            file_html.write("<br> Исключённые регионы: <b>" + str(exl) + "</b>.\n")
            file_html.write("<br> Выбор конкретных регионов: <b>" + str(one) + "</b>.\n")
            file_html.write("<br> База Snoop (demo version): <b>" + str(flagBS) + "</b>" + " Websites.\n")
            file_html.write("<br> Обновлено: " + "<i><b>" + time.strftime("%Y-%m-%d</b>_%H:%M:%S", TIME_DATE) + \
                            ".</i><br><br>\n</div>\n")
            file_html.write("""
<br>

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

function rnd(min, max) {
  return Math.random() * (max - min) + min;
}

var don = decodeURIComponent(escape(window.atob("\\
4oyb77iPINCh0L/QsNGB0LjQsdC+INC30LAg0LjQvdGC0LXRgNC10YEg0LogU25vb3AgZGVtbyB2\\
ZXJzaW9uLgoK0JXRgdC70Lgg0LjQvNC10LXRgtGB0Y8g0LLQvtC30LzQvtC20L3QvtGB0YLRjCwg\\
0L/QvtC00LTQtdGA0LbQuNGC0LUg0YTQuNC90LDQvdGB0L7QstC+INGN0YLQvtGCINGD0L3QuNC6\\
0LDQu9GM0L3Ri9C5IElULdC/0YDQvtC10LrRgjoK0L/QvtC70YPRh9C40YLQtSBTbm9vcCBmdWxs\\
IHZlcnNpb24g0LHQtdC3INC+0LPRgNCw0L3QuNGH0LXQvdC40LkuCgpD0LwuICJzbm9vcF9jbGku\\
YmluIC0taGVscCAvIHNub29wX2NsaS5leGUgLS1oZWxwIi4K")))

var don1 = decodeURIComponent(escape(window.atob("\\
PGZvbnQgY29sb3I9InJlZCIgc2l6ZT0iMiI+4oybIFNub29wIGRlbW8gdmVyc2lvbi48L2ZvbnQ+\\
Cjxicj48YnI+CtCU0LvRjyDQv9C+0LTQtNC10YDQttC60Lgg0JHQlCDQuCDQtNCw0LvRjNC90LXQ\\
udGI0LXQs9C+INGA0LDQt9Cy0LjRgtC40Y8g0J/QniDigJQg0L/RgNC+0LXQutGC0YMg0YLRgNC1\\
0LHRg9C10YLRgdGPINGE0LjQvdCw0L3RgdC+0LLQsNGPINC/0L7QtNC00LXRgNC20LrQsC48YnI+\\
CtCf0L7QtNC00LXRgNC20LjRgtC1INGA0LDQt9GA0LDQsdC+0YLRh9C40LrQsCDQuCDQtdCz0L4g\\
0LjRgdGB0LvQtdC00L7QstCw0L3QuNGPINC00L7QvdCw0YLQvtC8LCDQuNC70Lgg0L/RgNC40L7Q\\
sdGA0LXRgtCw0Y8gPGI+PGZvbnQgY29sb3I9ImdyZWVuIj5Tbm9vcCBmdWxsIHZlcnNpb24hPC9m\\
b250PjwvYj4KPGJyPjxicj4KQ9C8LiAic25vb3BfY2xpLmJpbiAtLWhlbHAgLyBzbm9vcF9jbGku\\
ZXhlIC0taGVscCIuCg==")))

func = setInterval(() => {alert(don)}, rnd(30, 45) * 1000)
func1 = setTimeout(() => {id777.onmouseover = function() {document.write(don1)}}, rnd(55, 75) * 1000)
</script>

<script src="../../../web/particles.js"></script>
<script src="../../../web/app.js"></script>

<audio title="Megapolis (remix).mp3" controls="controls" autoplay="autoplay">
<source src="../../../web/Megapolis%20(remix).mp3" type="audio/mpeg">
</audio>

<br>

<audio title="for snoop in cyberpunk.mp3" controls="controls">
<source src="../../../web/for%20snoop%20in%20cyberpunk.mp3" type="audio/mpeg">
</audio>

<br><br>

<div id='buttons'>
<a target='_blank' href='https://github.com/snooppr/snoop' class="SnA"><span class="SnSpan">🛠  Source Исходный код</span></a>
<a target='_blank' href='https://drive.google.com/file/d/12DzAQMgTcgeG-zJrfDxpUbFjlXcBq5ih/view' \
class="DnA"><span class="DnSpan">📖 Doc Документация</span></a>
<a onclick='bay()' class="DnA"><span class="DnSpan">💳 Get Full_Version</span></a>
</div>

<br><br>\n
""" + \

snoopbanner.buy() + \

f"""\n\n<p class='str1'><span style="color: gray"><small><small>Отчёт создан в ПО Snoop Project. <br> ©2020-\
{time.localtime().tm_year} «Snoop Project».</small></small></span></p>

<script>
if(typeof don == "undefined" || typeof don1 == "undefined" || don.length != 216 || don1.length != 335 || typeof func == "undefined" \
|| typeof func1 == "undefined")
document.getElementById('snoop').innerHTML=""
</script>

</body>
</html>""")
            file_html.close()


## Запись в csv отчет.
            if rus_windows is False:
                file_csv = open(f"{DIRPATH}/results/nicknames/csv/{username}.csv", "w", newline='', encoding="utf-8")
            else:
                file_csv = open(f"{DIRPATH}/results/nicknames/csv/{username}.csv", "w", newline='') #для ru_пользователей

            usernamCSV = re.sub(" ", "_", nick)

            try:
                err_all = dic_binding.get('censors') / kef_user  #err_connection_all
                flagBS_err = round(err_all * 100 / (len(BDdemo_new) - len(dic_binding.get("badraw"))), 2)
            except ZeroDivisionError:
                flagBS_err = 0

            try:
                bad_zone = f"~{Counter(dic_binding.get('badzone')).most_common(2)[0][0]}/" + \
                           f"{Counter(dic_binding.get('badzone')).most_common(2)[1][0]}"
            except IndexError:
                try:
                    bad_zone = f"~{Counter(dic_binding.get('badzone')).most_common(2)[0][0]}"
                except IndexError:
                    bad_zone = "ERR"

            writer = csv.writer(file_csv)
            if rus_windows or rus_unix or ANDROID:
                writer.writerow(['Ресурс', 'Страна', 'Url', 'Ссылка_на_профиль', 'Статус', 'Статус_http',
                                 'Общее_замедление/сек', 'Отклик/сек', 'Общее_время/сек', 'Сессия/Kb'])
            else:
                writer.writerow(['resource', 'country', 'url', 'url_username', 'status', 'http',
                                 'deceleration/s', 'response/s', 'time/s', 'session/Kb'])

            for site in FULL:
                if FULL[site]['session_size'] == 0:
                    Ssession = "Head"
                elif type(FULL[site]['session_size']) != str:
                    Ssession = str(FULL.get(site).get("session_size")).replace('.', locale.localeconv()['decimal_point'])
                else:
                    Ssession = "Bad"

                writer.writerow([site, FULL[site]['countryCSV'], FULL[site]['url_main'], FULL[site]['url_user'],
                                 FULL[site]['exists'], FULL[site]['http_status'],
                                 FULL[site]['response_time_site_ms'].replace('.', locale.localeconv()['decimal_point']),
                                 FULL[site]['check_time_ms'].replace('.', locale.localeconv()['decimal_point']),
                                 FULL[site]['response_time_ms'].replace('.', locale.localeconv()['decimal_point']),
                                 Ssession])

            writer.writerow(['«' + '-'*35, '-'*4, '-'*35, '-'*56, '-'*13, '-'*17, '-'*32, '-'*13, '-'*23, '-'*16 + '»'])
            writer.writerow([f'БД_(demoversion)={flagBS}_Websites'])
            writer.writerow([f"Nick={usernamCSV}"])
            writer.writerow('')
            writer.writerow([f'Исключённые_регионы={exl}'])
            writer.writerow([f'Выбор_конкретных_регионов={one}'])
            writer.writerow([f"Bad_raw:_{flagBS_err}%_БД,_bad_zone_{bad_zone}" if flagBS_err >= 2 else ''])
            writer.writerow('')
            writer.writerow(['Дата'])
            writer.writerow([time.strftime("%Y-%m-%d_%H:%M:%S", TIME_DATE)])
            writer.writerow([f'©2020-{time.localtime().tm_year} «Snoop Project»\n(demo version).'])

            file_csv.close()

            ungzip.clear()
            dic_binding.get("badraw").clear()


## Финишный вывод в CLI.
        if bool(FULL) is True:
            direct_results = f"{DIRPATH}/results/nicknames/*" if not WINDOWS else f"{DIRPATH}\\results\\nicknames\\*"

            print(f"{Fore.CYAN}├─Результаты:{Style.RESET_ALL} найдено --> {len(find_url_lst)} " + \
                  f"url (сессия: {time_all}_сек__{s_size_all}_Mb)")
            print(f"{Fore.CYAN}├──Сохранено в:{Style.RESET_ALL} {direct_results}")

            if flagBS_err >= 2:  #perc_%
                bad_raw(flagBS_err, bad_zone, nick, [args.exclude_country, args.one_level, args.site_list])
            else:
                print(f"{Fore.CYAN}└───Дата поиска:{Style.RESET_ALL} {time.strftime('%Y-%m-%d__%H:%M:%S', TIME_DATE)}\n")

            if "demo" in VERSION:
                console.print(f"[italic]  Получить Snoop Full Version ({web_sites} сайтов):[/italic]\n[dim yellow]  " + \
                              f"$ {'python ' if 'source' in VERSION else ''}" + \
                              f"{os.path.basename(sys.argv[0])} --donate[/dim yellow]\n", highlight=False)
            elif "full" in VERSION and WINDOWS and not any([args.norm, args.speed, args.one_level, args.site_list]):
                console.print(format_txt(f"[bold red] ![/bold red] [bold yellow]Обратите внимание: скорость поиска можно " + \
                                         f"существенно ускорить, используя опции::[/bold yellow]", k=True, m=True))
                console.print(format_txt(f"[bold yellow]   [-[bold green]-q[/bold green]uick/-[bold green]-p[/bold green]ool/" + \
                                         f"-[bold green]-f[/bold green]ound-print][/bold yellow]", k=True, m=True),
                                         "\n", highlight=False)

            console.print(Panel(f"{E_MAIL} до {date_off}", title='лицензия', style=STL(color="white", bgcolor="blue")))


## Открывать/нет браузер с результатами поиска.
            if args.no_func is False and exists_counter >= 1:
                try:
                    if not ANDROID:
                        try:
                            webbrowser.open(f"file://{DIRPATH}/results/nicknames/html/{username}.html")
                        except Exception:
                            console.print("[bold red]Невозможно открыть web-браузер, проблемы в операционной системе.")
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
                                    if ("allow-external-apps" in line and "#" not in line) and line.split("=")[1]\
                                                                                                   .strip()\
                                                                                                   .lower() == "true":
                                        termux_sv = True

                            if termux_sv is True:
                                subprocess.run(f"termux-open {DIRPATH}/results/nicknames/html/{username}.html", shell=True)
                            else:
                                print(install_service)

                        else:
                            print(install_service)
                except Exception:
                    print(f"\n\033[31;1mНе удалось открыть результаты\033[0m")
        try:
            hardware.shutdown()
        except Exception:
            pass


## Поиск по выбранным пользователям: либо из CLI, либо из файла.
    starts(args.username) if args.user is False else starts(USERLIST)


## Arbeiten...
if __name__ == '__main__':
    try:
        main_cli()
    except KeyboardInterrupt:
        console.print(f"\n[bold red]Прерывание [italic](Ctrl + c)[/italic][/bold red]")
        if WINDOWS:
            os.kill(os.getpid(), signal.SIGBREAK)
        elif dic_binding.get('android_lame_workhorse') is True:
            os.kill(os.getpid(), signal.SIGKILL)
        else:
            [pid.terminate() for pid in active_children()]

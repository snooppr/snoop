#! /usr/bin/env python3
# Copyright (c) 2020 Snoop Project <snoopproject@protonmail.com>
"Плагины Snoop Project"

import csv
import folium
import itertools
import json
import locale
import os
import platform
import re
import random
import requests
import shutil
import socket
import sys
import threading
import time
import webbrowser

from collections import Counter
from colorama import Fore, Style, init
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from folium.plugins import MarkerCluster
from operator import itemgetter
from requests.adapters import HTTPAdapter
from requests_futures.sessions import FuturesSession
try:
    from  more_itertools import unique_everseen
    from rich.console import Console
    from rich.progress import (track,BarColumn,TimeRemainingColumn,SpinnerColumn,TimeElapsedColumn,Progress)
    from rich.table import Table
    from rich.panel import Panel
    from rich.style import Style as STL
except:
    print("Обновите lib python:\n'cd ~/snoop && python3 -m pip install -r requirements.txt'")
    sys.exit(0)
from urllib.parse import urlparse

if sys.platform == 'win32':
    locale.setlocale(locale.LC_ALL, '')

head0 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
url = "https://freegeoip.app/json/"
time_data = time.localtime()

# раскраска
init(autoreset=True)
console = Console()

def ravno():
    console.rule(characters = '=', style="cyan bold")
def helpend():
    console.rule("[bold red]Конец справки")

wZ1bad=[] #отфильтрованные ip (не ip) или отфильтрованные данные Yandex, отфильтрованные 'геокоординаты'.
azS=[] #список результатов future request.
coord=[]

class ElapsedFuturesSession(FuturesSession):
    """test_metrica: API:: https://pypi.org/project/requests-futures/"""
    def request(self, method, url, *args, **kwargs):
        """test"""
        return super(ElapsedFuturesSession, self).request(method, url, *args, **kwargs)
my_session = requests.Session()
da = requests.adapters.HTTPAdapter(max_retries=4)
my_session.mount('https://', da)

if not sys.platform == 'win32':
    sessionY = ElapsedFuturesSession(executor=ProcessPoolExecutor(max_workers=10), session=my_session)
else:
    sessionY = ElapsedFuturesSession(executor=ThreadPoolExecutor(max_workers=10), session=my_session)

dirresults = os.getcwd()
progressYa = Progress(TimeElapsedColumn(), "[progress.percentage]{task.percentage:>1.0f}%", auto_refresh=False)

def Erf(hvostfile):
    print(f"\033[31;1m\nНе могу найти/прочитать '\033[0m\033[31m{hvostfile}\033[0m\033[31;1m'!\033[0m \033[36m\nПожалуйста \
укажите текстовый файл в кодировке —\033[0m \033[36;1mutf-8.\033[0m\n")
    print("\033[36mПо умолчанию блокнот в OS Windows сохраняет текст в кодировке — ANSI\033[0m")
    print("\033[36mОткройте файл и измените кодировку [файл ---> сохранить как ---> utf-8]")
    print("\033[36mИли удалите из файла нечитаемые символы.")
    ravno()
    
def donate():
    print("")
    console.print(Panel("""[cyan]
╭donate/Buy:
├──Яндекс.Деньги (yoomoney):: [white]4100111364257544[/white]
├──Visa:: [white]4274320047338002[/white]
└──PayPal::[/cyan] [white]snoopproject@protonmail.com[/white]

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

Snoop Full Version: плагины без ограничений; 1500+ Websites; 
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

## Модуль Yandex_parser
def module3():
    while True:
        listlogin = []
        dicYa = {}

        def parsingYa(login):
# Запись в txt
            if Ya == '4':
                file_txt = open(dirresults + "/results/Yandex_parser/" + str(hvostfile) + '_' + \
                time.strftime("%d_%m_%Y_%H_%M_%S", time_data) + ".txt", "w", encoding="utf-8")
            #raise Exception("")
            else:
                file_txt = open(dirresults + "/results/Yandex_parser/" + str(login) + ".txt", "w", encoding="utf-8")

# Парсинг
            for login in listlogin:
                urlYa = f'https://yandex.ru/collections/api/users/{login}/'
                try:
                    r = sessionY.get(urlYa, headers = head0, timeout=3)
                    azS.append(r)
                except:
                    print(Fore.RED + "\nОшибка" + Style.RESET_ALL)
                    if Ya != '4':
                        ravno()
                    continue

            with progressYa:
                if Ya == '4':
                    task = progressYa.add_task("", total=len(listlogin))

                for reqY, login in zip(azS, listlogin):
                    if Ya == '4':
                        progressYa.refresh()
                        progressYa.update(task, advance=1)
                    rY=reqY.result()
                    try:
                        rdict = json.loads(rY.text)
                    except:
                        rdict = {}
                        rdict.update(public_id="Увы", display_name="-No-")

                    pub = rdict.get("public_id")
                    name = rdict.get("display_name")
                    email=str(login)+"@yandex.ru"

                    if rdict.get("display_name") == "-No-":
                        if Ya != '4':
                            print(Style.BRIGHT + Fore.RED + "\nНе сработало")
                            console.rule(characters = '=', style="cyan bold\n")
                        else:
                            wZ1bad.append(str(login))
                            continue
                        continue
                    else:
                        table1 = Table(title = "\n" + Style.BRIGHT + Fore.RED + str(login) + Style.RESET_ALL, style="green")
                        table1.add_column("Имя", style="magenta", overflow="fold")
                        table1.add_column("Логин", style="cyan", overflow="fold")
                        table1.add_column("E-mail", style="cyan", overflow="fold")
                        if Ya == '3':
                            table1.add_row(name,"Пропуск","Пропуск")
                        else:
                            table1.add_row(name,login,email)
                        console.print(table1)

                        otzyv=f"https://reviews.yandex.ru/user/{pub}"
                        market=f"https://market.yandex.ru/user/{pub}/reviews"
                        collections=f"https://yandex.ru/collections/user/{login}/"
                        if Ya == '3':
                            music=f"\033[33;1mПропуск\033[0m"
                        else:
                            music=f"https://music.yandex.ru/users/{login}/tracks"
                        dzen=f"https://zen.yandex.ru/user/{pub}"
                        qu=f"https://yandex.ru/q/profile/{pub}/"

                        print("\033[32;1mЯ.Отзывы:\033[0m", otzyv)
                        print("\033[32;1mЯ.Маркет:\033[0m", market)
                        print("\033[32;1mЯ.Картинки:\033[0m", collections)
                        print("\033[32;1mЯ.Музыка:\033[0m", music)
                        print("\033[32;1mЯ.Дзен:\033[0m", dzen)
                        print("\033[32;1mЯ.Кью:\033[0m", qu)

                        yalist=[otzyv, market, collections, music, dzen, qu]

                        file_txt.write(f"{login} | {email} | {name}\n{otzyv}\n{market}\n{collections}\n{music}\n{dzen}\n{qu}\n\n")

                    for webopen in yalist:
                        if webopen == music and Ya == '3':
                            continue
                        else:
                            webbrowser.open(webopen)
            ravno()
            azS.clear()

# сохранение в html
            if Ya == '4':
# запись в txt концовка
                file_txt.write(f"\nНеобработанные данные из файла '{hvostfile}' ({len(wZ1bad)}):\n")
                for badsites in wZ1bad:
                    file_txt.write(f"{badsites}\n")
                file_txt.write(f"\nОбновлено: " + time.strftime("%d/%m/%Y_%H:%M:%S", time_data) + ".")
                file_txt.close()
    # Конец функции

        print(
"\n\033[36m[\033[0m\033[32;1m1\033[0m\033[36m] --> Указать логин пользователя\n\
[\033[0m\033[32;1m2\033[0m\033[36m] --> Указать публичную ссылку на Яндекс.Диск\n\
[\033[0m\033[32;1m3\033[0m\033[36m] --> Указать идентификатор пользователя\n\
[\033[0m\033[32;1m4\033[0m\033[36m] --> Указать файл с именами пользователей\n\
[\033[0m\033[32;1mhelp\033[0m\033[36m] --> Справка\n\
[\033[0m\033[31;1mq\033[0m\033[36m] --> Выход\n")

        Ya = input()

# Выход
        if Ya == "q":
            print(Style.BRIGHT + Fore.RED + "Выход")
            sys.exit()

# Help
        elif Ya == "help":
            print("""\033[32;1m└──[Справка]

Однопользовательский режим\033[0m
\033[32m* Логин — левая часть до символа '@', например, bobbimonov@ya.ru, логин
'\033[36mbobbimonov\033[0m\033[32m'.
* Публичная ссылка на Яндекс.Диск — это ссылка для скачивания/просмотра материалов,
которую пользователь выложил в публичный доступ, например,
'\033[36mhttps://yadi.sk/d/7C6Z9q_Ds1wXkw\033[0m\033[32m'.
* Идентификатор — хэш, который указан в url на странице пользователя,
например, в сервисе Я.Район: https://local.yandex.ru/users/tr6r2c8ea4tvdt3xmpy5atuwg0/
идентификатор — '\033[36mtr6r2c8ea4tvdt3xmpy5atuwg0\033[0m\033[32m'.
Плагин Yandex_parser выдает меньше информации по идентификатор-у пользователя
(в сравнении с другими методами), причина — fix уязвимости от Яндекса.

По окончанию успешного поиска выводится отчёт в CLI, сохраняется в txt и
открывается браузер с персональными страницами пользователя в сервисах Яндекс-а.

\033[32;1mМногопользовательский режим\033[0m
\033[32m* Файл с именами пользователей — файл (в кодировке UTF-8 с расширеннием .txt или без него), в котором записаны логины.
Каждый логин в файле должен быть записан с новой строки, например:

\033[36mbobbimonov
username
username2
username3
случайная строка\033[0m

\033[32mПри использовании многопользовательского режима по окончанию поиска (быстро)
открывается браузер с расширенным отчётом, в котором перечислены:
логины пользователей; их имена; e-mail's и их персональные ссылки на сервисы Яндекса.

Плагин генерирует, но не проверяет 'доступность' персональных страниц пользователей
по причине: частая защита страниц Я.капчей.

Все результаты сохраняются в '\033[36m~/snoop/results/Yandex_parser/*\033[0m\033[32m'\033[0m""")
            helpend()

# Указать login
        elif Ya == '1':
            print("\033[36m└──Введите username/login разыскиваемого пользователя, например,\033[0m\033[32;1m bobbimonov\033[0m\n")
            login = input()
            listlogin.append(login)

            parsingYa(login)

# Указать ссылку на Я.Диск
        elif Ya == '2':
            print("\033[36m└──Введите публичную ссылку на Яндекс.Диск, например,\033[0m\033[32;1m https://yadi.sk/d/7C6Z9q_Ds1wXkw\033[0m\n")
            urlYD = input()

            try:
                r2 = my_session.get(urlYD, headers = head0, timeout=3)
            except:
                print(Fore.RED + "\nОшибка" + Style.RESET_ALL)
                console.rule(characters = '=', style="cyan bold\n")
                continue
            try:
                login = r2.text.split('displayName":"')[1].split('"')[0]
            except:
                login = "NoneStop"
                print(Style.BRIGHT + Fore.RED + "\nНе сработало")

            if login != "NoneStop":
                listlogin.append(login)
                parsingYa(login)

# Указать идентиффикатор Яндекс пользователя
        elif Ya == '3':
            print("\033[36m└──Введите идентификатор пользователя Яндекс, например,\033[0m\033[32;1m tr6r2c8ea4tvdt3xmpy5atuwg0\033[0m\n")
            login = input()
            listlogin.append(login)

            if len(login) != 26:
                print(Style.BRIGHT + Fore.RED + "└──Неверно указан идентификатор пользователя" + Style.RESET_ALL)
                ravno()
            else:
                parsingYa(login)

# Указать файл с логинами
        elif Ya == '4':
            print("\033[31;1m└──В Demo version этот метод плагина недоступен\033[0m\n")
            donate()
        else:
            print(Style.BRIGHT + Fore.RED + "└──Неверный выбор" + Style.RESET_ALL)
            ravno()

## Модуль Reverse Vgeocoder
def module2():
    while True:
        print("""
\033[36m[\033[0m\033[32;1m1\033[0m\033[36m] --> Выбрать файл\n\
[\033[0m\033[32;1mhelp\033[0m\033[36m] --> Справка\n\
[\033[0m\033[31;1mq\033[0m\033[36m] --> Выход\n""")

        Vgeo  = input()

# Выход
        if Vgeo == "q":
            print(Style.BRIGHT + Fore.RED + "Выход")
            sys.exit()

# Help
        elif Vgeo == "help":
            print("""\033[32;1m└──[Справка]\033[0m
\033[32m
В Snoop Project поддерживается два режима геокодирования:
Метод '\033[32;1mПростой\033[0m\033[32m':: На карте OSM расставляются маркеры по координатам. Все маркеры подписаны геометками.
Для данного метода доступны сокращенные отчёты с геометками в html формате и статистической информацией в txt формате.

Метод '\033[32;1mПодробный\033[0m\033[32m':: На карте OSM расставляются маркеры по координатам. Все маркеры подписаны геометками; странами;
округами и городами. Статистические отчёты (с расширенной геоинформацией, а также расчётом количественной информацией процентного
соотношения) сохраняются с подробностями в [txt.html.csv] форматах.
Данный метод довольно точно расставляет маркеры с геометками, но подписывает их адресом к ближайшим населенным пунктам
от 2000 человек. Например, если пользователь загрузит для обработки, координаты указывающие в 500 метрах от г. Выкса (лес),
то маркер на карте OSM встанет точно (в лесу), а подписан он будет примерно так: 'Ш:55.3301 Д:42.2604::Страна:RU::ГородскойОкруг1:
Nizjnij Novgorod::ГородскойОкруг2:Vyksa'. То есть метод работает на основе — 'Евклидово дерево'.

\033[32;1mПлагин Reverse Vgeocoder\033[0m \033[32m- работает в оффлайн режиме и укомплектован гео-БД (БД предоставляются под свободной лицензией от
download.geonames.org/export/dump/). То есть для работы плагина не требуется выход в сеть.

Для визуализации данных на карте OSM укажите (при запросе) текстовый файл с координатами в кодировке utf-8 (с расширением .txt или без расширения).
Каждая точка координат (широта, долгота) с новой строки в файле (желательно).
Snoop довольно умён: распознаёт и выбирает геокоординаты через запятую, пробел'ы или делает интеллектуальную выборку, вычищая случайные строки.
Пример файла с координатами (как может быть записан файл с координатами, который необходимо указывать):
\033[36m
51.352, 108.625
55.466,64.776
52.40662,66.77631
53.028 -104.680
54.505    73.773
Москва55.75, 37.62 Калининград54.71, 20.51 Ростов-на-Дону47.23, 39.72
случайная_строка1, которая_будет обработана Казань 55.7734/49.1436
случайная строка2, которая не будет обработана
\033[0m\033[32m
По окончанию рендеринга откроется webrowser с результатом.
Все результаты сохраняются в '~/snoop/results/ReverseVgeocoder/*[.txt.html.csv]'

Это удобный плагин, если пользователю необходимо, например, не только обработать геокоординаты, но и найти хаотичные данные - или наоборот.""")
            helpend()

# выбрать файл с геокоординатами
        elif Vgeo == '1':
            float_patern = '[-]? (?: (?: \d* \. \d+ ))'
            rx = re.compile(float_patern, re.VERBOSE)
            while True:
                print("\033[36m└──Введите \033[0m\033[32;1mабсолютный путь\033[0m \033[36mк файлу (кодировка файла -> utf-8) с данными: \n\
        [геокоординаты] или перетащите файл в окно терминала\033[0m\n")
                put = input()
                if sys.platform == 'win32':
                    put=put.replace('"', '').strip()
                else:
                    put=put.replace("'", "").strip()

# Создание карты 'Обратный геокодер'

                maps = folium.Map(location=[48.5, -33.2], zoom_start = 2)
                marker_cluster = MarkerCluster().add_to(maps)
# Проверка пути файла с координатами
                try:
                    with open(put, "r", encoding="utf8") as geo:
# Выборка геокоординат
                        for line in geo.readlines():
                            a1=line[:-1]
                            s=rx.findall(a1)
                            s_bad = not rx.findall(a1)
                            wZ1bad.append(str(a1) if s_bad==True else "")
                            if len(s)==0 or len(s)==1 or len(s)==3 or len(s)==5 or len(s) >=7:
                                wZ1bad.append(', '.join(s))
                                continue
                            try:
                                coord.append(list(map(float, s[4:6]))) if s[4:6] else ""
                            except:
                                pass
                            try:
                                coord.append(list(map(float, s[2:4]))) if s[2:4] else ""
                            except:
                                pass
                            try:
                                coord.append(list(map(float, s[0:2]))) if s[0:2] else ""
                            except:
                                pass
# Удалили дубли
                        coord2 = list(unique_everseen(coord))
                        coord.clear()
# Конец выборки
                        if sys.platform == 'win32':
                            print('\033[32;1m|\n└──Good!\033[0m')
                        else:
                            print('\033[32;1m┃\n┗━━Good!\033[0m')
                    break
                except:
                    print("\033[31;1m└──Указан неверный путь. Укажите правильный абсолютный путь к файлу или перетащите файл в окно терминала\033[0m")
                    hvostput = os.path.split(put)[1].replace('"', '')
                    Erf(hvostput)

            while True:
                print(
"""\n\033[36m╭Выберите режим геокодирования:\033[0m
\033[36m├──\033[36m[\033[0m\033[32;1m1\033[0m\033[36m] --> Простой\033[0m
\033[36m├──\033[36m[\033[0m\033[32;1m2\033[0m\033[36m] --> Подробный\033[0m
\033[36m└──\033[36m[\033[0m\033[31;1mq\033[0m\033[36m] --> Выход\033[0m\n""")
                rGeo = input()

                if rGeo == "q" or rGeo == '1' or rGeo == '2':
                    break
                else:
                    print(Style.BRIGHT + Fore.RED + "└──Неверный выбор" + Style.RESET_ALL)
                    ravno()

            if rGeo == "q":
                print(Style.BRIGHT + Fore.RED + "Выход")
                break
                sys.exit()
            if rGeo == '1':
                timestartR = time.time()
                with console.status("[green bold]Ожидайте, идёт геокодирование...",spinner=random.choice(["dots", "dots12"])):
                    n_yes=0
                    for geo_sh_do in coord2:
# Гео ш-д от +-90/+-180
                        if not -90.1 <= geo_sh_do[0] <=90.1 or not -180.1 <= geo_sh_do[1] <=180.1:
                            wZ1bad.append(str(geo_sh_do))
                            continue
                        n_yes+=1
                        coord.append(geo_sh_do)
# 1. Простой метод
                        try:
                            if rGeo == '1':
                                folium.Marker(location=geo_sh_do, popup="Ш:" + str(geo_sh_do[0]) + \
                                " Д:" + str(geo_sh_do[1]), icon=folium.Icon(color='blue', icon='ok-sign')).add_to(marker_cluster)
# 2. Подробный метод
                        except:
                            continue
# Сохранение карты osm
                    namemaps = time.strftime("%d_%m_%Y_%H_%M_%S", time_data)
                    namemaps = (f'Maps_{namemaps}.html')
                    mapsme = str(dirresults + "/results/ReverseVgeocoder/" + str(namemaps))
                    maps.save(mapsme)
# Обработка bad (извлечение вложенного списка)
                    wZ1bad_raw=[]
                    for i in wZ1bad:
                        [wZ1bad_raw.append(i2) for i2 in i] if isinstance(i, list) else wZ1bad_raw.append(i)
                    wZ1bad_raw2 = list(unique_everseen(wZ1bad_raw))
                    wZ1bad_raw2.remove('')
# Кол-во обработанных координат
                    lcoord, lwZ1bad = n_yes, len(wZ1bad_raw2)

                hvostR = os.path.split(put)[1]
                timefinishR = time.time() - timestartR

                print(Style.RESET_ALL + Fore.CYAN +f"├─Время обработки файла '\033[36;1m{hvostR}\033[0m\033[36m' -->",
                "\033[36;1m(%.0f" % float(timefinishR) +"sec)")
                print(Style.RESET_ALL + Fore.CYAN +f"├─Успешно обработано --> '\033[32;1m{lcoord}\033[0m\033[36m' геокоординат")
                if lwZ1bad >= 1:
                    print(Style.RESET_ALL + Fore.CYAN +f"├─Отброшено --> '\033[31;1m{lwZ1bad}\033[0m\033[36m' случайных данных")
                print(Style.RESET_ALL + Fore.CYAN + "└──Статистические результаты сохранены в: " + Style.RESET_ALL + \
                f"\033[36;1m{dirresults}/results/ReverseVgeocoder/{hvostR}[.txt.html.csv]")
                try:
                    if lcoord >= 1:
                        webbrowser.open(str("file://" + mapsme))
                except:
                    pass
# Запись в txt
                try:
                    file_txtR = open(dirresults + "/results/ReverseVgeocoder/" + str(hvostR) + ".txt", "w", encoding="utf-8")
                except:
                    pass
                file_txtR.write(f"Полученные и обработанные данные из файла '{hvostR}' ({lcoord}):\n")
                for coord_geo in coord:
                    coord_geo=",".join([str(i) for i in coord_geo])
                    file_txtR.write(f"{coord_geo}\n")
                file_txtR.write("===================================" + "\n\n")
                file_txtR.write(f"Необработанные данные из файла '{hvostR}' ({lwZ1bad}):\n")
                for badGEO in wZ1bad_raw2:
                    file_txtR.write(f"{badGEO}\n")
                file_txtR.write("===================================" + "\n\n")
                file_txtR.write(time.strftime(f"Дата обработки файла '{hvostR}': %d_%m_%Y_%H_%M_%S", time_data))
                file_txtR.close()
            if rGeo == '2':
                print("\033[31;1m└──В Demo version этот метод плагина недоступен\033[0m\n")
                donate()
            break
            sys.exit()
            #coord.clear(), coord2.clear(), wZ1bad.clear()
        else:
            print(Style.BRIGHT + Fore.RED + "└──Неверный выбор" + Style.RESET_ALL)
            ravno()

## Модуль GEO_IP/domain
def module1():
# Домен > IPv4/v6
    def res46(dipp):
        try:
            res46 = socket.getaddrinfo(f"{dipp}", 80)
        except:
            pass
        try:
            res4 = res46[0][4][0]
        except:
            res4 = "-"
        try:
            if ":" not in res46[-1][4][0]:
                res6 = "-"
            else:
                res6 = res46[-1][4][0]
        except:
            res6 = "-"
        #print(res46)
        return res4, res6

# Запрос future request
    def reqZ():
        try:
            r=req.result()
            return r.text
        except requests.exceptions.ConnectionError:
            print(Fore.RED + "\nОшибка соединения\n" + Style.RESET_ALL)
        except requests.exceptions.Timeout:
            print(Fore.RED + "\nОшибка таймаут\n" + Style.RESET_ALL)
        except requests.exceptions.RequestException:
            print(Fore.RED + "\nОшибка не идентифицирована\n" + Style.RESET_ALL)
        except requests.exceptions.HTTPError:
            print(Fore.RED + "\nОшибка HTTPS\n" + Style.RESET_ALL)
        return "Err"

# Выбор поиска одиночный или '-f'
    ravno()
    print("\n\033[36mВведите домен (пример:\033[0m \033[32;1mexample.com\033[0m\033[36m), или IPv4/IPv6 (пример:\033[0m \033[32;1m8.8.8.8\033[0m\033[36m),\n\
или url (пример: \033[32;1mhttps://example.com/1/2/3/foo\033[0m\033[36m), \n\
или укажите файл_с данными, выбрав ключ (пример:\033[0m \033[32;1m--file\033[0m\033[36m или\033[0m \033[32;1m-f\033[0m\033[36m)\n\
[\033[0m\033[32;1m-f\033[0m\033[36m] --> обработатка файла данных\n\
[\033[0m\033[32;1menter\033[0m\033[36m] --> информация о своем GEO_IP\n\
[\033[0m\033[31;1mq\033[0m\033[36m] --> Выход")
    dip = input("\n")

# выход
    if dip == "q":
        print(Style.BRIGHT + Fore.RED + "Выход")
        sys.exit()

# проверка данных
    elif dip == '--file' or dip == '-f':
        while True:
            print("""\033[36m├──Выберите тип поиска
│
[\033[0m\033[32;1m1\033[0m\033[36m] --> Online (медленно)
[\033[0m\033[32;1m2\033[0m\033[36m] --> Offline (быстро)
[\033[0m\033[32;1m3\033[0m\033[36m] --> Offline_тихий (очень быстро)
[\033[0m\033[32;1mhelp\033[0m\033[36m] --> Справка\n\
[\033[31;1mq\033[0m\033[36m] --> Выход\033[0m""")

            dipbaza = input('\n')

# Выход
            if dipbaza == "q":
                print("\033[31;1mВыход\033[0m")
                sys.exit(0)
# Справка
            elif dipbaza == "help":
                print("\033[32;1m└──Справка\033[0m\n")
                print("""\033[32mРежим '\033[32;1mOnline поиск\033[0m\033[32m'. Модуль GEO_IP/domain от Snoop Project использует публичный api
и создает статистическую и визуализированную информацию по ip/url/domain цели (массиву данных)
    (ограничения: запросы ~15к/час, невысокая скорость обработки данных, отсутствие информации о провайдерах).
Преимущества использования 'Online поиска':
в качестве входных данных можно использовать не только ip-адреса, но и domain/url.
Пример файла с данными (список.txt):

\033[36m1.1.1.1
2606:2800:220:1:248:1893:25c8:1946
google.com
https://example.org/fo/bar/7564
случайная строка\033[0m

\033[32mРежим '\033[32;1mOffline поиск\033[0m\033[32m'. Модуль GEO_IP/domain от Snoop Project использует специальные базы данных
и создает статистическую и визуализированную информацию только по ip цели (массиве данных)
    (базы данных доступны свободно от компании Maxmind).
Преимущества использования 'Offline поиска': скорость (обработка тысяч ip без задержек),
стабильность (отсутствие зависимости от интернет соединения и персональных настроек DNS/IPv6 пользователя),
масштабный охват/покрытие (предоставляется информация об интернет-провайдерах).

Режим '\033[32;1mOffline_тихий поиск\033[0m\033[32m':: Тот же режим, что и режим 'Offline', но не выводит на печать промежуточные таблицы с данными.
Даёт прирост в производительности в ~4 раза.
Пример файла с данными (список.txt):

\033[36m8.8.8.8
93.184.216.34
2606:2800:220:1:248:1893:25c8:1946
случайная строка\033[0m

\033[32mSnoop довольно умён и способен определять и различать во входных данных: IPv4/v6/domain/url, вычищая ошибки и случайные строки.
По окончанию обработки данных пользователю предоставляются:
статистические отчеты в [txt/csv и визуализированные данные на карте OSM].

Примеры для чего можно использовать модуль GEO_IP/domain от Snoop Project.
Например, если у пользователя имеется список ip адресов от DDoS атаки,
он может проанализировать откуда исходила  max/min атака и от кого (провайдеры).
Например, решая квесты CTF, где используются GPS/IPv4/v6.\033[0m""")
                helpend()

# Оффлайн поиск
# Открываем GeoCity
            elif dipbaza == "2" or dipbaza == "3":
                while True:
                    print("\033[31;1m└──В Demo version этот метод плагина недоступен\033[0m\n")
                    donate()
                    break

                break

# Онлайн поиск
            elif dipbaza == "1":
                print("\033[31;1m└──В Demo version этот метод плагина недоступен\033[0m\n")
                donate()
                break

# Неверный выбор ключа при оффлайн/онлайн поиске. Выход
            else:
                print(Style.BRIGHT + Fore.RED + "└──Неверный выбор" + Style.RESET_ALL)
                ravno()

# одиночный запрос
    else:
        if dip == "":
            pass
            uu3 = dip
        else:
            u = urlparse(dip).hostname
            uu3 = dip
            if bool(u) == False:
                dip=dip.split("/")[0].strip()
            else:
                dip=u.replace("www.", "").strip()
        session = requests.Session()
        url2 = 'https://freegeoip.app/json/{}'.format(dip)
        try:
            r=session.get(url=url2, headers = head0, timeout=3)
            dip1 = r.text
            dip_dic = json.loads(dip1)
            T1=dip_dic.get("country_code")
            T2=dip_dic.get("time_zone")
            T3=dip_dic.get("latitude")
            T4=dip_dic.get("longitude")
            T5=dip_dic.get("ip")
        except:
            T1="-"
            T2="-"
            T3="stop"
            T4="stop"
            T5="-"
            print("""\033[31;1m\n
|\ | _ ._  _
| \|(_)| |(/_
        \033[0m""")

# IP/Домен > Домен и IPv4v6
        try:
            resD1=socket.getfqdn(dip)
            res4, res6 = res46(resD1)
        except:
            resD1="-"
            print("err")

        table = Table(title = Style.BRIGHT + Fore.RED + str(uu3) + Style.RESET_ALL, style="green")
        table.add_column("Сountry", style="magenta")
        if dip == "":
            table.add_column("Your IP", style="cyan", overflow="fold")
        else:
            table.add_column("IPv4", style="cyan", overflow="fold")
            table.add_column("IPv6", style="cyan", overflow="fold")
        table.add_column("Domain", style="green", overflow="fold")
        table.add_column("Time_Zone", style="green", overflow="fold")
        if dip == "":
            table.add_row(T1,T5,resD1,T2)
        else:
            table.add_row(T1,res4,res6,resD1,T2)
        console.print(table)
        if T3 == "stop" and T4 =="stop":
            print("\n")
            URL_GEO = ""
        else:
            URL_GEO = f"https://www.openstreetmap.org/#map=13/{T3}/{T4}"
            URL_GEO2 = f"https://www.google.com/maps/@{T3},{T4},28m/data=!3m1!1e3"
            print(Style.BRIGHT + Fore.BLACK + f"{URL_GEO}" + Style.RESET_ALL)
            print(Style.BRIGHT + Fore.BLACK + f"{URL_GEO2}\n" + Style.RESET_ALL)

        module1()
if __name__ == "__main__":
    module1()

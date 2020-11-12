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
from requests.adapters import HTTPAdapter
from requests_futures.sessions import FuturesSession
from rich.console import Console
from rich.progress import (Progress, TimeRemainingColumn)
from rich.table import Table
from urllib.parse import urlparse

if sys.platform == 'win32':
    locale.setlocale(locale.LC_ALL, '')

init(autoreset=True)
head0 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
url = "https://freegeoip.app/json/"
time_data = time.localtime()
wZ1bad=[] #отфильтрованные ip (не ip) или отфильтрованные данные Yandex

class ElapsedFuturesSession(FuturesSession):
    """test_metrica: API:: https://pypi.org/project/requests-futures/"""
    def request(self, method, url, *args, **kwargs):
        """test"""
        return super(ElapsedFuturesSession, self).request(method, url, *args, **kwargs)
my_session = requests.Session()
da = requests.adapters.HTTPAdapter(max_retries=8)
my_session.mount('https://', da)

if not sys.platform == 'win32':
    session1 = ElapsedFuturesSession(executor=ProcessPoolExecutor(max_workers=10), session=my_session)
else:
    session1 = ElapsedFuturesSession(executor=ThreadPoolExecutor(max_workers=10), session=my_session)

dirresults = os.getcwd()

def Erf(hvostfile):
    print(f"\033[31;1m\nНе могу найти/прочитать '\033[0m\033[31m{hvostfile}\033[0m\033[31;1m'!\033[0m \033[36m\nПожалуйста \
укажите текстовый файл в кодировке —\033[0m \033[36;1mutf-8.\033[0m\n")
    print("\033[36mПо умолчанию блокнот в OS Windows сохраняет текст в кодировке — ANSI\033[0m")
    print("\033[36mОткройте файл и измените кодировку [файл ---> сохранить как ---> utf-8]")
    print("\033[36mИли удалите из файла нечитаемые символы.")
    print("\033[36;1m================================================================\033[0m\n")

# Модуль Yandex_parser
def module3():
    while True:
        listlogin = []
        dicYa = {}

        def parsingYa(login):
            # Запись в txt
            if Ya == '4':
                file_txt = open(dirresults + "/results/Yandex_parser/" + str(hvostfile) + '_' + time.strftime("%d_%m_%Y_%H_%M_%S", time_data) + ".txt", "w", encoding="utf-8")
            # raise Exception("")
            else:
                file_txt = open(dirresults + "/results/Yandex_parser/" + str(login) + ".txt", "w", encoding="utf-8")

            progressYa = Progress("[progress.percentage]{task.percentage:>3.0f}%", auto_refresh=False)

    # Парсинг
            for login in progressYa.track(listlogin, description=""):
                urlYa = f'https://yandex.ru/collections/api/users/{login}/'
                try:
                    r = my_session.get(urlYa, headers = head0, timeout=3)
                except:
                    print(Fore.RED + "\nОшибка\n" + Style.RESET_ALL)
                    continue
                try:
                    rdict = json.loads(r.text)
                except:
                    rdict = {}
                    rdict.update(public_id="Увы", display_name="-No-")

                pub = rdict.get("public_id")
                name = rdict.get("display_name")
                email=str(login)+"@yandex.ru"

                if rdict.get("display_name") == "-No-":
                    if Ya != '4':
                        print(Style.BRIGHT + Fore.RED + "\nНе сработало")
                    else:
                        wZ1bad.append(str(login))
                        continue
                    continue
                else:
                    table1 = Table(title = "\n" + Style.BRIGHT + Fore.RED + str(login) + Style.RESET_ALL, style="green")
                    table1.add_column("Имя", style="magenta")
                    table1.add_column("Логин", style="cyan")
                    table1.add_column("E-mail", style="cyan")
                    if Ya == '3':
                        table1.add_row(name,"Пропуск","Пропуск")
                    else:
                        table1.add_row(name,login,email)
                    console = Console()
                    console.print(table1)

                    market=f"https://market.yandex.ru/user/{pub}/reviews"
                    collections=f"https://yandex.ru/collections/user/{login}/"
                    if Ya == '3':
                        music=f"\033[33;1mПропуск\033[0m"
                    else:
                        music=f"https://music.yandex.ru/users/{login}/tracks"
                    dzen=f"https://zen.yandex.ru/user/{pub}"
                    qu=f"https://yandex.ru/q/profile/{pub}/"
                    raion=f"https://local.yandex.ru/users/{pub}/"

                    print("\033[32;1mЯ.Маркет:\033[0m", market)
                    print("\033[32;1mЯ.Картинки:\033[0m", collections)
                    print("\033[32;1mЯ.Музыка:\033[0m", music)
                    print("\033[32;1mЯ.Дзен:\033[0m", dzen)
                    print("\033[32;1mЯ.Кью:\033[0m", qu)
                    print("\033[32;1mЯ.Район:\033[0m", raion)

                    yalist=[market, collections, music, dzen, qu, raion]

                    file_txt.write(f"{login} | {email} | {name}\n{market}\n{collections}\n{music}\n{dzen}\n{qu}\n{raion}\n\n\n",)
                    progressYa.refresh()

                for webopen in yalist:
                    if webopen == music and Ya == '3':
                        continue
                    else:
                        webbrowser.open(webopen)

            if Ya == '4':
    # запись в txt концовка
                file_txt.write(f"\nНеобработанные данные из файла '{hvostfile}':\n")
                for badsites in wZ1bad:
                    file_txt.write(f"{badsites}\n")
                file_txt.write(f"\nОбновлено: " + time.strftime("%d/%m/%Y_%H:%M:%S", time_data) + ".")
                file_txt.close()
    # Конец функции

        if sys.platform != 'win32':
            Ya = input("\033[36m[\033[0m\033[32;1m1\033[0m\033[36m] --> Указать логин пользователя\n\
[\033[0m\033[32;1m2\033[0m\033[36m] --> Указать публичную ссылку на Яндекс.Диск\n\
[\033[0m\033[32;1m3\033[0m\033[36m] --> Указать идентификатор пользователя\n\
[\033[0m\033[32;1m4\033[0m\033[36m] --> Указать файл с именами пользователей\n\
[\033[0m\033[32;1mhelp\033[0m\033[36m] --> Справка\n\
[\033[0m\033[31;1mq\033[0m\033[36m] --> Выход\n\033[36;1m================================================================\033[0m\n\n")
        else:
            Ya = input("[1] --> Указать логин пользователя\n\
[2] --> Указать публичную ссылку на Яндекс.Диск\n\
[3] --> Указать идентификатор пользователя\n\
[4] --> Указать файл с именами пользователей\n\
[help] --> Справка\n\
[q] --> Выход\n================================================================\n\n")

        # Выход
        if Ya == "q":
            print(Style.BRIGHT + Fore.RED + "Выход")
            sys.exit()

    # Help
        elif Ya == "help":
            print("""\033[32;1m└──[Справка]

Однопользовательский режим\033[0m
\033[32m* Логин — левая часть до символа '@', например, bobbimonov@ya.ru, логин '\033[36mbobbimonov\033[0m\033[32m'.
* Публичная ссылка на Яндекс.Диск — это ссылка для скачивания/просмотра материалов,
которую пользователь выложил в публичный доступ, например '\033[36mhttps://yadi.sk/d/7C6Z9q_Ds1wXkw\033[0m\033[32m'.
* Идентификатор — хэш, который указан в url на странице пользователя,
например, в сервисе Я.Район: https://local.yandex.ru/users/tr6r2c8ea4tvdt3xmpy5atuwg0/
идентификатор — '\033[36mtr6r2c8ea4tvdt3xmpy5atuwg0\033[0m\033[32m'.
Плагин Yandex_parser выдает меньше информации по идентификатор-у пользователя
(в сравнении с другими методами), причина — fix уязвимости от Яндекса.

По окончанию успешного поиска выводится отчёт в CLI, сохраняется в txt и
открывается браузер с персональными страницами пользователя в сервисах Яндекс-а.

\033[32;1mМногопользовательский режим\033[0m
\033[32m* Файл с именами пользователей — файл (с расширеннем .txt или без него), в котором записаны логины.
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

Все результаты сохраняются в '\033[36m~/snoop/results/Yandex_parser/*\033[0m\033[32m'\033[0m
""")
            print("\033[36;1m================================================================\033[0m")
    # Указать login
        elif Ya == '1':
            if sys.platform != 'win32':
                login = input("\033[36m└──Введите username/login разыскиваемого пользователя, например,\033[0m\033[32;1m bobbimonov\033[0m\n")
            else:
                login = input("└──Введите username/login разыскиваемого пользователя, например, bobbimonov\n")
            listlogin.append(login)

            parsingYa(login)

# Указать ссылку на Я.Диск
        elif Ya == '2':
            if sys.platform != 'win32':
                urlYD = input("\033[36m└──Введите публичную ссылку на Яндекс.Диск, например,\033[0m\033[32;1m https://yadi.sk/d/7C6Z9q_Ds1wXkw\033[0m\n")
            else:
                urlYD = input("└──Введите публичную ссылку на Яндекс.Диск, например, https://yadi.sk/d/7C6Z9q_Ds1wXkw\n")

            try:
                r2 = my_session.get(urlYD, headers = head0, timeout=3)
            except:
                print(Fore.RED + "\nОшибка\n" + Style.RESET_ALL)
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
            if sys.platform != 'win32':
                login = input("\033[36m└──Введите идентификатор пользователя Яндекс, например,\033[0m\033[32;1m tr6r2c8ea4tvdt3xmpy5atuwg0\033[0m\n")
            else:
                login = input("└──Введите идентификатор пользователя Яндекс, например, tr6r2c8ea4tvdt3xmpy5atuwg0\n")
            listlogin.append(login)

            if len(login) != 26:
                print(Style.BRIGHT + Fore.RED + "└──Неверно указан идентификатор пользователя\n" + Style.RESET_ALL)
            else:
                parsingYa(login)

# Указать файл с логинами
        elif Ya == '4':
            print("\033[31;1m└──В Demo version этот метод плагина недоступен\033[0m\n")
        else:
            print(Style.BRIGHT + Fore.RED + "├──Неверный выбор" + Style.RESET_ALL)

# Модуль Vgeocoder
def module2():
    try:
        os.makedirs(str(dirresults + "/results/ReverseVgeocoder"))
    except:
        pass
    while True:
        if sys.platform != 'win32':
            Vgeo = input("\033[36m[\033[0m\033[32;1m1\033[0m\033[36m] --> Выбрать файл\n\
[\033[0m\033[32;1mhelp\033[0m\033[36m] --> Справка\n\
[\033[0m\033[31;1mq\033[0m\033[36m] --> Выход\n\033[36;1m================================================================\033[0m\n\n")
        else:
            Vgeo = input("[1] --> Выбрать файл\n\
[help] --> Справка\n\
[q] --> Выход\n================================================================\n\n")

    # Выход
        if Vgeo == "q":
            print(Style.BRIGHT + Fore.RED + "Выход")
            sys.exit()

    # Help
        elif Vgeo == "help":
            print("""\033[32;1m└──[Справка]\033[0m
\033[32m
Для визуализации данных на карте OSM укажите (при запросе) файл с координатами (с расширением .txt или без расширения).
Каждая точка координат (широта, долгота) с новой строки в файле.
Snoop довольно умён: распознаёт координаты через запятую или пробел'ы и вычищает случайные строки.
Пример файла с координатами (как может быть записан файл с координатами, который необходимо указывать):
\033[36m
51.352, 108.625
55.466,64.776
52.40662,66.77631
53.028 -104.680
54.505    73.773
случайная строка
\033[0m\033[32m
По окончанию рендеринга откроется webrowser с результатом.
Все результаты сохраняются в '~/snoop/results/ReverseVgeocoder/Maps_date'
""")
            print("\033[36;1m================================================================\033[0m")

    # выбрать файл с геокоординатами
        elif Vgeo == '1':
            if sys.platform != 'win32':
                put = input("\033[36m└──Введите \033[0m\033[32;1mабсолютный путь\033[0m \033[36mк файлу (кодировка файла -> utf-8) с массивом данных: \n\
    [геокоординаты] или перетащите файл в окно терминала\033[0m\n")
                put=put.replace("'", "").strip()
            else:
                put = input("└──Введите абсолютный путь к файлу (кодировка файла -> utf-8) с массивом данных: \n\
    [геокоординаты] или перетащите файл в окно терминала\n")
                put=put.replace('"', "").strip()

    # Проверка пути файла с координатами
            if not os.path.exists(put):
                print("\033[31;1m└──Указан неверный путь. Укажите правильный абсолютный путь к файлу или перетащите файл в окно терминала\033[0m")

    # Создание карты 'Обратный геокодер'
            try:
                maps = folium.Map(location=[48.5, -33.2], zoom_start = 2)
                marker_cluster = MarkerCluster().add_to(maps)

                with open(put, "r", encoding="utf8") as geo:
                    Geo = geo.read().splitlines() #список готов

                    coord2=[]
                    for a1 in Geo:
                        try:
                            if "," in a1:
                                 g1=(a1.split(','))
                            elif any(' ' in a1 for a1 in a1):
                                 g1=(a1.split())
                            g11=float(g1[0])
                            g22=float(g1[1])
                            coord2.append(g11)
                            coord2.append(g22)
                            folium.Marker(location=coord2, popup="Ш:" + str(g11) + \
                            " Д:" + str(g22), icon=folium.Icon(color='blue', icon='ok-sign'),).add_to(marker_cluster)
                        except:
                            continue
                        coord2.clear()

                    namemaps = time.strftime("%d_%m_%Y_%H_%M_%S", time_data)
                    namemaps = (f'Maps_{namemaps}.html')
                    mapsme = str(dirresults + "/results/ReverseVgeocoder/" + str(namemaps))
                    maps.save(mapsme)
                    print("\033[32;1m\nГотово!\033[0m")

                    try:
                        webbrowser.open(str("file://" + mapsme))
                    except:
                        pass
                    break
                    sys.exit(0)
            except:
                hvostput = os.path.split(put)[1]
                Erf(hvostput)

        else:
            print(Style.BRIGHT + Fore.RED + "├──Неверный выбор" + Style.RESET_ALL)

# Модуль GEO/IP
def module1():
    try:
        os.makedirs(str(dirresults + "/results/domain"))
    except:
        pass
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
#            print(res46)
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
    if sys.platform != 'win32':
        dip = input("\n\033[36mВведите домен (пример:\033[0m \033[32;1mexample.com\033[0m\033[36m), или IPv4/IPv6 (пример:\033[0m \033[32;1m8.8.8.8\033[0m\033[36m),\n\
или url (пример: \033[32;1mhttps://example.com/1/2/3/foo\033[0m\033[36m), \n\
или укажите файл_массив, выбрав ключ (пример:\033[0m \033[32;1m--file\033[0m\033[36m или\033[0m \033[32;1m-f\033[0m\033[36m)\n\
[\033[0m\033[32;1m-f\033[0m\033[36m] --> обработатка массива данных\n\
[\033[0m\033[32;1menter\033[0m\033[36m] --> информация о своем GEO_IP\n\
[\033[0m\033[31;1mq\033[0m\033[36m] --> Выход\n\033[36;1m================================================================\033[0m\n\n")
    else:
        dip = input("\nВведите домен (пример: example.com), или IPv4/IPv6 (пример: 93.184.216.34),\n\
или url (пример: https://example.com/1/2/3/foo), \n\
или укажите файл_массив, выбрав ключ (пример --file или -f)\n\
[-f] --> обработатка массива данных\n\
[enter] --> информация о своем GEO_IP\n\
[q] --> Выход\n================================================================\n\n")

#выход
    if dip == "q":
        print(Style.BRIGHT + Fore.RED + "Выход")
        sys.exit()

# проверка массива
    elif dip == '--file' or dip == '-f':
        while True:
            if sys.platform == 'win32':
                dipbaza = input("Выберите тип поиска\n[1] --> Online (медленно)\n[2] --> Offline (быстро)\n"\
"[help] --> Справка\n\
[q]--> Выход\n================================================================\n\n")
            else:
                dipbaza = input("""\033[36m├──Выберите тип поиска\n[\033[0m\033[32;1m1\033[0m\033[36m] --> Online (медленно)\n[\033[0m\033[32;1m2\033[0m\033[36m] --> Offline (быстро)
[\033[0m\033[32;1mhelp\033[0m\033[36m] --> Справка\n\
[\033[31;1mq\033[0m\033[36m] --> Выход\033[0m\n
\033[36;1m================================================================\033[0m\n""")

# Выход
            if dipbaza == "q":
                print("\033[31;1mВыход\033[0m")
                sys.exit(0)
# Справка
            elif dipbaza == "help":
                print("\033[32;1m└──Справка\033[0m\n")
                print("""\033[32mМетод '\033[32;1mOnline поиск\033[0m\033[32m'. Модуль GEO_IP/domain от Snoop Project использует публичный api
и создает статистическую и визуализированную информацию по ip/url/domain цели (массиве данных)
    (ограничения: запросы ~15к/час, невысокая скорость обработки данных, отсутствие информации о провайдерах).
Преимущества использования 'Online поиска':
в качестве массива данных можно использовать не только ip-адреса, но и domain/url.
Пример файла массива данных (массив.txt):

\033[36m1.1.1.1
2606:2800:220:1:248:1893:25c8:1946
google.com
https://example.org/fo/bar/7564
случайная строка\033[0m

\033[32mМетод '\033[32;1mOffline поиск\033[0m\033[32m'. Модуль GEO_IP/domain от Snoop Project использует специальные базы данных
и создает статистическую и визуализированную информацию только по ip цели (массиве данных)
    (базы данных доступны свободно от компании Maxmind).
Преимущества использования 'Offline поиска': скорость (обработка миллионов ip без задержек),
стабильность (отсутствие зависимости от интернет соединения и персональных настроек DNS/IPv6 пользователя),
масштабный охват/покрытие (предоставляется информация о интернет-провайдерах).
Пример файла массива данных (массив.txt):

\033[36m8.8.8.8
93.184.216.34
2606:2800:220:1:248:1893:25c8:1946
случайная строка\033[0m

\033[32mSnoop довольно умён и способен определять в массиве данных: IPv4/v6/domain/url, вычищая ошибки и случайные строки.
По окончанию обработки данных пользователю предоставляются:
статистические отчеты в [txt/csv и визуализированные данные на карте OSM].

Примеры для чего можно использовать модуль GEO_IP/domain от Snoop Project.
Например, если у пользователя имеется список ip адресов от DDoS атаки,
он может проанализировать откуда исходила  max/min атака и от кого (провайдеры).
Например, решая квесты CTF, где используются GPS/IPv4/v6.\033[0m""")
                print("\033[36;1m================================================================\033[0m")

# Оффлайн поиск
# Открываем GeoCity
            elif dipbaza == "2":
                while True:
                    print("\033[31;1m└──В Demo version плагин недоступен\033[0m\n")
                    break

                break

# Онлайн поиск
            elif dipbaza == "1":
                print("\033[31;1m└──В Demo version плагин недоступен\033[0m\n")
                break
    # Неверный выбор ключа при оффлайн/онлайн поиске. Выход
            else:
                print(Style.BRIGHT + Fore.RED + "├──Неверный выбор" + Style.RESET_ALL)

#одиночный запрос
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
#            print(Fore.RED + "Err connect" + Style.RESET_ALL)
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
            table.add_column("Your IP", style="cyan")
        else:
            table.add_column("IPv4", style="cyan")
            table.add_column("IPv6", style="cyan")
        table.add_column("Domain", style="green")
        table.add_column("Time_Zone", style="green")
        if dip == "":
            table.add_row(T1,T5,resD1,T2)
        else:
            table.add_row(T1,res4,res6,resD1,T2)
        console = Console()
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

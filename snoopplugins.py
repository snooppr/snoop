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

# Модуль Vgeocoder
def module2():
    while True:
        if sys.platform != 'win32':
            Vgeo = input("\033[36m[\033[0m\033[32;1m1\033[0m\033[36m] --> Выбрать файл\n\
[\033[0m\033[32;1mhelp\033[0m\033[36m] --> Справка\n\
[\033[0m\033[31;1mq\033[0m\033[36m] --> Выход\n\033[36;1m================================================================\033[0m\n\n")
        else:
            Vgeo = input("[1] --> Выбрать файл\n\
[help] --> Справка\n\
[q] --> Выход\n================================================================\n\n")  

# выход
#    while True:
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
                put = input("Введите абсолютный путь к файлу (кодировка файла -> utf-8) с массивом данных: \n\
    [геокоординаты] или перетащите файл в окно терминала\n")
                put=put.replace('"', "").strip()

    # Проверка пути файла с координатами
            if not os.path.exists(put):
                print("\033[31;1mУказан неверный путь. Укажите правильный абсолютный путь к файлу или перетащите файл в окно терминала\033[0m")

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
                print(f"\033[31;1m\nНе могу прочитать '\033[0m\033[31m{hvostput}\033[0m\033[31;1m'!\033[0m \033[36m\nПожалуйста \
укажите текстовый файл в кодировке —\033[0m \033[36;1mutf-8.\033[0m\n")
                print("\033[36mПо умолчанию блокнот в OS Windows сохраняет текст в кодировке — ANSI\033[0m")
                print("\033[36mОткройте файл и измените кодировку [файл ---> сохранить как ---> utf-8]")
                print("\033[36mИли удалите из файла нечитаемые символы.")
                print("\033[36;1m================================================================\033[0m\n")

        else:
            print(Style.BRIGHT + Fore.RED + "├──Неверный выбор" + Style.RESET_ALL)

# Модуль GEO/IP
def module1():
    try:
        os.makedirs(str("results/domain"))
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

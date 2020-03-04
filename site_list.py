#! /usr/bin/env python3
"""Snoop: скрипт для обновления БД списка сайтов
"""

import json
import sys
import requests
import threading
import xml.etree.ElementTree as ET
from datetime import datetime
from argparse import ArgumentParser, RawDescriptionHelpFormatter

pool = list()
pool1 = list()


def get_rank(domain_to_query, dest):
    result = -1

# Получить данные рейтинга через API рейтинг Alexa.
    url = f"http://data.alexa.com/data?cli=10&url={domain_to_query}"
    xml_data = requests.get(url).text
    root = ET.fromstring(xml_data)
    try:
# Получить рейтинг для этого сайта.
        dest['rank'] = int(root.find(".//REACH").attrib["RANK"])
    except:
# Не находим
        print(f"Ошибка при получении информации о ранге для '{domain_to_query}'")
        print(f"     Возвращённый XML |{xml_data}|")

    return

parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter
                        )
parser.add_argument("--rank","-r",
                    action="store_true",  dest="rank", default=False,
                    help="Обновить все ранги сайта (не рекомендуется)."
                    )
args = parser.parse_args()

with open("bad_data.json", "r", encoding="utf8") as bad_file:
    data1 = json.load(bad_file)

with open("bad_site.md", "w", encoding="utf8") as bad_site:
    data_length1 = len(data1)
    bad_site.write(f'## Snoop БД Неподдерживаемых сайтов (список), всего — {data_length1} сайт(ов)!\n')



    for social_network_bad in data1:
        url_main_bad = data1.get(social_network_bad).get("urlMain")
        country_bad = data1.get(social_network_bad).get("country")        
        data1.get(social_network_bad)["rank"] = 0
        if args.rank:
            th1 = threading.Thread(target=get_rank, args=(url_main_bad, data1.get(social_network_bad)))
        else:
            th1 = None
        pool.append((country_bad, social_network_bad, url_main_bad, th1))
        if args.rank:
            th1.start()

    index0 = 1
    for country_bad, social_network_bad, url_main_bad, th1 in pool:
        if args.rank:
            th1.join()
        bad_site.write(f'{index0}. {country_bad} [{social_network_bad}]({url_main_bad})\n')            
        sys.stdout.write("\r{0}".format(f"Обновлено, всего — {data_length1} сайта(ов) в чёрном списке"))
        sys.stdout.flush()
        index0 = index0 + 1
        
    if args.rank:
        bad_site.write(f'\nAlexa.com rank data fetched at ({datetime.utcnow()} UTC)\n')

sorted_json_data_bad = json.dumps(data1, indent=2, sort_keys=True)

with open("bad_data.json", "w", encoding="utf8") as bad_file:
    bad_file.write(sorted_json_data_bad)

with open("data.json", "r", encoding="utf8") as data_file:
    data = json.load(data_file)

with open("sites.md", "w", encoding="utf8") as site_file:
    data_length = len(data)
    site_file.write(f'## Snoop БД поддерживаемых сайтов (список), всего — {data_length} сайт(ов)!\n')

    for social_network in data:
        url_main = data.get(social_network).get("urlMain")
        country = data.get(social_network).get("country")
        data.get(social_network)["rank"] = 0
        if args.rank:
            th = threading.Thread(target=get_rank, args=(url_main, data.get(social_network)))
        else:
            th = None
        pool1.append((country, social_network, url_main, th))
        if args.rank:
            th.start()

    index = 1
    for country, social_network, url_main, th in pool1:
        if args.rank:
            th.join()
        site_file.write(f'{index}. {country} [{social_network}]({url_main})\n')
        sys.stdout.write("\r{0}".format(f"Обновлено, всего — {data_length} поддерживаемых сайта(ов)"))
        sys.stdout.flush()
        index = index + 1
        
        
    if args.rank:
        site_file.write(f'\nAlexa.com rank data fetched at ({datetime.utcnow()} UTC)\n')

sorted_json_data = json.dumps(data, indent=2, sort_keys=True)

with open("data.json", "w", encoding="utf8") as data_file:
    data_file.write(sorted_json_data)
    
print("\n" "Обновлено, всего —" ,data_length1, "сайта(ов) в чёрном списке")
print("\nБД сайтов (.json) упорядочена по алфавиту.")

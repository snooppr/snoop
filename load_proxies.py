import csv
import requests
import time
from collections import namedtuple
from colorama import Fore, Style


def load_proxies_from_csv(path_to_list):
    """
     Функция, которая загружает прокси из CSV-файла в список.

     Входные данные: путь к CSV-файлу, содержащему прокси, описываемый полями: «ip», «port», «protocol».

     Выходы: список, содержащий прокси, хранящиеся в именованных кортежах.
    """
    Proxy = namedtuple('Proxy', ['ip', 'port', 'protocol'])

    with open(path_to_list, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        proxies = [Proxy(line['ip'],line['port'],line['protocol']) for line in csv_reader]

    return proxies


def check_proxy(proxy_ip, proxy_port, protocol):
    """
    Функция, которая проверяет прокси, пытаясь сделать запрос на указанный сайт.

    Мы используем «wikipedia.org» в качестве теста, так как мы можем проверить анонимность прокси
    путем проверки, совпадает ли возвращаемый заголовок «X-Client-IP» с прокси ip.
    """
    full_proxy = f'{protocol}://{proxy_ip}:{proxy_port}'
    proxies = {'http': full_proxy, 'https': full_proxy}
    try:
        r = requests.get('https://www.wikipedia.org',proxies=proxies, timeout=4)
        return_proxy = r.headers['X-Client-IP']
        if proxy_ip==return_proxy:
            return True
        else:
            return False
    except Exception:
        return False


def check_proxy_list(proxy_list, max_proxies=None):
    """
    Функция, которая принимает один обязательный аргумент -> список прокси в
    формат, возвращаемый функцией load_proxies_from_csv.

    Он также принимает необязательный аргумент 'max_proxies', если пользователь желает
    ограничить количество проверенных прокси.

    Каждый прокси проверяется функцией check_proxy. Так как каждый тест проводится на
    «wikipedia.org», чтобы быть внимательным к серверам Википедии, 
    мы не используем никаких асинхронных модулей,
    но отправляют последовательные запросы,
    каждый из которых разделен не менее чем на 1 секунду.

    Выходы: список, содержащий прокси, хранящиеся в именованных кортежах.
    """
    print((Style.BRIGHT + Fore.GREEN + "[" +
           Fore.YELLOW + "*" +
           Fore.GREEN + "] Started checking proxies."))
    working_proxies = []

    # If the user has limited the number of proxies we need,
    # the function will stop when the working_proxies
    # loads the max number of requested proxies.
    if max_proxies != None:
        for proxy in proxy_list:
            if len(working_proxies) < max_proxies:
                time.sleep(1)
                if check_proxy(proxy.ip,proxy.port,proxy.protocol) == True:
                    working_proxies.append(proxy)
            else:
                break
    else:
        for proxy in proxy_list:
            time.sleep(1)
            if check_proxy(proxy.ip,proxy.port,proxy.protocol) == True:
                working_proxies.append(proxy)

    if len(working_proxies) > 0:
        print((Style.BRIGHT + Fore.GREEN + "[" +
               Fore.YELLOW + "*" +
               Fore.GREEN + "] Finished checking proxies."))
        return working_proxies

    else:
        raise Exception("Found no working proxies.")

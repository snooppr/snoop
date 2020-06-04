#! /usr/bin/env python3
"Самотестирование сети"

def nettest():
    from colorama import Fore, Style, init
    import sys
    try:
        import speedtest
    except ModuleNotFoundError:
        print(f"Установить модуль 'speedtest', в GNU команда:\n" + \
        Style.BRIGHT + Fore.RED + "cd ~/snoop && python3 -m pip install -r requirements.txt" + \
        Style.RESET_ALL)
        sys.exit(0)

    servers = []
    threads = None

    print("\n\033[36mОжидайте, идёт самотестирование сети...\033[0m\n")

    s = speedtest.Speedtest()
    s.get_servers(servers)
    s.get_best_server()
    s.download(threads=threads)
    s.upload(threads=threads)

    a = s.results.dict()

    v1 = round(a.get("download")/1000000,2)
    v2 = round(a.get("upload")/1000000,2)
    v3 = round(a.get("ping"))
    v4 = (a.get("client"))

    # Скорость загрузки
    def func_v1():
        if v1 < 3:
            return (Style.BRIGHT + Fore.RED + str(v1) + Style.RESET_ALL)
        elif 3 <= v1 <= 5.5:
            return (Style.BRIGHT + Fore.YELLOW + str(v1) + Style.RESET_ALL)
        elif v1 > 5.5:
            return (Style.BRIGHT + Fore.GREEN + str(v1) + Style.RESET_ALL)

    # Скорость выгрузки
    def func_v2():
        if v2 < 0.8:
            return (Style.BRIGHT + Fore.RED + str(v2) + Style.RESET_ALL)
        elif 0.8 <= v2 <= 1.5:
            return (Style.BRIGHT + Fore.YELLOW + str(v2) + Style.RESET_ALL)
        elif v2 > 1.5:
            return (Style.BRIGHT + Fore.GREEN + str(v2) + Style.RESET_ALL)

    # Ping
    def func_v3():
        if v3 >= 250:
            return (Style.BRIGHT + Fore.RED + str(v3) + Style.RESET_ALL)
        elif 60 <= v3 < 250:
            return (Style.BRIGHT + Fore.YELLOW + str(v3) + Style.RESET_ALL)
        elif v3 < 60:
            return (Style.BRIGHT + Fore.GREEN + str(v3) + Style.RESET_ALL)

    print("\033[36mТест сети:\033[0m Download::", func_v1(), "Мбит/с, Upload::", func_v2(), "Мбит/с, Ping::", func_v3(), "мс")
    print("\033[36mВаш ip:\033[0m", v4.get("ip"), "\n\033[36mПровайдер:\033[0m", v4.get("isp"))
    print("\033[36mЛокация:\033[0m", v4.get("country"))

#! /usr/bin/env python3
# Copyright (c) 2020 Snoop Project <snoopproject@protonmail.com> 
"Самотестирование сети"

import speedtest
from colorama import Fore, Style, init
from rich.panel import Panel
from rich.style import Style as STL
from rich.console import Console

init(autoreset=True)
console2 = Console()

def nettest():
    with console2.status("[cyan] Ожидайте, идёт самотестирование сети..."):
        servers = []
        threads = None
        try:
            s = speedtest.Speedtest(secure=True)
            s.get_servers(servers)
            s.get_best_server()
            s.download(threads=threads)
            s.upload(threads=threads)

            a = s.results.dict()

            d = round(a.get("download") / 1_000_000, 2)
            u = round(a.get("upload") / 1_000_000, 2)
            p = round(a.get("ping"))
            v4 = a.get("client")

# Скорость загрузки.
            try:
                if d < 3: d = f"Download: [bold red]{d}[/bold red] Мбит/с"
                elif 3 <= d <= 5.5: d = f"Download: [yellow]{d}[/yellow] Мбит/с"
                elif d > 5.5: d = f"Download: [bold green]{d}[/bold green] Мбит/с"
            except:
                d = f"Download: [bold red]Сбой[/bold red]"

# Скорость выгрузки.
            try:
                if u < 0.8: u = f"Upload: [bold red]{u}[/bold red] Мбит/с"
                elif 0.8 <= u <= 1.5: u = f"Upload: [yellow]{u}[/yellow] Мбит/с"
                elif u > 1.5: u = f"Upload: [bold green]{u}[/bold green] Мбит/с"
            except:
                u = f"Upload: [bold red]Сбой[/bold red]"
# Ping.
            try:
                if p >= 250: p = f"Ping: [bold red]{p}[/bold red] мс"
                elif 60 <= p < 250: p = f"Ping: [yellow]{p}[/yellow] мс"
                elif p < 60: p = f"Ping: [bold green]{p}[/bold green] мс"
            except:
                p = f"Ping: [bold red]Сбой[/bold red]"
# Результат.
            console2.print(Panel.fit(f"{d}\n{u}\n{p}\n\nВаш ip: {v4.get('ip')}\nПровайдер: {v4.get('isp')}\nЛокация: {v4.get('country')}",
                                     title="🌐 Тест сети", style=STL(color="cyan")))
            console2.log("[cyan]--> завершен")
        except Exception:
            console2.print(f"[bold red]Нет сети?!\nТест будет пропущен...")

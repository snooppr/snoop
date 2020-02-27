Ветка Snoop master (GNU/Linux)
=============================

## Snoop Project один из самых заточенных OSINT-инструментов по СНГ локации

<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/snoop.png" />

Snoop Project — это форк Sherlock Project-a и он разыскивает никнеймы в публичных данных.

Различия смотри
https://raw.githubusercontent.com/snooppr/snoop/master/changelog.txt

**В базе 470 сайтов, база расширяется**

## Установка

**Примечание**: Требуемая версия python 3.6 и выше.

```bash
# Клонировать репозиторий
$ git clone https://github.com/snooppr/snoop

# Войти в рабочий каталог
$ cd ~/snoop

# Установить python3 и python3-pip, если они не установлены
$ apt-get update && apt-get install python3

# Установить зависимости 'requirements'
$ pip install --upgrade pip
$ python3 -m pip install -r requirements.txt
# Либо установить все зависимости из 'requirements.txt' в ручную через
$ pip3 install module
```
## Работа Snoop на Android-е
Смотри ветку Termux
https://github.com/snooppr/snoop/tree/termux

Project Snoop работает на OS GNU/Linux & OS Windows & OS Android/Termux.

## Использование

```bash
$ python3 snoop.py --help

usage: snoop.py [-h] [--donate Y] [--sort Y] [--version] [--verbose]
                [--folderoutput FOLDEROUTPUT] [--output OUTPUT] [--tor]
                [--unique-tor] [--proxy PROXY_URL] [--proxy_list PROXY_LIST]
                [--check_proxies CHECK_PROXY] [--csv] [--json JSON_FILE]
                [--site SITE_NAME] [--timeout --time 9] [--print-found]
                [--no-func] [--list all] [--update Y]
                USERNAMES [USERNAMES ...]


Snoop: поиск никнейма по всем фронтам! (Version 1.0.0_rus)

positional arguments:
  USERNAMES             Никнейм разыскиваемого пользователя, поддерживается
                        несколько имён

optional arguments:
  -h, --help            show this help message and exit
  --donate Y            Пожертвовать на развитие Snoop project-а
  --sort Y              Обновление/сортировка черного и белого списков (.json)
                        сайтов БД Snoop
  --version, -V         Вывод на дисплей: версий Snoop, Python; Сублицензии
  --verbose, -v, -d, --debug
                        Вывод на дисплей отладочной информации и подробная её
                        вербализация
  --folderoutput FOLDEROUTPUT, -fo FOLDEROUTPUT
                        Указать каталог отличный от стандартного, куда будут
                        сохранены результаты поиска при разовом поиске
                        нескольких имён
  --output OUTPUT, -o OUTPUT
                        Указать отличный от стандартного файл с сохранением
                        результатов. По умолчанию файл для сохранения
                        результатов — переменное username.txt
  --tor, -t             Делать запросы через Tor-службу; требуется чтобы Tor
                        был установлен по системному стандартному пути и не
                        модифицирован torrc
  --unique-tor, -u      Делать запросы через Tor-службу с новой цепочкой Tor
                        после каждого запроса; увеличивает время выполнения;
                        требуется чтобы Tor был установлен по системному
                        стандартному пути
  --proxy PROXY_URL, -p PROXY_URL
                        Делать запросы через прокси, например,
                        socks5://127.0.0.1:9070
  --proxy_list PROXY_LIST, -pl PROXY_LIST
                        Поиск 'username' через случайный прокси, указать
                        file.csv с прокси
  --check_proxies CHECK_PROXY, -cp CHECK_PROXY
                        Связка с параметром '--proxy_list'. Скрипт проверяет
                        рабочие ли предоставленные прокси из file.csv,
                        являются ли они анонимными. Установите '0' для
                        безлимитного количества успешно-проверенных прокси,
                        установите > '1' для ограничения
  --csv                 Сохранить файл в формате (nickname.CSV) с расширенным
                        анализом
  --json JSON_FILE, -j JSON_FILE
                        Указать для поиска 'username' другую БД сайтов в
                        формате file.json
  --site SITE_NAME      Указать имя сайта из БД (data.json). Ограничение
                        поиска 'username' до одного ресурса
  --timeout --time 9    Выделение макс.времени на ожидание ответа от сервера
                        Влияет на продолжительность поиска. Оптимальное
                        значение при хорошем интернет соединении и нескольких
                        'упавших' сайтов = 9с.
  --print-found         Выводить на печать только найденные аккаунты
  --no-func, -n         ✓Монохромный терминал, не использовать цвета в url
                        ✓Отключить звук
                        ✓Запретить открытие web browser-a
                        Отключить звук  
  --list all            Вывод на дисплей БД (БС+ЧС) поддерживаемых сайтов
  --update Y            Обновить Snoop
```

Для поиска только одного пользователя::
```
python3 snoop.py username1
```

Для поиска одного и более юзеров:
```
python3 snoop.py username1 username2 username3
```

Найденные учетные записи будут храниться в ~/snoop/results/*/username.{txt.csv.html}

Обновляйте Snoop для поддержки ПО и БД в актуальном состоянии:
```
python3 snoop.py --update Y 
#Требуется установка Git.
```

<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/Run.gif"/>

## Основные ошибки ложно-положительного отклика/соединения при поиске username
Cайт изменил свой ответ.
Блокировка сервером диапазона ip-адресов клиента.
Блокировка доступа к ресурсам при помощи РКН-а.
Срабатывание/защита ресурса captch-ей.
Недостаточная скорость интернет соединения EDGE/3G (желательная скорость >= 3Mbps).
В некоторых случаях недопустимое username.
Проблемы с openssl на стороне сервера (использование старой базы кода).
Некоторые сайты временно недоступны, например, технические работы.


**Например**

Если вы постоянно (*Debian) получаете "ошибку соединения" на этих ресурсах:

[GipsysTeam;
RamblerDating;
Mamochki;
и т.д.]

Решение следующее (проверенное):
```bash
$ sudo nano /etc/ssl/openssl.cnf

# Изменить в самом низу файла строки:
[CipherString = DEFAULT@SECLEVEL=2]

на

[CipherString = DEFAULT@SECLEVEL=1]
```
https://wiki.debian.org/ContinuousIntegration/TriagingTips/openssl-1.1.1

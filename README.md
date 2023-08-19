Snoop Project
=============

### Snoop Project один из самых перспективных OSINT-инструментов по поиску никнеймов
- [X] This is the most powerful software taking into account the CIS location.

<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/snoop.jpg" />

Is your life slideshow? Ask Snoop.  
Snoop project is developed without taking into account the opinions of the NSA and their friends,  
that is, it is available to the average user *(project creation date: February 14, 2020)*.  

 • [🌎 ENGLISH readme](https://github.com/snooppr/snoop/blob/master/README.en.md "Please feel free to improve the translation of this page.") 
 • [🇹🇷 TÜRKÇE oku beni](https://github.com/snooppr/snoop/blob/master/README.tr.md "İsterseniz translate de çevirebilirsiniz") 
 • [🇪🇸 ESPAÑOL readme](https://github.com/snooppr/snoop/blob/master/README.es.md "Por favor, siéntase libre de mejorar la traducción de esta página.")  
 • [🇩🇪 DEUTSCHE readme](https://github.com/snooppr/snoop/blob/master/README.de.md "Bitte zögern Sie nicht, die Übersetzung dieser Seite zu verbessern..")  
 • [🇨🇳 中国人 readme](https://github.com/snooppr/snoop/blob/master/README.cn.md "请随时改进此页面的翻译。")  
 • [🇫🇷 FRANÇAIS readme](https://github.com/snooppr/snoop/blob/master/README.fr.md "N'hésitez pas à améliorer la traduction de cette page.")  

 ---
 
> *Snoop — это исследовательская работа (собственная база данных/закрытые багбаунти) в области поиска и обработки публичных данных в сети интернет. По части специализированного поиска Snoop способен конкурировать с традиционными поисковыми системами.*  

Сравнение индексаций БД-никнеймов подобных инструментов:  
<img src="https://img.shields.io/badge/Snoop-~3100+%20websites-success" width="50%" />  
<img src="https://img.shields.io/badge/Sherlock-~350 websites-yellowgreen" width="20%" />  
<img src="https://img.shields.io/badge/Spiderfoot-~350 websites-yellowgreen" width="20%" />  
<img src="https://img.shields.io/badge/Whatsmyname-~300 websites-yellowgreen" width="20%" />  
<img src="https://img.shields.io/badge/Namechk-~100 websites-red" width="15%" />  


| Платформа             | Поддержка |
|-----------------------|:---------:|
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/Linux.png" width="5%" /> GNU/Linux             |     ✅    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/Windows.png" width="5%" /> Windows 7/10 (32/64)  |     ✅    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/Android.png" width="5%" /> Android (Termux)      |     ✅    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/macOS.png" width="5%" /> macOS                 |     ❗️    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/IOS.png" width="5%" /> IOS                   |     🚫    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/WSL.png" width="5%" /> WSL                   |     🚫    |  


Snoop for OS Windows and GNU/Linux
==================================

**Snoop Local database**  
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/snoop_run.png" />  
[Snoop full version database 3100+ websites ⚡️⚡️⚡️](https://github.com/snooppr/snoop/blob/master/websites.md "Database Snoop")  

## Релиз/Release
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/snoop box.png" width="35%" />  

**RU**: Snoop поставляется готовыми сборками (релиз) и не требует зависимостей (библиотек) или установки python,
то есть работает на чистой машине с OS Windows или GNU/Linux.  
**EN**: Snoop comes with ready-made assemblies (release) and does not require dependencies (libraries) or python installation, that is, it runs on a clean machine with OS Windows or GNU/Linux.  
┗━━ ⬇️[Download Snoop Project](https://github.com/snooppr/snoop/releases "скачать готовую сборку Snoop для Windows и GNU/Linux")  

<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/Run.gif"/>  

<details>
<summary> 🟣 Snoop Project Plugins</summary>  

### 1. Demonstration of one of the methods in the Plugin — 〘GEO_IP/domain〙  
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/GEO_IP.gif" />  

$$$$

Reports are also available in csv/txt/CLI/maps  
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/GEO_IPcsv.jpeg" />  

$$$$

### 2. Demonstration of one of the methods in the Plugin — 〘Yandex_parser〙  
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/Yandex_parser.gif" />  

$$$$

Search report dozen nickname (Plugin — Yandex_parser)  
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/Yandex_parser 4.png" />  

$$$$

### 3. Demonstration of one of the methods in the Plugin — 〘Reverse Vgeocoder〙  
https://github.com/snooppr/snoop/assets/61022210/aeea3c0e-0d1b-429e-8e42-725a6a1a6653  

Snoop выбирает из грязных данных (цифры, буквы, спецсимволы) лишь геокоррдинаты.  

</details>

<details>
<summary> 🟤 Самостоятельная сборка ПО из исходного кода/Self-build software from source</summary>  

**Native Installation**  
+ Примечание: не делать так, если хотите установить snoop на android/termux
*(установка отличается, для этого смотри специальный пункт ниже).*  
+ Примечание: требуемая версия python 3.7+

```
# Клонировать репозиторий
$ git clone https://github.com/snooppr/snoop

# Войти в рабочий каталог
$ cd ~/snoop

# Установить python3 и python3-pip, если они не установлены
$ apt-get update && apt-get install python3 python3-pip

# Установить зависимости 'requirements'
$ pip install --upgrade pip
$ python3 -m pip install -r requirements.txt
# Если вместо флагов стран отображаются спецсимволы, доставить пакет шрифта, например (цветной)
$ apt-get install fonts-noto-color-emoji или $ apt-get install ttf-ancient-fonts (монохромный)
# На OS Windows использовать cmd или powershell (на выбор по удобству), но не WSL!
```
</details>

<details>
<summary> 🟢 Использование/Using</summary>  

```
usage: snoop_cli [search arguments...] nickname
or
usage: snoop_cli [service arguments | plugins arguments]


$ snoop_cli --help #запуск сборки на GNU/Linux

Справка

optional arguments:
  -h, --help            show this help message and exit

service arguments:
  --version, -V         About: вывод на печать версий:: OS; Snoop;
                        Python и Лицензии
  --list-all, -l        Вывести на печать детальную информацию о базе
                        данных Snoop
  --donate, -d          Пожертвовать на развитие Snoop Project-а,
                        получить/приобрести Snoop full version
  --autoclean, -a       Удалить все отчеты, очистить место
  --update, -U          Обновить Snoop

plugins arguments:
  --module, -m          OSINT поиск: задействовать различные плагины
                        Snoop:: IP/GEO/YANDEX

search arguments:
  nickname              Никнейм разыскиваемого пользователя.
                        Поддерживается поиск одновременно нескольких имен.
                        Ник, содержащий в своем имени пробел, заключается в
                        кавычки
  --verbose, -v         Во время поиска 'nickname' выводить на печать
                        подробную вербализацию
  --web-base, -w        Подключиться для поиска 'nickname' к
                        динамично-обновляемой web_БД (3100+ сайтов). В demo
                        version функция отключена
  --site , -s <site_name> 
                        Указать имя сайта из БД '--list-all'. Поиск
                        'nickname' на одном указанном ресурсе, допустимо
                        использовать опцию '-s' несколько раз
  --exclude , -e <country_code> 
                        Исключить из поиска выбранный регион,
                        допустимо использовать опцию '-e' несколько раз,
                        например, '-e RU -e WR' исключить из поиска Россию и
                        Мир
  --include , -i <country_code> 
                        Включить в поиск только выбранный регион,
                        допустимо использовать опцию '-i' несколько раз,
                        например, '-i US -i UA' поиск по США и Украине
  --country-sort, -c    Печать и запись результатов по странам, а не по алфавиту
  --time-out , -t <digit> 
                        Установить выделение макс.времени на ожидание
                        ответа от сервера (секунды). Влияет на
                        продолжительность поиска. Влияет на 'Timeout ошибки'.
                        Вкл. эту опцию необходимо при медленном интернет
                        соединении (по умолчанию 9с)
  --found-print, -f     Выводить на печать только найденные аккаунты
  --no-func, -n         ✓Монохромный терминал, не использовать цвета
                        в url ✓Отключить звук ✓Запретить открытие web
                        browser-а ✓Отключить вывод на печать флагов стран
                        ✓Отключить индикацию и статус прогресса
  --userlist , -u <file> 
                        Указать файл со списком user-ов. Snoop
                        интеллектуально обработает данные и предоставит
                        доп.отчеты
  --save-page, -S       Сохранять найденные странички пользователей в
                        локальные html-файлы
  --cert-on, -C         Вкл проверку сертификатов на серверах. По
                        умолчанию проверка сертификатов на серверах отключена,
                        что позволяет обрабатывать проблемные сайты без ошибок
  --headers , -H <User-Agent> 
                        Задать user-agent вручную, агент заключается
                        в кавычки, по умолчанию для каждого сайта задается
                        случайный либо переопределенный user-agent из БД snoop
  --quick, -q           Быстрый и агрессивный режим поиска. Не
                        обрабатывает повторно сбойные ресурсы, в следствие
                        чего, ускоряется поиск, но и повышается Bad_raw. Не
                        выводит промежуточные результаты на печать. Потребляет
                        больше ресурсов. Режим эффективен в full version
```  

**Example**
```
# Для поиска только одного пользователя:
$ python3 snoop.py nickname1 #Running from source
$ snoop_cli nickname1 #Running from release linux
# Или, например, кириллица поддерживается:
$ python3 snoop.py олеся #Running from source
# Для поиска имени, содержащего пробел:
$ snoop_cli "ivan ivanov" #Running from release linux
$ snoop_cli ivan_ivanov #Running from release linux
$ snoop_cli ivan-ivanov #Running from release linux

# Запуск на OS Windows:
$ python snoop.py nickname1 #Running from source
$ snoop_cli.exe nickname1 #Running from release win
# Для поиска одного и более юзеров:
$ snoop_cli.exe nickname1 nickname2 nickname123321 #Running from release win

# Поиск множества юзеров — сортировка вывода результатов по странам;
# избежание зависаний на сайтах (чаще 'мёртвая зона' зависит от ip-адреса пользователя);
# выводить на печать только найденные аккаунты; сохранять странички найденных
# аккаунтов локально; указать файл со списком разыскиваемых аккаунтов;
# подключиться для поиска к расширяемой и обновляемой web-base Snoop;
# исключить из поиска все сайты в RU-регионе:
$ snoop_cli -с -t 6 -f -S -u ~/file.txt -w -e RU #Running from release linux

# проверить базу данных Snoop:
$ snoop_cli --list-all #Running from release linux

# распечатать справку по функциям Snoop:
$ snoop_cli --help #Running from release linux

# Задействовать плагины Snoop:
$ snoop_cli --module #Running from release linux
```

+ **'ctrl + c'** — прервать поиск.  
+ Найденные учетные записи будут храниться в
`~/snoop/results/nicknames/*{txt|csv|html}`.  
+ csv открывать в *office, разделитель полей **запятая**.  
+ Уничтожить **все** результаты поиска — удалить каталог '~/snoop/results',
или `snoop_cli.exe --autoclean #Running from release OS Windows`.

```
# Обновляйте Snoop для тестирования новых функций в ПО:
$ python3 snoop.py --update #требуется установка Git.
```
</details>  

<details>
<summary> 🔵 Snoop for Android</summary>  

 • [Для удобства отдельный мануал (необязательно)](https://github.com/snooppr/snoop/tree/snoop_termux "Snoop for Android")  

<p align="center">  
  <img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/Snoop_2android.png" width="70%"/>  
</p>  

$$search-nickname$$  
<p align="center">  
  <img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/snoopandroid.png" />  
</p>  

$$plugins$$
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/Snoop_termux.plugins.png" />  

**Native Installation**  

Установить [Termux](https://f-droid.org/ru/packages/com.termux/ "F-Droid")  
```
# ПРИМЕЧАНИЕ_1!: если у пользователя ошибки при $ 'pkg update', например из-за цензуры в стране,
# и/или из-за того, что Termux давно не обновлялся на устройстве пользователя,
# то удаление/установка Termux-приложения не поможет,
# т.к. после удаления старые репозитории остаются на устройстве пользователя, решение:
$ termux-change-repo 
# и выбрать получение обновлений (для всех репо) из другого зеркала-репозитория.

# Войти в домашнюю папку Termux (т.е. просто открыть Termux)
$ termux-setup-storage
$ pwd #/data/data/com.termux/files/home #дефолтный/домашний каталог

# Установить python3 и зависимости
$ apt update && pkg upgrade && pkg install python libcrypt libxml2 libxslt git
$ pip install --upgrade pip

# Клонировать репозиторий
$ git clone https://github.com/snooppr/snoop -b snoop_termux

# Войти в рабочий каталог Snoop и установить зависимости 'requirements'
$ cd ~/snoop
$ python3 -m pip install -r requirements.txt

# Опционально ↓
# Чтобы расширить вывод терминала в Termux (по умолчанию 2к строк отображение в CLI),
# например, отображение всей БД опции '--list-all [1/2]'  
# добавить строку 'terminal-transcript-rows=10000' в файл '~/.termux/termux.properties'
# (крайне полезная опция доступна в Termux v0.114+). 
# Перезапустить Termux.  

# Пользователь также может запускать snoop по команде 'snoop' из любого места в CLI, создав alias.
$ cd && echo "alias snoop='cd && cd snoop && python snoop.py'" >> .bashrc && bash  

# Пользователь также может выполнить быструю проверку интересующего его сайта по БД,
# не используя опцию "--list-all", используя команду "snoopcheck".
$ cd && echo "alias snoopcheck='cd && cd snoop && echo 2 | python snoop.py --list-all | grep -i'" >> .bashrc && bash  

# ПРИМЕЧАНИЕ_2!: Snoop довольно умён и может автоматически открывать результаты поиска во внешнем веб-браузере:  
$ cd && pkg install termux-tools; echo 'allow-external-apps=true' >>.termux/termux.properties  
# перезапустить Termux.  
# По окончанию поиска работы snoop на запрос выбора, "чем открыть результаты поиска" выбрать дефолтный/системный HTMLviewer.  

# ПРИМЕЧАНИЕ_3!: после отключения РФ от Лондонской точки обмена интернет-трафиком скорость поиска Snoop
# (возможно и у других поставщиков связи) на мобильных операторах Мегафон/Yota упала в ~2 раза.
```
ПРИМЕЧАНИЕ_4!: если у пользователя Android ущербный (то есть 12+) и ломает Termux, читайте инструкцию по решению проблемы [здесь](https://github.com/agnostic-apollo/Android-Docs/blob/master/en/docs/apps/processes/phantom-cached-and-empty-processes.md#how-to-disable-the-phantom-processes-killing).  
ПРИМЕЧАНИЕ_5!: поддерживаются старые пропатченные python версии 3.7-3.10 из [termux_tur repo](https://github.com/termux-user-repository/tur/tree/master/tur).  

<p align="center">  
  <img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/Android%20snoop_run.gif" width="40%" />  
</p>  

</details>

<details>
<summary> 🔴 Основные ошибки/Basic errors in</summary>

|  Сторона  |                         Проблема                      | Решение |
|:---------:| ------------------------------------------------------|:-------:|
| ========= |=======================================================| ======= |
| Клиент    |Блокировка соединения проактивной защитой (*Kaspersky) |    1    |
|           |Недостаточная скорость интернет соединения EDGE/3G     |    2    |
|           |Слишком низкое значение опции '-t'                     |    2    |
|           |недопустимое nickname                                  |    3    |
|           |Ошибки соединения: [GipsysTeam; Nixp; Ddo; Mamochki;   |    7    |
|           |Ложные результаты (Беларусь): [D3; ChangeORG]          |    4    |
|           |Отсутсвие результатов (РФ): [Strava]                   |    4    |
| ========= |=======================================================| ======= |
| Провайдер |Internet Censorship                                    |    4    |
| ========= |=======================================================| ======= |
| Сервер    |Сайт изменил свой ответ/API; обновился CF/WAF          |    5    |
|           |Блокировка сервером диапазона ip-адресов клиента       |    4    |
|           |Срабатывание/защита ресурса captch-ей                  |    4    |
|           |Некоторые сайты временно недоступны, технические работы|    6    |
| ========= |=======================================================| ======= |

Примечание — в Snoop Project разработана мощная система детектирования различных проблем в т.ч. и интернет-цензуры. Условно в большинстве случаев пользователь не получает ложноположительные результаты при поиске на «проблемных ресурсах», т.к. Snoop отлично их подавляет, а в некоторых случаях, например, Etsy/Poker сайты — получает (намеренная, неограниченная демонстрация проблемы пользователю и того, что поиск в Snoop Project можно было бы произвести более эффективными способами, например, используя прокси/vpn из свободных от цензуры локаций).  

Решения:
1. Перенастроить свой Firewall *(например, замечено, что Kaspersky блочит доступ к ресурсам для взрослых)*.

2. Проверить скорость своего интернет соединения:  
`python3 snoop.py -v nickname`  
Если какой-либо из параметров сети выделен красным цветом, Snoop может подвисать во время поиска.  
При низкой скорости увеличить значение 'x' опции '--time-out x':  
`python3 snoop.py -t 15 nickname`  

3. Фактически это не ошибка. Исправить nickname  
*(например, на некоторых сайтах недопустимы символы кириллицы; "пробелы" или 'вьетнамо-китайская кодировка'
в именах пользователей, в целях экономии времени: — запросы фильтруются)*.

4. **Сменить свой ip-адрес**  
Интернет цензура (внутренняя и внешняя по локационному признаку/санкции) — самое распространенное из-за чего пользователь получает ошибки пропуска/ложного срабатывания/и в некоторых случаях '**Увы**'.
Иногда, при частом повторном сканировании за короткий промежуток времени, сервер конкретного ресурса может заблочить ip-адрес клиента на непродолжительное время (обычно до одной минуты, в течение которой бессмысленно выполнять запросы).  
При использовании Snoop с IP адреса провайдера мобильного оператора скорость **может** упасть в разы, зависит от провайдера.  
Самый действенный способ решить проблему — **ИСПОЛЬЗОВАТЬ VPN**, TOR слабо подходит на роль помощника и сам подвергается сильнейшему давлению со стороны цензурирования многих веб-сайтов.  

<p align="center">  
  <img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/censorship.png" width="70%" />  
</p>  
<p align="center">  
Пример внутренней интернет-цензуры.  
</p>  

<p align="center">  
  <img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/internet_censorship.png" width="90%" />  
</p>  
<p align="center">  
Пример внешней интернет-цензуры.  
</p>  

5. Открыть в Snoop репозитории на Github-e Issue/Pull request  
*(сообщить об этом разработчику)*.

6. Не обращать внимание, сайты иногда уходят на ремонтные работы и возвращаются в строй.

7. [Проблема](https://wiki.debian.org/ContinuousIntegration/TriagingTips/openssl-1.1.1 "проблема простая и решаемая") с openssl в некоторых дистрибутивах GNU/Linux, а также проблема с сайтами, которые не обновлялись годами. Проблема эта встречается, если пользователь намеренно запустил snoop с опцией '--cert-on'.  
Решение не использовать опцию «--cert-on» или:
```
$ sudo nano /etc/ssl/openssl.cnf

# Изменить в самом низу файла строки:
[MinProtocol = TLSv1.2]
на
[MinProtocol = TLSv1]

[CipherString = DEFAULT@SECLEVEL=2]
на
[CipherString = DEFAULT@SECLEVEL=1]
```
</details>

<details>
<summary> 🟠 Дополнительная информация/Additional information</summary>

 • [История развития проекта/History](https://raw.githubusercontent.com/snooppr/snoop/master/changelog.txt "Project development history").  

 • [Лицензия Snoop Project/License](https://github.com/snooppr/snoop/blob/master/COPYRIGHT).  

 • [Документация/Documentation](https://drive.google.com/open?id=12DzAQMgTcgeG-zJrfDxpUbFjlXcBq5ih).  

 • **Отпечаток публичного ключа:**	[076DB9A00B583FFB606964322F1154A0203EAE9D](https://raw.githubusercontent.com/snooppr/snoop/master/PublicKey.asc "pgp key").  

 • **Информация для госслужащих:** Snoop Project включен в реестр отечественного ПО с заявленным кодом: 26.30.11.16 Программное Обеспечение, обеспечивающее выполнение установленных действий при проведении оперативно-розыскных мероприятий.
Приказ Минкомсвязи РФ №515 реестровый № 7012.  

 • **Snoop неидеален:** вэб-сайты падают; закрывающие теги отсутствуют; соединения цензурируются; хостинги вовремя не оплачиваются.
Время от времени необходимо следить за всем этим "Web rock 'n' roll", поэтому донаты приветствуются:
[примеры коррекции БД/Example close/bad websites](https://drive.google.com/file/d/1CJxGRJECezDsaGwxpEw34iJ8MJ9LXCIG/view?usp=sharing).    

 • **Сжатие репозитория 27 января 2022г.:** если возникли проблемы сделайте 'git clone' по новому.  

 • **Внимание**❗️ Из-за цензуры письма с 'mailru' и 'yandex' не доходят до 'protonmail'. Для пользователей mailru/yandex пишите запросы на запасную почту, email: snoopproject@ya.ru  

 • **Визуализация  коммитов:** от рождения проекта до пятницы тринадцатого 2023г.  

https://user-images.githubusercontent.com/61022210/212534128-bc0e5779-a367-4d0a-86cb-c52503ee53c4.mp4  
</details>  
</p>

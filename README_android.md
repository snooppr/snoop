Snoop Project for Termux
========================

## Snoop Project один из самых перспективных OSINT-инструментов — поиск по нику
- [X] This is the most powerful software taking into account the CIS location.  
• [English readme Snoop for Termux](https://github.com/snooppr/snoop/blob/master/README_android.en.md "Please feel free to improve the translation of this page.")  

<p align="center">  
  <img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/Snoop_2android.png" />  
</p>  

<p align="center">  
  <img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/snoopandroid.png" />  
</p>  

Ваша жизнь Слайд-шоу? Спросите снуп.  
Snoop Project разработан без учета мнения АНБ и их приятелей, то есть доступен рядовому пользователю.  

## Самостоятельная сборка ПО из исходного кода  
**Snoop for Android/Demo**  
<p align="center">  
  <img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/Snoop_termux.plugins.png" width="90%" />  
</p>  

**Инсталляция**  

Установить [Termux](https://f-droid.org/ru/packages/com.termux/ "Termux с F-Droid, на GP Termux больше не обновляется!")  
```sh
# ПРИМЕЧАНИЕ_1!: если у пользователя ошибки при $ 'pkg update', например из-за того, 
# что Termux давно не обновлялся на устройстве пользователя,
# то удаление/установка Termux-приложения не поможет,
# т.к. после удаления старые репозитории остаются на устройстве пользователя, решение:
$ termux-change-repo 
# и выбрать получение обновлений (для всех репо) из другого зеркала-репозитория.

# Открыть доступ к диску
$ termux-setup-storage

# Установить python3 и зависимости
$ apt update && pkg upgrade && pkg install python libcrypt libxml2 libxslt git
$ pip install --upgrade pip

# Клонировать репозиторий
$ git clone https://github.com/snooppr/snoop

# Войти в рабочий каталог Snoop
$ cd ~/snoop
# Установить зависимости 'requirements.txt'
$ python3 -m pip install -r requirements.txt


# Опционально↓
# Чтобы расширить вывод терминала в Termux (по умолчанию 2к строк отображение в CLI), например, 
# отображение всей БД опции '--list-all [1/2]'
# добавить строку 'terminal-transcript-rows=10000' в файл '~/.termux/termux.properties'
# (крайне полезная опция доступна в Termux v0.114+). 
# Перезапустить Termux.  

# Пользователь также может запустить snoop по команде 'snoop' из любого места в CLI, создав alias.  
$ cd && echo "alias snoop='cd && cd snoop && python snoop.py'" >> .bashrc && bash  

# Пользователь также может выполнить быструю проверку интересующего его сайта по БД,  
# не используя опцию "--list-all", используя команду "snoopcheck"  
$ cd && echo "alias snoopcheck='cd && cd snoop && echo 2 | python snoop.py --list-all | grep -i'" >> .bashrc && bash  

# ПРИМЕЧАНИЕ_2!: Snoop довольно умён и может автоматически открывать результаты поиска во внешнем веб-браузере, не смотря на Google ограничения:  
$ cd && pkg install termux-tools; echo 'allow-external-apps=true' >>.termux/termux.properties  
# перезапустить Termux.  
# По окончанию поиска работы snoop на запрос выбора, "чем открыть результаты поиска" выбрать, встоенный в OS Android, дефолтный/системный HTMLviewer.  

# ПРИМЕЧАНИЕ_3!: после отключения РФ от Лондонской точки обмена интернет-трафиком скорость поиска Snoop
# (возможно и у других поставщиков связи) на Мегафон/Yota упала в ~2 раза.
```
ПРИМЕЧАНИЕ_4!: если у пользователя Android ущербный (то есть версия OS 12+ со множеством ограничений) и ломает Termux, читайте инструкцию по решению проблемы [здесь](https://github.com/agnostic-apollo/Android-Docs/blob/master/en/docs/apps/processes/phantom-cached-and-empty-processes.md#how-to-disable-the-phantom-processes-killing).  
ПРИМЕЧАНИЕ_5!: поддерживаются старые пропатченные python версии 3.7-3.11 из [termux_tur repo](https://github.com/termux-user-repository/tur/tree/master/tur).  

<p align="center">  
  <img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/snoop_alias.gif" width="40%" />  
</p>  


## Использование
```
usage: python3 snoop.py [search arguments...] nickname
or
usage: python3 snoop.py [service arguments | plugins arguments]


service arguments:
  --version, -V         About: вывод на печать версии ПО, snoop info
                        и Лицензии.
  --list-all, -l        Вывести на печать детальную информацию о базе
                        данных Snoop.
  --donate, -d          Пожертвовать на развитие Snoop Project-а,
                        получить/приобрести Snoop full version.
  --autoclean, -a       Удалить все отчеты, очистить кэш.
  --update, -U          Обновить Snoop.

plugins arguments:
  --module, -m          OSINT поиск: задействовать различные плагины
                        Snoop:: IP/GEO/YANDEX.

search arguments:
  nickname              Никнейм разыскиваемого пользователя.
                        Поддерживается поиск одновременно нескольких имен.
                        Ник, содержащий в своем имени пробел, заключается в
                        кавычки.
  --web-base, -w        Подключиться для поиска 'nickname' к
                        динамично-обновляемой web_БД (5300+ сайтов).
  --site , -s <site_name> 
                        Указать имя сайта из БД '--list-all'. Поиск
                        'nickname' на одном указанном ресурсе, допустимо
                        использовать опцию '-s' несколько раз.
  --exclude , -e <country_code> 
                        Исключить из поиска выбранный регион,
                        допустимо использовать опцию '-e' несколько раз,
                        например, '-e RU -e WR' исключить из поиска Россию и
                        Мир.
  --include , -i <country_code> 
                        Включить в поиск только выбранный регион,
                        допустимо использовать опцию '-i' несколько раз,
                        например, '-i US -i UA' поиск по США и Украине.
  --time-out , -t <digit> 
                        Установить max время ожидания ответа от
                        сервера (секунды). Влияет на продолжительность поиска
                        и 'timeout ошибки' (по умолчанию задано 9 сек).
  --country-sort, -c    Печать и запись результатов по странам, а не
                        по алфавиту.
  --no-func, -n         ✓Монохромный терминал, не использовать цвета в url
                        ✓Запретить открытие web browser-а
                        ✓Отключить вывод на печать флагов стран
                        ✓Отключить индикацию и статус прогресса.
  --found-print, -f     Выводить на печать только найденные аккаунты.
  --verbose, -v         Во время поиска 'nickname' выводить на печать
                        подробную вербализацию.
  --userlist , -u <file> 
                        Указать файл со списком user-ов. Snoop
                        интеллектуально обработает данные и предоставит
                        доп.отчеты.
  --save-page, -S       Сохранять найденные странички пользователей в
                        локальные html-файлы, медленный режим.
  --pool , -p <digit>   Отключить автооптимизацию и задать вручную
                        скорость поиска от 1 до 300 макс. процессов. По
                        умолчанию используется высокая нагрузка на ресурсы ЭВМ
                        в Quick-режиме, в остальных режимах используется
                        умеренное потребление мощностей. Слишком низкое или
                        высокое значение может существенно замедлить работу
                        ПО. ~Расчетное оптимальное значение для данного
                        устройства выводится в 'snoop info', параметр
                        'Recommended pool', опция [--version/-V]. Данную опцию
                        предлагается задействовать 1) если пользователь имеет
                        многоядерную ЭВМ и запас ОЗУ или наоборот слабую,
                        арендованную VPS 2) ускорять, замедлять поиск
                        рекомендуется в тандеме с опцией [--found-print/-f'].
  --quick, -q           Быстрый и агрессивный режим поиска. Не обрабатывает
                        повторно сбойные ресурсы, вследствие чего ускоряется
                        поиск, но и немного повышается Bad_raw.
                        Quick-режим подстраивается под мощность ПК, не выводит
                        промежуточные результаты на печать, эффективен и
                        предназначен для Snoop full version.
```


**Примеры**
```sh
# Для поиска только одного пользователя:
$ python3 snoop.py username1
# Или, например, кириллица поддерживается:
$ python3 snoop.py олеся
# Для поиска имени, содержащего пробел:
$ python3 snoop.py "ivan ivanov"
$ python3 snoop.py ivan_ivanov
$ python3 snoop.py ivan-ivanov

# Для поиска одного и более юзеров:
$ python3 snoop.py username1 username2 username3 username4

# Поиск множества юзеров — сортировка вывода результатов по странам;
# избежание длительных зависаний на сайтах (чаще 'мёртвая зона' зависит от вашего ip-адреса);
# выводить на печать только найденные аккаунты; сохранять странички найденных
# аккаунтов локально; указать файл со списком разыскиваемых аккаунтов;
# подключиться для поиска к расширяемой и обновляемой web-base Snoop:
$ python3 snoop.py -с -t 9 -f -S -u ~/file.txt -w

# Поиск двух username на двух ресурсах:
$ python snoop.py -s habr -s lichess chikamaria irina

# Получить Snoop full version:
$ python snoop.py --donate
```
**'ctrl + c'** — прервать поиск (остановить корректно ПО).  

Результаты будут сохранены в в '/storage/emulated/0/snoop/results/nicknames/*{txt|csv|html}'.  
csv открывать в *office, разделитель полей **запятая**.  

Уничтожить **все** результаты поиска — удалить каталог '~/snoop/results'.  
или ```python snoop.py --autoclean```

```sh
# Обновляйте Snoop для тестирования новых функций в ПО:
$ python3 snoop.py --update #Требуется установка Git.
```

**Пример работы snoop for Android/Termux**  
<p align="center">  
  <img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/Android%20snoop_run.gif" width="40%" />  
</p>  

 • **Проведено агрессивное сжатие репозитория 11 декабря 2024г.** Сохранен полный бэкап истории.
 Пользователи, собирающие Snoop из исходного кода, должны сделать 'git clone' по-новому.  

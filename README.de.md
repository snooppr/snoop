Snoop Projekt
=============

### Snoop Projekt ist eines der vielversprechendsten OSINT-Tools zum Finden von Spitznamen
- [X] Dies ist die leistungsfähigste Software unter Berücksichtigung des GUS-Standorts.

<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/EN__snoop.png" />

Ist Ihr Leben eine Diashow? Frag Snoop.  
Das Snoop-Projekt wird entwickelt, ohne die Meinungen der NSA und ihrer Freunde zu berücksichtigen,  
das heißt, es steht dem durchschnittlichen Benutzer zur Verfügung *(14. Februar 2020)*.  

> *Snoop ist ein Forschungswerk (eigene Datenbank/geschlossenes Bugbounty) im Bereich der Suche und Verarbeitung öffentlicher Daten im Internet. In Bezug auf die spezialisierte Suche kann Snoop mit traditionellen Suchmaschinen konkurrieren.*  

Vergleich der Indizierung von Datenbank-Nicknames ähnlicher Tools:  
<img src="https://img.shields.io/badge/Snoop-~3100+%20websites-success" width="50%" />  
<img src="https://img.shields.io/badge/Sherlock-~350 websites-yellowgreen" width="20%" />  
<img src="https://img.shields.io/badge/Spiderfoot-~350 websites-yellowgreen" width="20%" />  
<img src="https://img.shields.io/badge/Whatsmyname-~300 websites-yellowgreen" width="20%" />  
<img src="https://img.shields.io/badge/Namechk-~100 websites-red" width="15%" />  


| Plattform             | Unterstützung |
|-----------------------|:---------:|
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/Linux.png" width="5%" /> GNU/Linux             |     ✅    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/Windows.png" width="5%" /> Windows 7/10 (32/64)  |     ✅    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/Android.png" width="5%" /> Android (Termux)      |     ✅    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/macOS.png" width="5%" /> macOS                 |     ❗️    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/IOS.png" width="5%" /> IOS                   |     🚫    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/WSL.png" width="5%" /> WSL                   |     🚫    |  


Snoop für Betriebssysteme Windows und GNU/Linux
==================================

**Snoop lokale Datenbank**  
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/EN_DB.png" />  
[Snoop-Vollversionsdatenbank mit über 3100+ Websites ⚡️⚡️⚡️](https://github.com/snooppr/snoop/blob/master/websites.md "Datenbank-Snoop")  

## Freigeben
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/snoop box.png" width="35%" />  

Snoop wird vorkonfiguriert (freigegeben) geliefert und erfordert keine Abhängigkeiten (Bibliotheken) oder Python3-Installation,
d. h. es läuft auf einem sauberen Computer mit dem Betriebssystem Windows oder GNU/Linux.  
┗━━ ⬇️[Snoop-Projekt herunterladen](https://github.com/snooppr/snoop/releases 'Vorgefertigtes Snoop für Windows und GNU/Linux herunterladen')  

<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/Run.gif"/>  

<details>
<summary> 🟣 Snoop-Projekt-Plugins</summary>  

### 1. Demonstration einer der Methoden im Plugin — 〘GEO_IP/domain〙  
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/GEO_IP.gif" />  

$$$$

Berichte sind auch in csv/txt/CLI/maps verfügbar  
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/GEO_IPcsv.jpeg" />  

$$$$

### 2. Demonstration einer der Methoden im Plugin — 〘Yandex_parser〙  
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/Yandex_parser.gif" />  

$$$$

Suchbericht Dutzend Spitzname (Plugin - Yandex_parser)  
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/Yandex_parser 4.png" />  

$$$$

### 3. Demonstration einer der Methoden im Plugin — 〘Reverse Vgeocoder〙  
https://github.com/snooppr/snoop/assets/61022210/aeea3c0e-0d1b-429e-8e42-725a6a1a6653  

Snoop wählt nur Geokoordinaten aus schmutzigen Daten (Zahlen, Buchstaben, Sonderzeichen) aus.  

</details>

<details>
<summary> 🟤 Selbstgebaute Software aus der Quelle</summary>  

**Native Installation**  
+ Hinweis: Tun Sie dies nicht, wenn Sie Snoop auf Android/Termux installieren möchten
*(Die Installation ist anders, siehe dazu den speziellen Absatz unten).*  
+ Hinweis: Die erforderliche Python-Version ist 3.7+

```
# Repository klonen
$ git clone https://github.com/snooppr/snoop

# Geben Sie das Arbeitsverzeichnis ein
$ cd ~/snoop

# Installieren Sie python3 und python3-pip, falls nicht installiert
$ apt-get update && apt-get install python3 python3-pip

# Abhängigkeiten 'Anforderungen' installieren
$ pip install --upgrade pip
$ python3 -m pip install -r requirements.txt
# Wenn anstelle von Länderflaggen Sonderzeichen angezeigt werden, liefern Sie ein Schriftpaket, z. B. monochrom
$ apt-get install ttf-ancient-fonts oder Farbe (empfohlen) $ apt-get install fonts-noto-color-emoji
# Verwenden Sie unter Windows-Betriebssystemen cmd oder Powershell (der Einfachheit halber Ihre Wahl), aber nicht WSL!
```
</details>

<details>
<summary> 🟢 Verwendung</summary>  

```
usage: snoop_cli [search arguments...] nickname
or
usage: snoop_cli [service arguments | plugins arguments]


$ snoop_cli --help #Build unter GNU/Linux ausführen

Hilfe

optional arguments:
  -h, --help            Diese Hilfemeldung anzeigen und beenden

service arguments:
  --version, -V         Über: Druckversionen:: OS; schnüffeln; Python und Lizenzen
  --list-all, -l        Drucken Sie detaillierte Informationen über
                        die Snoop-Datenbank
  --donate, -d          Spende für die Entwicklung des Snoop-Projekts,
                        erhalte/kaufe die Snoop-Vollversion
  --autoclean, -a       Alle Berichte löschen, Speicherplatz freigeben
  --update, -U          Snoop aktualisieren

plugins arguments:
  --module, -m          OSINT-Suche: verschiedene Snoop-Plugins aktivieren:
                        IP/GEO/YANDEX

search arguments:
  nickname              Spitzname des gesuchten Benutzers. Die gleichzeitige
                        Suche nach mehreren Namen wird unterstützt. Ein Spitzname,
                        der ein Leerzeichen in seinem Namen enthält, wird in
                        Anführungszeichen eingeschlossen
  --verbose, -v         Geben Sie bei der Suche nach 'Spitzname' eine detaillierte
                        Verbalisierung aus
  --web-base, -w        Stellen Sie eine Verbindung zu einer dynamisch aktualisierten
                        web_DB (über 3100+ Websites) her, um nach 'Spitzname'
                        zu suchen. In der Demoversion ist die Funktion deaktiviert
  --site , -s <site_name> 
                        Geben Sie den Site-Namen aus der Datenbank '--list-all' an.
                        Suchen Sie nach 'Spitzname' in einer einzelnen
                        angegebenenRessource. Es ist zulässig, die Option '-s'
                        mehrmals zu verwenden
  --exclude , -e <country_code> 
                        Schließen Sie die ausgewählte Region von der Suche aus,
                        es ist akzeptabel, die Option '-e' mehrmals zu verwenden, z. B.
                        '-e RU -e WR', schließen Sie Russland und die Welt von der
                        Suche aus
  --include , -i <country_code> 
                        Wenn Sie nur die ausgewählte Region in die Suche einbeziehen, 
                        können Sie die Option '-i' mehrmals verwenden, z. B.
                        '-i US -i UA', um nach den USA und der Ukraine zu suchen
  --country-sort, -c    Drucken und Aufzeichnen von Ergebnissen nach Land,
                        nicht alphabetisch
  --time-out , -t <digit> 
                        Legen Sie die Zuweisung der maximalen Zeit fest,
                        die auf eineAntwort vom Server gewartet werden soll (Sekunden).
                        Beeinflusst die Dauer der Suche. Beeinflusst das
                        'Fehlerzeitüberschreitung'. An Diese Option ist für eine
                        langsame Internetverbindung erforderlich (Standard 9s)
  --found-print, -f     Drucken Sie nur gefundene Konten
  --no-func, -n         ✓Monochrom-Terminal, verwenden Sie keine Farben in der URL
                        ✓Ton stummschalten
                        ✓Öffnen des Webbrowsers verbieten
                        ✓Deaktivieren Sie das Drucken von Länderflaggen
                        ✓Anzeige und Fortschrittsstatus deaktivieren
  --userlist , -u <file> 
                        Geben Sie eine Datei mit einer Liste von Benutzern an.
                        Snoop wird die Daten intelligent verarbeiten und
                        zusätzliche Berichte bereitstellen
  --save-page, -S       Gefundene Benutzerseiten in lokalen HTML-Dateien speichern
  --cert-on, -C         Aktivieren Sie die Überprüfung von Zertifikaten auf Servern.
                        Standardmäßig ist die Zertifikatsüberprüfung auf
                        Servern deaktiviert, sodass Sie problematische Websites
                        fehlerfrei verarbeiten können.
  --headers , -H <User-Agent> 
                        Setzen Sie den User-Agent manuell, der Agent wird in
                        Anführungszeichen gesetzt, standardmäßig wird ein zufälliger
                        oder überschriebener User-Agent aus der Snoop-Datenbank
                        für jede Site gesetzt
  --quick, -q           Schneller und aggressiver Suchmodus. Verarbeitet schlechte
                        Ressourcen nicht erneut, wodurch die Suche beschleunigt wird,
                        aber Bad_raw erhöht sich auch. Druckt keine Zwischenergebnisse.
                        Verbraucht mehr Ressourcen. Der Modus ist in der Vollversion
                        wirksam
```  

**Beispiel**
```
# So suchen Sie nach nur einem Benutzer:
$ python3 snoop.py nickname1 #Aus dem Quellcode ausgeführt
$ snoop_cli nickname1 #Ausführen eines Builds unter Linux
# Oder es wird beispielsweise Kyrillisch unterstützt:
$ python3 snoop.py олеся #Aus dem Quellcode ausgeführt
# So suchen Sie nach einem Namen, der ein Leerzeichen enthält:
$ snoop_cli "ivan ivanov" #Ausführen eines Builds unter Linux
$ snoop_cli ivan_ivanov #Ausführen eines Builds unter Linux
$ snoop_cli ivan-ivanov #Ausführen eines Builds unter Linux

# Auf dem Betriebssystem Windows ausführen:
$ python snoop.py nickname1 #Aus dem Quellcode ausgeführt
$ snoop_cli.exe nickname1 #Ausführen eines Builds unter Windows
# Um nach einem oder mehreren Benutzern zu suchen:
$ snoop_cli.exe nickname1 nickname2 nickname123321 #Ausführen eines Builds unter Windows

# Suche nach mehreren Benutzern - Sortierung der Ergebnisausgabe nach Ländern;
# Vermeiden von Einfrieren auf Websites (häufiger hängt die „tote Zone“
# von der IP-Adresse des Benutzers ab); nur gefundene Accounts drucken;
# Seiten gefundener Accounts lokal speichern; Geben Sie eine Datei mit einer
# Liste der gewünschten Konten an. Verbinden Sie sich für die Suche mit der
# erweiterbaren und aktualisierbaren Snoop-Webbasis; alle Standorte in
# der Region RU von der Suche ausschließen:
$ snoop_cli -с -t 6 -f -S -u ~/file.txt -w -e RU #Ausführen eines Builds unter Linux

# Überprüfen Sie die Snoop-Datenbank:
$ snoop_cli --list-all #Ausführen eines Builds unter Linux

# Hilfe zu Snoop-Funktionen drucken:
$ snoop_cli --help #Ausführen eines Builds unter Linux

# Snoop-Plugins aktivieren:
$ snoop_cli --module #Ausführen eines Builds unter Linux
```

+ **'ctrl + c'** — Suche abbrechen.  
+ Gefundene Konten werden gespeichert in
`~/snoop/results/nicknames/*{txt|csv|html}`.  
+ csv in *office öffnen, Feldtrenner **Komma**.  
+ **Alle** Suchergebnisse beenden - Verzeichnis '~/snoop/results' löschen,
oder `snoop_cli.exe --autoclean #Ausführen eines Builds unter Windows

```
# Aktualisieren Sie Snoop, um neue Funktionen in der Software zu testen:
$ python3 snoop.py --update #Git-Installation erforderlich.
```
</details>  

<details>
<summary> 🔵 Snoop für Android</summary>  

 • [Ausführliche Anleitung in Englisch](https://github.com/snooppr/snoop/blob/snoop_termux/README.en.md "Snoop für Android")  

</details>

<details>
<summary> 🔴 Grundfehler</summary>

|  Seiten   |                         Problem                       | Lösung  |
|:---------:| ------------------------------------------------------|:-------:|
| ========= |=======================================================| ======= |
| Klient    |Verbindung durch proaktiven Schutz blockiert (*Kaspe.) |    1    |
|           |Unzureichende Geschwindigkeit der Interne. EDGE/3G     |    2    |
|           |'-t'-Option zu niedrig                                 |    2    |
|           |ungültiger Spitzname                                   |    3    |
|           |Verbindungsfehler: [GipsysTeam; Nixp; Ddo; Mamochki]   |    7    |
| ========= |=======================================================| ======= |
| Anbieter  |Internetzensur                                         |    4    |
| ========= |=======================================================| ======= |
| Server    |Die Seite hat ihre Antwort/API geändert;               |    5    |
|           |aktualisierte CF/WAF                                   |    5    |
|           |Sperren des IP-Adressbere. des Clients durch den Server|    4    |
|           |Auslösen/Schutz von Captch-Ressourcen                  |    4    |
|           |Einige Seiten sind vorübergehend nicht verfügbar,      |    6    |
|           |technische Arbeitsverzeichnis                          |    6    |
| ========= |=======================================================| ======= |

Lösungen:
1. Konfigurieren Sie Ihre Firewall neu *(z. B. blockiert Kaspersky Ressourcen für Erwachsene)*.

2. Überprüfen Sie die Geschwindigkeit Ihrer Internetverbindung:  
`python3 snoop.py -v nickname`  
Wenn eine der Netzwerkoptionen rot hervorgehoben ist, kann Snoop während der Suche hängen bleiben.  
Erhöhen Sie bei niedriger Geschwindigkeit den 'x'-Wert der Option '--time-out x':  
`python3 snoop.py -t 15 nickname`  

3. Tatsächlich ist dies kein Fehler. Spitznamen korrigieren  
*(z. B. sind kyrillische Zeichen auf einigen Websites nicht zulässig; „Leerzeichen“ oder „Vietnam-Chinesisch-Codierung“
in Benutzernamen, um Zeit zu sparen: - Anfragen werden gefiltert)*.

4. **Ändern Sie Ihre IP-Adresse**  
Internetzensur ist die häufigste Ursache dafür, dass der Benutzer übersprungene/falsch positive Fehler/und in einigen Fällen „**Ach**“ erhält.
Manchmal: Bei häufigem erneutem Scannen kann der Server einer bestimmten Ressource die IP-Adresse des Clients für eine Weile blockieren.
Bei der Nutzung von Snoop von der IP-Adresse des Providers des Mobilfunkbetreibers **kann** die Geschwindigkeit je nach Provider deutlich sinken.
Zum Beispiel ist der effektivste Weg, ein Problem zu lösen, **ein VPN zu VERWENDEN**, Tor ist kein guter Helfer.  

<p align="center">  
  <img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/censorship.png" width="70%" />  
</p>  

5. In Snoop-Repositories auf Github-e Issue/Pull-Request öffnen  
*(Entwickler benachrichtigen)*.

6. Achten Sie nicht darauf, dass Standorte manchmal repariert und wieder in Betrieb genommen werden.

7. [Problem](https://wiki.debian.org/ContinuousIntegration/TriagingTips/openssl-1.1.1 "das problem ist einfach und lösbar") mit openssl auf einigen GNU/Linux-Distributionen und ein Problem mit Seiten, die seit Jahren nicht aktualisiert wurden. Dieses Problem tritt auf, wenn der Benutzer Snoop absichtlich mit der Option „--cert-on“ gestartet hat.
Die Lösung besteht darin, die Option "--cert-on" nicht zu verwenden, oder:
```
$ sudo nano /etc/ssl/openssl.cnf

# Ändern Sie die Zeile ganz unten in der Datei:
[MinProtocol = TLSv1.2]
An
[MinProtocol = TLSv1]

[CipherString = DEFAULT@SECLEVEL=2]
An
[CipherString = DEFAULT@SECLEVEL=1]
```
</details>

<details>
<summary> 🟠 Weitere Informationen</summary>

 • [Geschichte der Projektentwicklung](https://raw.githubusercontent.com/snooppr/snoop/master/changelog.txt "Geschichte der Projektentwicklung").  

 • [Snoop-Projektlizenz](https://github.com/snooppr/snoop/blob/master/COPYRIGHT).  

 • [Dokumentation/RU](https://drive.google.com/open?id=12DzAQMgTcgeG-zJrfDxpUbFjlXcBq5ih).  

 • **Fingerabdruck des öffentlichen Schlüssels:**	[076DB9A00B583FFB606964322F1154A0203EAE9D](https://raw.githubusercontent.com/snooppr/snoop/master/PublicKey.asc "pgp-Schlüssel").  

 • **Informationen für Beamte/RU:** Das Snoop-Projekt ist im Register der inländischen Software mit dem angegebenen Code aufgeführt: 26.30.11.16 Software, die die Umsetzung festgelegter Maßnahmen während der operativen Suchtätigkeiten sicherstellt.
Verordnung des Ministeriums für Telekommunikation und Massenkommunikation der Russischen Föderation Nr. 515, Registernummer 7012.  

 • **Snoop ist nicht perfekt:** Websites fallen aus; es gibt keine schließenden Tags; Verbindungen werden zensiert; Hosting wird nicht rechtzeitig bezahlt. All dieser "Web Rock 'n' Roll" muss von Zeit zu Zeit angeschaut werden, daher sind Spenden willkommen:
[Beispiele für geschlossene/schlechte Websites](https://drive.google.com/file/d/1CJxGRJECezDsaGwxpEw34iJ8MJ9LXCIG/view?usp=sharing).    

 • **Repository-Komprimierung 27. Januar 2022:** Wenn Sie Probleme haben, erstellen Sie einen neuen „Git-Klon“.  


 • **Visualisierung von Commits:** von der Geburt des Projekts bis Freitag, den dreizehnten 2023.  

https://user-images.githubusercontent.com/61022210/212534128-bc0e5779-a367-4d0a-86cb-c52503ee53c4.mp4  
</details>

【RU -> DE】 Dies ist eine übersetzte [➰Readme auf Russisch](https://github.com/snooppr/snoop "Wenn Sie möchten, können Sie die maschinelle Übersetzung dieser Seite auf Deutsche verbessern (PR)").

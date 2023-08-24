Projet Snoop
=============

### Projet Snoop L'un des outils OSINT les plus prometteurs pour rechercher des surnoms
- [X] C'est le logiciel le plus puissant compte tenu de l'emplacement de la CEI.

<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/EN__snoop.png" />

Votre vie est-elle un diaporama ? Demandez à Snoop.
Le projet Snoop est développé sans tenir compte des avis de la NSA et de leurs amis,
c'est-à-dire qu'il est disponible pour l'utilisateur moyen *(date de création du projet : 14 février 2020)*.

> *Snoop est un dev-work de recherche (base de données propre/bounty fermé) dans la recherche et le traitement de données publiques sur Internet.
Selon la recherche spécialisée de Snoop, il est capable de concurrencer les moteurs de recherche traditionnels.*

Comparaison des indexations de bases de données tels outils:
<img src="https://img.shields.io/badge/Snoop-~3100+%20sites Internet-success" width="50%" />
<img src="https://img.shields.io/badge/Sherlock-~350 sites Internet-yellowgreen" width="20%" />
<img src="https://img.shields.io/badge/Spiderfoot-~350 sites Internet-yellowgreen" width="20%" />
<img src="https://img.shields.io/badge/Whatsmyname-~300 sites Internet-yellowgreen" width="20%" />
<img src="https://img.shields.io/badge/Namechk-~100 sites Internet-red" width="15%" />


| Plateforme              | Soutien |
|-----------------------|:---------:|
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/Linux.png" width="5%" /> GNU/Linux             |     ✅    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/Windows.png" width="5%" /> Windows 7/10 (32/64)  |     ✅    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/Android.png" width="5%" /> Android (Termux)      |     ✅    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/macOS.png" width="5%" /> macOS                 |     ❗️    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/IOS.png" width="5%" /> IOS                   |     🚫    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/WSL.png" width="5%" /> WSL                   |     🚫    |


Snoop pour OS Windows et GNU/Linux
==================================

**Base de données locale Snoop**
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/EN_DB.png" />
[Base de données de la version complète de Snoop 3100+ sites Web ⚡️⚡️⚡️](https://github.com/snooppr/snoop/blob/master/websites.md "Database Snoop")

## Libérer
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/snoop box.png" width="35%" />

Snoop est livré avec des assemblages prêts à l'emploi (version) et ne nécessite pas de dépendances (bibliothèques) ou d'installation de python, c'est-à-dire qu'il s'exécute sur une machine propre avec OS Windows ou GNU/Linux.
┗━━ ⬇️[Télécharger le projet Snoop](https://github.com/snooppr/snoop/releases "télécharger l'assembly SNOOP prêt à l'emploi pour Windows et GNU/Linux")

<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/Run.gif"/>

<details>
<summary> 🟣 Plugins du projet Snoop</summary>

### 1. Démonstration de l'une des méthodes du plugin — 〘GEO_IP/domain〙
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/GEO_IP.gif" />

$$$$

Les rapports sont également disponibles au format csv/txt/CLI/maps
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/GEO_IPcsv.jpeg" />

$$$$

### 2. Démonstration de l'une des méthodes du plugin — 〘Yandex_parser〙
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/Yandex_parser.gif" />

$$$$

Nom d'utilisateur du rapport de recherche douzaine (Plugin - Yandex_parser)
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/Yandex_parser 4.png" />

$$$$

### 3. Démonstration de l'une des méthodes du plugin — 〘Reverse Vgeocoder〙
https://github.com/snooppr/snoop/assets/61022210/aeea3c0e-0d1b-429e-8e42-725a6a1a6653

Snoop ne sélectionne que les géocoordonnées à partir de données sales (chiffres, lettres, caractères spéciaux).

</details>

<details>
<summary> 🟤 Logiciel d'auto-construction à partir de la source</summary>

**Installation native**
+ Remarque : ne le faites pas si vous voulez installer snoop sur android/termux
*(l'installation est différente, voir la section dédiée ci-dessous pour cela).*
+ Remarque : la version requise de Python 3.7+

```
# Cloner le dépôt
$ git clone https://github.com/snooppr/snoop

# Connectez-vous au répertoire de travail
$ cd ~/snoop

# Installez python3 et python3-pip s'ils ne sont pas installés
$ apt-get update && apt-get install python3 python3-pip

# Installer les dépendances 'exigences'
$ pip install --upgrade pip
$ python3 -m pip install -r requirements.txt
# Si au lieu des drapeaux des pays sont affichés dans des mélanges spéciaux, livrez un ensemble de polices, telles que monochrome
$ apt-get install ttf-ancient-fonts or color (recommander) $ apt-get install polices-noto-couleur-emoji
# Sur le système d'exploitation Windows, utilisez CMD ou PowerShell (au choix), mais pas ~~WSL~~ !
```
</details>

<details>
<summary> 🟢 En utilisant</summary>

```
usage: snoop_cli [search arguments...] nickname
or
usage: snoop_cli [service arguments | plugins arguments]


$ snoop_cli --help #manuel snoop build version GNU/Linux

Aider

optional arguments:
  -h, --help            afficher ce message d'aide et quitter

service arguments:
  --version, -V         versions d'impression de :: OS ; Espionner;
                        Python et licences
  --list-all, -l        Imprimer des informations détaillées sur la base
                        de données Snoop
  --donate, -d          Faites un don pour le développement du projet Snoop,
                        obtenez/achetez la version complète de Snoop
  --autoclean, -a       Supprimer tous les rapports, libérer de l'espace
  --update, -U          Mettre à jour Snoop

plugins arguments:
  --module, -m          Recherche OSINT : utilisez divers plugins Snoop ::
                        IP/GEO/YANDEX

search arguments:
  nickname              Le surnom de l'utilisateur recherché.
                        La recherche de plusieurs noms en même temps est prise en
                        charge. Les surnoms contenant un espace dans leur nom sont
                        entre guillemets
  --verbose, -v         Lors de la recherche de "surnom", imprimez la verbalisation
                        détaillée
  --web-base, -w        Connectez-vous pour rechercher 'surnom' dans la base de
                        données web mise à jour (plus de 3100+ sites Web).
                        Dans la version de démonstration, la fonction est désactivée
  --site , -s <site_name>
                        Spécifiez le nom du site à partir de la base de données
                        '--list-all'. Rechercher 'surnom' sur une ressource spécifiée,
                        il est acceptable d'utiliser l'option '-s' plusieurs fois
  --exclude , -e <country_code>
                        Exclure la région sélectionnée de la recherche, il est permis
                        d'utiliser l'option '-e' plusieurs fois, par exemple,
                        '-e RU -e WR' exclut la Russie et le Monde de la recherche
  --include , -i <country_code>
                        N'incluez que la région sélectionnée dans la recherche,
                        il est permis d'utiliser l'option '-i' plusieurs fois,
                        par exemple, '-i US -i UA' recherche pour les USA et l'Ukraine
  --country-sort, -c    Imprimer et enregistrer les résultats par pays, et non par
                        ordre alphabétique
  --time-out , -t <digit>
                        Définissez l'allocation de temps maximale pour attendre une
                        réponse du serveur (secondes). Affecte la durée de la recherche.
                        Affecte 'Erreurs de dépassement de délai :' Activé. cette option
                        est nécessaire avec une connexion Internet lente (par défaut 9s)
  --found-print, -f     Imprimer uniquement les comptes trouvés
  --no-func, -n         ✓Terminal monochrome, ne pas utiliser de couleurs dans l'url
                        ✓Désactiver le son
                        ✓Désactiver l'ouverture du navigateur Web
                        ✓Désactiver l'impression des drapeaux de pays
                        ✓Désactiver l'indication et l'état de progression
  --userlist , -u <file>
                        Spécifiez un fichier avec une liste d'utilisateurs.
                        Snoop traitera intelligemment les données et fournira des rapports
                        supplémentaires
  --save-page, -S       Enregistrer les pages utilisateur trouvées dans des fichiers locaux
  --cert-on, -C         Activez la vérification des certificats sur les serveurs. Par défaut,
                        la vérification des certificats sur les serveurs est désactivée,
                        ce qui vous permet de traiter les sites problématiques sans erreurs
  --headers , -H <User-Agent>
                        Définissez l'agent utilisateur manuellement, l'agent est entouré de
                        guillemets, par défaut, un agent utilisateur aléatoire ou remplacé
                        de la base de données snoop est défini pour chaque site
  --quick, -q           Mode de recherche rapide et agressif. Ne retraite pas les mauvaises
                        ressources, ce qui accélère la recherche, mais Bad_raw augmente
                        également. N'imprime pas les résultats intermédiaires. Consomme plus
                        de ressources. Le mode est efficace en version complète
```

**Exemple**
```
# Pour rechercher un seul utilisateur :
$ python3 snoop.py username1 #Exécution à partir de la source
$ snoop_cli username1 #Exécution à partir de la version Linux
# Ou, par exemple, le cyrillique est pris en charge :
$ python3 snoop.py олеся #Exécution à partir de la source
# Pour rechercher un nom contenant un espace :
$ snoop_cli "bob dylan" #Exécution à partir de la version Linux
$ snoop_cli dob_dylan #Exécution à partir de la version Linux
$ snoop_cli bob-dylan #Exécution à partir de la version Linux

# Fonctionnant sur le système d'exploitation Windows :
$ python snoop.py username1 #Exécution à partir de la source
$ snoop_cli.exe username1 #Exécution à partir des fenêtres de publication
# To search for one or more users:
$ snoop_cli.exe username1 username2 username3 username4 #Exécution à partir des fenêtres de publication

# Rechercher un grand nombre d'utilisateurs en triant la sortie des résultats par pays ;
# éviter les gels sur les sites Web (le plus souvent la "zone morte" dépend de l'adresse IP de l'utilisateur) ;
# n'imprime que les comptes trouvés ; enregistrer localement les pages des comptes trouvés ;
# spécifiez un fichier avec une liste de comptes recherchés ;
# connectez-vous à la base Web extensible et mise à jour Snoop pour la recherche :
$ snoop_cli -с -t 6 -f -S -u ~/file.txt -w #Exécution à partir de la version Linux
# consultez la base de données Snoop :
$ snoop_cli --list all #Exécution à partir de la version Linux
# imprimer l'aide pour les fonctions Snoop :
$ snoop_cli --help #Exécution à partir de la version Linux

# Activer les plug-ins Snoop :
$ snoop_cli --module #Exécution à partir de la version Linux
```
+ 'ctrl-c' — abandonner la recherche.
+ Les comptes trouvés seront stockés dans `~/snoop/results/nicknames/*{txt|csv|html}`.
+ Ouvrir csv dans office in, séparateur de champs **virgule**.
+ Détruire **tous** les résultats de la recherche — supprimez le répertoire '~/snoop/results'.
ou `snoop_cli.exe --autoclean #Exécution à partir de la version du système d'exploitation Windows`.
```
# Mettre à jour Snoop pour tester les nouvelles fonctionnalités du logiciel
$ python3 snoop.py --update #L'installation de Git est requise
```
</details>

<details>
<summary> 🔵 Fouineur pour Android</summary>

 • [Manuel détaillé en anglais](https://github.com/snooppr/snoop/blob/snoop_termux/README.en.md "Fouineur pour Android")

</details>

<details>
<summary> 🔴 Erreurs de base</summary>

|  Côté     |                         Problème                      | Solving |
|:---------:| ------------------------------------------------------|:-------:|
| ========= |=======================================================| ======= |
| Client    |Bloquez la connexion avec un pare-feu de               |    1    |
|           |protection proactive                                   |    1    |
|           |Débit insuffisant de la connexion Internet EDGE/3G     |    2    |
|           |La valeur de l'option '-t' est trop faible             |    2    |
|           |nom d'utilisateur invalide                             |    3    |
|           |Erreurs de connexion : [GipsysTeam; Nixp; Ddo]         |    7    |
| ========= |=======================================================| ======= |
|Fournisseur|Censure d'Internet                                     |    4    |
| ========= |=======================================================| ======= |
| Serveur   |Le site a changé sa réponse/API ;                      |    5    |
|           |CF/WAF a été mis à jour                                |    5    |
|           |Bloc. de la plage d'adr. IP du client par le serveur   |    4    |
|           |Déclencher/protéger une ressource captcha              |    4    |
|           |Certains sites sont momentanément indisponibles,       |    6    |
|           |travaux techniques                                     |    6    |
| ========= |=======================================================| ======= |

Résoudre :
1. Reconfigurez votre pare-feu *(par exemple, Kaspersky bloque les ressources pour les adultes).*

2. Vérifiez la vitesse de votre connexion Internet :
`python3 snoop.py -v username`
Si l'un des paramètres réseau est surligné en rouge, Snoop peut se bloquer pendant la recherche.
A basse vitesse, augmentez la valeur 'x' de l'option '--time-out x' :
`python3 snoop.py -t 15 username`.

3. En fait, ce n'est pas une erreur. Corriger le nom d'utilisateur
*(par exemple, certains sites n'autorisent pas les caractères cyrilliques ; "espaces" ou "encodage vietnamien-chinois"
dans les noms d'utilisateurs, afin de gagner du temps : - les requêtes sont filtrées).*

4. **Changer votre adresse IP**
La censure est la raison la plus courante pour laquelle l'utilisateur reçoit des erreurs de saut/des faux positifs/et dans certains cas '**Hélas**'.
Lorsque vous utilisez Snoop à partir de l'adresse IP du fournisseur de l'opérateur mobile, la vitesse **peut** chuter de manière significative, selon le fournisseur.
Par exemple, le moyen le plus efficace de résoudre le problème est ** D'UTILISER UN VPN **, Tor n'est pas très bien adapté à cette tâche. Règle : un scan depuis une adresse IP ne suffit pas pour tirer le meilleur parti de Snoop.

5. Ouvrir dans le référentiel Snoop sur Github-e Issue/Pull request
*(en informer le développeur).*

6. Ne faites pas attention, les sites partent parfois pour des travaux de réparation et se remettent en marche.

7. Il y a un [problème](https://wiki.debian.org/ContinuousIntegration/TriagingTips/openssl-1.1.1 "le problème est simple et résoluble") avec openssl dans certaines distributions GNU/Linux, et aussi le problème avec les sites qui n'ont pas été mis à jour depuis des années. Ces problèmes surviennent si l'utilisateur a intentionnellement lancé snoop avec l'option '--cert-on'.
Résoudre :
```
$ sudo nano /etc/ssl/openssl.cnf

# Modifiez les lignes tout en bas du fichier :
[MinProtocol = TLSv1.2]
sur
[MinProtocol = TLSv1]

[CipherString = DEFAULT@SECLEVEL=2]
sur
[CipherString = DEFAULT@SECLEVEL=1]
```
</details>

<details>
<summary> 🟠 Informations Complémentaires</summary>

 • [Historique du développement du projet](https://raw.githubusercontent.com/snooppr/snoop/master/changelog.txt "journal des modifications").

 • [Licence](https://github.com/snooppr/snoop/blob/master/COPYRIGHT "La version de la licence en anglais se trouve dans la version EN de Snoop Build").

 • [Documentation/ru](https://drive.google.com/open?id=12DzAQMgTcgeG-zJrfDxpUbFjlXcBq5ih).

 • **Empreinte de la clé publique :**	[076DB9A00B583FFB606964322F1154A0203EAE9D](https://raw.githubusercontent.com/snooppr/snoop/master/PublicKey.asc "clé pgp").

 • **Informations pour les fonctionnaires/UR :** Snoop Project est inclus dans le registre des logiciels domestiques avec le code déclaré : 26.30.11.16 Logiciel qui assure la mise en œuvre des actions établies lors des activités de recherche opérationnelle.
Arrêté du Ministère des communications de la Fédération de Russie n° 515 enregistré n° 7012.

 • **Snoop n'est pas parfait** : les sites Web tombent ; les balises de fermeture sont manquantes ; le réseau est censuré ; les services d'hébergement ne sont pas payés à temps.
De temps en temps, il faut suivre tout ce "Web rock'n'roll", alors les dons sont les bienvenus :
[exemple de sites Web fermés/mauvais](https://drive.google.com/file/d/1CJxGRJECezDsaGwxpEw34iJ8MJ9LXCIG/view?usp=sharing).

 • **Visualisation des commits :** de la naissance du projet au vendredi 13 2023.

https://user-images.githubusercontent.com/61022210/212534128-bc0e5779-a367-4d0a-86cb-c52503ee53c4.mp4
</details>

【RU -> FR】 Ceci est une traduction [➰Lisez-moi en russe](https://github.com/snooppr/snoop "Si vous le souhaitez, vous pouvez améliorer (PR) la traduction automatique de cette page en français").

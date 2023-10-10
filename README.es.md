Proyecto Snoop
=============

### Snoop Project Una de las herramientas OSINT más prometedoras para buscar apodos
- [X] Este es el software más potente teniendo en cuenta la ubicación de la CEI.

<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/EN__snoop.png" />

¿Tu vida es una presentación de diapositivas? Pregúntale a Snoop.  
El proyecto Snoop se desarrolla sin tener en cuenta las opiniones de la NSA y sus amigos,  
es decir, está al alcance del usuario medio *(14 de febrero de 2020)*.  

> *Snoop es un trabajo de desarrollo de investigación (base de datos propia/bugbounty cerrado) en la búsqueda y procesamiento de datos públicos en Internet. Según la búsqueda especializada de Snoop, es capaz de competir con los motores de búsqueda tradicionales.*  

Comparación de indexaciones de bases de datos tales herramientas:  
<img src="https://img.shields.io/badge/Snoop-~3200+%20sitios web-success" width="50%" />  
<img src="https://img.shields.io/badge/Sherlock-~400 sitios web-yellowgreen" width="20%" />  
<img src="https://img.shields.io/badge/Spiderfoot-~350 sitios web-yellowgreen" width="20%" />  
<img src="https://img.shields.io/badge/Whatsmyname-~300 sitios web-yellowgreen" width="20%" />  
<img src="https://img.shields.io/badge/Namechk-~100 websites-red" width="15%" />  


| Plataforma            | Apoyo |
|-----------------------|:---------:|
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/Linux.png" width="5%" /> GNU/Linux             |     ✅    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/Windows.png" width="5%" /> Windows 7/10 (32/64)  |     ✅    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/Android.png" width="5%" /> Android (Termux)      |     ✅    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/macOS.png" width="5%" /> macOS                 |     ❗️    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/IOS.png" width="5%" /> IOS                   |     🚫    |
| <img src="https://raw.githubusercontent.com/snooppr/snoop/master/icons/WSL.png" width="5%" /> WSL                   |     🚫    |  


Snoop para SO Windows y GNU/Linux
==================================

**Snoop Local database**  
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/EN_DB.png" />  
[Base de datos de la versión completa de Snoop Más de 3200+ sitios web ⚡️⚡️⚡️](https://github.com/snooppr/snoop/blob/master/websites.md "Database Snoop")  

## Liberar
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/snoop box.png" width="35%" />  

Snoop viene con ensamblajes listos para usar (versión) y no requiere dependencias (bibliotecas) ni la instalación de python, es decir, se ejecuta en una máquina limpia con sistema operativo Windows o GNU/Linux.  
┗━━ ⬇️[Descargar Proyecto Snoop](https://github.com/snooppr/snoop/releases "download the ready-made SNOOP assembly for Windows and GNU/Linux")  

<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/Run.gif"/>  

<details>
<summary> 🟣 Complementos del proyecto Snoop</summary>  

### 1. Demostración de uno de los métodos en el Complemento — 〘GEO_IP/domain〙  
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/GEO_IP.gif" />  

$$$$

Los informes también están disponibles en csv/txt/CLI/maps  
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/GEO_IPcsv.jpeg" />  

$$$$

### 2. Demostración de uno de los métodos en el Complemento — 〘Yandex_parser〙  
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/Yandex_parser.gif" />  

$$$$

Informe de búsqueda docena de nombre de usuario (Complemento - Yandex_parser)  
<img src="https://raw.githubusercontent.com/snooppr/snoop/master/images/Yandex_parser 4.png" />  

$$$$

### 3. Demostración de uno de los métodos en el Complemento — 〘Reverse Vgeocoder〙  
https://github.com/snooppr/snoop/assets/61022210/aeea3c0e-0d1b-429e-8e42-725a6a1a6653  

Snoop selecciona solo geocoordenadas de datos sucios (números, letras, caracteres especiales).  

</details>

<details>
<summary> 🟤 Software de autoconstrucción desde la fuente</summary>  

**Instalación Nativa**  
+ Nota: no hagas esto si quieres instalar snoop en Android/termux
*(la instalación es diferente, vea la sección dedicada a continuación para eso).*  
+ Nota: la versión requerida de Python 3.7+

```
# Clonar el repositorio
$ git clone https://github.com/snooppr/snoop

# Iniciar sesión en el directorio de trabajo
$ cd ~/snoop

# Instale python3 y python3-pip si no están instalados
$ apt-get update && apt-get install python3 python3-pip

# Instalar dependencias 'requisitos'
$ pip install --upgrade pip
$ python3 -m pip install -r requirements.txt
# Si en lugar de las banderas de los países se muestran en mezclas especiales, entregue un paquete de fuentes, como monocromo
$ apt-get install ttf-ancient-fonts or color (recomendado) $ apt-get install fonts-noto-color-emoji
# En el sistema operativo Windows, use CMD o PowerShell (para elegir según su conveniencia), ¡pero no ~~WSL~~!
```
</details>

<details>
<summary> 🟢 Usando</summary>  

```
uso: snoop_cli [argumentos de búsqueda...] nickname
o
uso: snoop_cli [argumentos de servicio | argumentos de complementos]


$ snoop_cli --help #versión de compilación manual de snoop GNU/Linux

Ayuda

argumentos opcionales:
  -h, --help            mostrar este mensaje de ayuda y salir

argumentos de servicio:
  --version, -V         Über: Druckversionen:: OS; schnüffeln; Python und Lizenzen
  --list-all, -l        Imprimir información detallada sobre la base
                        de datos de Snoop
  --donate, -d          Done al desarrollo del Proyecto Snoop, obtenga/compre
                        la versión completa de Snoop
  --autoclean, -a       Eliminar todos los informes, borrar espacio
  --update, -U          Actualizar Snoop

argumentos de complementos:
  --module, -m          OSINT search: use various plugins Snoop ::
                        IP/GEO/YANDEX

argumentos de búsqueda:
  nickname              Apodo del usuario buscado. Se admite la búsqueda
                        de varios nombres al mismo tiempo. Un apodo que contiene
                        un espacio en su nombre se escribe entre comillas
  --verbose, -v         Cuando busque 'apodo', imprima verbalización detallada
  --web-base, -w        Conéctese a una web_DB dinámicamente actualizada
                        (más de 3200+ sitios) para buscar 'apodo'.
                        En la versión de demostración, la función está deshabilitada
  --site , -s <site_name> 
                        Especifique el nombre del sitio de la base de datos '--list-all'.
                        Busque 'apodo' en un solo recurso especificado,
                        es aceptable usar la opción '-s' varias veces
  --exclude , -e <country_code> 
                        Excluye la región seleccionada de la búsqueda,
                        es aceptable usar la opción '-e' varias veces, por ejemplo,
                        '-e RU -e WR' excluye Rusia y el mundo de la búsqueda
  --include , -i <country_code> 
                        Incluya solo la región seleccionada en la búsqueda,
                        es aceptable usar la opción '-i' varias veces, por ejemplo,
                        '-i US -i UA' busque EE. UU. y Ucrania
  --country-sort, -c    Impresión y registro de resultados por país, no alfabéticamente
  --time-out , -t <digit> 
                        Establezca la asignación de tiempo máximo para esperar una
                        respuesta del servidor (segundos). Afecta a la duración de
                        la búsqueda. Afecta al 'Tiempo de espera de error'.
                        En esta opción es necesaria para una conexión a Internet
                        lenta (9s por defecto)
  --found-print, -f     Imprimir solo cuentas encontradas
  --no-func, -n         ✓Terminal monocromática, no usar colores en url
                        ✓Deshabilitar el sonido
                        ✓Deshabilitar la apertura del navegador web
                        ✓Deshabilitar la impresión de banderas de países
                        ✓Indicación de desactivación y estado de progreso
  --userlist , -u <file> 
                        Especifique un archivo con una lista de usuarios.
                        Snoop procesará los datos de forma inteligente
                        y proporcionará informes adicionales
  --save-page, -S       Guarde las páginas de usuario encontradas
                        en archivos html locales
  --cert-on, -C         Habilite la verificación de certificados en los servidores.
                        De forma predeterminada, la verificación de certificados
                        en los servidores está deshabilitada,
                        lo que le permite procesar sitios problemáticos sin errores
  --headers , -H <User-Agent> 
                        Establezca el agente de usuario manualmente,
                        el agente está entre comillas, de manera predeterminada,
                        se configura un agente de usuario aleatorio o anulado
                        de la base de datos de snoop para cada sitio
  --quick, -q           Modo de búsqueda rápido y agresivo.
                        No reprocesa los malos recursos, por lo que se acelera
                        la búsqueda, pero también aumenta Bad_raw. 
                        No imprime resultados intermedios. Consume más recursos.
                        El modo es efectivo en la versión completa
```

**Ejemplo**
```
# Para buscar solo un usuario:
$ python3 snoop.py username1 #Ejecutando desde la fuente
$ snoop_cli username1 #Ejecutando desde la versión de Linux
# O, por ejemplo, se admite cirílico:
$ python3 snoop.py олеся #Ejecutando desde la fuente
# Para buscar un nombre que contenga un espacio:
$ snoop_cli "bob dylan" #Ejecutando desde la versión de linux
$ snoop_cli dob_dylan #Ejecutando desde la versión de linux
$ snoop_cli bob-dylan #Ejecutando desde la versión de linux

# Ejecutándose en el sistema operativo Windows:
$ python snoop.py username1 #Corriendo desde la fuente
$ snoop_cli.exe username1 #Ejecución desde ventanas de lanzamiento
# Para buscar uno o más usuarios:
$ snoop_cli.exe username1 username2 username3 username4 #Ejecución desde ventanas de lanzamiento

# Busque una gran cantidad de usuarios: ordene la salida de los resultados por país;
# evitar bloqueos en sitios web (más a menudo, la "zona muerta" depende de la dirección IP del usuario);
# imprimir solo las cuentas encontradas; guardar páginas de cuentas encontradas localmente;
# especificar un archivo con una lista de cuentas buscadas;
# conectarse a la base web ampliable y actualizada de Snoop para la búsqueda:
$ snoop_cli -с -t 6 -f -S -u ~/file.txt -w #Ejecutando desde la versión de linux
# verifique la base de datos de Snoop:
$ snoop_cli --list all #Ejecutando desde la versión de Linux
# imprime la ayuda para las funciones de Snoop:
$ snoop_cli --help #Ejecutando desde la versión de Linux

# Habilitar los complementos de Snoop:
$ snoop_cli --module #Ejecutando desde la versión de Linux
```
+ 'ctrl-c' — abortar búsqueda.  
+ Las cuentas encontradas se almacenarán en `~/snoop/results/nicknames/*{txt|csv|html}`.  
+ Abrir csv en office in, separador de campo **coma**.  
+ Destruir todos los resultados de búsqueda: eliminar el '~/snoop/results' directorio.  
o `snoop_cli.exe --autoclean #Ejecutando desde la versión OS Windows`.
```
# Actualice Snoop para probar nuevas funciones en el software
$ python3 snoop.py --update #Se requiere la instalación de Git
```
</details>  

<details>
<summary> 🔵 Snoop para Android</summary>  

 • [Manual detallado en ingles](https://github.com/snooppr/snoop/blob/snoop_termux/README.en.md "Snoop para Android")  

</details>

<details>
<summary> 🔴 Errores básicos</summary>

|  Lado     |                         Problema                      | Resolv. |
|:---------:| ------------------------------------------------------|:-------:|
| ========= |=======================================================| ======= |
| Cliente   |Conexión bloqueada por defensa proactiva (*Kaspersky)  |    1    |
|           |Velocidad de conexión a Internet insuficiente EDGE/3G  |    2    |
|           |El valor de la opción '-t' es demasiado bajo           |    2    |
|           |nombre de usuario no válido                            |    3    |
|           |Err de conexión: [GipsysTeam; Nixp; Ddo; Mamochki]     |    7    |
| ========= |=======================================================| ======= |
| Proveedor |censura en internet                                    |    4    |
| ========= |=======================================================| ======= |
| Servidor  |El sitio ha cambiado su respuesta/API;                 |    5    |
|           |CF/WAF ha sido actualizado                             |    5    |
|           |Bloqueo del rango de direcciones IP del cliente por    |    4    |
|           |parte del servidor                                     |    4    |
|           |Activar/proteger un recurso de captcha                 |    4    |
|           |Algunos sitios no están disponibles temporalmente,     |    6    |
|           |trabajo técnico                                        |    6    |
| ========= |=======================================================| ======= |

Resolviendo:
1. Reconfigura tu Firewall *(por ejemplo, Kaspersky bloquea recursos para adultos)*.

2. Comprueba la velocidad de tu conexión a Internet:  
`python3 snoop.py -v nickname`  
Si alguna de las opciones de red está resaltada en rojo, es posible que Snoop se cuelgue durante la búsqueda.  
A baja velocidad, aumente el valor 'x' de la opción '--time-out x':  
`python3 snoop.py -t 15 nickname`  

3. De hecho, esto no es un error. Arreglar apodo  
*(por ejemplo, los caracteres cirílicos no están permitidos en algunos sitios; "espacios" o 'codificación Vietnam-Chino'
en los nombres de usuario, para ahorrar tiempo: - se filtran las solicitudes)*.

4. **Cambie su dirección IP**  
La censura son las razones más comunes por las que el usuario recibe errores de omisión/falsos positivos/y, en algunos casos, '**Alas**'.  
Al usar Snoop desde la dirección IP del proveedor del operador móvil, la velocidad **puede** disminuir significativamente, según el proveedor.  
Por ejemplo, la forma más efectiva de resolver el problema es **UTILIZAR UNA VPN**, Tor no es muy adecuado para esta tarea.  
Regla: un escaneo desde una ip no es suficiente para sacar el máximo provecho de Snoop.

5. Abrir en el repositorio de Snoop en Github-e Issue/Pull request  
*(informar al desarrollador sobre esto).*

6. No preste atención, los sitios a veces se reparan y vuelven a funcionar.

7. Hay [problema](https://wiki.debian.org/ContinuousIntegration/TriagingTips/openssl-1.1.1 "el problema es simple y solucionable") con openssl en algunas distribuciones GNU/Linux, y también el problema con sitios que no han sido actualizados en años. Estos problemas ocurren si el usuario inició snoop intencionalmente con la opción '--cert-on'.  
Resolviendo:
```
$ sudo nano /etc/ssl/openssl.cnf

# Edite las líneas en la parte inferior del archivo:
[MinProtocol = TLSv1.2]
en
[MinProtocol = TLSv1]

[CipherString = DEFAULT@SECLEVEL=2]
en
[CipherString = DEFAULT@SECLEVEL=1]
```
</details>

<details>
<summary> 🟠 Información adicional</summary>

 • [Historial de desarrollo del proyecto](https://raw.githubusercontent.com/snooppr/snoop/master/changelog.txt "registro de cambios").  

 • [Licencia](https://github.com/snooppr/snoop/blob/master/COPYRIGHT "La versión de la Licencia en inglés se puede encontrar en la versión EN de Snoop Build").  

 • [documentación/ruso](https://drive.google.com/open?id=12DzAQMgTcgeG-zJrfDxpUbFjlXcBq5ih).  

 • **Huella digital de clave pública:**	[076DB9A00B583FFB606964322F1154A0203EAE9D](https://raw.githubusercontent.com/snooppr/snoop/master/PublicKey.asc "pgp Clave").  

 • **Información para personas jurídicas/ruso:** Snoop Project está incluido en el registro de software doméstico con el código declarado: 26.30.11.16 Software que asegura la implementación de las acciones establecidas durante las actividades de búsqueda operativa.
Orden del Ministerio de Comunicaciones de la Federación Rusa No. 515 registrada No. 7012.  

 • **Snoop no es perfecto**: los sitios web están cayendo; faltan etiquetas de cierre; la red está siendo censurada; los servicios de hospedaje no se pagan a tiempo.  
De vez en cuando, es necesario seguir todo este "rock'n'roll web", por lo que las donaciones son bienvenidas:
[ejemplo de sitios web cercanos/malos](https://drive.google.com/file/d/1CJxGRJECezDsaGwxpEw34iJ8MJ9LXCIG/view?usp=sharing).  

 • **Visualización de commits:** from the birth of the project to Friday the thirteenth, 2023.  

https://user-images.githubusercontent.com/61022210/212534128-bc0e5779-a367-4d0a-86cb-c52503ee53c4.mp4  
</details>

【RU -> ES】 Este es un [➰Léame en ruso](https://github.com/snooppr/snoop "Si lo desea, puede mejorar (PR) la traducción automática de esta página en español").

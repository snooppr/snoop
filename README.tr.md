 Snoop Projesi 
=============
🇹🇷 ❤️ 🇷🇺
### Snoop Projesi, takma adları aramak için en umut verici OSINT araçlarından biridir.
- [X] Bu, CIS konumunu dikkate alan en güçlü yazılımdır.

<img src="https://github.com/snooppr/snoop/master/images/TR__snoop.png" />

Hayatınız bir slayt gösterisi mi? Snoop'a sorun.
Snoop projesi, NSA'nın ve onların arkadaşlarının görüşlerini dikkate almadan geliştirilmiştir,
yani ortalama kullanıcının erişimine açıktır *(proje oluşturma tarihi: 14 Şubat 2020)*.

> *Snoop, internet üzerindeki genel verilerin araştırılması ve işlenmesi için bir araştırma geliştirme çalışmasıdır (kendi veritabanı/kapalı hata avı).
Snoop'ın uzmanlaşmış aramasına göre, geleneksel arama motorlarıyla rekabet edebilme yeteneğine sahiptir.*

Bu tür araçların veritabanı dizinlemelerinin karşılaştırması:
<img src="https://img.shields.io/badge/Snoop-~3100+%20web sitesi-başarılı" width="50%" />
<img src="https://img.shields.io/badge/Sherlock-~350 web sitesi-sarı yeşil" width="20%" />
<img src="https://img.shields.io/badge/Spiderfoot-~350 web sitesi-sarı yeşil" width="20%" />
<img src="https://img.shields.io/badge/Whatsmyname-~300 web sitesi-sarı yeşil" width="20%" />
<img src="https://img.shields.io/badge/Namechk-~100 web sitesi-kırmızı" width="15%" />

| Platform              | Destek |
|-----------------------|:---------:|
| <img src="https://github.com/snooppr/snoop/master/icons/Linux.png" width="5%" /> GNU/Linux             |     ✅    |
| <img src="https://github.com/snooppr/snoop/master/icons/Windows.png" width="5%" /> Windows 7/10 (32/64)  |     ✅    |
| <img src="https://github.com/snooppr/snoop/master/icons/Android.png" width="5%" /> Android (Termux)      |     ✅    |
| <img src="https://github.com/snooppr/snoop/master/icons/macOS.png" width="5%" /> macOS                 |     ❗️    |
| <img src="https://github.com/snooppr/snoop/master/icons/IOS.png" width="5%" /> IOS                   |     🚫    |
| <img src="https://github.com/snooppr/snoop/master/icons/WSL.png" width="5%" /> WSL                   |     🚫    |

Snoop Windows ve GNU/Linux İçin
==================================

**Snoop Yerel veritabanı**
<img src="https://github.com/snooppr/snoop/master/images/TR_DB.png" />
[Snoop Tam sürüm veritabanı 3100+ web sitesi ⚡️⚡️⚡️](https://github.com/snooppr/snoop/blob/master/websites.md "Database Snoop")

## Sürüm
<img src="https://github.com/snooppr/snoop/master/images/snoop box.png" width="35%" />

Snoop, hazır montajlarla birlikte gelir ve bağımlılıkları (kütüphaneler) veya Python kurulumu gerektirmez, yani temiz bir makinede OS Windows veya GNU/Linux üzerinde çalışır.
┗━━ ⬇️[Snoop Projesi'ni İndirin](https://github.com/snooppr/snoop/releases "Windows ve GNU/Linux için hazır SNOOP montajını indirin")

<img src="https://github.com/snooppr/snoop/master/images/Run.gif"/>

<details>
<summary> 🟣 Snoop Projesi Eklentileri</summary>  

### 1. Eklentilerden birinin gösterimi — 〘GEO_IP/domain〙
<img src="https://github.com/snooppr/snoop/master/images/GEO_IP.gif" />

$$$$

Raporlar ayrıca csv/txt/CLI/haritalar olarak mevcuttur
<img src="https://github.com/snooppr/snoop/master/images/GEO_IPcsv.jpeg" />

$$$$

### 2. Eklentilerden birinin gösterimi — 〘Yandex_parser〙
<img src="https://github.com/snooppr/snoop/master/images/Yandex_parser.gif" />

$$$$

Kullanıcı adı araması (Eklenti — Yandex_parser) için raporlar
<img src="https://github.com/snooppr/snoop/master/images/Yandex_parser 4.png" />

$$$$

### 3. Eklentilerden birinin gösterimi — 〘Reverse Vgeocoder〙  
https://github.com/snooppr/snoop/assets/61022210/aeea3c0e-0d1b-429e-8e42-725a6a1a6653  

Snoop, kirli verilerden (sayılar, harfler, özel karakterler) yalnızca coğrafi koordinatları seçer.
</details>

<details>
<summary> 🟤 Kaynak kodundan kendiniz derleyerek yazılımı kullanma</summary>  

**Yerel Kurulum**  
+ Not: Bu işlemi android/termux'a snoop kurmak istiyorsanız yapmayın
*(kurulum farklıdır, bunun için ayrılan bölüme bakın).*
+ Not: Gerekli Python 3.7+ sürümü gerekmektedir.

Depoyu klonla

$ git clone https://github.com/snooppr/snoop
Çalışma dizinine gir

$ cd ~/snoop
Eğer kurulu değilse python3 ve python3-pip'i kur

$ apt-get update && apt-get install python3 python3-pip
Bağımlılıkları 'requirements' olarak kur

$ pip install --upgrade pip
$ python3 -m pip install -r requirements.txt
Bayrak yerine ülkelerin bayrakları özel karışımlarla görüntüleniyorsa, renk gibi bir font paketi yükleyin

$ apt-get install fonts-noto-color-emoji veya (monochrome) $ apt-get install ttf-ancient-fonts
Windows işletim sisteminde CMD veya PowerShell kullanın (konfora göre seçim yapın), ancak WSL kullanmayın!
</details>

<details>
<summary> 🟢 Kullanım</summary>  

kullanım: snoop_cli [arama argümanları...] takma ad
veya
kullanım: snoop_cli [hizmet argümanları | eklenti argümanları]

$ snoop_cli --help #manuel snoop GNU/Linux sürümünü çalıştırın

Yardım

isteğe bağlı argümanlar:
-h, --help bu yardım mesajını gösterir ve çıkar

hizmet argümanları:
--version, -V Sürümleri yazdır :: İşletim Sistemi; Snoop;
Python ve Lisanslar
--list-all, -l Snoop veritabanı hakkında ayrıntılı bilgiyi yazdırın
--donate, -d Snoop Projesi'nin geliştirilmesine bağış yapın,
Snoop Tam Sürümü alın/satın alın
--autoclean, -a Tüm raporları sil, alanı temizle
--update, -U Snoop'u güncelleyin

eklenti argümanları:
--module, -m OSINT araması: çeşitli eklentileri kullanın :: IP/GEO/YANDEX

arama argümanları:
takma ad Aranmak istenen kullanıcının takma adı.
Aynı anda birkaç isim arama desteklenir. İsimlerin adında
bir boşluk bulunuyorsa, adı tırnak işaretleri içine alın
--verbose, -v 'takma ad' aranırken ayrıntılı açıklamaları yazdırın
--web-base, -w 'takma ad' aramak için genişletilebilir ve güncellenmiş web_DB'ye bağlanın
(3100+ web sitesi). Demo sürümünde bu işlev devre dışı bırakılmıştır
--site , -s <site_adi>
Veritabanındaki sitenin adını belirtin
'--list-all'. 'takma ad'ı belirtilen bir kaynakta arayın,
'-s' seçeneğini birden fazla kez kullanmak kabul edilebilir
--exclude , -e <ülke_kodu>
Aramadan seçilen bölgeyi hariç tutun,
'-e' seçeneğini birden fazla kez kullanmak kabul edilebilir,
örneğin, '-e RU -e WR' Rusya ve Dünya'yı aramadan çıkarın
--include , -i <ülke_kodu>
Aramada sadece seçilen bölgeyi içerecek şekilde ayarlayın,
'-i' seçeneğini birden fazla kez kullanmak kabul edilebilir,
örneğin, '-i US -i UA' ABD ve Ukrayna için arama yapın
--country-sort, -c Ülkeye göre yazdır ve sonuçları kaydet
--time-out , -t <sayı>
Sunucudan yanıt bekleme için maksimum süre tahsis edin
(saniye). Arama süresini etkiler.
'Süre Aşımı hataları:' üzerine etki eder. Bu seçenek yavaş bir internet bağlantısıyla kullanılmak zorundadır (varsayılan olarak 9s)
--found-print, -f Yalnızca bulunan hesapları yazdır
--no-func, -n ✓Tek renkli terminal, url'lerde renk kullanma
✓Ses devre dışı
✓Web tarayıcıyı açmayı devre dışı bırak
✓Ülke bayraklarını yazdırmayı devre dışı bırak
✓İşaretlemeyi ve ilerleme durumunu devre dışı bırak
--userlist , -u <dosya>
Kullanıcı listesi içeren bir dosya belirtin. Snoop,
verileri zekice işleyecek ve ek raporlar sağlayacaktır
--save-page, -S Bulunan kullanıcı sayfalarını yerel dosyalara kaydedin
--cert-on, -C Sunuculardaki sertifikaları doğrulamayı etkinleştirin.
Varsayılan olarak, sunucudaki sertifika doğrulaması devre dışı bırakılmıştır,
bu da sorunlu siteleri hatalar olmadan işlemenizi sağlar
--headers , -H <Kullanıcı-Agent>
Kullanıcı ajanını el ile ayarlayın, ajan tırnak işaretleri içine alın,
varsayılan olarak rastgele veya geçersiz kılınan kullanıcı ajanı
her bir site için snoop veritabanından ayarlanır
--quick, -q Hızlı ve agresif arama modu. Kötü kaynakları yeniden işlemez,
bu nedenle arama hızlandırılır, ancak Bad_raw da artar.
Aralık sonuçlarını yazdırmaz. Daha fazla kaynak tüketir.
Mod tam sürümde etkilidir


**Örnek**
Sadece bir kullanıcı için arama:

$ python3 snoop.py kullanici_adi #Kaynaktan çalıştırma
$ snoop_cli kullanici_adi #Linux sürümünden çalıştırma
Veya örneğin, Kiril alfabesi desteklenir:

$ python3 snoop.py олеся #Kaynaktan çalıştırma
İsmi boşluk içeren bir isim arama:

$ snoop_cli "bob dylan" #Linux sürümünden çalıştırma
$ snoop_cli dob_dylan #Linux sürümünden çalıştırma
$ snoop_cli bob-dylan #Linux sürümünden çalıştırma
Windows işletim sisteminde çalıştırma:

$ python snoop.py kullanici_adi #Kaynaktan çalıştırma
$ snoop_cli.exe kullanici_adi #Windows sürümünden çalıştırma
Bir veya daha fazla kullanıcı arama:

$ snoop_cli.exe kullanici_adi kullanici_adi kullanici_adi kullanici_adi #Windows sürümünden çalıştırma
Çok sayıda kullanıcı arama - sonuçları ülkeye göre sıralama;
websitelerinde donmayı önleme (çoğu zaman "ölü bölge" kullanıcının ip adresine bağlıdır);
yalnızca bulunan hesapları yazdırma; bulunan hesapların sayfalarını yerel olarak kaydetme;
istenen hesapların listesini belirten bir dosya belirtme;
genişletilebilir ve güncellenen Snoop web tabanına bağlanma:

$ snoop_cli -с -t 6 -f -S -u ~/dosya.txt -w #Linux sürümünden çalıştırma
Snoop veritabanını kontrol etme:

$ snoop_cli --list all #Linux sürümünden çalıştırma
Snoop işlevlerinin yardımını yazdırma:

$ snoop_cli --help #Linux sürümünden çalıştırma
Snoop eklentilerini etkinleştirme:

$ snoop_cli --module #Linux sürümünden çalıştırma

+ 'ctrl-c' — aramayı iptal eder.
+ Bulunan hesaplar `~/snoop/results/nicknames/*{txt|csv|html}` içinde saklanır.
+ CSV'yi ofiste aynı şekilde aç, alan ayırıcı **virgül** olmalıdır.
+ Tüm arama sonuçlarını yok etmek için '~/snoop/results' dizinini silin.
veya `snoop_cli.exe --autoclean #Windows sürümünden çalıştırma`.

Snoop'u güncellemek, yazılımdaki yeni özellikleri test etmek için

$ python3 snoop.py --update #Git kurulumu gereklidir
</details>  

<details>
<summary> 🔵 Android için Snoop</summary>  

 • [Detaylı kılavuz İngilizce](https://github.com/snooppr/snoop/blob/snoop_termux/README.en.md "Android için Snoop")  

</details>

<details>
<summary> 🔴 Temel hatalar</summary>

|  Taraf    |                         Sorun                          | Çözüm |
|:---------:| -------------------------------------------------------|:-----:|
| ========= | ======================================================| ======= |
| İstemci   | Proaktif koruma Firewall ile bağlantıyı engelleme      |    1    |
|           | EDGE/3G İnternet bağlantısının yetersiz hızı          |    2    |
|           | '-t' seçeneğinin değeri çok düşük                    |    2    |
|           | geçersiz kullanıcı adı                                |    3    |
|           | Bağlantı hataları: [GipsysTeam; Nixp; Ddo; Mamochki] |    7    |
| ========= | ======================================================| ======= |
| Sağlayıcı | İnternet Sansürü                                     |    4    |
| ========= | ======================================================| ======= |
| Sunucu    | Site yanıtını/API'sını değiştirdi;                     |    5    |
|           | CF/WAF güncellendi                                   |    5    |
|           | Sunucunun IP adres aralığını engelleme                 |    4    |
|           | Captcha kaynağını tetikleme/korumaya alma               |    4    |
|           | Bazı siteler geçici olarak kullanılamaz, teknik çalışma |    6    |
| ========= | ======================================================| ======= |

Çözüm:
1. Firewall'ünüzü yeniden yapılandırın *(örneğin, Kaspersky yetişkinler için kaynakları engelliyor)*.

2. İnternet bağlantınızın hızını kontrol edin:
`python3 snoop.py -v kullanici_adi`
Ağ parametrelerinden herhangi biri kırmızıyla vurgulandıysa, Snoop arama sırasında takılabilir.
Düşük hızda, '--time-out x' seçeneğinin 'x' değerini artırın:
`python3 snoop.py -t 15 kullanici_adi`.

3. Aslında bu bir hata değil. Kullanıcı adını düzeltin
*(örneğin, bazı siteler Kiril karakterlerine izin vermez; "boşluklar" veya "Vietnamca-Çince kodlaması" ile ilgili diğer hatalar)*.

4. İnternet sansürü, IP aralığı engelleme (kısmi, "özür dilerim, alan adınızı bulamıyorum") hakkında sorunlar.
En iyi çözüm, VPN (Sanal Özel Ağ) veya Tor (gizlilik için bir ağ) kullanmaktır.
Kullanıcı adınız için hiçbir izlenme olmaksızın sitelere ve web hizmetlerine erişim sağlar.
Not: VKontakte, Odnoklassniki ve Mail.ru - ayrıca VK'un ses engellemesi.
Bazen hız düşük olabilir, ancak sansürlü sitelere erişim mümkün olacaktır.

5. API'yi ve API anahtarını güncelleme gerekliliği veya sitenin yasaklandığı anlamına gelir,
veya CloudFlare güvenliği (WAF) ayarlarını güncellemiş olabilir.
Not: En iyi çözüm VPN veya Tor kullanmaktır.

6. Bazı siteler geçici olarak çalışmayabilir, bu tür sorunlar teknik sorunlarla ilgilidir ve çözülmesi uzun sürebilir.
Kullanıcı adı kaynaklarına birkaç gün boyunca erişim sağlayamazsanız, daha sonra tekrar deneyin.

7. Eğer CF/WAF (CloudFlare/Web Application Firewall) hataları hakkında konuşuyorsak, sadece site sahibi bunları düzeltebilir.
Kullanıcılar bu tür hataları çözemez.

Eğer bu öneriler sorununuzu çözmezse, lütfen daha fazla destek için Snoop'un GitHub sayfasını ziyaret edin ve geliştirici ekibiyle iletişime geçin.

</details>
  
<details>
<summary> ⚫️  Geri bildirim</summary>  

Eğer Snoop Projesi hakkında sorunuz, öneriniz veya geri bildiriminiz varsa, lütfen aşağıdaki iletişim bilgilerini kullanarak bize ulaşın:

+  Web sitesi: [https://snoop-project.com/](https://snoop-project.com/)
+  GitHub: [https://github.com/snooppr/snoop](https://github.com/snooppr/snoop)
+  E-posta: [info@snoop-project.com](mailto:info@snoop-project.com)
+  Instagram: [https://www.instagram.com/snoop_project/](https://www.instagram.com/snoop_project/)
+  Grup: [https://t.me/snoop_project](https://t.me/snoop_project)
+  Discord: [https://discord.gg/BNUsXRG](https://discord.gg/BNUsXRG)

</details>

Snoop Projesi hakkında daha fazla bilgi almak veya projeyi indirmek isterseniz, yukarıdaki rehberi takip edebilirsiniz.

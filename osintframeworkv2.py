#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════╗
║      CODX OSINT FRAMEWORK v2.0           ║
║                @codza                    ║
║      Açık Kaynak İstihbarat Araçı        ║
╚══════════════════════════════════════════╝

NE İŞE YARAR?
─────────────
Bu araç, OSINT (Açık Kaynak İstihbarat) alanında
kullanılan en popüler web tabanlı araçları kategorize
ederek Termux üzerinden kolayca erişmenizi sağlar.


ÖZELLİKLER:
  ✦ 10 Kategori, 50+ OSINT aracı
  ✦ Favori kaydetme sistemi
  ✦ Araç içi arama
  ✦ Araç kopyalama (clipboard)
  ✦ Link geçmişi (son 10 ziyaret)
  ✦ Her araç için açıklama
  ✦ Termux otomatik URL açma
"""

import os
import sys
import subprocess
import json
import time

#RENKLER 
class C:
    GREEN   = '\033[92m'
    BLUE    = '\033[94m'
    YELLOW  = '\033[93m'
    RED     = '\033[91m'
    PURPLE  = '\033[95m'
    CYAN    = '\033[96m'
    WHITE   = '\033[97m'
    GRAY    = '\033[90m'
    END     = '\033[0m'
    BOLD    = '\033[1m'
    UL      = '\033[4m'

#VERİ DOSYALARI
DATA_DIR  = os.path.expanduser("~")
FAV_FILE  = os.path.join(DATA_DIR, ".codx_favorites.json")
HIST_FILE = os.path.join(DATA_DIR, ".codx_history.json")
NOTE_FILE = os.path.join(DATA_DIR, ".codx_notes.json")

def _load(path):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return []

def _save(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except:
        pass

favorites = _load(FAV_FILE)
history   = _load(HIST_FILE)   # [{"name":..,"url":..,"time":..}]
notes     = _load(NOTE_FILE)   # [{"url":..,"note":..}]

#OSINT VERİ KÜTÜPHANESİ
# Format: (Araç Adı, URL, Kısa Açıklama, Detaylı Kullanım)
OSINT_DATA = {
    "1": {
        "title": "📚 GENEL OSINT FRAMEWORKS",
        "desc":  "OSINT'e başlamak için en kapsamlı rehber ve araç listeleri.",
        "color": C.CYAN,
        "tools": [
            ("OSINT Framework",
             "https://osintframework.com/",
             "Tüm OSINT araçlarının interaktif ağaç haritası",
             "Soldaki menüden kategori seç, dallara tıklayarak araçlara ulaş. Başlangıç için ideal."),

            ("IntelTechniques",
             "https://inteltechniques.com/tools/index.html",
             "Michael Bazzell'in profesyonel araç koleksiyonu",
             "FBI eski ajanının kurduğu site. Sosyal medya, domain, kişi araması için formlar mevcut."),

            ("Bellingcat Toolkit",
             "https://docs.bellingcat.com/",
             "Araştırmacı gazeteci OSINT rehberi",
             "Coğrafi doğrulama, görsel analiz ve kaynak araştırması için adım adım kılavuzlar."),

            ("OSINT Curious",
             "https://osintcuriosity.com/",
             "OSINT topluluk blogu ve eğitim içerikleri",
             "Gerçek vaka analizleri ve teknik makaleler. Podcast serisi de mevcut."),

            ("Start.me OSINT",
             "https://start.me/p/rx6Qj8/nixintel-s-osint",
             "Nixintel'in kategorize araç başlangıç sayfası",
             "Tarayıcı başlangıç sayfası olarak ayarla. Yüzlerce araç tek ekranda."),
        ]
    },
    "2": {
        "title": "🔓 ŞİFRE & HASH KIRMA",
        "desc":  "Hash'lenmiş (MD5/SHA/NTLM) verileri tersine çevirir, sızdırılmış şifreleri arar.",
        "color": C.RED,
        "tools": [
            ("CrackStation",
             "https://crackstation.net/",
             "15 milyar+ hash içeren ücretsiz Rainbow Table DB",
             "MD5, SHA1, SHA256 destekler. Hash kutusuna yapıştır, 'Crack Hashes' tıkla."),

            ("Hashkiller",
             "https://hashkiller.io/",
             "MD5, SHA1, NTLM toplu hash kırma",
             "Birden fazla hash'i aynı anda kırabiliriz. 'Listmanager' ile toplu işlem."),

            ("LostMyPass",
             "https://www.lostmypass.com/",
             "Şifreli ZIP, RAR, PDF, Office dosya kurtarma",
             "Dosyayı yükle, şifre korumalı arşivler için brute-force dener."),

            ("MD5Decrypt",
             "https://md5decrypt.net/",
             "Hızlı MD5 & SHA1 tersine çevirme",
             "Sadece MD5/SHA1. En hızlı sonuç için ilk denenecek site."),

            ("Hashes.com",
             "https://hashes.com/en/decrypt/hash",
             "Hash tipi tanımlama + kırma servisi",
             "Hangi hash türü olduğunu bilmiyorsan önce 'Hash Analyzer' ile tespit et."),
        ]
    },
    "3": {
        "title": "🔡 ENCODING & STEGANOGRAFİ",
        "desc":  "Şifreli/kodlanmış metinleri çözer, görsel/ses içine gizlenmiş verileri ortaya çıkarır.",
        "color": C.PURPLE,
        "tools": [
            ("CyberChef",
             "https://gchq.github.io/CyberChef/",
             "İsviçre çakısı: 300+ şifre çözme & dönüşüm",
             "Sol panelden 'recipe' sürükle. 'Magic' butonu otomatik kodlama tespiti yapar. CTF için olmazsa olmaz."),

            ("D-Code.fr",
             "https://www.dcode.fr/",
             "800+ şifre ve kriptografi çözücü koleksiyonu",
             "Caesar, Vigenere, Morse dahil neredeyse her klasik şifre burada. Sağ üstten Türkçe seçilebilir."),

            ("Aperi'Solve",
             "https://www.aperisolve.com/",
             "Otomatik çoklu stego analiz (zsteg+stegano+exiftool)",
             "Görseli yükle, 10+ araçla otomatik tarar. CTF steganografi için tek durak."),

            ("StegOnline",
             "https://stegonline.georgeom.net/upload",
             "Bit düzeyinde görsel steganografi analizi",
             "LSB (En Anlamsız Bit) analizinde mükemmel. Renk kanallarını ayrı görüntüle."),

            ("Base64 Decode",
             "https://www.base64decode.org/",
             "Hızlı Base64 & Base32 çözücü",
             "URL Safe Base64 de destekler. 'Decode from File' ile dosyadan okuyabilir."),
        ]
    },
    "4": {
        "title": "🌐 DOMAIN & NETWORK",
        "desc":  "Alan adı geçmişi, DNS kayıtları, WHOIS ve internet'e bağlı cihaz araştırması.",
        "color": C.BLUE,
        "tools": [
            ("Shodan",
             "https://www.shodan.io/",
             "İnternet'e bağlı cihaz arama motoru (IoT/ICS)",
             "Kameralara, router'lara, ICS sistemlerine ulaş. 'country:TR port:22' gibi filtreler kullan."),

            ("DNS Dumpster",
             "https://dnsdumpster.com/",
             "DNS kayıtları ve subdomain haritası",
             "Domain gir, tüm DNS kayıtlarını ve subdomain'leri görselleştirir. Ücretsiz en iyisi."),

            ("WHOIS Lookup",
             "https://www.whois.com/whois/",
             "Domain kayıt tarihi ve sahip bilgileri",
             "Gizlilik koruması yoksa kayıt eden kişinin adı/mail/telefonu görünür."),

            ("crt.sh",
             "https://crt.sh/",
             "SSL sertifikası geçmişi ve subdomain tespiti",
             "'%.domain.com' araması ile tüm subdomain'leri listeler. Pasif keşif için güçlü."),

            ("Wayback Machine",
             "https://web.archive.org/",
             "Silinmiş/değiştirilmiş web sayfası arşivi",
             "URL gir, geçmişte nasıl göründüğünü gör. Delinen kanıtlar için kritik."),

            ("SecurityTrails",
             "https://securitytrails.com/",
             "Tarihsel DNS, IP ve subdomain veri tabanı",
             "Domaine bağlı eski IP'leri bul. CDN arkasındaki gerçek IP tespitinde kullanılır."),
        ]
    },
    "5": {
        "title": "🕵️ KİŞİ & SOSYAL MEDYA",
        "desc":  "İsim, e-posta, telefon veya yüz fotoğrafı üzerinden kimlik araştırması.",
        "color": C.YELLOW,
        "tools": [
            ("PimEyes",
             "https://pimeyes.com/en",
             "Yüz tanıma ile kişi internet araması",
             "Fotoğraf yükle, internette nerede çıktığını gösterir. Ücretsiz sürüm URL'leri gizler."),

            ("Sherlock",
             "https://sherlock-project.github.io/",
             "300+ platformda kullanıcı adı varlık tespiti",
             "Termux'ta: pip install sherlock-project && sherlock kullanici_adi"),

            ("Epieos",
             "https://epieos.com/",
             "E-posta ile Google/sosyal medya hesap araması",
             "Gmail gir, hangi servislere kayıtlı olduğunu gösterir. Telefon araması da yapar."),

            ("WhatsMyName",
             "https://whatsmyname.app/",
             "600+ sitede kullanıcı adı sorgulama",
             "Sherlock'a web alternatifi. Sonuçları JSON olarak indirebilirsin."),

            ("OSINT Industries",
             "https://www.osint.industries/",
             "E-posta/Tel ile kapsamlı profil oluşturma",
             "Ücretsiz 5 sorgu/gün. Sonuçları görsel zaman çizelgesi olarak sunar."),

            ("Maigret GitHub",
             "https://github.com/soxoj/maigret",
             "3000+ sitede profil araması (Sherlock++)",
             "Termux: pip install maigret && maigret kullanici_adi — Sherlock'tan çok daha kapsamlı."),
        ]
    },
    "6": {
        "title": "🗺️ COĞRAFİ KONUM & GÖRSEL",
        "desc":  "Fotoğraf koordinatları, uydu analizi ve gölge/güneş ile konum doğrulama.",
        "color": C.GREEN,
        "tools": [
            ("SunCalc",
             "https://suncalc.org/",
             "Gölge yönü ile fotoğraf konumu/zamanı tespiti",
             "Haritada konumu ayarla, tarih/saati değiştir. Gölgeler eşleşince konum/zaman bulunur."),

            ("Google Earth Web",
             "https://earth.google.com/web/",
             "3D uydu görüntüsü ve tarihsel görüntü karşılaştırma",
             "'Geçmiş görüntüler' ile yıllar içindeki değişimi izle. Koordinat arama destekler."),

            ("ExifTool Online",
             "https://exif.tools/",
             "Fotoğraf GPS & metadata (çekim tarihi/cihaz) okuma",
             "Fotoğrafı yükle, GPS varsa haritada gösterir. Sosyal medya paylaşımları metadata siler."),

            ("Mapillary",
             "https://www.mapillary.com/",
             "Topluluk katkılı sokak seviyesi fotoğraflar",
             "Google Street View'in olmadığı yerler dahil. Fotoğraftaki konumu doğrulamak için ideal."),

            ("GeoGuessr",
             "https://www.geoguessr.com/",
             "Sokak görüntüsünden konum tahmin oyunu/eğitimi",
             "OSINT için harika pratik. Tabelalar, bitki örtüsü, altyapıdan ülke tespit etmeyi öğretir."),

            ("What3Words",
             "https://what3words.com/",
             "3 kelime ile 3m² hassasiyetinde konum sistemi",
             "Adres sisteminin olmadığı yerlerde kullanılır. 'what3words.com/kelime.kelime.kelime' formatı."),
        ]
    },
    "7": {
        "title": "🎥 VİDEO ANALİZ",
        "desc":  "Video doğrulama, sahte tespit ve içeriğe gizlenmiş verileri bulma.",
        "color": C.CYAN,
        "tools": [
            ("InVID / WeVerify",
             "https://weverify.eu/verification-plugin/",
             "Video doğrulama ve deepfake tespit eklentisi",
             "Chrome eklentisi yükle. Video URL yapıştır, kare kare ters görsel arama yapar."),

            ("YouTube Metadata",
             "https://mattw.io/youtube-metadata/",
             "YouTube video gizli metadatası ve kanal bilgisi",
             "Video ID yapıştır. Yüklenme tarihi, düzenleme geçmişi, thumbnail versiyonlarını gösterir."),

            ("Watch Frame by Frame",
             "http://www.watchframebyframe.com/",
             "YouTube/Vimeo videolarını kare kare ilerleme",
             "Video URL gir, ok tuşlarıyla kare kare ilerle. Gizli mesaj/görüntü aramak için."),

            ("Amnesty Citizen Evidence",
             "https://citizenevidence.amnestyusa.org/",
             "YouTube videosunda tarih ve konum doğrulama",
             "Video URL gir. Yükleme zamanı, thumbnail bilgisi ve coğrafi veriyi analiz eder."),

            ("Bellingcat Toolkit",
             "https://docs.bellingcat.com/",
             "Araştırmacı gazetecilik OSINT kılavuzu",
             "Gerçek dünya vakalarına dayalı adım adım rehberler. Özellikle çatışma bölgesi doğrulama."),
        ]
    },
    "8": {
        "title": "🎵 SES ANALİZ & STEGO",
        "desc":  "Ses dosyasındaki spektogram analizi ve ses içine gizlenmiş mesajları çözme.",
        "color": C.PURPLE,
        "tools": [
            ("Academo Spectrum",
             "https://academo.org/demos/spectrum-analyzer/",
             "Gerçek zamanlı ses frekans spektrogramı",
             "Mikrofon veya dosya yükle. CTF'te görsel olarak mesaj gizlenmiş ses dosyaları burada çözülür."),

            ("Sonic Visualiser",
             "https://www.sonicvisualiser.org/",
             "Akademik düzeyde ses analiz ve görselleştirme",
             "İndir ve yükle. Spectrogram görünümüne geç (View > Add Spectrogram). En güçlü araç."),

            ("Steganography Online",
             "https://stylesuxx.github.io/steganography/",
             "Görsel içine metin gizleme & çıkarma (LSB)",
             "Encode: metin + görsel → steganografik görsel. Decode: şüpheli görseli yükle."),

            ("Audacity İndir",
             "https://www.audacityteam.org/download/",
             "Açık kaynak profesyonel ses editörü",
             "Termux: pkg install audacity (GUI gerekir). Spectogram: View > Spectrogram."),
        ]
    },
    "9": {
        "title": "🦠 MALWARE & LİNK ANALİZ",
        "desc":  "Şüpheli dosya/bağlantıyı açmadan sandbox ortamında analiz etme.",
        "color": C.RED,
        "tools": [
            ("VirusTotal",
             "https://www.virustotal.com/",
             "70+ antivirüs motoru ile dosya/URL/hash tarama",
             "Dosya yükle veya URL/hash yapıştır. 'Relations' sekmesi ile bağlantılı altyapıyı gör."),

            ("urlscan.io",
             "https://urlscan.io/",
             "Web sayfası davranışı, bağlantı ve kaynak analizi",
             "URL gir, sayfanın ekran görüntüsü, DOM, bağlantılar ve IP bilgisi raporlanır."),

            ("Any.run",
             "https://any.run/",
             "İnteraktif gerçek zamanlı malware sandbox",
             "Ücretsiz public sandbox. Dosyayı Windows VM'de çalıştır, ağ trafiğini canlı izle."),

            ("Hybrid Analysis",
             "https://www.hybrid-analysis.com/",
             "Falcon Sandbox destekli malware analiz raporu",
             "Dosya/URL gönder. MITRE ATT&CK etiketleri ile detaylı davranış raporu üretir."),

            ("Joe Sandbox",
             "https://www.joesandbox.com/",
             "Çok platformlu (Win/Mac/Android) sandbox analiz",
             "Android APK analizi için ideal. Ücretsiz rapor görüntüleme mevcut."),
        ]
    },
    "10": {
        "title": "🔍 VERİ SIZINTISI & E-POSTA",
        "desc":  "E-posta veya parolanın veri ihlallerinde yer alıp almadığını sorgular.",
        "color": C.YELLOW,
        "tools": [
            ("HaveIBeenPwned",
             "https://haveibeenpwned.com/",
             "E-posta adresinin hangi sızıntılarda yer aldığı",
             "E-postayı gir. Kaç ihlalde yer aldığını ve hangi verilerinin (şifre, tel, adres) sızdığını gösterir."),

            ("DeHashed",
             "https://dehashed.com/",
             "Sızdırılmış veri arama motoru (e-posta/kullanıcı/IP)",
             "Ücretsiz sorgu sayısı limitli. E-posta, kullanıcı adı, IP veya domain ile arama yapar."),

            ("LeakCheck",
             "https://leakcheck.io/",
             "E-posta ve kullanıcı adı sızıntı sorgulama",
             "API erişimi de mevcut. Termux scriptlerine entegre edilebilir."),

            ("Breach Directory",
             "https://breachdirectory.org/",
             "Ücretsiz kısmi hash görüntüleme ile sızıntı kontrolü",
             "Şifrenin SHA1 hash'ini kısmen gösterir. Tam şifreyi vermez ama ihlali kanıtlar."),

            ("Emailrep.io",
             "https://emailrep.io/",
             "E-posta adresi itibar ve risk skoru analizi",
             "API ile kullanılabilir: curl emailrep.io/hedef@mail.com — Spam/risk tespiti."),
        ]
    },
}

#YARDIMCI 
def clear():
    os.system('clear')

def open_url(url):
    for cmd in [["termux-open", url], ["xdg-open", url], ["open", url]]:
        try:
            r = subprocess.run(cmd, capture_output=True, timeout=3)
            if r.returncode == 0:
                return True
        except:
            continue
    return False

def copy_to_clipboard(text):
    """Termux clipboard"""
    try:
        subprocess.run(["termux-clipboard-set"], input=text.encode(), timeout=3)
        return True
    except:
        return False

def add_history(name, url):
    entry = {"name": name, "url": url, "time": time.strftime("%d.%m %H:%M")}
    history.insert(0, entry)
    if len(history) > 10:
        history.pop()
    _save(HIST_FILE, history)

def get_note(url):
    for n in notes:
        if n.get("url") == url:
            return n.get("note", "")
    return ""

def set_note(url, text):
    for n in notes:
        if n.get("url") == url:
            n["note"] = text
            _save(NOTE_FILE, notes)
            return
    notes.append({"url": url, "note": text})
    _save(NOTE_FILE, notes)

#BANNER
def banner():
    print(f"""{C.CYAN}{C.BOLD}
   ██████╗ ██████╗ ██████╗ ██╗  ██╗
  ██╔════╝██╔═══██╗██╔══██╗╚██╗██╔╝
  ██║     ██║   ██║██║  ██║ ╚███╔╝
  ██║     ██║   ██║██║  ██║ ██╔██╗
  ╚██████╗╚██████╔╝██████╔╝██╔╝ ██╗
   ╚═════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝{C.END}""")
    print(f"  {C.YELLOW}{C.BOLD}OSINT FRAMEWORK v2.0{C.END}  {C.GRAY}@codza{C.END}")
    print(f"  {C.GRAY}Açık Kaynak İstihbarat {C.END}")
    print(f"  {C.CYAN}" + "─"*42 + f"{C.END}")

def show_stats():
    total = sum(len(v["tools"]) for v in OSINT_DATA.values())
    cats  = len(OSINT_DATA)
    favs  = len(favorites)
    hist  = len(history)
    print(f"\n  {C.GRAY}📦 {cats} kategori  🛠️  {total} araç  ⭐ {favs} favori  🕐 {hist} geçmiş{C.END}\n")

#ANA MENÜ
def main_menu():
    clear()
    banner()
    show_stats()
    print(f"  {C.WHITE}{C.BOLD}KATEGORİLER:{C.END}\n")

    for key, value in OSINT_DATA.items():
        color = value.get("color", C.GREEN)
        cnt   = len(value["tools"])
        print(f"  {color}[{key:>2}]{C.END} {value['title']:<36}{C.GRAY}({cnt}){C.END}")

    print(f"\n  {C.CYAN}[ S] 🔎 Araç Ara{C.END}")
    print(f"  {C.YELLOW}[ F] ⭐ Favorilerim  [{len(favorites)}]{C.END}")
    print(f"  {C.BLUE}[ G] 🕐 Geçmişim     [{len(history)}]{C.END}")
    print(f"  {C.GREEN}[ H] ❓ Nasıl kullanılır?{C.END}")
    print(f"  {C.RED}[99] ❌ Çıkış{C.END}")
    print(f"\n  {C.CYAN}" + "─"*42 + f"{C.END}")

# ─── ALT MENÜ ──────────────────────────────────────────────
def sub_menu(choice):
    category = OSINT_DATA[choice]
    color    = category.get("color", C.GREEN)

    while True:
        clear()
        banner()
        print(f"\n  {color}{C.BOLD}{category['title']}{C.END}")
        print(f"  {C.GRAY}ℹ  {category['desc']}{C.END}\n")
        print(f"  {C.WHITE}{'':3}{'ARAÇ ADI':<22}AÇIKLAMA{C.END}")
        print(f"  {C.GRAY}" + "─"*55 + C.END)

        for i, (name, url, short_desc, _) in enumerate(category['tools'], 1):
            fav  = f"{C.YELLOW}★{C.END}" if url in favorites else " "
            note = f"{C.BLUE}✎{C.END}" if get_note(url) else " "
            print(f"  {fav}{note}{color}[{i}]{C.END} {C.WHITE}{name:<22}{C.END}{C.GRAY}{short_desc}{C.END}")

        print(f"\n  {C.CYAN}Komutlar:{C.END}")
        print(f"  {C.GRAY}[1-{len(category['tools'])}] Aç   [F#] Favori   [N#] Not   [D#] Detay   [0] Geri{C.END}")
        print(f"\n  {C.CYAN}" + "─"*42 + C.END)

        sub_choice = input(f"\n  {C.BOLD}>> {C.END}").strip()

        if sub_choice == "0":
            break

        # ── Favori toggle ──
        elif sub_choice.upper().startswith("F") and len(sub_choice) > 1:
            try:
                idx = int(sub_choice[1:]) - 1
                if 0 <= idx < len(category['tools']):
                    _, url, _, _ = category['tools'][idx]
                    name = category['tools'][idx][0]
                    if url in favorites:
                        favorites.remove(url)
                        print(f"\n  {C.GRAY}'{name}' favorilerden çıkarıldı.{C.END}")
                    else:
                        favorites.append(url)
                        print(f"\n  {C.YELLOW}⭐ '{name}' favorilere eklendi!{C.END}")
                    _save(FAV_FILE, favorites)
            except:
                pass
            time.sleep(1)

        # ── Not ──
        elif sub_choice.upper().startswith("N") and len(sub_choice) > 1:
            try:
                idx = int(sub_choice[1:]) - 1
                if 0 <= idx < len(category['tools']):
                    name, url, _, _ = category['tools'][idx]
                    mevcut = get_note(url)
                    if mevcut:
                        print(f"\n  {C.YELLOW}Mevcut not: {mevcut}{C.END}")
                    yeni = input(f"  {C.BOLD}Yeni not (boş bırak=sil): {C.END}").strip()
                    set_note(url, yeni)
                    print(f"  {C.GREEN}Not kaydedildi.{C.END}")
            except:
                pass
            time.sleep(1)

        # ── Detay ──
        elif sub_choice.upper().startswith("D") and len(sub_choice) > 1:
            try:
                idx = int(sub_choice[1:]) - 1
                if 0 <= idx < len(category['tools']):
                    name, url, short, detail = category['tools'][idx]
                    print(f"\n  {color}{C.BOLD}► {name}{C.END}")
                    print(f"  {C.WHITE}Özet   : {C.GRAY}{short}{C.END}")
                    print(f"  {C.WHITE}Kullanım: {C.CYAN}{detail}{C.END}")
                    print(f"  {C.WHITE}Link   : {C.PURPLE}{C.UL}{url}{C.END}")
                    not_m = get_note(url)
                    if not_m:
                        print(f"  {C.WHITE}Notum  : {C.YELLOW}{not_m}{C.END}")
            except:
                pass
            input(f"\n  {C.GRAY}ENTER...{C.END}")

        # ── Araç aç ──
        else:
            try:
                idx = int(sub_choice) - 1
                if 0 <= idx < len(category['tools']):
                    name, url, short, detail = category['tools'][idx]

                    print(f"\n  {color}{C.BOLD}► {name}{C.END}")
                    print(f"  {C.GRAY}{detail}{C.END}")
                    print(f"\n  {C.PURPLE}{C.BOLD}🔗 {C.UL}{url}{C.END}\n")

                    copied = copy_to_clipboard(url)
                    opened = open_url(url)

                    if opened:
                        print(f"  {C.GREEN}✓ Tarayıcıda açılıyor...{C.END}")
                    elif copied:
                        print(f"  {C.YELLOW}✓ Link panoya kopyalandı!{C.END}")
                    else:
                        print(f"  {C.YELLOW}⚠  Linki manuel kopyalayın.{C.END}")

                    not_m = get_note(url)
                    if not_m:
                        print(f"\n  {C.BLUE}📝 Notun: {not_m}{C.END}")

                    add_history(name, url)
                    input(f"\n  {C.GRAY}ENTER ile devam...{C.END}")
                else:
                    print(f"\n  {C.RED}[!] Geçersiz numara!{C.END}")
                    time.sleep(1)
            except ValueError:
                print(f"\n  {C.RED}[!] Geçerli bir komut girin.{C.END}")
                time.sleep(1)

# ─── ARAMA ─────────────────────────────────────────────────
def search_menu():
    clear()
    banner()
    print(f"\n  {C.CYAN}{C.BOLD}🔎 ARAÇ ARA{C.END}\n")
    query = input(f"  {C.BOLD}Arama kelimesi: {C.END}").strip().lower()
    if not query:
        return

    results = []
    for cat in OSINT_DATA.values():
        for name, url, short, detail in cat['tools']:
            if (query in name.lower() or query in short.lower()
                    or query in detail.lower() or query in cat['title'].lower()):
                results.append((cat['title'], cat.get('color', C.GREEN), name, url, short, detail))

    clear()
    banner()
    print(f"\n  {C.CYAN}🔎 \"{query}\" — {len(results)} sonuç{C.END}\n")

    if not results:
        print(f"  {C.RED}Sonuç bulunamadı.{C.END}")
        input(f"\n  {C.GRAY}ENTER...{C.END}")
        return

    for i, (cat_t, col, name, url, short, _) in enumerate(results, 1):
        fav = f"{C.YELLOW}★ {C.END}" if url in favorites else "  "
        print(f"  {fav}{col}[{i}]{C.END} {C.WHITE}{name}{C.END}")
        print(f"      {C.GRAY}{short}{C.END}")
        print(f"      {C.PURPLE}{C.UL}{url}{C.END}")
        print(f"      {C.YELLOW}📂 {cat_t}{C.END}\n")

    sub = input(f"  {C.BOLD}Aç (numara) / 0=geri: {C.END}").strip()
    try:
        idx = int(sub) - 1
        if 0 <= idx < len(results):
            _, _, name, url, _, detail = results[idx]
            print(f"\n  {C.CYAN}{detail}{C.END}")
            print(f"\n  {C.PURPLE}{C.BOLD}🔗 {C.UL}{url}{C.END}\n")
            copy_to_clipboard(url)
            open_url(url)
            add_history(name, url)
            input(f"  {C.GRAY}ENTER...{C.END}")
    except:
        pass

# ─── FAVORİLER ─────────────────────────────────────────────
def favorites_menu():
    while True:
        clear()
        banner()
        print(f"\n  {C.YELLOW}{C.BOLD}⭐ FAVORİLERİM{C.END}\n")

        if not favorites:
            print(f"  {C.GRAY}Favori araç yok.")
            print(f"  Alt menülerde [F#] ile ekleyebilirsin.{C.END}")
            input(f"\n  {C.GRAY}ENTER...{C.END}")
            return

        # URL'den isim bul
        fav_list = []
        for url in favorites:
            name = url
            for cat in OSINT_DATA.values():
                for t in cat['tools']:
                    if t[1] == url:
                        name = t[0]
                        break
            fav_list.append((name, url))

        for i, (name, url) in enumerate(fav_list, 1):
            not_m = get_note(url)
            print(f"  {C.YELLOW}[{i}]{C.END} {C.WHITE}{name}{C.END}")
            print(f"      {C.GRAY}{url}{C.END}")
            if not_m:
                print(f"      {C.BLUE}📝 {not_m}{C.END}")
            print()

        print(f"  {C.RED}[C] Tümünü sil  [0] Geri{C.END}")
        ch = input(f"\n  {C.BOLD}Aç (numara): {C.END}").strip()

        if ch == "0":
            break
        elif ch.upper() == "C":
            favorites.clear()
            _save(FAV_FILE, favorites)
            print(f"  {C.GREEN}Favoriler temizlendi.{C.END}")
            time.sleep(1)
            break
        else:
            try:
                idx = int(ch) - 1
                if 0 <= idx < len(fav_list):
                    name, url = fav_list[idx]
                    print(f"\n  {C.PURPLE}{C.BOLD}🔗 {C.UL}{url}{C.END}\n")
                    copy_to_clipboard(url)
                    open_url(url)
                    add_history(name, url)
                    input(f"  {C.GRAY}ENTER...{C.END}")
            except:
                pass

# ─── GEÇMİŞ ────────────────────────────────────────────────
def history_menu():
    while True:
        clear()
        banner()
        print(f"\n  {C.BLUE}{C.BOLD}🕐 ZİYARET GEÇMİŞİ{C.END}\n")

        if not history:
            print(f"  {C.GRAY}Henüz geçmiş yok.{C.END}")
            input(f"\n  {C.GRAY}ENTER...{C.END}")
            return

        for i, entry in enumerate(history, 1):
            print(f"  {C.BLUE}[{i}]{C.END} {C.WHITE}{entry['name']}{C.END}  {C.GRAY}{entry['time']}{C.END}")
            print(f"      {C.GRAY}{entry['url']}{C.END}\n")

        print(f"  {C.RED}[C] Geçmişi temizle  [0] Geri{C.END}")
        ch = input(f"\n  {C.BOLD}Aç (numara): {C.END}").strip()

        if ch == "0":
            break
        elif ch.upper() == "C":
            history.clear()
            _save(HIST_FILE, history)
            print(f"  {C.GREEN}Geçmiş temizlendi.{C.END}")
            time.sleep(1)
            break
        else:
            try:
                idx = int(ch) - 1
                if 0 <= idx < len(history):
                    entry = history[idx]
                    print(f"\n  {C.PURPLE}{C.BOLD}🔗 {C.UL}{entry['url']}{C.END}\n")
                    copy_to_clipboard(entry['url'])
                    open_url(entry['url'])
                    input(f"  {C.GRAY}ENTER...{C.END}")
            except:
                pass

# ─── YARDIM ─────────────────────────────────────────────────
def help_menu():
    clear()
    banner()
    print(f"""
  {C.CYAN}{C.BOLD}❓ NASIL KULLANILIR?{C.END}

  {C.WHITE}Bu araç hakkında:{C.END}
  {C.GRAY}CODX, OSINT (Açık Kaynak İstihbarat) alanındaki
  en popüler web araçlarını kategorize eden ve
  Termux üzerinden kolayca erişim sağlayan eğitim
  amaçlı bir framework'tür.{C.END}

  {C.WHITE}Temel Komutlar:{C.END}
  {C.GREEN}[1-10]{C.END}  {C.GRAY}Kategori menüsüne gir{C.END}
  {C.CYAN}[S]{C.END}     {C.GRAY}Araç adı/açıklama ile arama{C.END}
  {C.YELLOW}[F]{C.END}     {C.GRAY}Favori araçların listesi{C.END}
  {C.BLUE}[G]{C.END}     {C.GRAY}Son ziyaret ettiğin araçlar{C.END}

  {C.WHITE}Alt Menü Komutları:{C.END}
  {C.GREEN}[#]{C.END}     {C.GRAY}Araç linkini aç{C.END}
  {C.YELLOW}[F#]{C.END}    {C.GRAY}Favoriye ekle/çıkar (F2, F5...){C.END}
  {C.BLUE}[N#]{C.END}    {C.GRAY}Araca not ekle (N1, N3...){C.END}
  {C.CYAN}[D#]{C.END}    {C.GRAY}Detaylı kullanım rehberi gör{C.END}

  {C.WHITE}Termux Kurulum:{C.END}
  {C.GRAY}pkg install python
  python codx_osint.py{C.END}

  {C.WHITE}Veriler nerede saklanır?{C.END}
  {C.GRAY}~/.codx_favorites.json  → Favoriler
  ~/.codx_history.json    → Geçmiş
  ~/.codx_notes.json      → Notlar{C.END}
""")
    input(f"  {C.GRAY}ENTER ile çık...{C.END}")

# ─── ANA DÖNGÜ ─────────────────────────────────────────────
def main():
    while True:
        main_menu()
        choice = input(f"\n  {C.BOLD}CODX > {C.END}").strip().upper()

        if choice == "99":
            clear()
            print(f"\n  {C.CYAN}Görüşmek üzere! 🎬 YouTube'u takip etmeyi unutma.{C.END}\n")
            sys.exit(0)
        elif choice == "S":
            search_menu()
        elif choice == "F":
            favorites_menu()
        elif choice == "G":
            history_menu()
        elif choice == "H":
            help_menu()
        elif choice in OSINT_DATA:
            sub_menu(choice)
        else:
            print(f"\n  {C.RED}[!] Geçersiz komut.{C.END}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {C.CYAN}Görüşmek üzere!{C.END}\n")
        sys.exit(0)

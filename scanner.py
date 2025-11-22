import argparse
import requests
import sys
import textwrap
from tabulate import tabulate  # tablo kütüphanesi
from colorama import Fore, Style, init

init(autoreset=True)

BANNER = f"""{Fore.CYAN}
    #######################################################
    #           HTTP HEADER SECURITY SCANNER v1.3         #
    #           ---------------------------------         #
    #           Coded by: Yasin (Cyber Security)          #
    #######################################################
{Style.RESET_ALL}"""

GUVENLIK_BASLIKLARI = {
    "Strict-Transport-Security": "Tarayıcıyı HTTPS kullanmaya zorlar (Man-in-the-Middle engeller).",
    "X-Frame-Options": "Sitenin başka sitelerde iframe içine alınmasını (Clickjacking) engeller.",
    "X-Content-Type-Options": "Dosya türü kandırmacalarını (MIME-sniffing) engeller.",
    "Content-Security-Policy": "XSS saldırılarını ve veri enjeksiyonunu engelleyen en kritik başlıktır.",
    "X-XSS-Protection": "Eski tarayıcılar için dahili XSS filtresini açar.",
    "Referrer-Policy": "Kullanıcı linke tıkladığında karşı tarafa giden kaynak bilgisini sınırlar.",
    "Permissions-Policy": "Kamera, mikrofon, konum gibi donanımlara izinsiz erişimi kapatır.",
    "Cross-Origin-Opener-Policy": "Siteyi diğer sekmelerden izole eder (Spectre saldırılarına karşı).",
    "Cross-Origin-Resource-Policy": "Başka sitelerin senin görsellerini/dosyalarını çalmasını engeller."
}

def argumanlari_al():
    print(BANNER)
    from argparse import RawTextHelpFormatter

    parser = argparse.ArgumentParser(
        description="HTTP Header Güvenlik Tarayıcısı",
        formatter_class=RawTextHelpFormatter,
        epilog=f"""{Fore.YELLOW}
Örnek Kullanım:
    python3 scanner.py -u https://google.com
    python3 scanner.py -u https://hedefsite.com -o sonuc.txt
{Style.RESET_ALL}""",
        add_help=False
    )

    parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS, help="Bu yardım menüsünü gösterir")
    parser.add_argument("-u", "--url", dest="hedef_url", help="Taranacak hedef URL")
    parser.add_argument("-o", "--output", dest="dosya_adi", metavar="DOSYA", help="Rapor dosyası")
    
    args = parser.parse_args()
    
    if not args.hedef_url:
        parser.print_help()
        sys.exit()
        
    return args

def siteye_baglan(url):
    try:
        kimlik = {'User-Agent': 'Mozilla/5.0 (compatible; SecurityScanner/1.3)'}
        print(f"{Fore.BLUE}[INFO] {url} adresine bağlanılıyor...{Style.RESET_ALL}")
        cevap = requests.get(url, headers=kimlik, timeout=10)
        return cevap.headers
    except Exception as e:
        print(f"{Fore.RED}[HATA] Bağlantı sorunu: {e}{Style.RESET_ALL}")
        return None

def main():
    args = argumanlari_al()
    url = args.hedef_url
    site_headerlari = siteye_baglan(url)

    if not site_headerlari:
        return

    print(f"\n{Fore.CYAN}[*] Analiz Tamamlandı. Tablo oluşturuluyor...{Style.RESET_ALL}\n")

    # Tablo verilerini tutacağımız boş liste
    tablo_verisi = []

    for baslik, aciklama in GUVENLIK_BASLIKLARI.items():
        # Açıklamayı 50 karakterde bir alt satıra indir 
        aciklama_sarilmis = textwrap.fill(aciklama, width=50)

        if baslik in site_headerlari:
            durum = f"{Fore.GREEN}[+] MEVCUT{Style.RESET_ALL}"
            # Tabloya satır ekle: [Durum, Başlık İsmi, Açıklama]
            tablo_verisi.append([durum, f"{Fore.GREEN}{baslik}{Style.RESET_ALL}", f"{Fore.WHITE}{aciklama_sarilmis}{Style.RESET_ALL}"])
        else:
            durum = f"{Fore.RED}[-] EKSİK{Style.RESET_ALL}"
            # Tabloya satır ekle
            tablo_verisi.append([durum, f"{Fore.RED}{baslik}{Style.RESET_ALL}", f"{Fore.WHITE}{aciklama_sarilmis}{Style.RESET_ALL}"])

    # --- TABLOYU OLUŞTUR VE BAS ---

    basliklar = ["DURUM", "GÜVENLİK BAŞLIĞI", "AÇIKLAMA"]
    tablo_ciktisi = tabulate(tablo_verisi, headers=basliklar, tablefmt="fancy_grid")
    
    print(tablo_ciktisi)

    # --- DOSYAYA KAYDETME ---
    if args.dosya_adi:
        try:
            with open(args.dosya_adi, "w", encoding="utf-8") as dosya:
                dosya.write(f"Hedef: {url}\n\n")
                dosya.write(tabulate(tablo_verisi, headers=basliklar, tablefmt="grid"))
            print(f"\n{Fore.CYAN}[INFO] Tablolu rapor kaydedildi: {args.dosya_adi}{Style.RESET_ALL}")
        except Exception as e:
            print(f"\n{Fore.RED}[HATA] Dosya yazılamadı: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
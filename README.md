# HTTP Header Security Scanner 🛡️

Web sitelerinin HTTP güvenlik başlıklarını analiz etmek için geliştirilmiş basit, renkli ve tablo tabanlı bir komut satırı aracıdır. Penetrasyon test uzmanlarının ve geliştiricilerin eksik güvenlik önlemlerini hızlıca tespit etmesine yardımcı olur.

## Ekran Görüntüsü

<img width="820" height="660" alt="image" src="https://github.com/user-attachments/assets/9c8407fc-1593-4b19-b230-475ddbe604e8" />

## Özellikler

* **Hızlı Analiz:** `requests` kütüphanesi ile seri tarama yapar.
* **Renkli Çıktı:** `colorama` ile okunaklı ve renkli sonuçlar verir.
* **Tablo Formatı:** `tabulate` kullanarak sonuçları profesyonel bir tablo içinde sunar.
* **Raporlama:** Sonuçları `-o` parametresi ile dosyaya kaydeder.
* **Kimlik Gizleme:** Kendini gerçek bir tarayıcı gibi tanıtarak (User-Agent Spoofing) temel güvenlik duvarlarını atlatır.

## Kurulum

1.  **Projeyi bilgisayarınıza indirin:**
    ```bash
    git clone https://github.com/myasinagzikuru/http-header-scanner.git
    cd http-header-scanner
    ```

2.  **Sanal Ortam oluşturun:**
    *(Sistem kütüphanelerinizin bozulmaması ve hata almamak için bu adım önerilir)*
    ```bash
    python3 -m venv venv
    ```

3.  **Sanal Ortamı aktif edin:**

        ```bash
        source venv/bin/activate
        ```

4.  **Gerekli kütüphaneleri yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```
## Kullanım

**Temel Tarama:**
```bash
python3 scanner.py -u https://google.com

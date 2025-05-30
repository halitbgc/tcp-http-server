# TCP Tabanlı Basit HTTP Sunucusu

> **Açık Kaynak Kodlu Yazılımlar** dersi kapsamında geliştirilmiştir.

## 📝 Proje Bilgileri

* **Ders:** Açık Kaynak Kodlu Yazılımlar (Marmara Üniversitesi)
* **Dönem:** 2024–2025 Bahar
* **Ödev:** HTTP Web Sunucusu Geliştirme

## 📋 Proje Tanımı

Bu proje, Python ile yazılmış, çoklu bağlantı (threading) destekli, TCP soket tabanlı bir HTTP sunucusudur. Temel olarak:

* Statik dosyaları (`.html`, `.css`, `.js`, resimler vb.) `/static` dizini altından sunar.
* `/api/hello` ve `/api/echo` gibi basit JSON API uç noktaları sağlar.
* Doğru MIME türü belirlemesi için Python’un `mimetypes` modülünü kullanır.
* HTTP 404 ve 500 hata yanıtları döner.
* Dockerfile ve `docker-compose.yml` ile containerize edilebilir.

## 🚀 Özellikler

1. **TCP Socket Üzerinden HTTP İstekleri**

   * GET ve POST metodlarını işler.
2. **Statik Dosya Servisi**

   * `/static` altındaki tüm kaynakları sunar.
3. **JSON API Uç Noktaları**

   * `GET /api/hello` → `{"message":"Hello, world!"}`
   * `POST /api/echo` → Gönderilen JSON’u echo’lar.
4. **MIME Tipi Belirleme**

   * `mimetypes.guess_type` ile Content-Type başlığı.
5. **Çoklu Bağlantı Desteği**

   * Her istemci isteği yeni bir thread içinde işlenir.
6. **Hata Yönetimi**

   * 404 Not Found ve 500 Internal Server Error sayfaları.
7. **Containerization**

   * Dockerfile ve opsiyonel `compose.yml` ile kolay deploy.

## 📂 Dosya Yapısı

```
project-root/
├── server.py            # Ana sunucu kodu
├── static/              # Statik kaynaklar (HTML/CSS/JS)
│   └── index.html       # Örnek anasayfa
├── .dockerignore        # Docker için ignore listesi
├── Dockerfile           # Docker imajı inşa tanımı
├── compose.yml          # Opsiyonel çoklu servis tanımı
├── README.md            # Bu dosya
├── LICENSE              # MIT Lisansı
├── NOTICE.md            # Telif ve kullanım bildirimi
├── CONTRIBUTING.md      # Katkıda bulunma rehberi
├── CODE_OF_CONDUCT.md   # Davranış kuralları
└── DELIVERY.md          # Teslimat ve çalışma yönergeleri
```

## ⚙️ Kurulum & Çalıştırma

### Yerel Kurulum

```bash
git clone <repo-url>
cd project-root
python server.py
```

Tarayıcıdan `http://localhost:8080` adresine gidin.

### Docker ile Çalıştırma

```bash
docker build -t my-http-server .
docker run --rm -p 8080:8080 my-http-server
```

Opsiyonel olarak:

```bash
docker-compose up --build
```

## 🤝 Katkıda Bulunma

Katkı için:

1. Fork’layın ve feature branch açın.
2. Değişiklik yapın, test edin, commit edin.
3. Pull request gönderin.

Detaylar için [CONTRIBUTING.md](./CONTRIBUTING.md)’a bakın.

## 📜 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır. Detaylar için [LICENSE](./LICENSE) dosyasına bakın.
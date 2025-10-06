# 🎯 Vize Randevu Yönetim Sistemi

Modern, güvenli ve kullanıcı dostu bir vize randevu yönetim sistemi. Flask ve MySQL ile geliştirilmiştir.

## 🌟 Özellikler

### 👨‍💼 Yönetici Paneli
- ✅ Kullanıcı yönetimi (oluşturma, düzenleme, silme)
- ✅ Ülke yönetimi ve kota atamaları
- ✅ Randevu talepleri yönetimi
- ✅ Güncelleme/Silme talepleri onaylama
- ✅ Detaylı sistem logları ve raporlama
- ✅ Gelişmiş filtreleme ve arama özellikleri

### 👥 Danışman Paneli
- ✅ Atanmış ülkeler için randevu oluşturma
- ✅ Kota takibi ve yönetimi
- ✅ Randevu düzenleme ve silme (belirli koşullarda)
- ✅ Güncelleme/Silme talepleri oluşturma
- ✅ Dashboard ve istatistikler

### 🔐 Güvenlik
- ✅ Güvenli şifre hashleme (Werkzeug)
- ✅ Flask-Login ile oturum yönetimi
- ✅ CSRF koruması
- ✅ IP adresi takibi
- ✅ Rol tabanlı erişim kontrolü

## 🚀 Hızlı Başlangıç

### Yerel Geliştirme

```bash
# Repository'yi klonlayın
git clone https://github.com/KULLANICI_ADINIZ/vize-randevu-sistemi.git
cd vize-randevu-sistemi

# Sanal ortam oluşturun
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# .env dosyası oluşturun
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# .env dosyasını düzenleyin:
# - SECRET_KEY: Güçlü bir anahtar
# - DB_HOST, DB_USER, DB_PASSWORD, DB_NAME: MySQL bilgileri
# - ADMIN_USERNAME, ADMIN_PASSWORD, ADMIN_EMAIL

# Veritabanını başlatın
python init_railway_db.py

# Uygulamayı çalıştırın
python app.py
```

Uygulama http://localhost:5000 adresinde çalışacaktır.

### Railway'e Deploy

Detaylı deployment rehberi için [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) dosyasına bakın.

**Hızlı Adımlar:**

1. GitHub'a push yapın
2. Railway'de yeni proje oluşturun
3. MySQL veritabanı ekleyin
4. Environment variables ayarlayın
5. Deploy!

## 📋 Gereksinimler

- Python 3.9+
- MySQL 8.0+
- Flask 3.0+
- Gunicorn (production için)

## 🔧 Yapılandırma

### Environment Variables

```bash
# Güvenlik
SECRET_KEY=your-secret-key-here

# Veritabanı
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your-password
DB_NAME=vize_randevu_db

# Admin Bilgileri
ADMIN_USERNAME=admin
ADMIN_PASSWORD=Admin123!
ADMIN_EMAIL=admin@example.com
```

### MySQL Veritabanı

Railway'de otomatik olarak oluşturulur. Yerel geliştirme için:

```sql
CREATE DATABASE vize_randevu_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 📚 Dokümantasyon

- [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) - Railway deployment rehberi
- [YONETICI_KULLANIM_KLAVUZU.md](YONETICI_KULLANIM_KLAVUZU.md) - Yönetici kullanım kılavuzu
- [DANISMAN_KULLANIM_KLAVUZU.md](DANISMAN_KULLANIM_KLAVUZU.md) - Danışman kullanım kılavuzu

## 🗂️ Proje Yapısı

```
.
├── app.py                      # Ana uygulama
├── config.py                   # Yapılandırma
├── models.py                   # Veritabanı modelleri
├── forms.py                    # Form tanımları
├── utils.py                    # Yardımcı fonksiyonlar
├── init_railway_db.py         # DB kurulum scripti
├── requirements.txt            # Python bağımlılıkları
├── Procfile                    # Railway/Heroku için
├── nixpacks.toml              # Railway build config
├── railway.json               # Railway deployment config
├── templates/                  # HTML şablonları
│   ├── base.html
│   ├── login.html
│   ├── admin/                 # Yönetici şablonları
│   └── user/                  # Kullanıcı şablonları
├── static/                     # Statik dosyalar
│   ├── css/
│   ├── js/
│   └── src/
└── exports/                    # Rapor dosyaları
```

## 🎨 Teknolojiler

### Backend
- **Flask** - Web framework
- **Flask-SQLAlchemy** - ORM
- **Flask-Login** - Kullanıcı oturum yönetimi
- **Flask-WTF** - Form işleme ve CSRF koruması
- **PyMySQL** - MySQL bağlantısı
- **Gunicorn** - WSGI server (production)

### Frontend
- **TailwindCSS** - CSS framework
- **JavaScript (Vanilla)** - İnteraktif özellikler
- **Font Awesome** - İkonlar

### Database
- **MySQL 8.0+** - İlişkisel veritabanı

## 🔒 Güvenlik Özellikleri

- ✅ Şifre hashleme (Werkzeug security)
- ✅ CSRF token koruması
- ✅ Session yönetimi
- ✅ IP adresi loglaması
- ✅ Rol tabanlı yetkilendirme
- ✅ SQL injection koruması (SQLAlchemy ORM)
- ✅ XSS koruması (Jinja2 auto-escaping)

## 📊 Özellikler Detayı

### Kullanıcı Yönetimi
- Kullanıcı oluşturma, düzenleme, silme
- Aktif/Pasif durum kontrolü
- Admin/Danışman rol ataması
- Kota yönetimi

### Randevu Yönetimi
- Dinamik form alanları (ülkeye göre)
- Durum takibi (Bekleme, Süreç Başlatıldı, Tamamlandı, İptal)
- Gelişmiş filtreleme ve arama
- Excel/PDF rapor oluşturma

### Talep Sistemi
- Düzenleme talepleri
- Silme talepleri
- Admin onay/red sistemi
- Talep geçmişi

### Log Sistemi
- Tüm işlemler loglanır
- IP adresi takibi
- Cihaz tipi belirleme
- Gelişmiş log filtreleme

## 🌐 Deployment Seçenekleri

### Railway (Önerilen)
- Otomatik deployment
- MySQL eklentisi
- SSL sertifikası
- Custom domain desteği

### Diğer Platformlar
- Heroku
- DigitalOcean
- AWS
- Google Cloud
- Azure

## 🐛 Sorun Giderme

### Problem: Database connection failed

**Çözüm:**
```bash
# MySQL servisinin çalıştığından emin olun
# Environment variables'ları kontrol edin
# config.py dosyasındaki bağlantı ayarlarını doğrulayın
```

### Problem: Static files not loading

**Çözüm:**
```bash
# static/ klasörünün mevcut olduğunu kontrol edin
# .gitignore'da exclude edilmediğinden emin olun
# Flask debug=True modda statik dosyaları otomatik serve eder
```

### Problem: Import errors

**Çözüm:**
```bash
# Tüm bağımlılıkların yüklü olduğundan emin olun
pip install -r requirements.txt --upgrade
```

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/YeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -m 'Yeni özellik: XYZ'`)
4. Branch'inizi push edin (`git push origin feature/YeniOzellik`)
5. Pull Request oluşturun

## 📝 Lisans

Bu proje özel kullanım içindir.

## 📧 İletişim

Sorularınız için:
- GitHub Issues: [Repository Issues](https://github.com/KULLANICI_ADINIZ/REPO_ADINIZ/issues)
- Email: admin@yourcompany.com

## 🎉 Teşekkürler

Bu proje aşağıdaki açık kaynak projeleri kullanmaktadır:
- Flask ve Flask eklentileri
- TailwindCSS
- Font Awesome
- ve daha fazlası...

---

**Made with ❤️ for efficient visa appointment management**

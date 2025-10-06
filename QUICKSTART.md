# 🚀 HIZLI BAŞLANGIÇ KILAVUZU

## ⚡ 5 Dakikada Başlat

### 1️⃣ Kurulum (İlk Kez)

**Windows PowerShell:**
```powershell
.\setup.ps1
```

**Windows CMD:**
```cmd
setup.bat
```

**Manuel Kurulum:**
```bash
# 1. Virtual environment oluştur
python -m venv venv

# 2. Aktif et (Windows)
venv\Scripts\activate

# 3. Bağımlılıkları yükle
pip install -r requirements.txt

# 4. .env dosyasını yapılandır
copy .env.example .env
# .env dosyasını düzenle!
```

### 2️⃣ Veritabanını Kur

**⚡ Otomatik Kurulum (ÖNERİLEN):**

```powershell
.\setup_database.ps1
```

Bu script:
- ✅ MySQL'i otomatik bulur
- ✅ Veritabanını ve tabloları oluşturur
- ✅ Admin kullanıcısı ekler (admin / Admin123!)
- ✅ 15 ülke ekler
- ✅ .env dosyasını günceller

**Manuel Kurulum:**

```bash
# Yöntem 1: SQL dosyası ile
mysql -u root -p < database_setup.sql

# Yöntem 2: Python ile
python init_db.py
```

**📚 Detaylı Bilgi:**
- 📖 `DATABASE_GUIDE.md` - Kapsamlı veritabanı kılavuzu
- 📄 `DATABASE_README.md` - Hızlı başlangıç özeti

### 3️⃣ Sistemi Başlat

```bash
python run.py
```

veya

```bash
python app.py
```

### 4️⃣ Giriş Yap

Tarayıcıda aç: **http://localhost:5000**

**Admin Girişi:**
- Kullanıcı: `admin`
- Şifre: `Admin123!`

**Test Kullanıcı:**
- Kullanıcı: `user1`
- Şifre: `User123!`

---

## 📋 Hızlı İşlemler

### Admin İşlemleri

#### Yeni Kullanıcı Ekle
1. Dashboard → Kullanıcılar
2. "Yeni Kullanıcı" butonuna tıkla
3. Bilgileri doldur
4. Kaydet

#### Kota Ata
1. Kullanıcılar → Kullanıcıyı düzenle
2. Aşağı kaydır → "Kota Ekle"
3. Ülke ve limit seç
4. Ekle

#### Rapor Al
1. Randevular sayfasına git
2. Filtreleme yap (opsiyonel)
3. "Excel İndir" veya "PDF İndir"

### Kullanıcı İşlemleri

#### Randevu Oluştur
1. Dashboard → Ülke seçbir (örn: 🇺🇸 Amerika)
2. "Yeni Kişi Ekle" butonuna tıkla
3. Başvuran bilgilerini gir
4. Kaydet

#### Randevu Düzenle
1. Randevularım → Randevuyu bul
2. "Düzenle" butonuna tıkla (sadece "Bekleme" durumundayken)
3. Değişiklikleri yap
4. Kaydet

#### Güncelleme Talebi Gönder
1. "Süreç Başlatıldı" durumundaki randevuyu bul
2. "Talep" butonuna tıkla
3. Talep nedenini yaz
4. Gönder

---

## 🔧 Yaygın Sorunlar

### "ModuleNotFoundError"
```bash
# Virtual environment aktif mi?
venv\Scripts\activate

# Bağımlılıkları yeniden yükle
pip install -r requirements.txt
```

### "Can't connect to MySQL"
```bash
# MySQL çalışıyor mu?
net start MySQL80

# .env dosyasındaki bilgiler doğru mu?
# DB_HOST, DB_USER, DB_PASSWORD, DB_NAME kontrol et
```

### "Port 5000 is already in use"
```python
# app.py dosyasında portu değiştir:
app.run(debug=True, host='0.0.0.0', port=5001)
```

### "Admin şifresini unuttum"
```bash
# Veritabanını sıfırla
python init_db.py
```

---

## 📚 Önemli Dosyalar

| Dosya | Açıklama |
|-------|----------|
| `app.py` | Ana uygulama |
| `run.py` | Başlatma scripti |
| `init_db.py` | Veritabanı ilklendirme |
| `.env` | Yapılandırma (GİZLİ!) |
| `models.py` | Veritabanı modelleri |
| `forms.py` | Form tanımları |
| `utils.py` | Yardımcı fonksiyonlar |

---

## 🎯 İlk Adımlar

### Sistem Yöneticisi için:

1. ✅ Sisteme giriş yap
2. ✅ Ülkeleri kontrol et (veya yeni ekle)
3. ✅ Kullanıcılar oluştur
4. ✅ Her kullanıcıya ülke kotaları ata
5. ✅ Kullanıcıları bilgilendir (kullanıcı adı/şifre)

### Kullanıcı için:

1. ✅ Sistem yöneticisinden kullanıcı adı/şifre al
2. ✅ Sisteme giriş yap
3. ✅ Dashboard'da atanmış ülkeleri gör
4. ✅ Randevu talebi oluştur
5. ✅ Durumu takip et

---

## 🌟 İpuçları

💡 **Performans için:** Production'da `FLASK_DEBUG=False` yapın

💡 **Güvenlik için:** `.env` dosyasındaki `SECRET_KEY`'i değiştirin

💡 **Yedekleme için:** Düzenli MySQL dump alın
```bash
mysqldump -u root -p vize_randevu_db > backup.sql
```

💡 **Geri yükleme için:**
```bash
mysql -u root -p vize_randevu_db < backup.sql
```

---

## 📞 Yardım

Sorun mu yaşıyorsunuz?

1. README.md dosyasını okuyun
2. Terminal'de hata mesajlarını kontrol edin
3. .env dosyanızı kontrol edin
4. MySQL bağlantınızı test edin

---

**Başarılar! 🎉**

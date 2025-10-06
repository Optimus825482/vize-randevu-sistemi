# 🗄️ VERİTABANI KURULUM DOSYALARI

Bu klasördeki veritabanı ile ilgili dosyalar ve kullanım amaçları:

---

## 📄 Dosya Listesi

### 1️⃣ `database_setup.sql`
**Ana SQL kurulum dosyası**

**İçerik:**
- ✅ Veritabanı oluşturma (vize_randevu_db)
- ✅ Kullanıcı oluşturma ve yetkilendirme
- ✅ 6 tablo (users, countries, user_country_quotas, appointments, update_requests, system_logs)
- ✅ Foreign key kısıtlamaları
- ✅ Index'ler
- ✅ 3 View (istatistik görünümleri)
- ✅ 2 Stored Procedure (kota kontrolü, istatistikler)
- ✅ 3 Trigger (insert/update/delete logları)
- ✅ Örnek veriler (admin + 15 ülke)
- ✅ Doğrulama sorguları

**Kullanım:**
```bash
mysql -u root -p < database_setup.sql
```

**Satır Sayısı:** ~400 satır

---

### 2️⃣ `setup_database.ps1`
**PowerShell otomatik kurulum scripti**

**Özellikler:**
- 🔍 MySQL'i otomatik bulur
- 🔒 Güvenli şifre girişi
- ✅ SQL dosyasını otomatik çalıştırır
- 📝 .env dosyasını günceller
- 🎨 Renkli çıktı (yeşil/kırmızı)
- ⚠️ Hata yönetimi

**Kullanım:**
```powershell
.\setup_database.ps1
```

**Gereksinimler:**
- Windows PowerShell 5.0+
- MySQL 5.7+

---

### 3️⃣ `DATABASE_GUIDE.md`
**Kapsamlı veritabanı kurulum kılavuzu**

**Bölümler:**
- 📖 Hızlı başlangıç
- 🛠️ Manuel kurulum adımları
- 📊 Tablo yapıları (detaylı)
- 👁️ View kullanımları
- 🔧 Stored procedure örnekleri
- 🔄 Trigger açıklamaları
- 💾 Yedekleme/Geri yükleme
- 🚨 Sorun giderme
- 🔐 Güvenlik önerileri
- ✅ Test sorguları

**Kullanım:**
Markdown okuyucu ile açın veya VS Code'da görüntüleyin

**Satır Sayısı:** ~300 satır

---

### 4️⃣ `DATABASE_README.md`
**Hızlı başvuru özeti**

**İçerik:**
- ⚡ 3 kurulum yöntemi
- 📋 Oluşturulan nesneler listesi
- 🔐 Varsayılan şifreler
- ⚙️ .env ayarları
- ✅ Kurulum doğrulama
- 🚨 Hızlı sorun giderme

**Kullanım:**
İlk kez kurulum yapacaklar için

**Satır Sayısı:** ~150 satır

---

### 5️⃣ `init_db.py`
**Python veritabanı başlatma scripti**

**Özellikler:**
- 🔄 Tabloları oluşturur
- 👤 Admin kullanıcısı ekler
- 🌍 Örnek ülkeler ekler
- 👥 Test kullanıcıları oluşturur
- 📊 Örnek kotalar atar

**Kullanım:**
```bash
python init_db.py
```

**Ne zaman kullanılır:**
- İlk kurulumda
- Veritabanını sıfırlamak için
- Test verileri eklemek için

---

## 🎯 Hangi Dosyayı Kullanmalıyım?

### Senaryo 1: İlk kez kurulum (Windows)
✅ **`setup_database.ps1`** kullanın
- En kolay yöntem
- Tamamen otomatik
- Hata kontrolü var

### Senaryo 2: Manuel kurulum
✅ **`database_setup.sql`** kullanın
```bash
mysql -u root -p < database_setup.sql
```

### Senaryo 3: phpMyAdmin/Workbench ile
✅ **`database_setup.sql`** dosyasını açın
- SQL sekmesine gidin
- Dosyayı import edin

### Senaryo 4: Python ile kurulum
✅ **`init_db.py`** kullanın
```bash
python init_db.py
```

### Senaryo 5: Detaylı bilgi gerekli
✅ **`DATABASE_GUIDE.md`** okuyun
- Tüm detaylar burada
- Sorun giderme burada

### Senaryo 6: Hızlı başvuru
✅ **`DATABASE_README.md`** okuyun
- Özet bilgi
- Hızlı hatırlatıcılar

---

## 🔄 Kurulum Akışı

```
1. README.md veya QUICKSTART.md oku
           ↓
2. setup_database.ps1 çalıştır
   (veya database_setup.sql kullan)
           ↓
3. .env dosyasını kontrol et
           ↓
4. python run.py ile başlat
           ↓
5. http://localhost:5000'e git
```

---

## 📊 Oluşturulan Veritabanı Nesneleri

| Nesne Tipi | Sayı | Dosya |
|------------|------|-------|
| Veritabanı | 1 | database_setup.sql |
| Tablo | 6 | database_setup.sql |
| View | 3 | database_setup.sql |
| Stored Procedure | 2 | database_setup.sql |
| Trigger | 3 | database_setup.sql |
| Kullanıcı | 1 | database_setup.sql |
| Örnek Ülke | 15 | database_setup.sql |
| Admin | 1 | database_setup.sql |

**Toplam:** 32 veritabanı nesnesi

---

## 🔐 Güvenlik Notları

### Varsayılan Şifreler
```
MySQL Kullanıcısı: vize_user
Şifre: VizeSecure2025!

Admin Kullanıcısı: admin
Şifre: Admin123!
```

### ⚠️ Production'da Mutlaka:
- ✅ MySQL şifresini değiştirin
- ✅ Admin şifresini değiştirin
- ✅ .env dosyasını gizli tutun
- ✅ Düzenli yedek alın

### Şifre Değiştirme
```sql
-- MySQL şifresi
ALTER USER 'vize_user'@'localhost' IDENTIFIED BY 'YeniGüvenliŞifre';

-- Admin şifresi (uygulama içinden)
Dashboard → Kullanıcılar → admin → Düzenle
```

---

## 💾 Yedekleme

### Yedek Alma
```bash
mysqldump -u root -p vize_randevu_db > backup_$(date +%Y%m%d).sql
```

### Geri Yükleme
```bash
mysql -u root -p vize_randevu_db < backup_20250105.sql
```

---

## 🚨 Sorun Giderme

### "ERROR 1045: Access denied"
- MySQL root şifresini kontrol edin
- Veya farklı kullanıcı ile deneyin

### "ERROR 1007: Can't create database"
- Veritabanı zaten var
- `DROP DATABASE vize_randevu_db;` ile silin

### "ERROR 2002: Can't connect"
- MySQL servisi çalışıyor mu?
- `net start MySQL80` (Windows)

### PowerShell script çalışmıyor
```powershell
# Execution policy ayarlayın
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📞 Yardım

Sorun devam ediyorsa:

1. ✅ `DATABASE_GUIDE.md` dosyasını okuyun
2. ✅ Hata mesajını not alın
3. ✅ MySQL log dosyalarını kontrol edin
4. ✅ .env dosyasının doğru olduğundan emin olun

---

## 🎓 Öğrenme Kaynakları

- **Tablolar:** `DATABASE_GUIDE.md` → "Tablo Yapısı" bölümü
- **View'lar:** `DATABASE_GUIDE.md` → "View Kullanımı" bölümü
- **Procedures:** `DATABASE_GUIDE.md` → "Stored Procedures" bölümü
- **Triggers:** `DATABASE_GUIDE.md` → "Triggers" bölümü

---

**Son Güncelleme:** 2025-01-05

**Versiyon:** 1.0.0

---

**Hazırsınız! 🚀**

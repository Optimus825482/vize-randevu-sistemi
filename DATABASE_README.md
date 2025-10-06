# 🗄️ VERİTABANI KURULUM - ÖZET

## 🎯 3 Farklı Yöntem

### ⚡ Yöntem 1: Otomatik Script (EN KOLAY)

```powershell
# PowerShell'de çalıştırın
.\setup_database.ps1
```

**Ne yapar?**
- ✅ MySQL'i otomatik bulur
- ✅ Veritabanını oluşturur
- ✅ Tabloları oluşturur
- ✅ Örnek verileri ekler
- ✅ .env dosyasını günceller

---

### 💻 Yöntem 2: MySQL Command Line

```bash
# 1. MySQL'e bağlan
mysql -u root -p

# 2. SQL dosyasını çalıştır
source database_setup.sql;
quit;
```

veya tek komutta:

```bash
mysql -u root -p < database_setup.sql
```

---

### 🌐 Yöntem 3: phpMyAdmin / MySQL Workbench

1. phpMyAdmin veya MySQL Workbench'i aç
2. "SQL" sekmesine git
3. `database_setup.sql` dosyasını aç veya içeriğini kopyala
4. Çalıştır

---

## 📋 Oluşturulan Veritabanı Nesneleri

### Tablolar (6 adet)
1. **users** - Kullanıcılar
2. **countries** - Ülkeler
3. **user_country_quotas** - Kullanıcı kotaları
4. **appointments** - Randevu talepleri
5. **update_requests** - Güncelleme/silme talepleri
6. **system_logs** - Sistem logları

### View'lar (3 adet)
1. **view_user_appointment_stats** - Kullanıcı istatistikleri
2. **view_country_appointment_stats** - Ülke istatistikleri
3. **view_user_quota_usage** - Kota kullanım durumu

### Stored Procedures (2 adet)
1. **sp_check_user_quota** - Kota kontrolü
2. **sp_get_appointment_statistics** - Randevu istatistikleri

### Trigger'lar (3 adet)
1. **trg_after_appointment_insert** - Randevu oluşturma logu
2. **trg_after_appointment_update** - Randevu güncelleme logu
3. **trg_after_appointment_delete** - Randevu silme logu

### Örnek Veriler
- ✅ Admin kullanıcısı
- ✅ 15 ülke
- ✅ Veritabanı kullanıcısı (vize_user)

---

## 🔐 Varsayılan Bilgiler

### MySQL Kullanıcısı
```
Host: localhost
Kullanıcı: vize_user
Şifre: VizeSecure2025!
Veritabanı: vize_randevu_db
```

### Uygulama Girişi
```
Kullanıcı: admin
Şifre: Admin123!
```

---

## ⚙️ .env Dosyası Ayarları

Kurulumdan sonra `.env` dosyanızı güncelleyin:

```env
DB_HOST=localhost
DB_USER=vize_user
DB_PASSWORD=VizeSecure2025!
DB_NAME=vize_randevu_db
```

⚠️ **Production'da mutlaka şifreyi değiştirin!**

---

## ✅ Kurulum Kontrolü

### Tabloları Kontrol Et
```sql
USE vize_randevu_db;
SHOW TABLES;
```

**Beklenen Çıktı:** 6 tablo görmeli

### Verileri Kontrol Et
```sql
SELECT * FROM countries;
SELECT * FROM users;
```

**Beklenen:** 15 ülke, 1 admin kullanıcısı

---

## 🚨 Sorun Giderme

### "Access denied"
```sql
-- Şifreyi kontrol edin
-- Veya yeni kullanıcı oluşturun:
CREATE USER 'vize_user'@'localhost' IDENTIFIED BY 'YeniŞifre';
GRANT ALL PRIVILEGES ON vize_randevu_db.* TO 'vize_user'@'localhost';
FLUSH PRIVILEGES;
```

### "Database exists"
```sql
-- Eski veritabanını silin (DİKKAT: Veriler silinir!)
DROP DATABASE vize_randevu_db;
-- SQL dosyasını tekrar çalıştırın
```

### "Can't connect to MySQL"
```bash
# MySQL servisini başlatın
# Windows:
net start MySQL80

# Linux:
sudo systemctl start mysql
```

---

## 📚 Detaylı Bilgi

Daha fazla bilgi için:
- 📖 **DATABASE_GUIDE.md** - Detaylı kurulum kılavuzu
- 📄 **database_setup.sql** - SQL dosyası (incelemek için)

---

## 🎯 Sonraki Adım

Veritabanı kurulumu tamamlandıktan sonra:

```powershell
# Uygulamayı başlat
python run.py
```

Tarayıcıda: **http://localhost:5000**

---

**Hazırsınız! 🚀**

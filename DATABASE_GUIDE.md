# 🗄️ VERİTABANI KURULUM KILAVUZU

## 📋 İçindekiler
1. [Hızlı Kurulum](#hızlı-kurulum)
2. [Manuel Kurulum](#manuel-kurulum)
3. [Tablo Yapısı](#tablo-yapısı)
4. [Yedekleme ve Geri Yükleme](#yedekleme-ve-geri-yükleme)

---

## 🚀 Hızlı Kurulum

### Yöntem 1: MySQL Command Line (Önerilen)

```bash
# 1. MySQL'e bağlan
mysql -u root -p

# 2. SQL dosyasını çalıştır
source d:/Claude/panel/database_setup.sql;

# veya tek komutta:
mysql -u root -p < d:/Claude/panel/database_setup.sql
```

### Yöntem 2: PowerShell

```powershell
# MySQL bin klasörünü PATH'e ekleyin veya tam yolu kullanın
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p < database_setup.sql
```

### Yöntem 3: phpMyAdmin

1. phpMyAdmin'i açın
2. "SQL" sekmesine gidin
3. `database_setup.sql` dosyasının içeriğini yapıştırın
4. "Go" butonuna tıklayın

---

## 📝 Manuel Kurulum

### 1. Veritabanı Oluştur

```sql
CREATE DATABASE vize_randevu_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE vize_randevu_db;
```

### 2. Kullanıcı Oluştur

```sql
CREATE USER 'vize_user'@'localhost' IDENTIFIED BY 'VizeSecure2025!';
GRANT ALL PRIVILEGES ON vize_randevu_db.* TO 'vize_user'@'localhost';
FLUSH PRIVILEGES;
```

### 3. SQL Dosyasını Çalıştır

Yukarıdaki yöntemlerden birini kullanın.

---

## 📊 Tablo Yapısı

### 1. users (Kullanıcılar)
- id, username, email, password_hash
- full_name, is_admin, is_active
- created_at, last_login

### 2. countries (Ülkeler)
- id, name, code, flag_emoji
- is_active, created_at

### 3. user_country_quotas (Kotalar)
- id, user_id, country_id
- quota_limit, created_at, updated_at

### 4. appointments (Randevular)
- id, user_id, country_id
- applicant_name, applicant_surname, passport_number
- birth_date, phone, email, address
- preferred_date, visa_type, notes
- status, created_at, updated_at, processed_at

### 5. update_requests (Talepler)
- id, user_id, appointment_id
- request_type, request_data, reason
- status, admin_note
- created_at, processed_at, processed_by

### 6. system_logs (Loglar)
- id, user_id, action, details
- ip_address, created_at

---

## 🔍 Oluşturulan View'lar

### 1. view_user_appointment_stats
Kullanıcı başına randevu istatistikleri

### 2. view_country_appointment_stats
Ülke başına randevu istatistikleri

### 3. view_user_quota_usage
Kota kullanım durumu

---

## 🔧 Stored Procedures

### 1. sp_check_user_quota
Kullanıcı kota kontrolü

```sql
CALL sp_check_user_quota(1, 1, @has_quota, @remaining);
SELECT @has_quota, @remaining;
```

### 2. sp_get_appointment_statistics
Tarih aralığında istatistik

```sql
CALL sp_get_appointment_statistics('2025-01-01', '2025-12-31');
```

---

## ⚙️ Trigger'lar

- **trg_after_appointment_insert**: Randevu oluşturulduğunda log
- **trg_after_appointment_update**: Randevu güncellendiğinde log
- **trg_after_appointment_delete**: Randevu silindiğinde log

---

## 💾 Yedekleme ve Geri Yükleme

### Yedekleme

```bash
# Tüm veritabanı
mysqldump -u root -p vize_randevu_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Sadece yapı (veriler olmadan)
mysqldump -u root -p --no-data vize_randevu_db > structure.sql

# Sadece veriler (yapı olmadan)
mysqldump -u root -p --no-create-info vize_randevu_db > data.sql
```

### Geri Yükleme

```bash
mysql -u root -p vize_randevu_db < backup.sql
```

---

## 🔒 Güvenlik

### Şifre Değiştirme

```sql
-- Uygulama kullanıcısı şifresi
ALTER USER 'vize_user'@'localhost' IDENTIFIED BY 'YeniGüçlüŞifre123!';
FLUSH PRIVILEGES;
```

### Root Şifresi (Dikkatli Olun!)

```sql
ALTER USER 'root'@'localhost' IDENTIFIED BY 'YeniRootŞifresi';
FLUSH PRIVILEGES;
```

---

## 🧪 Test ve Doğrulama

### Tabloları Kontrol Et

```sql
SHOW TABLES;
```

### Tablo Yapısını İncele

```sql
DESCRIBE users;
DESCRIBE appointments;
```

### Kayıt Sayılarını Kontrol Et

```sql
SELECT 
    'users' AS tablo, COUNT(*) AS kayit_sayisi FROM users
UNION ALL
SELECT 'countries', COUNT(*) FROM countries
UNION ALL
SELECT 'appointments', COUNT(*) FROM appointments;
```

### İlişkileri Kontrol Et

```sql
SELECT 
    TABLE_NAME, 
    COLUMN_NAME, 
    CONSTRAINT_NAME, 
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'vize_randevu_db'
AND REFERENCED_TABLE_NAME IS NOT NULL;
```

---

## ❗ Sorun Giderme

### "Access denied for user"

```sql
-- Yetkileri kontrol et
SHOW GRANTS FOR 'vize_user'@'localhost';

-- Yeniden yetki ver
GRANT ALL PRIVILEGES ON vize_randevu_db.* TO 'vize_user'@'localhost';
FLUSH PRIVILEGES;
```

### "Table already exists"

```sql
-- Tabloyu sil ve yeniden oluştur
DROP TABLE IF EXISTS appointments;
-- SQL dosyasını tekrar çalıştır
```

### "Character set" Hatası

```sql
-- Veritabanı karakter setini kontrol et
SHOW CREATE DATABASE vize_randevu_db;

-- Değiştir
ALTER DATABASE vize_randevu_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;
```

### Tüm Veritabanını Sıfırla

```sql
-- DİKKAT: TÜM VERİLER SİLİNİR!
DROP DATABASE IF EXISTS vize_randevu_db;
-- Sonra SQL dosyasını tekrar çalıştır
```

---

## 📋 Kontrol Listesi

- [ ] MySQL servisi çalışıyor
- [ ] Root şifresi doğru
- [ ] `database_setup.sql` dosyası mevcut
- [ ] SQL dosyası başarıyla çalıştırıldı
- [ ] Tablolar oluşturuldu (6 tablo)
- [ ] View'lar oluşturuldu (3 view)
- [ ] Stored procedures oluşturuldu (2 adet)
- [ ] Trigger'lar oluşturuldu (3 adet)
- [ ] Uygulama kullanıcısı oluşturuldu
- [ ] Örnek veriler eklendi
- [ ] `.env` dosyası güncellendi

---

## 🔗 .env Dosyası Ayarları

SQL kurulumundan sonra `.env` dosyanızı güncelleyin:

```env
DB_HOST=localhost
DB_USER=vize_user
DB_PASSWORD=VizeSecure2025!
DB_NAME=vize_randevu_db
```

---

## 📞 Yardım

Sorun yaşıyorsanız:

1. MySQL servisinin çalıştığından emin olun
2. Kullanıcı adı ve şifrenin doğru olduğunu kontrol edin
3. Port numarasının doğru olduğunu kontrol edin (varsayılan: 3306)
4. Firewall ayarlarını kontrol edin

---

**Başarılar! 🎉**

Veritabanınız hazır, şimdi uygulamayı başlatabilirsiniz!

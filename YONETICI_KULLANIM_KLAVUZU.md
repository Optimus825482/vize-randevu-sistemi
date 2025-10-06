# 👔 SİSTEM YÖNETİCİSİ KULLANIM KILAVUZU
## Vize Randevu Yönetim Sistemi

**Versiyon:** 1.0.0  
**Güncelleme Tarihi:** 06.01.2025  
**Hedef Kitle:** Sistem Yöneticileri

---

## 📑 İçindekiler

1. [Sistem Genel Bakış](#1-sistem-genel-bakış)
2. [Giriş ve Güvenlik](#2-giriş-ve-güvenlik)
3. [Admin Dashboard](#3-admin-dashboard)
4. [Kullanıcı Yönetimi](#4-kullanıcı-yönetimi)
5. [Ülke Yönetimi](#5-ülke-yönetimi)
6. [Kota Yönetimi](#6-kota-yönetimi)
7. [Randevu Yönetimi](#7-randevu-yönetimi)
8. [Talep Yönetimi](#8-talep-yönetimi)
9. [Raporlama ve Analiz](#9-raporlama-ve-analiz)
10. [Sistem Bakımı](#10-sistem-bakımı)
11. [Sorun Giderme](#11-sorun-giderme)

---

## 1. Sistem Genel Bakış

### 1.1 Sistem Mimarisi

```
┌─────────────────────────────────────────┐
│         Flask Web Application           │
│  (Python 3.x, Flask, SQLAlchemy)        │
└─────────────────────────────────────────┘
                    ↕
┌─────────────────────────────────────────┐
│         MySQL Database                   │
│  (Tablolar, Views, Stored Procedures)   │
└─────────────────────────────────────────┘
```

### 1.2 Ana Bileşenler

| Bileşen | Teknoloji | Açıklama |
|---------|-----------|----------|
| **Backend** | Flask 3.0 | Web framework |
| **Database** | MySQL 8.0+ | Veri depolama |
| **ORM** | SQLAlchemy | Veritabanı yönetimi |
| **Auth** | Flask-Login | Kimlik doğrulama |
| **Forms** | WTForms | Form validasyonu |
| **Reports** | Pandas, ReportLab | Excel/PDF raporlar |

### 1.3 Kullanıcı Rolleri

| Rol | Yetki Seviyesi | Özellikler |
|-----|----------------|------------|
| **Admin** | Tam Yetki | Tüm sistem yönetimi |
| **Danışman** | Sınırlı | Sadece kendi randevuları |

---

## 2. Giriş ve Güvenlik

### 2.1 İlk Kurulum Sonrası Giriş

**Varsayılan Admin Bilgileri:**
```
Kullanıcı Adı: admin
Şifre: Admin123!
```

⚠️ **ÇOK ÖNEMLİ:** İlk girişten sonra mutlaka şifre değişti rin!

### 2.2 Güvenlik En İyi Uygulamaları

#### 2.2.1 Şifre Politikası

✅ **Yapılması Gerekenler:**
- Minimum 12 karakter
- Büyük/küçük harf, rakam, özel karakter
- 90 günde bir değiştirin
- Önceki 5 şifreyi kullanmayın

❌ **Yapılmaması Gerekenler:**
- Sözlük kelimeleri kullanmayın
- Kişisel bilgiler (isim, doğum tarihi)
- Basit şifreler (123456, password)
- Şifreyi paylaşmayın

#### 2.2.2 .env Dosyası Yapılandırması

```bash
# .env dosyası örneği
SECRET_KEY=super-secret-random-key-here-change-me
DB_HOST=localhost
DB_USER=vize_user
DB_PASSWORD=VerySecurePassword2025!
DB_NAME=vize_randevu_db

ADMIN_USERNAME=admin
ADMIN_PASSWORD=YourSecurePassword123!
ADMIN_EMAIL=admin@yourdomain.com

FLASK_ENV=production
FLASK_DEBUG=False
```

#### 2.2.3 Oturum Yönetimi

- **Timeout:** 1 saat (3600 saniye)
- **Cookie Güvenliği:** HttpOnly, SameSite=Lax
- **HTTPS Zorunluluğu:** Production'da aktif olmalı

### 2.3 İki Faktörlü Kimlik Doğrulama (2FA)

⚠️ **Şu an sistemde yok, gelecek sürümde eklenecek**

---

## 3. Admin Dashboard

### 3.1 Dashboard Bileşenleri

#### 3.1.1 Ana İstatistik Kartları

| Kart | Gösterilen Bilgi | Güncellenme |
|------|------------------|-------------|
| **Toplam Kullanıcılar** | Aktif danışman sayısı | Gerçek zamanlı |
| **Aktif Kullanıcılar** | Giriş yapabilen kullanıcılar | Gerçek zamanlı |
| **Toplam Randevular** | Sistemdeki tüm randevular | Gerçek zamanlı |
| **Bekleyen Randevular** | İnceleme bekleyen | Gerçek zamanlı |
| **İşlemdeki Randevular** | Süreç başlatılanlar | Gerçek zamanlı |
| **Tamamlanan** | Bitmiş randevular | Gerçek zamanlı |
| **Aktif Ülkeler** | Kullanılabilen ülke sayısı | Gerçek zamanlı |
| **Bekleyen Talepler** | Onay bekleyen talepler | Gerçek zamanlı |

#### 3.1.2 Grafikler ve Görseller

**Ülkelere Göre Dağılım:**
- Pasta grafik veya bar chart
- En çok kullanılan ülkeler
- Kota kullanım oranları

**En Aktif Kullanıcılar:**
- Top 5 danışman
- Randevu sayıları
- Performans metrikleri

#### 3.1.3 Son İşlemler

- Son 10 randevu
- Son kullanıcı giriş/çıkışları
- Son sistem logları

### 3.2 Hızlı Erişim Menüsü

```
├── 🏠 Dashboard
├── 👥 Kullanıcılar
│   ├── Kullanıcı Listesi
│   └── Yeni Kullanıcı Ekle
├── 🌍 Ülkeler
│   ├── Ülke Listesi
│   └── Yeni Ülke Ekle
├── 📅 Randevular
│   ├── Tüm Randevular
│   └── Filtreleme & Arama
├── 📋 Talepler
│   ├── Bekleyen Talepler
│   └── İşlenmiş Talepler
└── 📊 Raporlar
    ├── Excel Export
    └── PDF Export
```

---

## 4. Kullanıcı Yönetimi

### 4.1 Kullanıcı Listeleme

**Erişim:** Sol menü → **Kullanıcılar**

#### 4.1.1 Filtreleme Seçenekleri

| Filtre | Değerler | Açıklama |
|--------|----------|----------|
| **Rol** | Tümü, Admin, Kullanıcı | Rol bazlı filtreleme |
| **Durum** | Tümü, Aktif, Pasif | Aktiflik durumu |
| **Sıralama** | Yeniden Eskiye, Eskiden Yeniye, İsme Göre | Sıralama |
| **Arama** | Metin | Ad, soyad, email, kullanıcı adı |

#### 4.1.2 Sayfa Başına Kayıt

- 10, 25, 50, 100 kayıt seçenekleri
- Pagination (sayfalama) otomatik

### 4.2 Yeni Kullanıcı Ekleme

**Adımlar:**

1. **Kullanıcılar** → **Yeni Kullanıcı Ekle**
2. Formu doldurun:

| Alan | Zorunlu | Açıklama | Örnek |
|------|---------|----------|-------|
| **Kullanıcı Adı** | ✅ | Benzersiz olmalı | ahmet.yilmaz |
| **E-posta** | ✅ | Geçerli email | ahmet@firma.com |
| **Ad Soyad** | ✅ | Tam ad | Ahmet Yılmaz |
| **Şifre** | ✅ | Min 6 karakter | Secure123! |
| **Şifre Tekrar** | ✅ | Eşleşmeli | Secure123! |
| **Yönetici** | ⬜ | Checkbox | ☐ / ☑ |
| **Aktif** | ⬜ | Varsayılan aktif | ☑ |

3. **"Kullanıcı Oluştur"** butonuna tıklayın
4. Başarılı mesajı aldıktan sonra otomatik olarak düzenleme sayfasına yönlendirilirsiniz
5. Burada kullanıcıya kota atayabilirsiniz

### 4.3 Kullanıcı Düzenleme

#### 4.3.1 Temel Bilgi Güncelleme

1. Kullanıcı listesinden **"Düzenle"** butonuna tıklayın
2. Aşağıdaki bilgileri güncelleyin:
   - Kullanıcı adı
   - E-posta
   - Ad soyad
   - Şifre (opsiyonel)
   - Admin yetkisi
   - Aktiflik durumu

3. **"Güncelle"** butonuna tıklayın

#### 4.3.2 Şifre Değiştirme

- **Şifre** alanı boş bırakılırsa değiştirilmez
- **Yeni şifre girildiyse:**
  - Minimum 6 karakter
  - Şifre Tekrar alanı eşleşmeli

#### 4.3.3 Kullanıcı Durumunu Değiştirme

**Aktif → Pasif:**
- "Aktif" checkbox'ını kaldırın
- Kullanıcı sisteme giriş yapamaz
- Mevcut oturumu hemen sonlanmaz (çıkış yapması gerekir)

**Pasif → Aktif:**
- "Aktif" checkbox'ını işaretleyin
- Kullanıcı tekrar giriş yapabilir

### 4.4 Kullanıcı Silme

⚠️ **DİKKAT:** Bu işlem geri alınamaz!

**Silinecekler:**
- Kullanıcı kaydı
- İlişkili kotalar
- İlişkili randevular (CASCADE)
- İlişkili talepler

**Adımlar:**
1. Kullanıcı listesinden **"Sil"** butonuna tıklayın
2. Onay penceresinde **"Evet, Sil"** deyin
3. Silme işlemi loglanır

**Kısıtlamalar:**
- Kendi hesabınızı silemezsiniz
- Aktif randevusu olan kullanıcıları silmeden önce düşünün

---

## 5. Ülke Yönetimi

### 5.1 Ülke Listeleme

**Erişim:** Sol menü → **Ülkeler**

Tablo Sütunları:
- 🚩 **Bayrak & Ülke Adı**
- 🔤 **Kod** (ISO)
- 📊 **Randevu Sayısı**
- ✅ **Durum** (Aktif/Pasif)
- ⚙️ **İşlemler** (Düzenle, Sil)

### 5.2 Yeni Ülke Ekleme

**Adımlar:**

1. **Ülkeler** → **Yeni Ülke Ekle**
2. Formu doldurun:

| Alan | Zorunlu | Açıklama | Örnek |
|------|---------|----------|-------|
| **Ülke Adı** | ✅ | Tam ad | Amerika Birleşik Devletleri |
| **Ülke Kodu** | ✅ | 2-3 harf ISO kodu | USA |
| **Bayrak Emoji** | ⬜ | Unicode emoji | 🇺🇸 |
| **Aktif** | ⬜ | Varsayılan aktif | ☑ |

3. **"Ülke Ekle"** butonuna tıklayın

#### 5.2.1 Bayrak Emoji Bulma

**Kaynaklar:**
- https://emojipedia.org/flags/
- https://getemoji.com/#flags

**Kopyala-Yapıştır:**
```
🇺🇸 Amerika
🇬🇧 İngiltere
🇩🇪 Almanya
🇫🇷 Fransa
🇮🇹 İtalya
🇪🇸 İspanya
🇨🇦 Kanada
🇦🇺 Avustralya
🇯🇵 Japonya
🇹🇷 Türkiye
```

### 5.3 Ülke Düzenleme

1. Ülke listesinden **"Düzenle"** butonuna tıklayın
2. Bilgileri güncelleyin
3. **"Güncelle"** butonuna tıklayın

**Dikkat:**
- Ülke adı değişirse tüm raporlarda yeni ad görünür
- Ülke kodu değiştirilmesi önerilmez

### 5.4 Ülke Silme

**Koşullar:**
- ❌ Randevusu varsa silinemez
- ✅ Hiç kullanılmamışsa silinebilir

**Alternatif:**
- Ülkeyi silmek yerine **"Pasif"** yapın
- Böylece eski veriler korunur
- Yeni randevu oluşturulamaz

### 5.5 Dinamik Form Alanları (Gelecek Özellik)

⚠️ **Şu an aktif değil, geliştirme aşamasında**

Her ülke için özel zorunlu alanlar tanımlanabilir:
```json
{
  "birth_date": {"required": true, "enabled": true},
  "phone": {"required": true, "enabled": true},
  "email": {"required": false, "enabled": true},
  "passport_issue_date": {"required": false, "enabled": false}
}
```

---

## 6. Kota Yönetimi

### 6.1 Kota Sistemi Mantığı

**Kota Nedir?**
- Bir danışmanın belirli bir ülke için oluşturabileceği maksimum randevu sayısı

**Örnek:**
```
Ahmet Yılmaz → ABD → 50 randevu hakkı
Ahmet Yılmaz → İngiltere → 30 randevu hakkı
Mehmet Kaya → ABD → 100 randevu hakkı
```

### 6.2 Kota Atama

**İki yöntem:**

#### Yöntem 1: Kullanıcı Düzenleme Sayfasından

1. **Kullanıcılar** → Kullanıcı seçin → **Düzenle**
2. Sayfanın alt bölümünde "Kota Yönetimi" kartı
3. **"Yeni Kota Ekle"** butonuna tıklayın
4. Modal pencerede:
   - Ülke seçin
   - Kota limiti girin (pozitif sayı)
5. **"Kota Ekle"** butonuna tıklayın

#### Yöntem 2: Toplu Kota Atama (Script ile)

```python
# Örnek Python scripti
from app import app, db
from models import User, Country, UserCountryQuota

with app.app_context():
    user = User.query.filter_by(username='ahmet.yilmaz').first()
    country = Country.query.filter_by(code='USA').first()
    
    quota = UserCountryQuota(
        user_id=user.id,
        country_id=country.id,
        quota_limit=50
    )
    db.session.add(quota)
    db.session.commit()
```

### 6.3 Kota Güncelleme

1. Kullanıcı düzenleme sayfasında mevcut kotalar listelenir
2. Kota satırındaki **"Düzenle"** ikonuna tıklayın
3. Yeni limit girin
4. **"Güncelle"** butonuna tıklayın

**Otomatik Güncelleme:**
- Aynı kullanıcı-ülke kombinasyonu için tekrar kota eklerseniz, mevcut kota güncellenir

### 6.4 Kota Silme

1. Kota satırındaki **"Sil"** ikonuna tıklayın
2. Onay verin
3. Kota silinir

**Dikkat:**
- Kota silinirse kullanıcı o ülke için randevu oluşturamaz
- Mevcut randevular silinmez

### 6.5 Kota Kullanım Takibi

**Dashboard'da:**
- Her kullanıcı için kota kullanım yüzdesi
- Kritik eşik: %90 üzeri kırmızı işaretlenir

**Kullanıcı Sayfasında:**
- İlerleme çubuğu
- Kullanılan / Toplam gösterimi

### 6.6 Kota Aşım Kontrolü

**Sistem Otomatik Kontrol Eder:**
```python
if remaining_quota <= 0:
    flash('Bu ülke için kota limitine ulaştınız', 'danger')
    return redirect(...)
```

**Race Condition Riski:**
- ⚠️ Aynı anda birden fazla randevu oluşturulursa kota aşımı olabilir
- Gelecek sürümde database-level constraint eklenecek

---

## 7. Randevu Yönetimi

### 7.1 Randevu Listesi

**Erişim:** Sol menü → **Randevular**

#### 7.1.1 Gelişmiş Filtreleme

| Filtre | Seçenekler | Açıklama |
|--------|------------|----------|
| **Durum** | Tümü, Bekleme, Süreç Başlatıldı, Tamamlandı, İptal | Durum filtreleme |
| **Ülke** | Dropdown | Ülkeye göre |
| **Kullanıcı** | Dropdown | Danışmana göre |
| **Tarih Aralığı** | Başlangıç - Bitiş | Oluşturma tarihi |
| **Sıralama** | Yeni→Eski, Eski→Yeni, Güncelleme, Tercih Tarihi | Sıralama |
| **Arama** | Metin | Ad, soyad, pasaport no |

#### 7.1.2 Toplu İşlemler

**Şu an mevcut değil, gelecek sürümde:**
- Toplu durum değiştirme
- Toplu silme
- Toplu export

### 7.2 Randevu Detayları

#### 7.2.1 Detay Modalı

Randevu satırındaki **"Detaylar"** butonuna tıklayınca:

**Gösterilen Bilgiler:**
```
Randevu Bilgileri
├── ID: #12345
├── Durum: Bekleme
├── Oluşturma Tarihi: 05.01.2025 14:30
└── Son Güncelleme: 05.01.2025 14:30

Başvuran Bilgileri
├── Ad Soyad: Ahmet Yılmaz
├── Pasaport No: U12345678
├── Doğum Tarihi: 15.05.1990
├── Telefon: +90 555 123 4567
├── E-posta: ahmet@email.com
├── Uyruk: Türkiye Cumhuriyeti
└── Adres: Atatürk Cad. No:123...

Randevu Detayları
├── Ülke: 🇺🇸 Amerika Birleşik Devletleri
├── Tercih Edilen Tarih: 10.02.2025 - 15.02.2025
├── Seyahat Tarihi: 20.07.2025
├── Vize Türü: Turistik
└── Notlar: Acil işlem gerekli

Danışman Bilgileri
├── Kullanıcı: ahmet.danismanım: Ahmet Yılmaz (Danışman)
└── E-posta: ahmet.danisman@firma.com
```

### 7.3 Randevu Durumu Değiştirme

#### 7.3.1 Durum Akışı

```
Bekleme (Yeni oluşturuldu)
    ↓
Süreç Başlatıldı (Yönetici onayladı)
    ↓
    ├→ Tamamlandı (Başarıyla bitti)
    └→ İptal (Herhangi bir nedenle iptal)
```

#### 7.3.2 Durum Güncelleme

1. Randevu satırındaki **"Durum Değiştir"** butonuna tıklayın
2. Modal açılır:
   - Yeni durum seçin
   - Yönetici notu ekleyin (opsiyonel)
3. **"Durumu Güncelle"** butonuna tıklayın

**Otomatik İşlemler:**
- `processed_at` alanı otomatik güncellenir
- Durum değişikliği loglanır
- Trigger otomatik çalışır

#### 7.3.3 Durum Değiştirme Kuralları

| Mevcut Durum | İzin Verilen Yeni Durumlar |
|--------------|----------------------------|
| Bekleme | Süreç Başlatıldı, İptal |
| Süreç Başlatıldı | Tamamlandı, İptal |
| Tamamlandı | - (değiştirilemez) |
| İptal | - (değiştirilemez) |

### 7.4 Randevu Düzenleme (Admin)

**Tam yetki ile düzenleme:**

1. Randevu satırındaki **"Düzenle"** butonuna tıklayın
2. Modal açılır, tüm alanlar düzenlenebilir
3. Değişiklikleri yapın
4. **"Kaydet"** butonuna tıklayın

**Admin'ler için:**
- ✅ Her durumda düzenleyebilir
- ✅ Durum kontrolü yok
- ✅ Kota kontrolü yok

### 7.5 Randevu Silme

**Dikkat:** Sadece "Bekleme" durumundaki randevular silinebilir!

**Diğer durumlar için:**
- "İptal" durumuna alın
- Böylece veri korunur
- Raporlarda görünür

**Silme Adımları:**
1. Randevu satırındaki **"Sil"** butonuna tıklayın
2. Onay verin
3. CASCADE DELETE: İlişkili talepler de silinir

---

## 8. Talep Yönetimi

### 8.1 Talep Türleri

| Tür | Açıklama | İşlem |
|-----|----------|-------|
| **Güncelleme Talebi** | Danışman randevu bilgilerini değiştirmek istiyor | Onayla veya reddet |
| **Silme Talebi** | Danışman randevuyu silmek istiyor | Onayla (siler) veya reddet |

### 8.2 Talep Listesi

**Erişim:** Sol menü → **Talepler**

#### 8.2.1 Filtreleme

| Filtre | Değerler |
|--------|----------|
| **Durum** | Tümü, Bekliyor, Onaylandı, Reddedildi |
| **Tür** | Tümü, Güncelleme, Silme |

#### 8.2.2 İstatistikler

Dashboard'da:
- **Bekleyen Talepler** (Kırmızı badge)
- Toplam onaylanan
- Toplam reddedilen

### 8.3 Talep İnceleme

1. Talep satırındaki **"Detaylar"** butonuna tıklayın
2. Modal açılır:
   - Talep türü
   - Talep nedeni
   - İlgili randevu bilgileri
   - Danışman bilgileri
   - Oluşturma tarihi

### 8.4 Talep Onaylama

**Güncelleme Talebi:**
1. **"Onayla"** butonuna tıklayın
2. Yönetici notu ekleyin (opsiyonel)
3. **"Onayla"** butonuna tıklayın
4. Talep durumu "Onaylandı" olur
5. ⚠️ **Şu an otomatik güncelleme yapılmıyor** (gelecek sürümde)

**Silme Talebi:**
1. **"Onayla"** butonuna tıklayın
2. Yönetici notu ekleyin (opsiyonel)
3. **"Onayla"** butonuna tıklayın
4. Randevu otomatik silinir
5. Talep durumu "Onaylandı" olur

### 8.5 Talep Reddetme

1. **"Reddet"** butonuna tıklayın
2. **Red nedeni girin** (zorunlu)
3. **"Reddet"** butonuna tıklayın
4. Talep durumu "Reddedildi" olur
5. Danışman red nedenini görebilir

### 8.6 Talep Geçmişi

- Tüm talepler kayıt altında
- `processed_at` alanı işlem tarihini gösterir
- `processed_by` admin kullanıcı ID'si

---

## 9. Raporlama ve Analiz

### 9.1 Excel Raporu

**Özellikler:**
- Tüm randevu bilgileri
- Filtrelenmiş sonuçlar
- Otomatik sütun genişliği
- Türkçe başlıklar

**Adımlar:**
1. Randevular sayfasında filtre uygulayın
2. **"Excel'e Aktar"** butonuna tıklayın
3. Dosya otomatik indirilir: `randevu_raporu_YYYY-MM-DD.xlsx`

**İçerik:**
```
ID | Kullanıcı | Ad Soyad | Ülke | Başvuran | Pasaport | 
Durum | Vize Türü | Oluşturma | Güncelleme
```

### 9.2 PDF Raporu

**Özellikler:**
- Tablo formatı
- Başlık ve tarih
- Profesyonel görünüm
- A4 landscape (yatay)

**Adımlar:**
1. Randevular sayfasında filtre uygulayın
2. **"PDF'e Aktar"** butonuna tıklayın
3. Dosya otomatik indirilir: `randevu_raporu_YYYY-MM-DD.pdf`

### 9.3 Analitik Raporlar

**Şu an sadece Dashboard'da:**
- Ülkelere göre dağılım
- En aktif kullanıcılar (Top 5)
- Durum bazlı sayılar

**Gelecek Sürümde:**
- Zaman bazlı trend grafikleri
- Performans metrikleri
- Kota kullanım analizi
- Özel tarih aralığı raporları

### 9.4 Database Views

**Hazır SQL Views:**

```sql
-- Kullanıcı istatistikleri
SELECT * FROM view_user_appointment_stats;

-- Ülke istatistikleri
SELECT * FROM view_country_appointment_stats;

-- Kota kullanım durumu
SELECT * FROM view_user_quota_usage;
```

**Kullanım:**
- phpMyAdmin'den görüntülenebilir
- Custom raporlar için kullanılabilir
- BI araçlarında kullanılabilir

---

## 10. Sistem Bakımı

### 10.1 Veritabanı Yedekleme

#### 10.1.1 Manuel Yedekleme (mysqldump)

**Windows PowerShell:**
```powershell
mysqldump -u root -p vize_randevu_db > backup_$(Get-Date -Format 'yyyy-MM-dd_HHmmss').sql
```

**Linux/Mac:**
```bash
mysqldump -u root -p vize_randevu_db > backup_$(date +%Y-%m-%d_%H%M%S).sql
```

#### 10.1.2 Otomatik Yedekleme Script'i

**backup.ps1** (Windows):
```powershell
$date = Get-Date -Format "yyyy-MM-dd_HHmmss"
$backupDir = "D:\Backups"
$filename = "vize_db_$date.sql"

mysqldump -u root -pYourPassword vize_randevu_db > "$backupDir\$filename"

# 30 günden eski yedekleri sil
Get-ChildItem $backupDir -Filter *.sql | Where-Object {
    $_.LastWriteTime -lt (Get-Date).AddDays(-30)
} | Remove-Item
```

**Zamanlanmış Görev (Windows Task Scheduler):**
1. Task Scheduler'ı açın
2. "Create Task" tıklayın
3. Trigger: Her gün 02:00
4. Action: PowerShell script çalıştır

#### 10.1.3 Yedek Geri Yükleme

```powershell
mysql -u root -p vize_randevu_db < backup_2025-01-06_020000.sql
```

### 10.2 Log Yönetimi

#### 10.2.1 Sistem Logları

**system_logs tablosu:**
- Her işlem kaydedilir
- IP adresi saklanır
- Kullanıcı izlenir

**Sorgu Örnekleri:**
```sql
-- Son 100 log kaydı
SELECT * FROM system_logs ORDER BY created_at DESC LIMIT 100;

-- Belirli kullanıcının işlemleri
SELECT * FROM system_logs WHERE user_id = 5;

-- Belirli tarih aralığı
SELECT * FROM system_logs 
WHERE created_at BETWEEN '2025-01-01' AND '2025-01-31';
```

#### 10.2.2 Log Temizleme

**90 günden eski logları sil:**
```sql
DELETE FROM system_logs 
WHERE created_at < DATE_SUB(NOW(), INTERVAL 90 DAY);
```

**Cronjob (Linux) - Her ayın ilk günü:**
```bash
0 0 1 * * mysql -u root -pPassword -e "DELETE FROM vize_randevu_db.system_logs WHERE created_at < DATE_SUB(NOW(), INTERVAL 90 DAY);"
```

### 10.3 Performans Optimizasyonu

#### 10.3.1 Index Kontrol

```sql
SHOW INDEX FROM appointments;
SHOW INDEX FROM users;
```

#### 10.3.2 Yavaş Sorgu Analizi

```sql
-- MySQL Slow Query Log'u aktif et
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2; -- 2 saniyeden uzun sorgular

-- Log dosyası: /var/log/mysql/mysql-slow.log
```

#### 10.3.3 Tablo Optimizasyonu

```sql
OPTIMIZE TABLE appointments;
OPTIMIZE TABLE users;
OPTIMIZE TABLE system_logs;
```

### 10.4 Güvenlik Güncellemeleri

#### 10.4.1 Python Paketleri

**Güncelleme kontrolü:**
```bash
pip list --outdated
```

**Güvenli güncelleme:**
```bash
pip install --upgrade Flask
pip install --upgrade SQLAlchemy
```

**requirements.txt güncelleme:**
```bash
pip freeze > requirements.txt
```

#### 10.4.2 MySQL Güncelleme

**Windows:**
- MySQL Installer kullan
- Yedek aldıktan sonra güncelle

**Linux:**
```bash
sudo apt update
sudo apt upgrade mysql-server
```

---

## 11. Sorun Giderme

### 11.1 Uygulama Başlamıyor

**Hata:** "Address already in use"
```
Çözüm:
1. Portı değiştir: app.run(port=5001)
2. Veya çalışan uygulamayı kapat
```

**Hata:** "Can't connect to MySQL server"
```
Çözüm:
1. MySQL servisinin çalıştığından emin ol
2. .env dosyasındaki bilgileri kontrol et
3. Firewall ayarlarını kontrol et
```

### 11.2 Veritabanı Hataları

**Hata:** "Table doesn't exist"
```
Çözüm:
1. database_setup.sql dosyasını çalıştır
2. Veya: python
   >>> from app import app, db
   >>> with app.app_context():
   ...     db.create_all()
```

**Hata:** "Duplicate entry"
```
Çözüm:
- Benzersiz alanları kontrol et (username, email, ülke kodu)
```

### 11.3 Performans Sorunları

**Sorun:** Sayfa yavaş yükleniyor

**Çözümler:**
1. Index eksikliği kontrolü
2. N+1 query problemi (lazy loading)
3. Pagination kullanımı
4. Cache mekanizması (Redis)

### 11.4 Kullanıcı Şifresi Sıfırlama

**Manuel sıfırlama (Database):**
```python
from app import app, db
from models import User

with app.app_context():
    user = User.query.filter_by(username='ahmet.yilmaz').first()
    user.set_password('YeniSifre123!')
    db.session.commit()
    print(f"Şifre sıfırlandı: {user.username}")
```

### 11.5 Sistem Loglarını İnceleme

**Python Flask Log:**
```bash
# Terminal çıktısını dosyaya yönlendir
python app.py > app.log 2>&1
```

**Hata Takibi:**
```python
# app.py içinde
import logging
logging.basicConfig(
    filename='error.log',
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s: %(message)s'
)
```

---

## 📞 Destek ve Kaynaklar

### Teknik Dokümantasyon

- **Flask:** https://flask.palletsprojects.com/
- **SQLAlchemy:** https://docs.sqlalchemy.org/
- **MySQL:** https://dev.mysql.com/doc/

### İletişim

- **Sistem Yöneticisi E-posta:** admin@vizesistemi.com
- **Teknik Destek:** support@vizesistemi.com
- **Acil Durum:** +90 XXX XXX XX XX

---

## ⚠️ Önemli Hatırlatmalar

1. ✅ **Her zaman yedek alın**
2. ✅ **Şifreleri güvenli tutun**
3. ✅ **Logları düzenli kontrol edin**
4. ✅ **Güncellemeleri takip edin**
5. ✅ **Test ortamında önce deneyin**
6. ✅ **Kullanıcılara eğitim verin**
7. ✅ **KVKK/GDPR uyumluluğu sağlayın**
8. ✅ **Performansı izleyin**

---

## 📝 Değişiklik Geçmişi

| Versiyon | Tarih | Değişiklikler |
|----------|-------|---------------|
| 1.0.0 | 06.01.2025 | İlk versiyon yayınlandı |

---

**© 2025 Vize Randevu Yönetim Sistemi**  
**Tüm hakları saklıdır.**

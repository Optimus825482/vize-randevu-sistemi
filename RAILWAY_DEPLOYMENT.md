# 🚂 Railway Deployment Rehberi

Bu rehber, Vize Randevu Sistemi'ni Railway'e deploy etmek için gereken adımları içerir.

## 📋 Gereksinimler

- GitHub hesabı
- Railway hesabı (https://railway.app/)
- MySQL veritabanı eklentisi

## 🚀 Deployment Adımları

### 1. GitHub Repository Hazırlığı

Projeyi GitHub'a yüklemeden önce:

```bash
# Git repository'sini başlat (eğer yoksa)
git init

# Tüm dosyaları ekle
git add .

# İlk commit
git commit -m "Initial commit - Vize Randevu Sistemi"

# GitHub'da yeni bir repository oluşturun ve uzak bağlantıyı ekleyin
git remote add origin https://github.com/KULLANICI_ADINIZ/REPO_ADINIZ.git

# Push yapın
git push -u origin main
```

### 2. Railway Projesi Oluşturma

1. Railway.app'e giriş yapın
2. "New Project" butonuna tıklayın
3. "Deploy from GitHub repo" seçeneğini seçin
4. Repository'nizi seçin

### 3. MySQL Veritabanı Ekleme

1. Railway Dashboard'da "New" -> "Database" -> "Add MySQL"
2. MySQL eklentisi otomatik olarak oluşturulacak
3. Railway otomatik olarak `DATABASE_URL` environment variable'ını oluşturacak

### 4. Environment Variables (Ortam Değişkenleri)

Railway Dashboard'da "Variables" sekmesine gidin ve şu değişkenleri ekleyin:

```bash
# Güvenlik
SECRET_KEY=uzun-rastgele-bir-key-buraya-yazin

# Admin Bilgileri
ADMIN_USERNAME=admin
ADMIN_PASSWORD=GüçlüŞifre123!
ADMIN_EMAIL=admin@yourcompany.com

# Railway otomatik olarak şunları sağlar:
# DATABASE_URL (MySQL bağlantı URL'i)
# PORT (Uygulama portu)
```

**ÖNEMLİ:** `SECRET_KEY` için güçlü, rastgele bir değer kullanın:
```python
# Python ile SECRET_KEY oluşturmak için:
import secrets
print(secrets.token_hex(32))
```

### 5. Veritabanı Kurulumu

Railway'de deployment sonrası veritabanı otomatik olarak kurulacaktır. Ancak manuel olarak kurmak isterseniz:

```bash
# Railway CLI yükleyin
npm i -g @railway/cli

# Giriş yapın
railway login

# Projeyi bağlayın
railway link

# Veritabanı kurulum scriptini çalıştırın
railway run python init_railway_db.py
```

### 6. Deployment

Railway otomatik olarak:
1. `requirements.txt` dosyasından bağımlılıkları yükleyecek
2. `Procfile` veya `nixpacks.toml` kullanarak uygulamayı başlatacak
3. Otomatik SSL sertifikası ekleyecek
4. Bir public URL verecek

## 🔍 Deployment Kontrolü

Deployment tamamlandıktan sonra:

1. Railway'in verdiği URL'i açın (örn: `https://your-app.up.railway.app`)
2. Admin kullanıcısıyla giriş yapın
3. Sistem loglarını kontrol edin: Railway Dashboard -> "Logs"

## 📊 Veritabanı Migration

Eğer veritabanı şemasında değişiklik yaparsanız:

```bash
# Railway CLI ile bağlanın
railway run python

# Python shell'de:
from app import app, db
with app.app_context():
    db.create_all()
```

## 🔧 Sorun Giderme

### Problem: "Internal Server Error"

**Çözüm:**
1. Railway logs'ları kontrol edin
2. Environment variables'ların doğru olduğundan emin olun
3. MySQL veritabanının aktif olduğunu kontrol edin

### Problem: "Database connection failed"

**Çözüm:**
1. MySQL eklentisinin çalıştığından emin olun
2. `DATABASE_URL` variable'ının otomatik olarak ayarlandığını kontrol edin
3. Railway Dashboard'da MySQL service'inin "Active" olduğunu doğrulayın

### Problem: "Static files not loading"

**Çözüm:**
Railway otomatik olarak static dosyaları serve eder, ancak sorun yaşarsanız:
1. `static/` klasörünün commit edildiğinden emin olun
2. `.gitignore` dosyasında static klasörünün exclude edilmediğini kontrol edin

## 🔐 Güvenlik Tavsiyeleri

1. **SECRET_KEY**: Asla default değer kullanmayın, güçlü bir key oluşturun
2. **ADMIN_PASSWORD**: Güçlü bir şifre kullanın (min 12 karakter, özel karakterler)
3. **Environment Variables**: Hassas bilgileri asla kod içinde tutmayın
4. **HTTPS**: Railway otomatik SSL sağlar, kullanın
5. **Database Backup**: Railway Dashboard'dan düzenli backup alın

## 📝 Railway Özel Komutlar

```bash
# Logs izleme
railway logs

# Environment variables listeleme
railway variables

# Yeni deployment tetikleme
railway up

# SSH bağlantısı
railway shell

# Veritabanına bağlanma
railway connect
```

## 🌐 Custom Domain Ekleme

Railway Dashboard'da:
1. "Settings" -> "Domains"
2. "Custom Domain" butonuna tıklayın
3. Domain'inizi girin (örn: `app.yourcompany.com`)
4. DNS kayıtlarını güncelleyin (Railway size CNAME kaydını gösterecek)

## 📈 Monitoring ve Scaling

Railway otomatik olarak:
- CPU ve Memory kullanımını izler
- Uygulama loglarını tutar
- Metrics sağlar (Dashboard -> Metrics)

Scaling için:
- Railway Pro plan'e geçin
- Otomatik scaling aktif hale gelir

## 🔄 Güncelleme ve Yeniden Deployment

Kod değişikliklerinden sonra:

```bash
git add .
git commit -m "Update: açıklama"
git push origin main
```

Railway otomatik olarak yeni deployment başlatacak.

## 📞 Destek

- Railway Docs: https://docs.railway.app/
- Railway Discord: https://discord.gg/railway
- GitHub Issues: Repository'nizin issues bölümü

## ✅ Deployment Checklist

- [ ] GitHub repository oluşturuldu
- [ ] Railway projesi oluşturuldu
- [ ] MySQL veritabanı eklendi
- [ ] Environment variables ayarlandı
- [ ] SECRET_KEY güçlü bir değere ayarlandı
- [ ] ADMIN_PASSWORD güvenli bir şifre
- [ ] İlk deployment başarılı
- [ ] Veritabanı tabloları oluştu
- [ ] Admin girişi test edildi
- [ ] SSL sertifikası aktif
- [ ] Custom domain (opsiyonel) yapılandırıldı
- [ ] Backup stratejisi belirlendi

---

**Not:** Railway ücretsiz planda sınırlamalar vardır. Production kullanımı için Pro plan önerilir.

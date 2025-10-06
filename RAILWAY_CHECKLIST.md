# 🚂 Railway Deployment Checklist

Bu checklist'i Railway'e deploy etmeden önce kontrol edin.

## 📋 Pre-Deployment Checklist

### 1. Kod Hazırlığı
- [ ] Tüm değişiklikler commit edildi
- [ ] `requirements.txt` güncel
- [ ] `.gitignore` dosyası doğru yapılandırılmış
- [ ] `.env` dosyası `.gitignore`'da (hassas bilgiler Git'e yüklenmeyecek)
- [ ] Statik dosyalar (`static/`) commit edildi
- [ ] Template dosyaları (`templates/`) commit edildi

### 2. Dosya Kontrolü
- [ ] `config.py` - DATABASE_URL desteği var
- [ ] `railway.json` - Deployment ayarları doğru
- [ ] `nixpacks.toml` - Build ayarları doğru
- [ ] `Procfile` - Start komutu doğru
- [ ] `start.sh` - Başlangıç scripti var
- [ ] `runtime.txt` - Python versiyonu belirtilmiş
- [ ] `init_railway_db.py` - DB kurulum scripti var
- [ ] `.dockerignore` - Gereksiz dosyalar exclude edilmiş

### 3. GitHub Repository
- [ ] Repository oluşturuldu
- [ ] Kod GitHub'a push edildi
- [ ] Repository public veya Railway'e erişim verildi
- [ ] `.git` klasörü mevcut

```powershell
# Son kontrol
git status
git log --oneline -5
git push origin main
```

---

## 🚀 Railway Deployment Checklist

### 1. Railway Hesabı ve Proje
- [ ] Railway hesabı oluşturuldu (https://railway.app)
- [ ] GitHub ile bağlantı kuruldu
- [ ] Yeni proje oluşturuldu ("New Project")
- [ ] GitHub repository seçildi

### 2. MySQL Database Ekleme
- [ ] "New" → "Database" → "Add MySQL" tıklandı
- [ ] MySQL servisi başarıyla oluşturuldu
- [ ] `DATABASE_URL` environment variable otomatik oluşturuldu (Variables sekmesinden kontrol edin)

### 3. Environment Variables Ayarlama

Railway Dashboard → Variables sekmesine gidin ve şunları ekleyin:

- [ ] `SECRET_KEY` - Güçlü, rastgele bir key
- [ ] `ADMIN_USERNAME` - Admin kullanıcı adı (örn: admin)
- [ ] `ADMIN_PASSWORD` - Güçlü bir şifre (min 12 karakter)
- [ ] `ADMIN_EMAIL` - Admin email adresi

**SECRET_KEY oluşturma:**
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

**⚠️ EKLEMEYIN (Railway otomatik sağlar):**
- ❌ `DATABASE_URL` - MySQL servisi tarafından otomatik oluşturulur
- ❌ `PORT` - Railway tarafından otomatik atanır

### 4. İlk Deployment
- [ ] Variables kaydedildi
- [ ] Otomatik deployment başladı
- [ ] Deployments sekmesinden ilerleme takip edildi
- [ ] "Building..." → "Deploying..." → "Success" mesajları görüldü

**Beklenen süre:** 3-5 dakika

---

## ✅ Post-Deployment Checklist

### 1. Domain ve Erişim
- [ ] Settings → Domains → "Generate Domain" yapıldı
- [ ] Railway URL'i alındı (örn: `https://your-app.up.railway.app`)
- [ ] URL tarayıcıda açıldı

### 2. Uygulama Kontrolü
- [ ] Login sayfası başarıyla yüklendi
- [ ] Admin kullanıcısıyla giriş yapıldı
- [ ] Dashboard açıldı
- [ ] Menüler çalışıyor
- [ ] Statik dosyalar yüklendi (logo, CSS, JS)

### 3. Veritabanı Kontrolü
- [ ] Admin panelinde "Kullanıcılar" sayfası açıldı
- [ ] Admin kullanıcısı listede görünüyor
- [ ] "Ülkeler" sayfası açıldı
- [ ] Örnek ülkeler görünüyor (10 ülke)

### 4. Log Kontrolü

Railway Dashboard → Deployments → View Logs

**Başarılı deployment logları:**
```
✅ Tablolar başarıyla oluşturuldu!
✅ Admin kullanıcısı oluşturuldu!
✅ Örnek ülkeler eklendi!
🎉 Railway veritabanı kurulumu başarıyla tamamlandı!
👤 Admin Kullanıcı Adı: admin
📊 Toplam Ülke: 10
🌐 Uygulama başlatılıyor...
```

### 5. Fonksiyon Testleri
- [ ] Yeni kullanıcı oluşturma testi
- [ ] Ülke ekleme/düzenleme testi
- [ ] Kota atama testi
- [ ] Kullanıcı girişi testi (admin dışında)
- [ ] Randevu oluşturma testi
- [ ] Logout/Login testi

---

## 🔧 Sorun Giderme Checklist

### "Internal Server Error" Alıyorsanız

- [ ] Railway Logs kontrol edildi
- [ ] Environment variables tamamı ayarlı mı?
  - [ ] SECRET_KEY var mı?
  - [ ] ADMIN_USERNAME var mı?
  - [ ] ADMIN_PASSWORD var mı?
  - [ ] ADMIN_EMAIL var mı?
- [ ] MySQL servisi çalışıyor mu? (Dashboard'da yeşil nokta)
- [ ] DATABASE_URL otomatik oluşturuldu mu?

### "Database Connection Failed" Alıyorsanız

- [ ] MySQL servisi aktif mi?
- [ ] Variables sekmesinde DATABASE_URL var mı?
- [ ] DATABASE_URL formatı doğru mu? (mysql:// ile başlamalı)
- [ ] MySQL servisi ile web servisi aynı Railway projesinde mi?

### "Application Failed to Start" Alıyorsanız

- [ ] Logs'da tam hata mesajı okundu
- [ ] `requirements.txt` tüm paketleri içeriyor mu?
- [ ] `start.sh` dosyası commit edildi mi?
- [ ] `nixpacks.toml` doğru mu?
- [ ] Python versiyonu uyumlu mu? (runtime.txt)

### Static Dosyalar Yüklenmiyor

- [ ] `static/` klasörü GitHub'a commit edildi mi?
- [ ] `.gitignore` dosyasında `static/` exclude edilmedi mi?
- [ ] Browser cache temizlendi mi?
- [ ] URL'de /static/... path'i doğru mu?

---

## 🔐 Güvenlik Checklist

### Deployment Sonrası Güvenlik
- [ ] Admin şifresi güçlü (min 12 karakter, özel karakterler)
- [ ] SECRET_KEY rastgele ve güçlü
- [ ] `.env` dosyası Git'e commit edilmedi
- [ ] Production'da DEBUG mode kapalı
- [ ] HTTPS aktif (Railway otomatik sağlar)

### Düzenli Bakım
- [ ] Admin şifresi periyodik olarak değiştirilecek
- [ ] Database backup'ları alınacak (Railway Dashboard → Database → Backups)
- [ ] Logs düzenli kontrol edilecek
- [ ] Railway maliyeti takip edilecek

---

## 📊 Monitoring Checklist

### İzlenecek Metrikler
- [ ] CPU kullanımı (Railway Dashboard → Metrics)
- [ ] Memory kullanımı
- [ ] Request sayısı
- [ ] Response time
- [ ] Error rate

### Log İzleme
- [ ] Error logları (günlük kontrol)
- [ ] Access logları (şüpheli aktivite)
- [ ] Database bağlantı hataları
- [ ] Authentication hataları

---

## 🎯 Production Readiness Checklist

### Önerilen Ek Ayarlar
- [ ] Custom domain eklendi (opsiyonel)
- [ ] SSL sertifikası aktif (Railway otomatik)
- [ ] Backup stratejisi belirlendi
- [ ] Monitoring ve alerting kuruldu (opsiyonel)
- [ ] Kullanıcı dokümantasyonu hazırlandı
- [ ] Destek/İletişim kanalları belirlendi

### Team Hazırlığı
- [ ] Admin bilgileri güvenli bir yerde saklandı
- [ ] Deployment süreci dokümante edildi
- [ ] Yedekleme prosedürü belirlendi
- [ ] Acil durum planı hazırlandı

---

## 🆘 Acil Durum İletişimi

**Railway Destek:**
- Dökümantasyon: https://docs.railway.app/
- Discord: https://discord.gg/railway
- Twitter: @Railway

**Proje Destek:**
- GitHub Issues: Repository'nizin Issues bölümü
- Email: Projenize ait destek email adresi

---

## ✨ Deployment Başarılı!

Tüm checklistler tamamlandıysa, tebrikler! 🎉

**Sistem artık production'da:**
- ✅ HTTPS ile güvenli erişim
- ✅ MySQL database aktif
- ✅ Otomatik backup
- ✅ 7/24 uptime
- ✅ Auto-scaling (Railway Pro)

**Sonraki Adımlar:**
1. Kullanıcıları sisteme ekleyin
2. Ülkeleri yapılandırın
3. Kotaları atayın
4. Kullanıcı eğitimi verin
5. Sistemi monitör edin

**İyi kullanımlar! 🚀**

---

## 📝 Notlar

Deployment tarihi: ________________

Railway Project URL: ________________

Production URL: ________________

Admin Credentials: (Güvenli yerde saklayın!)

Database: MySQL (Railway)

Backup Schedule: ________________

Notes:
________________
________________
________________

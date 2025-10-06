# 🚂 Railway Deployment - Hızlı Başlangıç

## 📋 Ön Hazırlık

Railway'e deploy etmeden önce bu adımları tamamlayın:

### 1. ✅ Checklist

- [ ] GitHub hesabı var
- [ ] Railway hesabı oluşturuldu (https://railway.app/)
- [ ] Proje GitHub'a yüklendi
- [ ] `.env` dosyası `.gitignore`'da var (hassas bilgilerin yüklenmemesi için)

---

## 🚀 Railway'e Deploy (Adım Adım)

### ADIM 1: GitHub Repository Hazırlığı

Eğer henüz yapmadıysanız:

```powershell
# Tüm dosyaları commit edin
git add .
git commit -m "Railway deployment hazırlığı"
git push origin main
```

### ADIM 2: Railway Projesi Oluşturma

1. **Railway.app'e giriş yapın**: https://railway.app/
2. **New Project** butonuna tıklayın
3. **Deploy from GitHub repo** seçin
4. Repository'nizi seçin ve onaylayın

### ADIM 3: MySQL Database Ekleme

1. Railway Dashboard'da **New** → **Database** → **Add MySQL**
2. MySQL servisi otomatik oluşturulacak
3. Railway otomatik olarak `DATABASE_URL` environment variable oluşturacak

### ADIM 4: Environment Variables (ÖNEMLİ!)

Railway Dashboard'da projenize gidin → **Variables** sekmesine tıklayın

Aşağıdaki değişkenleri ekleyin:

```bash
SECRET_KEY=BURAYA-UZUN-RASTGELE-BIR-KEY-YAZIN
ADMIN_USERNAME=admin
ADMIN_PASSWORD=GucluSifre123!@#
ADMIN_EMAIL=admin@yourcompany.com
```

**SECRET_KEY oluşturmak için:**

Python ile:
```python
import secrets
print(secrets.token_hex(32))
```

veya PowerShell ile:
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

**⚠️ ÖNEMLİ NOTLAR:**
- `DATABASE_URL` ve `PORT` Railway tarafından otomatik sağlanır, EKLEMEYIN!
- `SECRET_KEY` mutlaka güçlü ve rastgele olmalı
- `ADMIN_PASSWORD` güçlü bir şifre seçin (min 12 karakter)

### ADIM 5: İlk Deployment

Variables ayarlandıktan sonra:

1. Railway otomatik olarak deploy başlatacak
2. **Deployments** sekmesinden ilerlemeyi takip edin
3. Logları **View Logs** ile kontrol edin

**Deploy süresi:** Yaklaşık 3-5 dakika

### ADIM 6: Domain ve Erişim

Deploy tamamlandıktan sonra:

1. **Settings** → **Domains** sekmesine gidin
2. **Generate Domain** butonuna tıklayın
3. Railway size bir URL verecek: `https://your-app.up.railway.app`

---

## ✅ Kurulum Kontrolü

Deploy tamamlandıktan sonra:

### 1. Siteyi Açın
Railway'in verdiği URL'i tarayıcıda açın

### 2. Admin Girişi Yapın
- **Kullanıcı Adı:** Environment variables'da belirlediğiniz `ADMIN_USERNAME`
- **Şifre:** Environment variables'da belirlediğiniz `ADMIN_PASSWORD`

### 3. Logları Kontrol Edin
Railway Dashboard → **Deployments** → **View Logs**

**Başarılı deployment mesajları:**
```
✅ Tablolar başarıyla oluşturuldu!
✅ Admin kullanıcısı oluşturuldu!
✅ Örnek ülkeler eklendi!
🎉 Railway veritabanı kurulumu başarıyla tamamlandı!
🌐 Uygulama başlatılıyor...
```

---

## 🔧 Sorun Giderme

### "Internal Server Error" alıyorum

**Çözüm:**
1. Railway Logs'ları kontrol edin
2. `SECRET_KEY` environment variable'ının ayarlandığını doğrulayın
3. MySQL servisinin aktif olduğunu kontrol edin (yeşil nokta)

### "Database connection failed"

**Çözüm:**
1. MySQL servisinin çalıştığını doğrulayın (Railway Dashboard)
2. `DATABASE_URL` otomatik oluşturuldu mu kontrol edin (Variables sekmesi)
3. Railway'deki MySQL servisine tıklayın → **Connect** → `DATABASE_URL` görünmeli

### "Application failed to start"

**Çözüm:**
1. Logs'da hata mesajını bulun
2. Environment variables'ın hepsinin ayarlandığını doğrulayın
3. GitHub'daki son commit'inizin doğru olduğunu kontrol edin

### Static dosyalar yüklenmiyor

**Çözüm:**
1. `static/` klasörünün GitHub'a commit edildiğini doğrulayın
2. `.gitignore` dosyasında `static/` klasörünün exclude edilmediğini kontrol edin

---

## 🔄 Güncelleme ve Yeniden Deploy

Kod değişikliklerinden sonra:

```powershell
# Değişiklikleri commit edin
git add .
git commit -m "Güncelleme açıklaması"
git push origin main
```

Railway otomatik olarak yeni deployment başlatacak (30 saniye içinde).

---

## 🌐 Custom Domain (Opsiyonel)

Kendi domain'inizi eklemek için:

1. Railway Dashboard → **Settings** → **Domains**
2. **Custom Domain** butonuna tıklayın
3. Domain'inizi girin (örn: `app.yourcompany.com`)
4. Railway size bir CNAME kaydı verecek
5. Domain sağlayıcınızda (GoDaddy, Namecheap vs.) bu CNAME kaydını ekleyin

**DNS ayarları:**
```
Type: CNAME
Name: app (veya subdomain'iniz)
Value: your-app.up.railway.app
```

DNS yayılması 5-30 dakika sürebilir.

---

## 📊 Monitoring

Railway otomatik olarak şunları sağlar:

- **CPU ve Memory kullanımı** (Dashboard → Metrics)
- **Application logs** (Dashboard → Logs)
- **Deployment history** (Dashboard → Deployments)
- **Automatic SSL** (HTTPS otomatik aktif)

---

## 💰 Maliyet

**Railway Free Tier:**
- $5 ücretsiz kredi/ay
- Hobby projeler için yeterli
- Uyku modu yok (7/24 aktif)

**Railway Pro (Önerilen):**
- $20/ay
- Production kullanımı için
- Daha fazla kaynak
- Prioritize destek

---

## 📞 Destek ve Yardım

**Railway Dökümantasyonu:**
- https://docs.railway.app/

**Railway Discord:**
- https://discord.gg/railway

**Proje Sorunları:**
- GitHub Issues bölümünü kullanın

---

## 🎉 Deployment Tamamlandı!

Artık Vize Randevu Sisteminiz Railway'de çalışıyor!

**Sonraki Adımlar:**
1. ✅ Admin paneline giriş yapın
2. ✅ Kullanıcıları ekleyin
3. ✅ Ülkeleri yapılandırın
4. ✅ Kota ayarlarını yapın
5. ✅ Sistemi test edin

**Güvenlik Önerileri:**
- Admin şifresini düzenli olarak değiştirin
- Railway Logs'ları düzenli kontrol edin
- Database backup'larını planlayın (Railway Dashboard → Database → Backups)

---

**İyi kullanımlar! 🚀**

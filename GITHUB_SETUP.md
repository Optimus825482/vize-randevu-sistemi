# 📦 GitHub Repository Kurulum Rehberi

Bu rehber, projenizi GitHub'a yüklemek için gereken adımları içerir.

## 🚀 Hızlı Başlangıç

### 1. Git Repository'sini Başlatın

```bash
# Proje dizinine gidin
cd d:\Claude\panel

# Git repository'sini başlatın (eğer yoksa)
git init

# Ana branch'i main olarak ayarlayın
git branch -M main
```

### 2. GitHub'da Yeni Repository Oluşturun

1. https://github.com adresine gidin
2. Sağ üstteki "+" işaretine tıklayın
3. "New repository" seçeneğini seçin
4. Repository bilgilerini girin:
   - **Repository name**: `vize-randevu-sistemi` (veya istediğiniz isim)
   - **Description**: "Modern vize randevu yönetim sistemi"
   - **Visibility**: Private veya Public (tercihinize göre)
   - ⚠️ "Add README", ".gitignore" veya "license" EKLEMEYIN (zaten mevcut)
5. "Create repository" butonuna tıklayın

### 3. Remote Repository'yi Bağlayın

GitHub'da oluşturduğunuz repository sayfasında gösterilen komutu kullanın:

```bash
# Remote repository'yi ekleyin
git remote add origin https://github.com/KULLANICI_ADINIZ/vize-randevu-sistemi.git

# Veya SSH kullanıyorsanız:
git remote add origin git@github.com:KULLANICI_ADINIZ/vize-randevu-sistemi.git
```

### 4. Dosyaları Commit Edin

```bash
# Tüm dosyaları staging area'ya ekleyin
git add .

# İlk commit'i yapın
git commit -m "Initial commit: Vize Randevu Sistemi

- Flask web uygulaması
- MySQL veritabanı entegrasyonu
- Admin ve kullanıcı panelleri
- Railway deployment hazır
- Güvenlik özellikleri
- Detaylı dokümantasyon"

# Uzak repository'ye push yapın
git push -u origin main
```

## 🔐 Güvenlik Kontrolleri

Push yapmadan önce şu dosyaların `.gitignore`'da olduğundan emin olun:

```bash
# Kontrol edin
cat .gitignore | grep -E "\.env|\.vscode|__pycache__|\.db"
```

✅ `.env` dosyası commit edilmemelidir!
✅ `.vscode/` klasörü commit edilmemelidir!
✅ `__pycache__/` klasörleri commit edilmemelidir!

## 📝 Önemli Notlar

### .env Dosyası

⚠️ **DİKKAT:** `.env` dosyasını asla GitHub'a yüklemeyin!

- ✅ `.env.example` dosyası repository'de olmalı
- ❌ `.env` dosyası repository'de olmamalı
- ✅ `.gitignore`'da `.env` olduğundan emin olun

### Hassas Bilgiler

Aşağıdaki bilgileri asla kodunuzda tutmayın:
- Veritabanı şifreleri
- API anahtarları
- SECRET_KEY
- Admin şifreleri

Bunları her zaman environment variables olarak kullanın.

## 🌿 Branch Stratejisi

### Ana Branchler

```bash
# Main branch - Production kodu
main

# Development branch (opsiyonel)
git checkout -b development
git push -u origin development
```

### Feature Branchler

Yeni özellikler eklerken:

```bash
# Yeni feature branch oluşturun
git checkout -b feature/yeni-ozellik-adi

# Değişiklikleri yapın ve commit edin
git add .
git commit -m "Feature: Yeni özellik eklendi"

# Push yapın
git push -u origin feature/yeni-ozellik-adi

# GitHub'da Pull Request oluşturun
```

## 🔄 Günlük İş Akışı

### Değişiklikleri Push Etme

```bash
# Mevcut durumu kontrol edin
git status

# Değişiklikleri görüntüleyin
git diff

# Dosyaları staging'e ekleyin
git add .
# veya belirli dosyalar için:
git add dosya1.py dosya2.py

# Commit yapın (açıklayıcı mesaj)
git commit -m "Fix: Randevu silme hatası düzeltildi"

# Push yapın
git push origin main
```

### Değişiklikleri Çekme

```bash
# Uzak repository'deki değişiklikleri çekin
git pull origin main
```

## 📊 Git Komutları Özeti

### Temel Komutlar

```bash
# Durum kontrolü
git status

# Log görüntüleme
git log --oneline

# Branch listesi
git branch -a

# Remote repository'ler
git remote -v

# Son commit'i geri alma (dikkatli!)
git reset --soft HEAD~1

# Dosya değişikliklerini geri alma
git checkout -- dosya.py

# Branch değiştirme
git checkout branch-adi

# Yeni branch oluştur ve geç
git checkout -b yeni-branch
```

### İleri Düzey

```bash
# Stash (geçici saklama)
git stash
git stash pop

# Cherry-pick (belirli commit'i alma)
git cherry-pick commit-hash

# Rebase
git rebase main

# Tag oluşturma (versiyon için)
git tag -a v1.0.0 -m "Version 1.0.0"
git push origin v1.0.0
```

## 🏷️ Commit Mesaj Standartları

İyi commit mesajları için:

```bash
# Format
<tip>: <kısa açıklama>

<detaylı açıklama (opsiyonel)>

# Tipler
feat: Yeni özellik
fix: Hata düzeltme
docs: Dokümantasyon
style: Formatla (kod değişikliği yok)
refactor: Kod yeniden yapılandırma
test: Test ekleme/düzenleme
chore: Yapılandırma değişiklikleri

# Örnekler
git commit -m "feat: Randevu filtreleme özelliği eklendi"
git commit -m "fix: Dashboard yükleme hatası düzeltildi"
git commit -m "docs: README güncellendi"
git commit -m "refactor: User model yeniden yapılandırıldı"
```

## 🔒 GitHub Security

### Secrets ve Variables

Railway deployment için GitHub Actions kullanıyorsanız:

1. GitHub Repository → Settings → Secrets and variables → Actions
2. "New repository secret" butonuna tıklayın
3. Hassas bilgileri ekleyin:
   - `SECRET_KEY`
   - `ADMIN_PASSWORD`
   - vb.

### Branch Protection

Production branch'ini korumak için:

1. GitHub Repository → Settings → Branches
2. "Add branch protection rule"
3. Branch name pattern: `main`
4. Şunları aktif edin:
   - ✅ Require pull request reviews
   - ✅ Require status checks to pass
   - ✅ Include administrators

## 📱 GitHub CLI (gh)

GitHub CLI kullanarak daha hızlı çalışın:

```bash
# GitHub CLI kurulumu (Windows)
winget install GitHub.cli

# Giriş yapın
gh auth login

# Repository oluşturma
gh repo create vize-randevu-sistemi --private --source=. --remote=origin --push

# Pull Request oluşturma
gh pr create --title "Yeni özellik" --body "Açıklama"

# Issues
gh issue create --title "Bug: Hata başlığı"
gh issue list
```

## 🎯 Checklist

Push yapmadan önce kontrol edin:

- [ ] `.env` dosyası `.gitignore`'da mı?
- [ ] Hassas bilgiler kodda yok mu?
- [ ] Commit mesajı açıklayıcı mı?
- [ ] Gereksiz dosyalar temizlendi mi?
- [ ] Test edildi mi?
- [ ] README güncel mi?
- [ ] Dokümantasyon tamamlandı mı?

## 🆘 Sorun Giderme

### Problem: "remote: Repository not found"

```bash
# Remote URL'i kontrol edin
git remote -v

# Doğru URL'i ayarlayın
git remote set-url origin https://github.com/KULLANICI_ADINIZ/REPO_ADINIZ.git
```

### Problem: ".env dosyası push edildi"

```bash
# Dosyayı repository'den kaldırın (ancak lokal'de bırakın)
git rm --cached .env

# .gitignore'a ekleyin (zaten olmalı)
echo ".env" >> .gitignore

# Commit ve push
git commit -m "Remove .env from repository"
git push origin main
```

### Problem: "Merge conflict"

```bash
# Mevcut değişiklikleri kaydedin
git stash

# Güncellemeleri çekin
git pull origin main

# Değişiklikleri geri getirin
git stash pop

# Çakışmaları manuel olarak çözün ve commit edin
```

## 📚 Ek Kaynaklar

- [Git Dokümantasyon](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Git Best Practices](https://www.git-tower.com/learn/git/ebook/en/command-line/appendix/best-practices)

---

**Hazır olduğunuzda Railway deployment için [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) rehberini takip edin!**

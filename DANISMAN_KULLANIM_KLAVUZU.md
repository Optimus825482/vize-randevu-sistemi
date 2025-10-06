# 📘 DANIŞMAN KULLANIM KILAVUZU
## Vize Randevu Yönetim Sistemi

**Versiyon:** 1.0.0  
**Güncelleme Tarihi:** 06.01.2025  
**Hedef Kitle:** Vize Danışmanları

---

## 📑 İçindekiler

1. [Giriş Yapma](#1-giriş-yapma)
2. [Ana Panel (Dashboard)](#2-ana-panel-dashboard)
3. [Randevu Talebi Oluşturma](#3-randevu-talebi-oluşturma)
4. [Randevu Listeleme ve Yönetimi](#4-randevu-listeleme-ve-yönetimi)
5. [Randevu Düzenleme](#5-randevu-düzenleme)
6. [Randevu Silme](#6-randevu-silme)
7. [Güncelleme ve Silme Talepleri](#7-güncelleme-ve-silme-talepleri)
8. [Kota Yönetimi](#8-kota-yönetimi)
9. [Ülke Bazlı İşlemler](#9-ülke-bazlı-i̇şlemler)
10. [Sık Karşılaşılan Sorunlar](#10-sık-karşılaşılan-sorunlar)

---

## 1. Giriş Yapma

### 1.1 İlk Giriş

1. Tarayıcınızda sisteme erişim adresi: `http://localhost:5000` veya sisteminizin IP adresi
2. Giriş sayfasında aşağıdaki bilgileri girin:
   - **Kullanıcı Adı:** Yöneticiniz tarafından size verilen kullanıcı adı
   - **Şifre:** Size verilen şifre
3. "Beni Hatırla" kutusunu işaretlerseniz, 30 gün boyunca otomatik giriş yaparsınız
4. **"Giriş Yap"** butonuna tıklayın

### 1.2 Şifre Güvenliği

⚠️ **Önemli Güvenlik Notları:**

- Paylaşımlı bilgisayarlarda "Beni Hatırla" seçeneğini kullanmayın

### 1.3 Çıkış Yapma

- Sağ üst köşedeki kullanıcı menüsünden **"Çıkış"** butonuna tıklayın
- Her zaman çıkış yapmayı unutmayın!

---

## 2. Ana Panel (Dashboard)

Giriş yaptıktan sonra karşınıza **Ana Panel** gelir. Burada:

### 2.1 İstatistikler

Dashboard'da şu istatistikleri görürsünüz:

| Kart | Açıklama |
|------|----------|
| **Toplam Randevular** | Tüm zamanlar boyunca oluşturduğunuz toplam randevu sayısı |
| **Bekleyen** | "Bekleme" durumundaki randevularınız |
| **İşlemde** | "Süreç Başlatıldı" durumundaki randevularınız |
| **Tamamlanan** | Başarıyla tamamlanmış randevularınız |
| **İptal Edilen** | İptal edilmiş randevularınız |

### 2.2 Hızlı Erişim Kartları

- **Atanmış Ülkeler:** Size atanan ülkeleri ve kotalarınızı görürsünüz
- **Son Randevular:** En son oluşturduğunuz 10 randevuyu listeler
- **Kota Durumu:** Her ülke için kullanılan ve kalan kotayı gösterir

### 2.3 Navigasyon Menüsü

Sol menüden şu sayfalara erişebilirsiniz:
- 🏠 **Ana Sayfa:** Dashboard
- 📅 **Randevularım:** Tüm randevularınızın listesi
- 🌍 **Ülkelere Göre:** Ülke bazlı randevu yönetimi

---

## 3. Randevu Talebi Oluşturma

### 3.1 Ülke Seçimi

1. Sol menüden **"Ülkelere Göre"** veya Dashboard'daki ülke kartlarından birine tıklayın
2. Size atanmış ülkelerin listesini göreceksiniz
3. Randevu oluşturmak istediğiniz ülkeye tıklayın

### 3.2 Kota Kontrolü

Ülke sayfasında:
- **Toplam Kota:** Size verilen toplam randevu limiti
- **Kullanılan:** Şu ana kadar oluşturduğunuz randevu sayısı
- **Kalan:** Oluşturabileceğiniz kalan randevu sayısı

⚠️ **Kota Doluysa:** Yeni randevu oluşturamazsınız. Yöneticinizle iletişime geçin.

### 3.3 Randevu Formu Doldurma

#### Zorunlu Bilgiler (Tüm Ülkeler İçin)

| Alan | Açıklama | Örnek |
|------|----------|-------|
| **Ad** | Başvuranın adı | Ahmet |
| **Soyad** | Başvuranın soyadı | Yılmaz |
| **Pasaport No** | Geçerli pasaport numarası | U12345678 |

#### Opsiyonel Bilgiler (Ülkeye Göre Değişir)

| Alan | Açıklama | Örnek |
|------|----------|-------|
| **Doğum Tarihi** | Başvuranın doğum tarihi | 15.05.1990 |
| **Telefon** | İletişim telefonu | +90 555 123 4567 |
| **E-posta** | İletişim e-postası | ahmet@email.com |
| **Pasaport Düzenleme Tarihi** | Pasaport verilme tarihi | 01.01.2020 |
| **Pasaport Geçerlilik Tarihi** | Pasaport son kullanma tarihi | 01.01.2030 |
| **Uyruk** | Vatandaşlık bilgisi | Türkiye Cumhuriyeti |
| **Seyahat Tarihi** | Planlanan seyahat tarihi | 20.07.2025 |
| **Adres** | İkametgah adresi | Atatürk Cad. No:123... |
| **Tercih Edilen Randevu Tarihi** | İstenen randevu tarihi aralığı | 10.02.2025 - 15.02.2025 |
| **Vize Türü** | Turistik, İş, Öğrenci vb. | Turistik |
| **Notlar** | Ek açıklamalar | Acil işlem gerekli |

### 3.4 Form Gönderme

1. Tüm gerekli bilgileri doldurun
2. **"Randevu Talebi Oluştur"** butonuna tıklayın
3. Başarılı mesajı aldıktan sonra randevu listeye eklenecektir
4. Randevu durumu otomatik olarak **"Bekleme"** olarak ayarlanır

### 3.5 Hata Durumları

| Hata Mesajı | Çözüm |
|-------------|-------|
| "Bu ülke için kota limitine ulaştınız" | Yöneticinizden kota artışı isteyin |
| "Zorunlu alanları doldurun" | Eksik alanları kontrol edin |
| "Geçersiz pasaport numarası" | Pasaport formatını kontrol edin |

---

## 4. Randevu Listeleme ve Yönetimi

### 4.1 Tüm Randevularım

Sol menüden **"Randevularım"** tıklayarak:
- Tüm randevularınızı görebilirsiniz
- Durum, ülke ve tarih bazında filtreleme yapabilirsiniz
- Detaylı arama yapabilirsiniz

### 4.2 Filtreleme Seçenekleri

| Filtre | Açıklama |
|--------|----------|
| **Durum** | Bekleme, Süreç Başlatıldı, Tamamlandı, İptal |
| **Ülke** | Belirli bir ülkeye ait randevular |
| **Arama** | Ad, soyad, pasaport no ile arama |

### 4.3 Randevu Kartı Bilgileri

Her randevu kartında:
- 📋 **Başvuran Bilgileri:** Ad, soyad
- 🌍 **Ülke:** Randevunun ülkesi
- 📅 **Oluşturma Tarihi:** Ne zaman oluşturuldu
- 🔔 **Durum:** Mevcut durumu (renkli etiket)
- ⚙️ **İşlemler:** Düzenle, Sil, Detaylar

### 4.4 Durum Renkleri

| Durum | Renk | Anlamı |
|-------|------|--------|
| **Bekleme** | 🟡 Sarı | Yönetici onayı bekleniyor |
| **Süreç Başlatıldı** | 🔵 Mavi | İşlem devam ediyor |
| **Tamamlandı** | 🟢 Yeşil | Başarıyla tamamlandı |
| **İptal** | 🔴 Kırmızı | İptal edildi |

---

## 5. Randevu Düzenleme

### 5.1 Düzenleme Koşulları

✅ **Düzenleyebilirsiniz:**
- Durum **"Bekleme"** olan randevular

❌ **Düzenleyemezsiniz:**
- Durum **"Süreç Başlatıldı"**, **"Tamamlandı"** veya **"İptal"** olan randevular
- Bu durumda "Güncelleme Talebi" oluşturmalısınız

### 5.2 Düzenleme Adımları

1. Randevu kartındaki **"Düzenle"** 🖊️ butonuna tıklayın
2. Düzenleme formunda değişiklik yapın
3. **"Güncelle"** butonuna tıklayın
4. Değişiklikler anında kaydedilir

⚠️ **Dikkat:** Zorunlu alanları (Ad, Soyad, Pasaport No) boş bırakmayın!

---

## 6. Randevu Silme

### 6.1 Silme Koşulları

✅ **Silebilirsiniz:**
- Durum **"Bekleme"** olan randevular

❌ **Silemezsiniz:**
- İşlem görmüş randevular
- Bu durumda "Silme Talebi" oluşturmalısınız

### 6.2 Silme Adımları

1. Randevu kartındaki **"Sil"** 🗑️ butonuna tıklayın
2. Onay penceresinde **"Evet, Sil"** deyin
3. Randevu kalıcı olarak silinir

⚠️ **Uyarı:** Silme işlemi geri alınamaz!

---

## 7. Güncelleme ve Silme Talepleri

### 7.1 Ne Zaman Talep Oluşturulur?

İşlem görmüş (Süreç Başlatıldı, Tamamlandı) randevularda:
- Değişiklik yapmak istiyorsanız → **Güncelleme Talebi**
- Silmek istiyorsanız → **Silme Talebi**

### 7.2 Güncelleme Talebi Oluşturma

1. Randevu kartında **"Güncelleme Talebi"** butonuna tıklayın
2. **Talep Nedeni** alanını doldurun (örnek: "Pasaport numarası değişti")
3. **"Talep Gönder"** butonuna tıklayın
4. Yönetici değerlendirecektir

### 7.3 Silme Talebi Oluşturma

1. Randevu kartında **"Silme Talebi"** butonuna tıklayın
2. **Silme Nedeni** alanını doldurun (örnek: "Yanlış ülke seçildi")
3. **"Talep Gönder"** butonuna tıklayın
4. Yönetici değerlendirecektir

### 7.4 Talep Durumları

| Durum | Açıklama | İşlem |
|-------|----------|-------|
| **Bekliyor** | Yönetici incelemesi bekleniyor | Bekleyin |
| **Onaylandı** | Talep kabul edildi | İşlem yapıldı |
| **Reddedildi** | Talep reddedildi | Yönetici notunu okuyun |

### 7.5 Talep Sonucunu Görme

- Dashboard veya randevu listesinde durum güncellenir
- Onaylanan talepler otomatik işlenir
- Reddedilen taleplerde yönetici notu görünür

---

## 8. Kota Yönetimi

### 8.1 Kotanızı Görme

**Ana Panel'de:**
- "Atanmış Ülkeler" kartında her ülke için kota görünür
- Kullanılan ve kalan kota oranı gösterilir

**Ülke Sayfasında:**
- Üst bölümde detaylı kota bilgisi
- İlerleme çubuğu ile görsel gösterim

### 8.2 Kota Tükendiğinde

❌ **Yeni randevu oluşturamazsınız**

✅ **Yapmanız Gerekenler:**
1. Yöneticinize kota artışı talebi gönderin
2. Mevcut randevularınızı kontrol edin
3. İptal edilmiş randevular varsa silin (kota serbest kalır)

### 8.3 Kota Artışı Talep Etme

1. Yöneticinize e-posta veya telefon ile ulaşın
2. Hangi ülke için kota artışı istediğinizi belirtin
3. Artış nedenini açıklayın
4. Yönetici onayından sonra yeni kota aktif olur

---

## 9. Ülke Bazlı İşlemler

### 9.1 Ülke Seçimi

Sol menüden **"Ülkelere Göre"** seçerek:
- Size atanmış tüm ülkeleri görürsünüz
- Her ülke için kota bilgisi gösterilir
- Ülkeye tıklayarak o ülkenin randevularını yönetirsiniz

### 9.2 Ülke Sayfası Özellikleri

| Bölüm | Açıklama |
|-------|----------|
| **Üst Bilgi** | Ülke adı, bayrak, kota durumu |
| **Yeni Randevu Formu** | Bu ülke için randevu oluşturma |
| **Randevu Listesi** | Bu ülkeye ait tüm randevularınız |
| **İstatistikler** | Durum bazında sayılar |

### 9.3 Ülke Bazlı Filtreleme

Ülke sayfasında:
- Sadece o ülkeye ait randevular görünür
- Durum filtresi uygulanabilir
- Tarih sıralama yapılabilir

---

## 10. Sık Karşılaşılan Sorunlar

### 10.1 Giriş Yapamıyorum

**Sorun:** Kullanıcı adı veya şifre hatalı

**Çözüm:**
- Kullanıcı adınızı ve şifrenizi kontrol edin
- Büyük/küçük harf duyarlılığına dikkat edin
- Şifrenizi unuttuysan yöneticinize başvurun

---

**Sorun:** "Hesabınız devre dışı bırakılmış" mesajı

**Çözüm:**
- Yöneticiniz hesabınızı pasif hale getirmiş
- Yöneticinize başvurun

### 10.2 Randevu Oluşturamıyorum

**Sorun:** "Kota limitine ulaştınız" hatası

**Çözüm:**
- Mevcut kotanızı kontrol edin
- Yöneticinizden kota artışı isteyin
- İptal edilmiş randevuları silin

---

**Sorun:** "Zorunlu alanları doldurun" hatası

**Çözüm:**
- Ad, Soyad, Pasaport No alanlarını doldurun
- Kırmızı çerçeveli alanları kontrol edin
- Geçerli veri formatı kullanın

### 10.3 Randevu Düzenleyemiyorum

**Sorun:** Düzenle butonu görünmüyor

**Çözüm:**
- Randevu durumu "Bekleme" değilse düzenleyemezsiniz
- "Güncelleme Talebi" oluşturun
- Yönetici onayı bekleyin

### 10.4 Sayfa Yüklenmiyor

**Sorun:** Beyaz sayfa veya hata mesajı

**Çözüm:**
1. Sayfayı yenileyin (F5)
2. Tarayıcı önbelleğini temizleyin
3. Farklı tarayıcı deneyin
4. İnternet bağlantınızı kontrol edin
5. IT destek ekibine başvurun

### 10.5 Veriler Kayboldu

**Sorun:** Oluşturduğum randevu görünmüyor

**Çözüm:**
- Filtre ayarlarını kontrol edin
- "Tüm Randevular" seçeneğini seçin
- Oturumu kapatıp tekrar girin
- Yöneticinize bildirin

---

## 📞 Destek ve İletişim

### Teknik Destek

- **E-posta:** support@vizesistemi.com
- **Telefon:** +90 XXX XXX XX XX
- **Çalışma Saatleri:** Hafta içi 09:00 - 18:00

### Sistem Yöneticisi

- İsim: [Yönetici Adı]
- E-posta: admin@vizesistemi.com
- Telefon: [Telefon]

### Acil Durumlar

Sistem tamamen erişilemezse:
1. IT destek ekibini arayın
2. Alternatif iletişim kanallarını kullanın
3. Mümkünse manuel süreçlere geçin

---

## ⚠️ Önemli Hatırlatmalar

1. ✅ **Şifrenizi kimseyle paylaşmayın**
2. ✅ **Çıkış yapmayı unutmayın**
3. ✅ **Düzenli olarak randevularınızı kontrol edin**
4. ✅ **Kota durumunuzu takip edin**
5. ✅ **Güncelleme taleplerinde açıklayıcı neden yazın**
6. ✅ **Kişisel verileri koruyun (KVKK/GDPR)**
7. ✅ **Yanlış bilgi girmeyin**
8. ✅ **Sistem güncellemelerini takip edin**

---

## 📋 Hızlı Referans Kılavuzu

### Kısayollar

| İşlem | Kısayol |
|-------|---------|
| Ana Sayfa | Sol menü → 🏠 Ana Sayfa |
| Yeni Randevu | Ülkeler → Ülke Seç → Form Doldur |
| Randevu Listesi | Sol menü → 📅 Randevularım |
| Çıkış | Sağ üst → Kullanıcı menüsü → Çıkış |

### Durum Akışı

```
Randevu Oluşturuldu (Bekleme)
         ↓
Yönetici İnceliyor (Süreç Başlatıldı)
         ↓
  ┌──────┴──────┐
  ↓             ↓
Tamamlandı    İptal
```

---

## 📝 Değişiklik Geçmişi

| Versiyon | Tarih | Değişiklikler |
|----------|-------|---------------|
| 1.0.0 | 06.01.2025 | İlk versiyon yayınlandı |

---

## 📄 Ek Kaynaklar

- [Sistem Yöneticisi Kılavuzu](YONETICI_KULLANIM_KLAVUZU.md)
- [Sık Sorulan Sorular (FAQ)](FAQ.md)
- [Video Eğitimler](https://youtube.com/...)

---

**© 2025 Vize Randevu Yönetim Sistemi**  
**Tüm hakları saklıdır.**

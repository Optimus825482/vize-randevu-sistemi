"""
Basit SMTP Test - Kütüphane bağımlılığı yok
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

print("=" * 70)
print("📧 SMTP BAĞLANTI TESTİ")
print("=" * 70)

# Gmail ayarları
sender_email = "vizal8254@gmail.com"
sender_password = "rsyg yksq tecj meel"  # Gmail uygulama şifresi
receiver_email = "test@example.com"  # Test için herhangi bir email

print(f"\n📮 Ayarlar:")
print(f"   ├─ Server: smtp.gmail.com")
print(f"   ├─ Port: 587")
print(f"   ├─ Gönderen: {sender_email}")
print(f"   └─ Alıcı: {receiver_email}")

try:
    print(f"\n🔄 SMTP sunucusuna bağlanılıyor...")
    server = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
    print(f"   ✅ Bağlantı kuruldu")
    
    print(f"\n🔒 TLS başlatılıyor...")
    server.starttls()
    print(f"   ✅ TLS aktif")
    
    print(f"\n🔑 Giriş yapılıyor...")
    server.login(sender_email, sender_password)
    print(f"   ✅ Kimlik doğrulama başarılı!")
    
    print(f"\n📧 Test maili oluşturuluyor...")
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Test Maili - Vize Randevu Sistemi"
    
    body = """
    Bu bir test mailidir.
    
    Eğer bu maili aldıysanız, mail sisteminiz çalışıyor demektir!
    """
    msg.attach(MIMEText(body, 'plain'))
    
    print(f"   ✅ Mail hazırlandı")
    
    print(f"\n📤 Mail gönderiliyor...")
    server.send_message(msg)
    print(f"   ✅ Mail başarıyla gönderildi!")
    
    server.quit()
    print(f"\n" + "=" * 70)
    print(f"✅✅✅ TÜM TESTLER BAŞARILI! ✅✅✅")
    print(f"=" * 70)
    print(f"\n💡 Railway'de çalışmıyorsa:")
    print(f"   1. Railway Variables bölümüne şu değişkenleri ekleyin:")
    print(f"      MAIL_USERNAME=vizal8254@gmail.com")
    print(f"      MAIL_PASSWORD=rsyg yksq tecj meel")
    print(f"   2. Deploy'u tetikleyin (herhangi bir değişiklik yapıp push edin)")
    
except smtplib.SMTPAuthenticationError as e:
    print(f"\n❌❌❌ KİMLİK DOĞRULAMA HATASI ❌❌❌")
    print(f"   Hata: {e}")
    print(f"\n🔧 ÇÖZÜM:")
    print(f"   1. Gmail'e giriş yapın: https://myaccount.google.com/security")
    print(f"   2. '2 Adımlı Doğrulama' AÇIK olmalı")
    print(f"   3. 'Uygulama Şifreleri' oluşturun")
    print(f"   4. 16 haneli şifreyi kullanın")
    
except smtplib.SMTPException as e:
    print(f"\n❌❌❌ SMTP HATASI ❌❌❌")
    print(f"   Hata: {e}")
    print(f"\n🔧 ÇÖZÜM:")
    print(f"   - İnternet bağlantınızı kontrol edin")
    print(f"   - Firewall/Antivirus SMTP'yi engelliyor olabilir")
    
except Exception as e:
    print(f"\n❌❌❌ BİLİNMEYEN HATA ❌❌❌")
    print(f"   Hata: {e}")
    print(f"   Tip: {type(e).__name__}")
    
    import traceback
    print(f"\n📋 Detaylı Hata:")
    traceback.print_exc()

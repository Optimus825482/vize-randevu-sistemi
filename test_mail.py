"""
Mail gönderme test scripti
Bu scripti çalıştırarak mail ayarlarınızı test edebilirsiniz
"""

import os
os.environ['FLASK_APP'] = 'app.py'

from app import app
from utils import send_new_user_credentials

print("=" * 70)
print("📧 MAİL GÖNDERİMİ TEST SCRIPTI")
print("=" * 70)

with app.app_context():
    print("\n📋 Mevcut Mail Ayarları:")
    print(f"   ├─ MAIL_SERVER: {app.config.get('MAIL_SERVER')}")
    print(f"   ├─ MAIL_PORT: {app.config.get('MAIL_PORT')}")
    print(f"   ├─ MAIL_USERNAME: {app.config.get('MAIL_USERNAME')}")
    print(f"   └─ MAIL_PASSWORD: {'*' * len(app.config.get('MAIL_PASSWORD', ''))}")
    
    print("\n🧪 Test Maili Gönderiliyor...")
    print("-" * 70)
    
    result = send_new_user_credentials(
        user_email='test@example.com',
        username='testuser',
        password='Test123!',
        full_name='Test User'
    )
    
    print("-" * 70)
    if result:
        print("✅ TEST BAŞARILI - Mail gönderildi!")
    else:
        print("❌ TEST BAŞARISIZ - Mail gönderilemedi!")
    
    print("\n💡 Railway'de test etmek için:")
    print("   1. Railway Dashboard → Variables")
    print("   2. MAIL_USERNAME ve MAIL_PASSWORD değişkenlerini kontrol edin")
    print("   3. Deployment loglarını inceleyin")

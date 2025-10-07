# Vize Randevu Sistemi - Veritabanı İlklendirme
# Veritabanını sıfırdan oluşturmak için: python init_db.py

from app import app, db
from models import User, Country, UserCountryQuota, Appointment, UpdateRequest, SystemLog
from config import Config

def init_database():
    """Veritabanını başlat ve örnek veriler ekle"""
    
    print("\n" + "="*60)
    print(" 🗄️  VERİTABANI İLKLENDİRME")
    print("="*60 + "\n")
    
    with app.app_context():
        # Tüm tabloları sil ve yeniden oluştur
        print("⚠️  Mevcut tablolar siliniyor...")
        db.drop_all()
        print("✓ Tablolar silindi\n")
        
        print("📋 Yeni tablolar oluşturuluyor...")
        db.create_all()
        print("✓ Tablolar oluşturuldu\n")
        
        # Admin kullanıcısı
        print("👤 Admin kullanıcısı oluşturuluyor...")
        admin = User(
            username=Config.ADMIN_USERNAME,
            email=Config.ADMIN_EMAIL,
            full_name='Sistem Yöneticisi',
            is_admin=True,
            is_active=True
        )
        admin.set_password(Config.ADMIN_PASSWORD)
        db.session.add(admin)
        print(f"✓ Admin: {Config.ADMIN_USERNAME}\n")
        
        # Örnek kullanıcılar
        print("👥 Örnek kullanıcılar oluşturuluyor...")
        sample_users = [
            {
                'username': 'user1',
                'email': 'user1@example.com',
                'full_name': 'Ahmet Yılmaz',
                'password': 'User123!'
            },
            {
                'username': 'user2',
                'email': 'user2@example.com',
                'full_name': 'Ayşe Demir',
                'password': 'User123!'
            },
        ]
        
        users = []
        for user_data in sample_users:
            password = user_data.pop('password')
            user = User(**user_data, is_admin=False, is_active=True)
            user.set_password(password)
            db.session.add(user)
            users.append(user)
            print(f"  • {user_data['username']} - {user_data['full_name']}")
        
        print("✓ Kullanıcılar oluşturuldu\n")
        
        # Ülkeler
        print("🌍 Ülkeler ekleniyor...")
        sample_countries = [
            {'name': 'Amerika Birleşik Devletleri', 'code': 'USA', 'flag_emoji': '🇺🇸'},
            {'name': 'İngiltere', 'code': 'GBR', 'flag_emoji': '🇬🇧'},
            {'name': 'Almanya', 'code': 'DEU', 'flag_emoji': '🇩🇪'},
            {'name': 'Fransa', 'code': 'FRA', 'flag_emoji': '🇫🇷'},
            {'name': 'İtalya', 'code': 'ITA', 'flag_emoji': '🇮🇹'},
            {'name': 'İspanya', 'code': 'ESP', 'flag_emoji': '🇪🇸'},
            {'name': 'Kanada', 'code': 'CAN', 'flag_emoji': '🇨🇦'},
            {'name': 'Avustralya', 'code': 'AUS', 'flag_emoji': '🇦🇺'},
            {'name': 'Japonya', 'code': 'JPN', 'flag_emoji': '🇯🇵'},
            {'name': 'Güney Kore', 'code': 'KOR', 'flag_emoji': '🇰🇷'},
        ]
        
        countries = []
        for country_data in sample_countries:
            country = Country(**country_data, is_active=True)
            db.session.add(country)
            countries.append(country)
            print(f"  {country_data['flag_emoji']} {country_data['name']}")
        
        db.session.commit()
        print("✓ Ülkeler eklendi\n")
        
        # Kullanıcılara kotalar ata
        print("📊 Kullanıcı kotaları atanıyor...")
        for user in users:
            # Her kullanıcıya rastgele 3-5 ülke ata
            import random
            assigned_countries = random.sample(countries, k=random.randint(3, 5))
            
            for country in assigned_countries:
                quota = UserCountryQuota(
                    user_id=user.id,
                    country_id=country.id,
                    quota_limit=random.randint(5, 20)
                )
                db.session.add(quota)
                print(f"  • {user.username} → {country.name} (Kota: {quota.quota_limit})")
        
        db.session.commit()
        print("✓ Kotalar atandı\n")
        
        print("="*60)
        print(" ✅ VERİTABANI BAŞARIYLA OLUŞTURULDU!")
        print("="*60)
        print("\n📝 GİRİŞ BİLGİLERİ:")
        print("-" * 60)
        print(f"  Admin Kullanıcı: {Config.ADMIN_USERNAME}")
        print(f"  Admin Şifre: {Config.ADMIN_PASSWORD}")
        print(f"\n  Test Kullanıcı: user1")
        print(f"  Test Şifre: User123!")
        print("-" * 60)
        print("\n🌐 Sistemi başlatmak için: python run.py")
        print("🌐 Veya: python app.py\n")


if __name__ == '__main__':
    response = input("⚠️  Tüm veriler silinecek! Devam etmek istediğinize emin misiniz? (E/H): ")
    if response.upper() in ['E', 'EVET', 'YES', 'Y']:
        init_database()
    else:
        print("\n❌ İşlem iptal edildi.")

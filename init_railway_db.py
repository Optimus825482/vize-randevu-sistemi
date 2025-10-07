#!/usr/bin/env python3
"""
Railway MySQL veritabanı otomatik kurulum scripti
Bu script Railway'de MySQL veritabanını otomatik olarak kurar
"""
import os
import sys
from sqlalchemy import create_engine, text
from models import db, User, Country
from app import app

def init_database():
    """Veritabanını başlat ve tabloları oluştur"""
    print("🚀 Railway veritabanı kurulumu başlatılıyor...")
    
    try:
        with app.app_context():
            # Tüm tabloları oluştur
            print("📋 Tablolar oluşturuluyor...")
            db.create_all()
            print("✅ Tablolar başarıyla oluşturuldu!")
            
            # Migration kontrolü - eksik kolonları ekle
            print("\n🔍 Veritabanı migration kontrolü yapılıyor...")
            engine = db.engine
            
            # residence_city_required kolonu kontrolü (countries tablosu)
            try:
                with engine.connect() as conn:
                    result = conn.execute(text("SHOW COLUMNS FROM countries LIKE 'residence_city_required'"))
                    if result.fetchone() is None:
                        print("   ➕ countries.residence_city_required ekleniyor...")
                        conn.execute(text("""
                            ALTER TABLE countries 
                            ADD COLUMN residence_city_required BOOLEAN NOT NULL DEFAULT FALSE
                            AFTER office_required
                        """))
                        conn.commit()
                        print("   ✅ countries.residence_city_required eklendi")
                    else:
                        print("   ✓ countries.residence_city_required mevcut")
            except Exception as e:
                print(f"   ⚠️  residence_city_required kontrolü hatası: {e}")
            
            # residence_city kolonu kontrolü (appointments tablosu)
            try:
                with engine.connect() as conn:
                    result = conn.execute(text("SHOW COLUMNS FROM appointments LIKE 'residence_city'"))
                    if result.fetchone() is None:
                        print("   ➕ appointments.residence_city ekleniyor...")
                        conn.execute(text("""
                            ALTER TABLE appointments 
                            ADD COLUMN residence_city VARCHAR(100) NULL
                            AFTER office
                        """))
                        conn.commit()
                        print("   ✅ appointments.residence_city eklendi")
                    else:
                        print("   ✓ appointments.residence_city mevcut")
            except Exception as e:
                print(f"   ⚠️  residence_city kontrolü hatası: {e}")
            
            print("✅ Migration kontrolü tamamlandı!")
            
            # Admin kullanıcısı kontrolü
            admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
            admin = User.query.filter_by(username=admin_username).first()
            
            if not admin:
                print(f"👤 Admin kullanıcısı oluşturuluyor: {admin_username}")
                admin = User(
                    username=admin_username,
                    email=os.environ.get('ADMIN_EMAIL', 'admin@vizesistemi.com'),
                    full_name='Sistem Yöneticisi',
                    is_admin=True,
                    is_active=True
                )
                admin.set_password(os.environ.get('ADMIN_PASSWORD', 'Admin123!'))
                db.session.add(admin)
                db.session.commit()
                print(f"✅ Admin kullanıcısı oluşturuldu!")
            else:
                print(f"ℹ️  Admin kullanıcısı zaten mevcut: {admin_username}")
            
            # Örnek ülkeler kontrolü
            if Country.query.count() == 0:
                print("🌍 Örnek ülkeler ekleniyor...")
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
                
                for country_data in sample_countries:
                    country = Country(**country_data)
                    db.session.add(country)
                
                db.session.commit()
                print(f"✅ {len(sample_countries)} örnek ülke eklendi!")
            else:
                print(f"ℹ️  Ülkeler zaten mevcut: {Country.query.count()} ülke")
            
            print("\n" + "="*60)
            print("🎉 Railway veritabanı kurulumu başarıyla tamamlandı!")
            print("="*60)
            print(f"👤 Admin Kullanıcı Adı: {admin_username}")
            print(f"🔑 Admin Şifresi: {os.environ.get('ADMIN_PASSWORD', 'Admin123!')}")
            print(f"📊 Toplam Ülke: {Country.query.count()}")
            print("="*60 + "\n")
            
            return True
            
    except Exception as e:
        print(f"❌ Hata oluştu: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = init_database()
    sys.exit(0 if success else 1)

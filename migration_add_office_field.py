"""
Migration: Randevu tablosuna ofis alanı ekleme
Oluşturma Tarihi: 07.10.2025

Bu migration:
- Appointment tablosuna 'office' alanı ekler (varchar 100)
- Country tablosuna 'office_required' alanı ekler (boolean, default False)
"""

import os
import sys
from sqlalchemy import create_engine, text

# DATABASE_URL'yi environment'tan al (Railway'de MYSQL_URL da kullanılabilir)
DATABASE_URL = os.environ.get('DATABASE_URL') or os.environ.get('MYSQL_URL')

if not DATABASE_URL:
    print("❌ DATABASE_URL veya MYSQL_URL environment variable bulunamadı!")
    print("Railway için: Railway Dashboard → Variables")
    print("Local için: .env dosyasına DATABASE_URL ekleyin")
    sys.exit(1)

# MySQL URL düzeltmesi (Railway bazen mysql:// yerine mysql+pymysql:// gerektirir)
if DATABASE_URL.startswith('mysql://'):
    DATABASE_URL = DATABASE_URL.replace('mysql://', 'mysql+pymysql://')

print("=" * 70)
print("📋 OFİS ALANI EKLEME MIGRATION")
print("=" * 70)
print(f"Database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'Unknown'}")
print()

try:
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        print("✅ Veritabanına bağlanıldı")
        
        # 1. Appointment tablosuna 'office' alanını ekle
        print("\n📝 Migration 1: Appointment tablosuna 'office' alanı ekleniyor...")
        
        # Önce alan var mı kontrol et
        check_column = text("""
            SELECT COUNT(*) as count 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE()
            AND TABLE_NAME = 'appointment' 
            AND COLUMN_NAME = 'office'
        """)
        
        result = conn.execute(check_column)
        column_exists = result.fetchone()[0] > 0
        
        if column_exists:
            print("   ℹ️  'office' alanı zaten mevcut, atlanıyor...")
        else:
            alter_appointment = text("""
                ALTER TABLE appointment 
                ADD COLUMN office VARCHAR(100) NULL
                COMMENT 'Vize başvurusunun yapılacağı ofis'
            """)
            conn.execute(alter_appointment)
            conn.commit()
            print("   ✅ Appointment.office alanı eklendi")
        
        # 2. Country tablosuna 'office_required' alanını ekle
        print("\n📝 Migration 2: Country tablosuna 'office_required' alanı ekleniyor...")
        
        check_country_column = text("""
            SELECT COUNT(*) as count 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE()
            AND TABLE_NAME = 'country' 
            AND COLUMN_NAME = 'office_required'
        """)
        
        result = conn.execute(check_country_column)
        country_column_exists = result.fetchone()[0] > 0
        
        if country_column_exists:
            print("   ℹ️  'office_required' alanı zaten mevcut, atlanıyor...")
        else:
            alter_country = text("""
                ALTER TABLE country 
                ADD COLUMN office_required BOOLEAN NOT NULL DEFAULT FALSE
                COMMENT 'Bu ülke için ofis seçimi zorunlu mu?'
            """)
            conn.execute(alter_country)
            conn.commit()
            print("   ✅ Country.office_required alanı eklendi")
        
        # 3. Mevcut kayıt sayılarını göster
        print("\n📊 Mevcut Veriler:")
        
        count_appointments = text("SELECT COUNT(*) FROM appointment")
        result = conn.execute(count_appointments)
        total_appointments = result.fetchone()[0]
        print(f"   ├─ Toplam Randevu: {total_appointments}")
        
        count_countries = text("SELECT COUNT(*) FROM country")
        result = conn.execute(count_countries)
        total_countries = result.fetchone()[0]
        print(f"   └─ Toplam Ülke: {total_countries}")
        
        print("\n✅✅✅ MİGRATION BAŞARILI! ✅✅✅")
        print()
        print("📌 NOT:")
        print("   - Mevcut randevular için 'office' alanı NULL (boş) olacak")
        print("   - Yeni randevularda kullanıcı ofis seçebilecek")
        print("   - Ülke ayarlarından hangi ülkeler için zorunlu olduğunu belirleyebilirsiniz")
        print()
        
except Exception as e:
    print(f"\n❌ Migration hatası: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

"""
Migration: Yerleşim yeri (residence_city) alanlarını ekle
"""
import os
import sys
import pymysql
from urllib.parse import urlparse

def run_migration():
    """Veritabanına residence_city alanlarını ekle"""
    
    # Railway DATABASE_URL'den bağlantı bilgilerini al
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL bulunamadı!")
        sys.exit(1)
    
    # URL'i parse et
    parsed = urlparse(database_url)
    
    # Bağlantı bilgileri
    host = parsed.hostname
    port = parsed.port or 3306
    user = parsed.username
    password = parsed.password
    database = parsed.path.lstrip('/')
    
    print(f"🔗 Veritabanına bağlanılıyor: {user}@{host}:{port}/{database}")
    
    try:
        # Veritabanına bağlan
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        print("\n📋 Migration başlıyor...\n")
        
        # 1. countries tablosuna residence_city_required kolonu ekle
        print("1️⃣ countries.residence_city_required kolonu ekleniyor...")
        try:
            cursor.execute("""
                ALTER TABLE countries 
                ADD COLUMN residence_city_required BOOLEAN NOT NULL DEFAULT FALSE
                AFTER office_required
            """)
            print("   ✅ countries.residence_city_required eklendi")
        except pymysql.err.OperationalError as e:
            if "Duplicate column name" in str(e):
                print("   ⚠️  Kolon zaten var, atlanıyor")
            else:
                raise
        
        # 2. appointments tablosuna residence_city kolonu ekle
        print("2️⃣ appointments.residence_city kolonu ekleniyor...")
        try:
            cursor.execute("""
                ALTER TABLE appointments 
                ADD COLUMN residence_city VARCHAR(100) NULL
                AFTER office
            """)
            print("   ✅ appointments.residence_city eklendi")
        except pymysql.err.OperationalError as e:
            if "Duplicate column name" in str(e):
                print("   ⚠️  Kolon zaten var, atlanıyor")
            else:
                raise
        
        # Commit
        connection.commit()
        
        print("\n✅ Migration başarıyla tamamlandı!\n")
        
        # Kontrol sorgusu
        cursor.execute("SHOW COLUMNS FROM countries LIKE 'residence_city_required'")
        result1 = cursor.fetchone()
        
        cursor.execute("SHOW COLUMNS FROM appointments LIKE 'residence_city'")
        result2 = cursor.fetchone()
        
        if result1 and result2:
            print("🔍 Doğrulama:")
            print(f"   ✅ countries.residence_city_required: {result1[1]}")
            print(f"   ✅ appointments.residence_city: {result2[1]}")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"\n❌ Migration hatası: {e}")
        sys.exit(1)

if __name__ == '__main__':
    run_migration()

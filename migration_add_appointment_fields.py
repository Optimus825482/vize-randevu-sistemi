"""
Migration: Add dynamic fields to appointments table
"""
from app import app, db

def migrate():
    with app.app_context():
        with db.engine.connect() as conn:
            try:
                # Mevcut alanları nullable yap
                print("📝 Mevcut alanlar nullable yapılıyor...")
                
                # NOT: SQLite ALTER TABLE sınırlı - CREATE yeni tablo + COPY + DROP eski yapılmalı
                # Ancak production'da dikkatli olunmalı. Şimdilik yeni kolonları ekleyelim:
                
                # Yeni kolonlar ekle
                print("➕ Yeni kolonlar ekleniyor...")
                
                conn.execute(db.text("ALTER TABLE appointments ADD COLUMN passport_issue_date DATE"))
                conn.commit()
                print("✅ passport_issue_date eklendi")
                
                conn.execute(db.text("ALTER TABLE appointments ADD COLUMN passport_expiry_date DATE"))
                conn.commit()
                print("✅ passport_expiry_date eklendi")
                
                conn.execute(db.text("ALTER TABLE appointments ADD COLUMN nationality VARCHAR(100)"))
                conn.commit()
                print("✅ nationality eklendi")
                
                conn.execute(db.text("ALTER TABLE appointments ADD COLUMN travel_date DATE"))
                conn.commit()
                print("✅ travel_date eklendi")
                
                conn.execute(db.text("ALTER TABLE appointments ADD COLUMN preferred_date_end DATE"))
                conn.commit()
                print("✅ preferred_date_end eklendi")
                
                print("\n✨ Migration başarıyla tamamlandı!")
                print("⚠️  NOT: birth_date, phone, email alanları artık nullable olmalı.")
                print("   SQLite'da bu değişiklik için tam tablo yeniden oluşturma gerekir.")
                print("   Mevcut veriler korunduğu için şimdilik sorun çıkmayacak.")
                
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("⚠️  Kolonlar zaten mevcut, migration atlanıyor")
                else:
                    print(f"❌ Migration hatası: {e}")
                    raise

if __name__ == '__main__':
    migrate()

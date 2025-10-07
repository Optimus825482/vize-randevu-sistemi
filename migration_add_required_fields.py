"""
Migration: Add required_fields column to countries table
"""
from app import app, db

def migrate():
    with app.app_context():
        # SQLite için ALTER TABLE
        with db.engine.connect() as conn:
            try:
                # Kolon ekle
                conn.execute(db.text("ALTER TABLE countries ADD COLUMN required_fields TEXT DEFAULT '{}'"))
                conn.commit()
                print("✅ Migration başarılı: required_fields kolonu eklendi")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("⚠️  Kolon zaten mevcut, migration atlanıyor")
                else:
                    print(f"❌ Migration hatası: {e}")
                    raise

if __name__ == '__main__':
    migrate()

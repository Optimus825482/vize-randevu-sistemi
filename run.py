# Vize Randevu Sistemi - Başlangıç Komutu
# Sistemi başlatmak için: python run.py

from app import app

if __name__ == '__main__':
    import os
    
    # DEBUG mode kontrolü - Production'da KAPALI olmalı
    DEBUG_MODE = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    PORT = int(os.environ.get('PORT', 5000))
    
    print("\n" + "="*60)
    print(" 🌍 VİZE RANDEVU YÖNETİM SİSTEMİ")
    print("="*60)
    print(f"\n📌 Sistem başlatılıyor...")
    print(f"   ├─ Debug Mode: {'✅ AÇIK (Development)' if DEBUG_MODE else '🔒 KAPALI (Production)'}")
    print(f"   ├─ Port: {PORT}")
    print(f"   └─ Host: 0.0.0.0\n")
    
    if DEBUG_MODE and os.environ.get('RAILWAY_ENVIRONMENT'):
        print("⚠️  WARNING: Production ortamında DEBUG mode açık!")
    
    try:
        app.run(
            debug=DEBUG_MODE,
            host='0.0.0.0',
            port=PORT,
            use_reloader=DEBUG_MODE  # Sadece debug modunda reloader kullan
        )
    except KeyboardInterrupt:
        print("\n\n✓ Sistem kapatıldı.")
    except Exception as e:
        print(f"\n\n✗ Hata: {e}")
        print("\nLütfen .env dosyanızı ve veritabanı ayarlarınızı kontrol edin.")

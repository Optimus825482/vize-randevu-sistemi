# Vize Randevu Sistemi - Başlangıç Komutu
# Sistemi başlatmak için: python run.py

from app import app

if __name__ == '__main__':
    print("\n" + "="*60)
    print(" 🌍 VİZE RANDEVU YÖNETİM SİSTEMİ")
    print("="*60)
    print("\n📌 Sistem başlatılıyor...\n")
    
    try:
        app.run(
            debug=True,
            host='0.0.0.0',
            port=5000,
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\n\n✓ Sistem kapatıldı.")
    except Exception as e:
        print(f"\n\n✗ Hata: {e}")
        print("\nLütfen .env dosyanızı ve veritabanı ayarlarınızı kontrol edin.")

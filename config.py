import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Uygulama yapılandırma sınıfı"""
    
    # Flask temel ayarları
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # SECRET_KEY kontrolü - Production için zorunlu
    if not SECRET_KEY:
        if os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('FLASK_ENV') == 'production':
            raise ValueError("❌ CRITICAL: SECRET_KEY environment variable zorunludur!")
        else:
            # Development için geçici key
            SECRET_KEY = 'dev-secret-key-ONLY-FOR-DEVELOPMENT'
            print("⚠️  WARNING: Development mode - Geçici SECRET_KEY kullanılıyor")
    
    # Veritabanı ayarları
    # Railway DATABASE_URL'i önce kontrol et - Tüm olası isimleri dene
    database_url = (
        os.environ.get('DATABASE_URL') or 
        os.environ.get('MYSQL_URL') or
        os.environ.get('DATABASE_PRIVATE_URL') or
        os.environ.get('MYSQLHOST')  # Eğer ayrı parametreler varsa
    )
    
    # Eğer MYSQLHOST var ama URL yok ise, manuel olarak oluştur
    if not database_url and os.environ.get('MYSQLHOST'):
        mysql_host = os.environ.get('MYSQLHOST')
        mysql_port = os.environ.get('MYSQLPORT', '3306')
        mysql_user = os.environ.get('MYSQLUSER', 'root')
        mysql_password = os.environ.get('MYSQLPASSWORD', '')
        mysql_database = os.environ.get('MYSQLDATABASE', 'railway')
        database_url = f"mysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}"
        print(f"🔧 Constructed DATABASE_URL from individual variables")
    
    # Debug için - TÜM environment variables'ı listele
    print("=" * 60)
    print("🔍 Environment Variables Check:")
    print("=" * 60)
    env_vars_to_check = [
        'DATABASE_URL', 'MYSQL_URL', 'DATABASE_PRIVATE_URL',
        'MYSQLHOST', 'MYSQLPORT', 'MYSQLUSER', 'MYSQLDATABASE',
        'RAILWAY_ENVIRONMENT', 'PORT'
    ]
    for var in env_vars_to_check:
        value = os.environ.get(var)
        if value and 'PASSWORD' not in var:
            print(f"✅ {var}: {value[:50]}...")
        elif value:
            print(f"✅ {var}: [HIDDEN]")
        else:
            print(f"❌ {var}: Not found")
    print("=" * 60)
    
    if database_url:
        # Railway MySQL URL formatını düzelt
        if database_url.startswith('mysql://'):
            database_url = database_url.replace('mysql://', 'mysql+pymysql://', 1)
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        # Local development için
        print("⚠️ No DATABASE_URL found, using local config")
        DB_HOST = os.environ.get('DB_HOST', 'localhost')
        DB_USER = os.environ.get('DB_USER', 'root')
        DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
        DB_NAME = os.environ.get('DB_NAME', 'vize_randevu_db')
        SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # Connection Pool Ayarları - Performance ve Security
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'max_overflow': 20,
        'pool_timeout': 30
    }
    
    # Güvenlik
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'  # Lax'tan Strict'e değiştirildi
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'  # HTTPS zorunlu production'da
    PERMANENT_SESSION_LIFETIME = 1800  # 30 dakika (1800 saniye)
    
    # CSRF Protection
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600  # 1 saat
    
    # Dosya yükleme
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = 'uploads'
    EXPORT_FOLDER = 'exports'
    
    # Sayfalama
    ITEMS_PER_PAGE = 10
    
    # Admin varsayılan bilgileri
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'Admin123!')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@vizesistemi.com')
    
    # Mail ayarları - ENVIRONMENT VARIABLES ZORUNLU
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', MAIL_USERNAME)
    
    # Mail credentials kontrolü - Production için zorunlu
    if os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('FLASK_ENV') == 'production':
        if not MAIL_USERNAME or not MAIL_PASSWORD:
            print("⚠️  WARNING: MAIL_USERNAME ve MAIL_PASSWORD environment variables ayarlanmamış!")
            print("   E-posta özellikleri çalışmayacak!")
    
    # Ofis seçenekleri
    OFFICE_CHOICES = [
        'İzmir Ofis',
        'İstanbul Gayrettepe Ofis',
        'İstanbul Beyoğlu Ofis',
        'İstanbul - Altunizade',
        'Antalya Ofis',
        'Bursa Ofis',
        'Edirne Ofis',
        'Ankara Ofis'
    ]
    
    # Türkiye İlleri (Yerleşim Yeri Seçenekleri)
    TURKEY_CITIES = [
        'Adana', 'Adıyaman', 'Afyonkarahisar', 'Ağrı', 'Aksaray', 'Amasya', 'Ankara', 'Antalya',
        'Ardahan', 'Artvin', 'Aydın', 'Balıkesir', 'Bartın', 'Batman', 'Bayburt', 'Bilecik',
        'Bingöl', 'Bitlis', 'Bolu', 'Burdur', 'Bursa', 'Çanakkale', 'Çankırı', 'Çorum',
        'Denizli', 'Diyarbakır', 'Düzce', 'Edirne', 'Elazığ', 'Erzincan', 'Erzurum', 'Eskişehir',
        'Gaziantep', 'Giresun', 'Gümüşhane', 'Hakkari', 'Hatay', 'Iğdır', 'Isparta', 'İstanbul',
        'İzmir', 'Kahramanmaraş', 'Karabük', 'Karaman', 'Kars', 'Kastamonu', 'Kayseri', 'Kilis',
        'Kırıkkale', 'Kırklareli', 'Kırşehir', 'Kocaeli', 'Konya', 'Kütahya', 'Malatya', 'Manisa',
        'Mardin', 'Mersin', 'Muğla', 'Muş', 'Nevşehir', 'Niğde', 'Ordu', 'Osmaniye',
        'Rize', 'Sakarya', 'Samsun', 'Şanlıurfa', 'Siirt', 'Sinop', 'Şırnak', 'Sivas',
        'Tekirdağ', 'Tokat', 'Trabzon', 'Tunceli', 'Uşak', 'Van', 'Yalova', 'Yozgat', 'Zonguldak'
    ]

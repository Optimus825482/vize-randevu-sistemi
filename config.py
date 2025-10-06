import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Uygulama yapılandırma sınıfı"""
    
    # Flask temel ayarları
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
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
    
    # Güvenlik
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 saat
    
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

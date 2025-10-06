import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Uygulama yapılandırma sınıfı"""
    
    # Flask temel ayarları
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Veritabanı ayarları
    # Railway DATABASE_URL'i önce kontrol et
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        # Railway MySQL URL formatını düzelt
        if database_url.startswith('mysql://'):
            database_url = database_url.replace('mysql://', 'mysql+pymysql://', 1)
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        # Local development için
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

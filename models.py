from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """Kullanıcı modeli"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # İlişkiler
    country_quotas = db.relationship('UserCountryQuota', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    appointments = db.relationship('Appointment', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    update_requests = db.relationship('UpdateRequest', foreign_keys='UpdateRequest.user_id', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    processed_requests = db.relationship('UpdateRequest', foreign_keys='UpdateRequest.processed_by', backref='processor', lazy='dynamic')
    
    def set_password(self, password):
        """Şifre hash'leme"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Şifre kontrolü"""
        return check_password_hash(self.password_hash, password)
    
    def get_quota_for_country(self, country_id):
        """Belirli bir ülke için kullanıcının kotasını al"""
        quota = UserCountryQuota.query.filter_by(
            user_id=self.id, 
            country_id=country_id
        ).first()
        return quota.quota_limit if quota else 0
    
    def get_used_quota_for_country(self, country_id):
        """Belirli bir ülke için kullanılan kota sayısı"""
        return Appointment.query.filter_by(
            user_id=self.id,
            country_id=country_id
        ).count()
    
    def __repr__(self):
        return f'<User {self.username}>'


class Country(db.Model):
    """Ülke modeli"""
    __tablename__ = 'countries'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    code = db.Column(db.String(3), unique=True, nullable=False)  # ISO kod
    flag_emoji = db.Column(db.String(10))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Dinamik form alanları (JSON)
    # Format: {"birth_date": {"required": true, "enabled": true}, ...}
    required_fields = db.Column(db.Text, default='{}')
    
    # İlişkiler
    quotas = db.relationship('UserCountryQuota', backref='country', lazy='dynamic', cascade='all, delete-orphan')
    appointments = db.relationship('Appointment', backref='country', lazy='dynamic', cascade='all, delete-orphan')
    
    def get_required_fields(self):
        """JSON string'i dict'e çevir"""
        import json
        try:
            return json.loads(self.required_fields) if self.required_fields else {}
        except Exception:
            return {}
    
    def set_required_fields(self, fields_dict):
        """Dict'i JSON string'e çevir"""
        import json
        self.required_fields = json.dumps(fields_dict)
    
    def __repr__(self):
        return f'<Country {self.name}>'


class UserCountryQuota(db.Model):
    """Kullanıcı-Ülke Kota İlişkisi"""
    __tablename__ = 'user_country_quotas'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=False)
    quota_limit = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Benzersiz constraint
    __table_args__ = (db.UniqueConstraint('user_id', 'country_id', name='unique_user_country'),)
    
    def __repr__(self):
        return f'<Quota User:{self.user_id} Country:{self.country_id} Limit:{self.quota_limit}>'


class Appointment(db.Model):
    """Randevu Talebi Modeli"""
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=False)
    
    # Başvuran kişi bilgileri (zorunlu alanlar)
    applicant_name = db.Column(db.String(150), nullable=False)
    applicant_surname = db.Column(db.String(150), nullable=False)
    passport_number = db.Column(db.String(50), nullable=False)
    
    # Opsiyonel başvuran bilgileri
    birth_date = db.Column(db.Date)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    passport_issue_date = db.Column(db.Date)
    passport_expiry_date = db.Column(db.Date)
    nationality = db.Column(db.String(100))
    travel_date = db.Column(db.Date)
    address = db.Column(db.Text)
    
    # Randevu bilgileri
    preferred_date = db.Column(db.Date)
    preferred_date_end = db.Column(db.Date)  # Tarih aralığı sonu
    visa_type = db.Column(db.String(100))  # Turist, İş, Öğrenci vb.
    notes = db.Column(db.Text)
    
    # Durum takibi
    status = db.Column(db.String(50), default='Bekleme')  # Bekleme, Süreç Başlatıldı, Tamamlandı, İptal
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    processed_at = db.Column(db.DateTime)
    
    # İlişkiler
    update_requests = db.relationship('UpdateRequest', backref='appointment', lazy='dynamic', cascade='all, delete-orphan')
    
    def can_edit(self):
        """Düzenleme yapılabilir mi?"""
        return self.status == 'Bekleme'
    
    def can_delete(self):
        """Silinebilir mi?"""
        return self.status == 'Bekleme'
    
    def __repr__(self):
        return f'<Appointment {self.id} - {self.applicant_name} {self.applicant_surname}>'


class UpdateRequest(db.Model):
    """Güncelleme/Silme Talep Modeli"""
    __tablename__ = 'update_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    
    request_type = db.Column(db.String(20), nullable=False)  # 'update' veya 'delete'
    request_data = db.Column(db.Text)  # JSON formatında güncelleme verileri
    reason = db.Column(db.Text)  # Talep nedeni
    
    status = db.Column(db.String(20), default='Bekliyor')  # Bekliyor, Onaylandı, Reddedildi
    admin_note = db.Column(db.Text)  # Admin'in notu
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime)
    processed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return f'<UpdateRequest {self.id} - {self.request_type}>'


class SystemLog(db.Model):
    """Gelişmiş Sistem Log Modeli"""
    __tablename__ = 'system_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(100), nullable=False, index=True)
    action_type = db.Column(db.String(50), index=True)  # login, logout, create, update, delete, view
    details = db.Column(db.Text)
    ip_address = db.Column(db.String(50), index=True)
    user_agent = db.Column(db.String(500))  # Tam user agent string
    device_type = db.Column(db.String(50))  # Desktop, Mobile, Tablet
    browser = db.Column(db.String(50))  # Chrome, Firefox, Safari, etc.
    os = db.Column(db.String(50))  # Windows, MacOS, Linux, Android, iOS
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # İlişki
    user = db.relationship('User', foreign_keys=[user_id], backref='logs')
    
    def get_device_info(self):
        """Cihaz bilgilerini dict olarak döndür"""
        return {
            'device_type': self.device_type or 'Unknown',
            'browser': self.browser or 'Unknown',
            'os': self.os or 'Unknown'
        }
    
    def __repr__(self):
        return f'<Log {self.id} - {self.action} by User {self.user_id}>'

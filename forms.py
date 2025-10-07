from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, IntegerField, TextAreaField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional, NumberRange
from models import User

class LoginForm(FlaskForm):
    """Giriş formu"""
    username = StringField('Kullanıcı Adı', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Şifre', validators=[DataRequired()])
    remember_me = BooleanField('Beni Hatırla')


class UserCreateForm(FlaskForm):
    """Kullanıcı oluşturma formu"""
    username = StringField('Kullanıcı Adı', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('E-posta', validators=[DataRequired(), Email()])
    full_name = StringField('Ad Soyad', validators=[DataRequired(), Length(max=150)])
    password = PasswordField('Şifre', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Şifre Tekrar', validators=[DataRequired(), EqualTo('password', message='Şifreler eşleşmiyor')])
    is_admin = BooleanField('Yönetici')
    is_active = BooleanField('Aktif', default=True)
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Bu kullanıcı adı zaten kullanımda.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Bu e-posta adresi zaten kullanımda.')


class UserEditForm(FlaskForm):
    """Kullanıcı düzenleme formu"""
    username = StringField('Kullanıcı Adı', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('E-posta', validators=[DataRequired(), Email()])
    full_name = StringField('Ad Soyad', validators=[DataRequired(), Length(max=150)])
    password = PasswordField('Yeni Şifre (boş bırakılabilir)', validators=[Optional(), Length(min=6)])
    password2 = PasswordField('Şifre Tekrar', validators=[EqualTo('password', message='Şifreler eşleşmiyor')])
    is_admin = BooleanField('Yönetici')
    is_active = BooleanField('Aktif')


class CountryForm(FlaskForm):
    """Ülke formu"""
    name = StringField('Ülke Adı', validators=[DataRequired(), Length(max=100)])
    code = StringField('Ülke Kodu (ISO)', validators=[DataRequired(), Length(min=2, max=3)])
    flag_emoji = StringField('Bayrak Emoji', validators=[Optional(), Length(max=10)])
    is_active = BooleanField('Aktif', default=True)
    office_required = BooleanField('Ofis Seçimi Zorunlu', default=False)


class QuotaForm(FlaskForm):
    """Kota formu"""
    country_id = SelectField('Ülke', coerce=int, validators=[DataRequired()])
    quota_limit = IntegerField('Kota Limiti', validators=[DataRequired(), NumberRange(min=1, message='Kota limiti 1 veya daha büyük olmalı')], render_kw={'min': 1})


class AppointmentForm(FlaskForm):
    """Randevu talebi formu - Dinamik alanlar için minimal validation"""
    country_id = SelectField('Ülke', coerce=int, validators=[DataRequired()])
    
    # Zorunlu alanlar (tüm ülkeler için)
    applicant_name = StringField('Ad', validators=[DataRequired(), Length(max=150)])
    applicant_surname = StringField('Soyad', validators=[DataRequired(), Length(max=150)])
    passport_number = StringField('Pasaport No', validators=[DataRequired(), Length(max=50)])
    
    # Ofis seçimi (ülkeye göre zorunlu/opsiyonel)
    office = SelectField('Ofis', validators=[Optional()], choices=[])
    
    # Dinamik alanlar (ülkeye göre zorunlu/opsiyonel)
    birth_date = DateField('Doğum Tarihi', validators=[Optional()])
    phone = StringField('Telefon', validators=[Optional(), Length(max=20)])
    email = StringField('E-posta', validators=[Optional(), Email()])
    passport_issue_date = DateField('Pasaport Düzenleme Tarihi', validators=[Optional()])
    passport_expiry_date = DateField('Pasaport Geçerlilik Tarihi', validators=[Optional()])
    nationality = StringField('Uyruk', validators=[Optional(), Length(max=100)])
    travel_date = DateField('Seyahat Tarihi', validators=[Optional()])
    preferred_date = DateField('Tercih Edilen Randevu Tarihi (Başlangıç)', validators=[Optional()])
    preferred_date_end = DateField('Tercih Edilen Randevu Tarihi (Bitiş)', validators=[Optional()])
    
    # Ek bilgiler
    address = TextAreaField('Adres', validators=[Optional()])
    visa_type = StringField('Vize Türü', validators=[Optional(), Length(max=100)])
    notes = TextAreaField('Notlar', validators=[Optional()])


class UpdateRequestForm(FlaskForm):
    """Güncelleme/Silme talep formu"""
    reason = TextAreaField('Talep Nedeni', validators=[DataRequired()])


class AdminNoteForm(FlaskForm):
    """Admin not formu"""
    admin_note = TextAreaField('Yönetici Notu', validators=[Optional()])

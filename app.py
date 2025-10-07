from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
import os

from config import Config
from models import db, User, Country, UserCountryQuota, Appointment, UpdateRequest
from forms import (LoginForm, UserCreateForm, UserEditForm, CountryForm,
                   QuotaForm, AppointmentForm, UpdateRequestForm)
from utils import get_dashboard_stats, log_action, send_admin_notification, send_new_user_credentials
from sqlalchemy import or_, and_

app = Flask(__name__)
app.config.from_object(Config)

# Extensions
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Bu sayfaya erişmek için giriş yapmalısınız.'
login_manager.login_message_category = 'warning'

# Railway için otomatik veritabanı kurulumu
def init_database():
    """Veritabanını başlat (Railway için) - Mevcut verileri korur"""
    try:
        with app.app_context():
            # Sadece eksik tabloları oluştur (mevcut verileri silmez)
            db.create_all()
            print("✅ Veritabanı tabloları kontrol edildi")
            
            # Admin kullanıcısı kontrolü - sadece yoksa oluştur
            admin_username = app.config['ADMIN_USERNAME']
            admin = User.query.filter_by(username=admin_username).first()
            
            if not admin:
                admin = User(
                    username=admin_username,
                    email=app.config['ADMIN_EMAIL'],
                    full_name='Sistem Yöneticisi',
                    is_admin=True,
                    is_active=True
                )
                admin.set_password(app.config['ADMIN_PASSWORD'])
                db.session.add(admin)
                db.session.commit()
                print(f"✅ Admin kullanıcısı oluşturuldu: {admin_username}")
            else:
                print(f"ℹ️  Admin kullanıcısı zaten mevcut: {admin_username}")
            
            # Ülke kontrolü - sadece boşsa örnek ekle
            country_count = Country.query.count()
            if country_count == 0:
                sample_countries = [
                    {'name': 'Amerika Birleşik Devletleri', 'code': 'USA', 'flag_emoji': '🇺🇸'},
                    {'name': 'İngiltere', 'code': 'GBR', 'flag_emoji': '🇬🇧'},
                    {'name': 'Almanya', 'code': 'DEU', 'flag_emoji': '🇩🇪'},
                    {'name': 'Fransa', 'code': 'FRA', 'flag_emoji': '🇫🇷'},
                    {'name': 'İtalya', 'code': 'ITA', 'flag_emoji': '🇮🇹'},
                    {'name': 'İspanya', 'code': 'ESP', 'flag_emoji': '🇪🇸'},
                    {'name': 'Kanada', 'code': 'CAN', 'flag_emoji': '🇨🇦'},
                    {'name': 'Avustralya', 'code': 'AUS', 'flag_emoji': '🇦🇺'},
                    {'name': 'Japonya', 'code': 'JPN', 'flag_emoji': '🇯🇵'},
                    {'name': 'Güney Kore', 'code': 'KOR', 'flag_emoji': '🇰🇷'},
                ]
                for country_data in sample_countries:
                    country = Country(**country_data)
                    db.session.add(country)
                db.session.commit()
                print(f"✅ {len(sample_countries)} örnek ülke eklendi")
            else:
                print(f"ℹ️  Veritabanında {country_count} ülke mevcut, yeni ülke eklenmedi")
            
            # Kullanıcı sayısı
            user_count = User.query.count()
            appointment_count = Appointment.query.count()
            print(f"ℹ️  Toplam kullanıcı: {user_count}")
            print(f"ℹ️  Toplam randevu: {appointment_count}")
            print("✅ Veritabanı hazır! (Mevcut veriler korundu)")
    except Exception as e:
        print(f"⚠️ Veritabanı kurulum hatası: {e}")
        import traceback
        traceback.print_exc()

# Railway deployment için veritabanını başlat
if os.environ.get('RAILWAY_ENVIRONMENT'):
    print("🚀 Railway ortamı algılandı, veritabanı kontrol ediliyor...")
    init_database()
else:
    print("💻 Local development ortamı")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Context processor
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}


# ============================================================================
# AUTH ROUTES
# ============================================================================

@app.route('/')
def index():
    """Ana sayfa - Dashboard'a yönlendir"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Giriş sayfası"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user is None or not user.check_password(form.password.data):
            flash('Geçersiz kullanıcı adı veya şifre.', 'danger')
            return redirect(url_for('login'))
        
        if not user.is_active:
            flash('Hesabınız devre dışı bırakılmış. Lütfen yöneticinize başvurun.', 'warning')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        log_action(user.id, 'login', ip_address=request.remote_addr)
        
        flash(f'Hoş geldiniz, {user.full_name}!', 'success')
        
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('dashboard')
        return redirect(next_page)
    
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """Çıkış"""
    log_action(current_user.id, 'logout', ip_address=request.remote_addr)
    logout_user()
    flash('Başarıyla çıkış yaptınız.', 'info')
    return redirect(url_for('login'))


# ============================================================================
# DASHBOARD
# ============================================================================

@app.route('/dashboard')
@login_required
def dashboard():
    """Ana panel"""
    stats = get_dashboard_stats(current_user)
    
    if current_user.is_admin:
        # Admin dashboard
        recent_appointments = Appointment.query.order_by(
            Appointment.created_at.desc()
        ).limit(10).all()
        
        pending_requests = UpdateRequest.query.filter_by(
            status='Bekliyor'
        ).count()
        
        return render_template('admin/dashboard.html', 
                             stats=stats, 
                             recent_appointments=recent_appointments,
                             pending_requests=pending_requests)
    else:
        # User dashboard
        recent_appointments = Appointment.query.filter_by(
            user_id=current_user.id
        ).order_by(Appointment.created_at.desc()).limit(10).all()
        
        # Kullanıcının kotaları
        quotas = UserCountryQuota.query.filter_by(user_id=current_user.id).all()
        quota_info = []
        for quota in quotas:
            used = current_user.get_used_quota_for_country(quota.country_id)
            quota_info.append({
                'country': quota.country,
                'limit': quota.quota_limit,
                'used': used,
                'remaining': quota.quota_limit - used
            })
        
        return render_template('user/dashboard.html', 
                             stats=stats,
                             recent_appointments=recent_appointments,
                             quota_info=quota_info)


# ============================================================================
# ADMIN - USER MANAGEMENT
# ============================================================================

@app.route('/admin/users')
@login_required
def admin_users():
    """Gelişmiş filtreleme ile kullanıcı listesi"""
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok.', 'danger')
        return redirect(url_for('dashboard'))

    page = request.args.get('page', 1, type=int)
    per_page_default = app.config.get('ITEMS_PER_PAGE', 10)
    per_page = request.args.get('per_page', per_page_default, type=int)
    per_page_choices = [10, 25, 50, 100]
    if per_page not in per_page_choices:
        per_page = per_page_default

    search = (request.args.get('q') or '').strip()
    role = request.args.get('role', 'all')  # user, admin, all
    status = request.args.get('status', 'all')  # all, active, passive
    sort = request.args.get('sort', 'newest')  # newest, oldest, name

    query = User.query

    if role == 'user':
        query = query.filter_by(is_admin=False)
    elif role == 'admin':
        query = query.filter_by(is_admin=True)

    if status == 'active':
        query = query.filter_by(is_active=True)
    elif status == 'passive':
        query = query.filter_by(is_active=False)

    if search:
        like = f"%{search}%"
        query = query.filter(
            or_(
                User.username.ilike(like),
                User.full_name.ilike(like),
                User.email.ilike(like)
            )
        )

    base_query = query

    filtered_admins = base_query.filter_by(is_admin=True).count()
    filtered_users = base_query.filter_by(is_admin=False).count()

    if sort == 'oldest':
        query = base_query.order_by(User.created_at.asc())
    elif sort == 'name':
        query = base_query.order_by(User.full_name.asc())
    else:
        query = base_query.order_by(User.created_at.desc())

    users = query.paginate(page=page, per_page=per_page, error_out=False)

    filters = {
        'q': search,
        'role': role,
        'status': status,
        'sort': sort,
        'per_page': per_page
    }

    stats = {
        'total': users.total,
        'active': base_query.filter_by(is_active=True).count() if status == 'all' else None,
        'passive': base_query.filter_by(is_active=False).count() if status == 'all' else None
    }

    return render_template('admin/users.html',
                           users=users,
                           filters=filters,
                           per_page_choices=per_page_choices,
                           stats=stats,
                           filtered_admins=filtered_admins,
                           filtered_users=filtered_users)


@app.route('/admin/users/create', methods=['GET', 'POST'])
@login_required
def admin_user_create():
    """Kullanıcı oluştur"""
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok.', 'danger')
        return redirect(url_for('dashboard'))
    
    form = UserCreateForm()
    if form.validate_on_submit():
        try:
            # Şifreyi sakla (mail göndermek için)
            plain_password = form.password.data
            
            user = User(
                username=form.username.data,
                email=form.email.data,
                full_name=form.full_name.data,
                is_admin=form.is_admin.data,
                is_active=form.is_active.data
            )
            user.set_password(plain_password)
            
            db.session.add(user)
            db.session.commit()
            
            log_action(current_user.id, 'create_user', 
                      details=f'Yeni kullanıcı oluşturuldu: {user.username}',
                      ip_address=request.remote_addr)
            
            # Kullanıcıya giriş bilgilerini mail ile gönder
            mail_sent = False
            mail_error = None
            try:
                mail_sent = send_new_user_credentials(
                    user_email=user.email,
                    username=user.username,
                    password=plain_password,
                    full_name=user.full_name
                )
            except Exception as mail_ex:
                mail_error = str(mail_ex)
                print(f"❌ Mail gönderme hatası: {mail_ex}")
                import traceback
                traceback.print_exc()
            
            # Kullanıcıya bilgi ver
            if mail_sent:
                flash(f'✅ Kullanıcı "{user.username}" başarıyla oluşturuldu. Giriş bilgileri e-posta ile gönderildi.', 'success')
            else:
                flash(f'✅ Kullanıcı "{user.username}" başarıyla oluşturuldu.', 'success')
                
                # Detaylı hata mesajı
                if mail_error:
                    if 'Authentication' in mail_error or '535' in mail_error:
                        flash('⚠️ E-posta gönderilemedi: Gmail kimlik doğrulama hatası. Lütfen Gmail ayarlarınızı kontrol edin.', 'danger')
                    elif 'Connection' in mail_error or 'timeout' in mail_error:
                        flash('⚠️ E-posta gönderilemedi: Mail sunucusuna bağlanılamadı. İnternet bağlantınızı kontrol edin.', 'danger')
                    else:
                        flash(f'⚠️ E-posta gönderilemedi: {mail_error}', 'danger')
                else:
                    flash('⚠️ E-posta gönderilemedi: Bilinmeyen hata.', 'warning')
                
                # Şifre bilgisi - Önemli!
                flash(f'🔑 ÖNEMLI: Kullanıcıya aşağıdaki şifresini manuel olarak iletin:', 'info')
                flash(f'Şifre: {plain_password}', 'info')
            
            return redirect(url_for('admin_user_edit', user_id=user.id))
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Kullanıcı oluşturma hatası: {e}")
            import traceback
            traceback.print_exc()
            flash(f'Kullanıcı oluşturulurken bir hata oluştu: {str(e)}', 'danger')
            return render_template('admin/user_form.html', form=form, user=None, title='Yeni Kullanıcı')
    
    return render_template('admin/user_form.html', form=form, user=None, title='Yeni Kullanıcı')


@app.route('/admin/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_user_edit(user_id):
    """Kullanıcı düzenle"""
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok.', 'danger')
        return redirect(url_for('dashboard'))
    
    user = User.query.get_or_404(user_id)
    form = UserEditForm(obj=user)
    quota_form = QuotaForm()
    active_countries = Country.query.filter_by(is_active=True).order_by(Country.name.asc()).all()
    quota_form.country_id.choices = [
        (country.id, f"{country.flag_emoji + ' ' if country.flag_emoji else ''}{country.name}")
        for country in active_countries
    ]
    quotas = (UserCountryQuota.query
              .filter_by(user_id=user.id)
              .join(Country)
              .order_by(Country.name.asc())
              .all())
    open_quota_modal = request.args.get('modal') == 'quotas'
    
    if form.validate_on_submit():
        # Kullanıcı adı ve email benzersizlik kontrolü
        if form.username.data != user.username:
            existing = User.query.filter_by(username=form.username.data).first()
            if existing:
                flash('Bu kullanıcı adı zaten kullanımda.', 'danger')
                return render_template('admin/user_form.html', form=form, user=user,
                                     quota_form=quota_form, title='Kullanıcı Düzenle')
        
        if form.email.data != user.email:
            existing = User.query.filter_by(email=form.email.data).first()
            if existing:
                flash('Bu e-posta adresi zaten kullanımda.', 'danger')
                return render_template('admin/user_form.html', form=form, user=user,
                                     quota_form=quota_form, title='Kullanıcı Düzenle')
        
        user.username = form.username.data
        user.email = form.email.data
        user.full_name = form.full_name.data
        user.is_admin = form.is_admin.data
        user.is_active = form.is_active.data
        
        if form.password.data:
            user.set_password(form.password.data)
        
        db.session.commit()
        
        log_action(current_user.id, 'update_user',
                  details=f'Kullanıcı güncellendi: {user.username}',
                  ip_address=request.remote_addr)
        
        flash(f'Kullanıcı "{user.username}" başarıyla güncellendi.', 'success')
        return redirect(url_for('admin_users'))
    
    return render_template('admin/user_form.html', form=form, user=user,
                           quotas=quotas, quota_form=quota_form,
                           open_quota_modal=open_quota_modal,
                           title='Kullanıcı Düzenle')


@app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@login_required
def admin_user_delete(user_id):
    """Kullanıcı sil"""
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        return jsonify({'success': False, 'message': 'Kendi hesabınızı silemezsiniz'}), 400
    
    username = user.username
    db.session.delete(user)
    db.session.commit()
    
    log_action(current_user.id, 'delete_user',
              details=f'Kullanıcı silindi: {username}',
              ip_address=request.remote_addr)
    
    return jsonify({'success': True, 'message': f'Kullanıcı "{username}" silindi'})


# ============================================================================
# ADMIN - QUOTA MANAGEMENT
# ============================================================================

@app.route('/admin/users/<int:user_id>/quotas/add', methods=['POST'])
@login_required
def admin_quota_add(user_id):
    """Kullanıcıya kota ekle"""
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    user = User.query.get_or_404(user_id)
    if user.is_admin:
        return jsonify({'success': False, 'message': 'Yöneticilere kota atanamaz.'}), 400

    country_id = request.form.get('country_id', type=int)
    quota_limit = request.form.get('quota_limit', type=int)
    
    if country_id is None or quota_limit is None:
        return jsonify({'success': False, 'message': 'Eksik bilgi gönderildi.'}), 400

    country = Country.query.get(country_id)
    if country is None:
        return jsonify({'success': False, 'message': 'Geçersiz ülke seçimi.'}), 404

    if quota_limit <= 0:
        return jsonify({'success': False, 'message': 'Kota limiti 0 veya negatif olamaz.'}), 400
    
    # Mevcut kota var mı kontrol et
    existing = UserCountryQuota.query.filter_by(
        user_id=user_id, 
        country_id=country_id
    ).first()
    
    if existing:
        existing.quota_limit = quota_limit
        existing.updated_at = datetime.utcnow()
        message = 'Kota güncellendi'
    else:
        quota = UserCountryQuota(
            user_id=user_id,
            country_id=country_id,
            quota_limit=quota_limit
        )
        db.session.add(quota)
        message = 'Kota eklendi'
    
    db.session.commit()

    log_action(current_user.id, 'update_quota',
              details=f'{user.username} için {country.name} kotası: {quota_limit}',
              ip_address=request.remote_addr)
    
    updated_quotas = (UserCountryQuota.query
                      .filter_by(user_id=user.id)
                      .join(Country)
                      .order_by(Country.name.asc())
                      .all())
    table_html = render_template('admin/partials/quota_table.html', user=user, quotas=updated_quotas)

    return jsonify({'success': True, 'message': message, 'html': table_html})


@app.route('/admin/users/<int:user_id>/quotas/<int:quota_id>/delete', methods=['POST'])
@login_required
def admin_quota_delete(user_id, quota_id):
    """Kota sil"""
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    quota = UserCountryQuota.query.get_or_404(quota_id)
    
    if quota.user_id != user_id:
        return jsonify({'success': False, 'message': 'Geçersiz işlem'}), 400
    
    # Silmeden önce user ve country_id'yi al
    user = quota.user
    country_id = quota.country_id
    
    db.session.delete(quota)
    db.session.commit()
    
    log_action(current_user.id, 'delete_quota',
              details=f'Kota silindi: User {user_id}, Country {country_id}',
              ip_address=request.remote_addr)

    updated_quotas = (UserCountryQuota.query
                      .filter_by(user_id=user_id)
                      .join(Country)
                      .order_by(Country.name.asc())
                      .all())
    table_html = render_template('admin/partials/quota_table.html', user=user, quotas=updated_quotas)

    return jsonify({'success': True, 'message': 'Kota silindi', 'html': table_html})


# ============================================================================
# ADMIN - COUNTRY MANAGEMENT
# ============================================================================

@app.route('/admin/countries')
@login_required
def admin_countries():
    """Ülke listesi"""
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok.', 'danger')
        return redirect(url_for('dashboard'))
    
    countries = Country.query.order_by(Country.name).all()
    return render_template('admin/countries.html', countries=countries)


@app.route('/admin/countries/create', methods=['GET', 'POST'])
@login_required
def admin_country_create():
    """Ülke oluştur"""
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok.', 'danger')
        return redirect(url_for('dashboard'))
    
    form = CountryForm()
    if form.validate_on_submit():
        country = Country(
            name=form.name.data,
            code=form.code.data.upper(),
            flag_emoji=form.flag_emoji.data,
            is_active=form.is_active.data,
            office_required=form.office_required.data,
            required_fields=request.form.get('required_fields', '{}')
        )
        
        db.session.add(country)
        db.session.commit()
        
        log_action(current_user.id, 'create_country',
                  details=f'Yeni ülke eklendi: {country.name}',
                  ip_address=request.remote_addr)
        
        flash(f'Ülke "{country.name}" başarıyla eklendi.', 'success')
        return redirect(url_for('admin_countries'))
    
    return render_template('admin/country_form.html', form=form, title='Yeni Ülke')


@app.route('/admin/countries/<int:country_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_country_edit(country_id):
    """Ülke düzenle"""
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok.', 'danger')
        return redirect(url_for('dashboard'))
    
    country = Country.query.get_or_404(country_id)
    form = CountryForm(obj=country)
    
    if form.validate_on_submit():
        country.name = form.name.data
        country.code = form.code.data.upper()
        country.flag_emoji = form.flag_emoji.data
        country.is_active = form.is_active.data
        country.office_required = form.office_required.data
        country.required_fields = request.form.get('required_fields', '{}')
        
        db.session.commit()
        
        log_action(current_user.id, 'update_country',
                  details=f'Ülke güncellendi: {country.name}',
                  ip_address=request.remote_addr)
        
        flash(f'Ülke "{country.name}" başarıyla güncellendi.', 'success')
        return redirect(url_for('admin_countries'))
    
    return render_template('admin/country_form.html', form=form, country=country, 
                         title='Ülke Düzenle')


@app.route('/admin/countries/<int:country_id>/delete', methods=['POST'])
@login_required
def admin_country_delete(country_id):
    """Ülke sil"""
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    country = Country.query.get_or_404(country_id)
    
    # Bağlı randevu var mı kontrol et
    if country.appointments.count() > 0:
        return jsonify({
            'success': False, 
            'message': 'Bu ülkeye ait randevular var, silinemez'
        }), 400
    
    name = country.name
    db.session.delete(country)
    db.session.commit()
    
    log_action(current_user.id, 'delete_country',
              details=f'Ülke silindi: {name}',
              ip_address=request.remote_addr)
    
    return jsonify({'success': True, 'message': f'Ülke "{name}" silindi'})


# ============================================================================
# API - COUNTRY REQUIRED FIELDS
# ============================================================================

@app.route('/api/countries/<int:country_id>/required-fields', methods=['GET'])
@login_required
def api_country_required_fields(country_id):
    """Ülkenin zorunlu alanlarını döndür (JSON)"""
    country = Country.query.get_or_404(country_id)
    
    return jsonify({
        'success': True,
        'country_id': country.id,
        'country_name': country.name,
        'country_code': country.code,
        'required_fields': country.get_required_fields()
    })


@app.route('/api/user/quota-info', methods=['GET'])
@login_required
def api_user_quota_info():
    """Kullanıcının kota bilgilerini döndür (JSON)"""
    if current_user.is_admin:
        return jsonify({
            'success': False,
            'message': 'Bu API sadece danışman kullanıcılar içindir.'
        }), 403
    
    # Kullanıcının atanmış olduğu ülkeleri getir
    user_countries = UserCountryQuota.query.filter_by(user_id=current_user.id).all()
    
    countries_data = []
    for uc in user_countries:
        country = Country.query.get(uc.country_id)
        if country and country.is_active:
            # Kullanıcının bu ülke için oluşturduğu randevu sayısı
            used_quota = Appointment.query.filter_by(
                user_id=current_user.id,
                country_id=country.id
            ).count()
            
            remaining = uc.quota_limit - used_quota
            
            countries_data.append({
                'country_id': country.id,
                'country_name': country.name,
                'country_code': country.code,
                'quota_limit': uc.quota_limit,
                'used_quota': used_quota,
                'remaining_quota': remaining
            })
    
    return jsonify({
        'success': True,
        'countries': countries_data
    })


# ============================================================================
# ADMIN - APPOINTMENT MANAGEMENT (Rotalar app_routes.py'den import edilecek)
# ============================================================================


@app.route('/admin/appointments')
@login_required
def admin_appointments():
    """Randevu talepleri listesi (gelişmiş filtrelerle)"""
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok.', 'danger')
        return redirect(url_for('dashboard'))

    page = request.args.get('page', 1, type=int)
    per_page_default = app.config.get('ITEMS_PER_PAGE', 10)
    per_page = request.args.get('per_page', per_page_default, type=int)
    per_page_choices = [10, 25, 50, 100]
    if per_page not in per_page_choices:
        per_page = per_page_default

    search = (request.args.get('q') or '').strip()
    status = request.args.get('status', 'all')
    country_id = request.args.get('country_id', type=int)
    user_id = request.args.get('user_id', type=int)
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    sort = request.args.get('sort', 'newest')

    filters = []

    if search:
        like = f"%{search}%"
        filters.append(or_(
            Appointment.applicant_name.ilike(like),
            Appointment.applicant_surname.ilike(like),
            Appointment.passport_number.ilike(like),
            User.username.ilike(like),
            User.full_name.ilike(like)
        ))

    if user_id:
        filters.append(Appointment.user_id == user_id)

    if country_id:
        filters.append(Appointment.country_id == country_id)

    if date_from:
        try:
            start_date = datetime.strptime(date_from, '%Y-%m-%d')
            filters.append(Appointment.created_at >= start_date)
        except ValueError:
            flash('Başlangıç tarihi geçerli formatta değil (YYYY-AA-GG).', 'warning')

    if date_to:
        try:
            end_date = datetime.strptime(date_to, '%Y-%m-%d') + timedelta(days=1)
            filters.append(Appointment.created_at < end_date)
        except ValueError:
            flash('Bitiş tarihi geçerli formatta değil (YYYY-AA-GG).', 'warning')

    base_query = Appointment.query.join(User).join(Country)
    if filters:
        base_query = base_query.filter(and_(*filters))

    query = base_query

    if status != 'all':
        query = query.filter(Appointment.status == status)

    if sort == 'oldest':
        query = query.order_by(Appointment.created_at.asc())
    elif sort == 'updated':
        query = query.order_by(Appointment.updated_at.desc())
    elif sort == 'preferred':
        query = query.order_by(Appointment.preferred_date.asc())
    else:
        query = query.order_by(Appointment.created_at.desc())

    appointments = query.paginate(page=page, per_page=per_page, error_out=False)

    status_options = ['Bekleme', 'Süreç Başlatıldı', 'Tamamlandı', 'İptal']
    status_query = base_query.with_entities(Appointment.status, db.func.count(Appointment.id)).group_by(Appointment.status)
    status_counts = {option: 0 for option in status_options}
    for status_value, count in status_query:
        status_counts[status_value] = count

    countries = Country.query.order_by(Country.name.asc()).all()
    users_list = User.query.order_by(User.full_name.asc()).all()

    filters_payload = {
        'q': search,
        'status': status,
        'country_id': country_id if country_id else '',
        'user_id': user_id if user_id else '',
        'date_from': date_from or '',
        'date_to': date_to or '',
        'sort': sort,
        'per_page': per_page
    }

    return render_template('admin/appointments.html',
                           appointments=appointments,
                           countries=countries,
                           users=users_list,
                           status_options=status_options,
                           per_page_choices=per_page_choices,
                           status_counts=status_counts,
                           filters=filters_payload)


# ============================================================================
# ADMIN - APPOINTMENT ACTIONS (MODALLAR İÇİN)
# ============================================================================

@app.route('/admin/appointments/<int:apt_id>/details', methods=['GET'])
@login_required
def admin_appointment_details(apt_id):
    """Randevu detaylarını getir (Modal için)"""
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    appointment = Appointment.query.get_or_404(apt_id)
    
    return jsonify({
        'success': True,
        'appointment': {
            'id': appointment.id,
            'applicant_name': appointment.applicant_name,
            'applicant_surname': appointment.applicant_surname,
            'passport_number': appointment.passport_number,
            'birth_date': appointment.birth_date.strftime('%d.%m.%Y') if appointment.birth_date else None,
            'phone': appointment.phone,
            'email': appointment.email,
            'passport_issue_date': appointment.passport_issue_date.strftime('%d.%m.%Y') if appointment.passport_issue_date else None,
            'passport_expiry_date': appointment.passport_expiry_date.strftime('%d.%m.%Y') if appointment.passport_expiry_date else None,
            'nationality': appointment.nationality,
            'travel_date': appointment.travel_date.strftime('%d.%m.%Y') if appointment.travel_date else None,
            'address': appointment.address,
            'preferred_date': appointment.preferred_date.strftime('%Y-%m-%d') if appointment.preferred_date else None,
            'preferred_date_end': appointment.preferred_date_end.strftime('%Y-%m-%d') if appointment.preferred_date_end else None,
            'visa_type': appointment.visa_type,
            'notes': appointment.notes,
            'status': appointment.status,
            'created_at': appointment.created_at.strftime('%d.%m.%Y %H:%M'),
            'updated_at': appointment.updated_at.strftime('%d.%m.%Y %H:%M'),
            'processed_at': appointment.processed_at.strftime('%d.%m.%Y %H:%M') if appointment.processed_at else None,
            'country': {
                'id': appointment.country.id,
                'name': appointment.country.name,
                'code': appointment.country.code,
                'flag_emoji': appointment.country.flag_emoji
            },
            'user': {
                'id': appointment.user.id,
                'username': appointment.user.username,
                'full_name': appointment.user.full_name,
                'email': appointment.user.email
            }
        }
    })

@app.route('/admin/appointments/<int:apt_id>/update-status', methods=['POST'])
@login_required
def admin_appointment_update_status(apt_id):
    """Randevu durumunu güncelle"""
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    appointment = Appointment.query.get_or_404(apt_id)
    
    new_status = request.form.get('status')
    admin_note = request.form.get('admin_note', '').strip()
    
    valid_statuses = ['Bekleme', 'Süreç Başlatıldı', 'Tamamlandı', 'İptal']
    if new_status not in valid_statuses:
        return jsonify({'success': False, 'message': 'Geçersiz durum'}), 400
    
    old_status = appointment.status
    appointment.status = new_status
    appointment.updated_at = datetime.utcnow()
    
    if new_status in ['Tamamlandı', 'İptal', 'Süreç Başlatıldı']:
        appointment.processed_at = datetime.utcnow()
    
    db.session.commit()
    
    log_action(current_user.id, 'update_appointment_status',
              details=f'Randevu #{apt_id} durumu: {old_status} → {new_status}. Not: {admin_note}',
              ip_address=request.remote_addr)
    
    return jsonify({
        'success': True,
        'message': f'Randevu durumu "{new_status}" olarak güncellendi',
        'appointment': {
            'id': appointment.id,
            'status': appointment.status,
            'updated_at': appointment.updated_at.strftime('%d.%m.%Y %H:%M')
        }
    })

@app.route('/admin/appointments/<int:apt_id>/update', methods=['POST'])
@login_required
def admin_appointment_update(apt_id):
    """Randevu bilgilerini güncelle"""
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    appointment = Appointment.query.get_or_404(apt_id)
    
    # Form verilerini al
    appointment.applicant_name = request.form.get('applicant_name', '').strip()
    appointment.applicant_surname = request.form.get('applicant_surname', '').strip()
    appointment.passport_number = request.form.get('passport_number', '').strip()
    
    # Zorunlu alanlar kontrolü
    if not all([appointment.applicant_name, appointment.applicant_surname, appointment.passport_number]):
        return jsonify({'success': False, 'message': 'Ad, soyad ve pasaport numarası zorunludur'}), 400
    
    # Tarih alanlarını parse et
    def parse_date(date_str):
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return None
    
    appointment.birth_date = parse_date(request.form.get('birth_date'))
    appointment.phone = request.form.get('phone', '').strip() or None
    appointment.email = request.form.get('email', '').strip() or None
    appointment.passport_issue_date = parse_date(request.form.get('passport_issue_date'))
    appointment.passport_expiry_date = parse_date(request.form.get('passport_expiry_date'))
    appointment.nationality = request.form.get('nationality', '').strip() or None
    appointment.travel_date = parse_date(request.form.get('travel_date'))
    appointment.address = request.form.get('address', '').strip() or None
    appointment.preferred_date = parse_date(request.form.get('preferred_date'))
    appointment.preferred_date_end = parse_date(request.form.get('preferred_date_end'))
    appointment.visa_type = request.form.get('visa_type', '').strip() or None
    appointment.notes = request.form.get('notes', '').strip() or None
    
    appointment.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    log_action(current_user.id, 'admin_update_appointment',
              details=f'Randevu #{apt_id} bilgileri güncellendi',
              ip_address=request.remote_addr)
    
    return jsonify({
        'success': True,
        'message': 'Randevu bilgileri başarıyla güncellendi',
        'appointment': {
            'id': appointment.id,
            'applicant_name': appointment.applicant_name,
            'applicant_surname': appointment.applicant_surname,
            'updated_at': appointment.updated_at.strftime('%d.%m.%Y %H:%M')
        }
    })

# ============================================================================
# USER - APPOINTMENT MANAGEMENT
# ============================================================================


@app.route('/user/appointments')
@login_required
def user_appointments():
    """Kullanıcının tüm randevularının listesi"""
    if current_user.is_admin:
        flash('Yönetici hesapları kullanıcı randevu listesine erişemez.', 'warning')
        return redirect(url_for('admin_appointments'))

    status_filter = request.args.get('status', 'all')
    country_filter = request.args.get('country_id', type=int)

    status_options = ['Bekleme', 'Süreç Başlatıldı', 'Tamamlandı', 'İptal']

    query = Appointment.query.filter_by(user_id=current_user.id)
    if status_filter in status_options:
        query = query.filter(Appointment.status == status_filter)
    if country_filter:
        query = query.filter(Appointment.country_id == country_filter)

    appointments = query.order_by(Appointment.created_at.desc()).all()

    status_counts = {option: 0 for option in status_options}
    status_query = (Appointment.query
                    .with_entities(Appointment.status, db.func.count(Appointment.id))
                    .filter(Appointment.user_id == current_user.id)
                    .group_by(Appointment.status)
                    .all())
    for status_value, count in status_query:
        if status_value in status_counts:
            status_counts[status_value] = count

    assigned_countries = (Country.query
                          .join(UserCountryQuota, UserCountryQuota.country_id == Country.id)
                          .filter(UserCountryQuota.user_id == current_user.id)
                          .order_by(Country.name.asc())
                          .all())

    return render_template('user/appointments.html',
                           appointments=appointments,
                           status_options=status_options,
                           status_filter=status_filter,
                           country_filter=country_filter,
                           status_counts=status_counts,
                           assigned_countries=assigned_countries)


@app.route('/user/appointments/country/<int:country_id>', methods=['GET', 'POST'])
@login_required
def user_appointments_by_country(country_id):
    """Belirli bir ülke için randevu oluşturma ve listeleme"""
    if current_user.is_admin:
        flash('Yönetici hesapları bu sayfaya erişemez.', 'warning')
        return redirect(url_for('admin_appointments'))

    country = Country.query.get_or_404(country_id)
    quota = UserCountryQuota.query.filter_by(user_id=current_user.id, country_id=country.id).first()

    if quota is None:
        flash('Bu ülke için atanmış kotanız bulunmuyor.', 'danger')
        return redirect(url_for('dashboard'))

    form = AppointmentForm()
    form.country_id.choices = [(country.id, f"{country.flag_emoji + ' ' if country.flag_emoji else ''}{country.name}")]
    
    # Ofis seçeneklerini config'den al ve forma ekle
    from config import Config
    form.office.choices = [('', 'Seçiniz...')] + [(office, office) for office in Config.OFFICE_CHOICES]
    
    if request.method == 'GET':
        form.country_id.data = country.id

    used_quota = current_user.get_used_quota_for_country(country.id)
    remaining_quota = max(quota.quota_limit - used_quota, 0)

    if form.validate_on_submit():
        if remaining_quota <= 0:
            flash('Bu ülke için kota limitine ulaştınız.', 'danger')
        else:
            # Ofis kontrolü - eğer ülke için zorunluysa
            selected_office = form.office.data
            if country.office_required and not selected_office:
                flash('Bu ülke için ofis seçimi zorunludur.', 'danger')
                return render_template('user/appointments_country.html',
                                     country=country,
                                     quota=quota,
                                     used_quota=used_quota,
                                     remaining_quota=remaining_quota,
                                     appointments=[],
                                     form=form)
            
            # Yardımcı fonksiyon - string tarih verisini Date objesine çevir
            def parse_date(date_str):
                if not date_str:
                    return None
                try:
                    from datetime import datetime
                    return datetime.strptime(date_str, '%Y-%m-%d').date()
                except (ValueError, TypeError):
                    return None
            
            appointment = Appointment(
                user_id=current_user.id,
                country_id=country.id,
                applicant_name=form.applicant_name.data,
                applicant_surname=form.applicant_surname.data,
                passport_number=form.passport_number.data,
                # Ofis bilgisi (yeni)
                office=selected_office if selected_office else None,
                # Dinamik alanlar
                birth_date=parse_date(request.form.get('birth_date')),
                phone=request.form.get('phone') or None,
                email=request.form.get('email') or None,
                passport_issue_date=parse_date(request.form.get('passport_issue_date')),
                passport_expiry_date=parse_date(request.form.get('passport_expiry_date')),
                nationality=request.form.get('nationality') or None,
                travel_date=parse_date(request.form.get('travel_date')),
                preferred_date=parse_date(request.form.get('preferred_date')),
                preferred_date_end=parse_date(request.form.get('preferred_date_end')),
                # Sabit alanlar
                address=form.address.data,
                visa_type=form.visa_type.data,
                notes=form.notes.data
            )
            db.session.add(appointment)
            db.session.commit()

            log_action(current_user.id, 'create_appointment',
                      details=f'{country.name} için yeni randevu talebi (#{appointment.id})',
                      ip_address=request.remote_addr)

            # Yöneticiye mail bildirimi gönder
            try:
                subject = "Yeni Randevu Talebi"
                message = f"""
                <p><strong>Danışman:</strong> {current_user.full_name} (@{current_user.username})</p>
                <p><strong>Ülke:</strong> {country.flag_emoji} {country.name}</p>
                <p><strong>Başvuran:</strong> {appointment.applicant_name} {appointment.applicant_surname}</p>
                <p><strong>Pasaport No:</strong> {appointment.passport_number}</p>
                <p><strong>Randevu ID:</strong> #{appointment.id}</p>
                <p><strong>Durum:</strong> <span style="color: #f59e0b;">Bekleme</span></p>
                """
                send_admin_notification(subject, message, action_type='info')
            except Exception as e:
                print(f"Mail gönderme hatası: {e}")

            flash('Randevu talebiniz kaydedildi.', 'success')
            return redirect(url_for('user_appointments_by_country', country_id=country.id))

    appointments = (Appointment.query
                    .filter_by(user_id=current_user.id, country_id=country.id)
                    .order_by(Appointment.created_at.desc())
                    .all())

    used_quota = current_user.get_used_quota_for_country(country.id)
    remaining_quota = max(quota.quota_limit - used_quota, 0)

    return render_template('user/appointments_country.html',
                           country=country,
                           quota=quota,
                           used_quota=used_quota,
                           remaining_quota=remaining_quota,
                           appointments=appointments,
                           form=form)


@app.route('/user/appointments/<int:apt_id>/edit', methods=['GET', 'POST'])
@login_required
def user_appointment_edit(apt_id):
    """Kullanıcı randevu düzenleme"""
    appointment = Appointment.query.get_or_404(apt_id)

    if appointment.user_id != current_user.id:
        flash('Bu randevuyu düzenleme yetkiniz yok.', 'danger')
        return redirect(url_for('user_appointments'))

    if not appointment.can_edit():
        flash('Bu randevu düzenlenemez. Güncelleme talebi oluşturabilirsiniz.', 'warning')
        return redirect(url_for('user_appointment_update_request', apt_id=apt_id))

    form = AppointmentForm(obj=appointment)
    form.country_id.choices = [(appointment.country_id, appointment.country.name)]
    form.country_id.data = appointment.country_id

    if form.validate_on_submit():
        appointment.applicant_name = form.applicant_name.data
        appointment.applicant_surname = form.applicant_surname.data
        appointment.passport_number = form.passport_number.data
        appointment.birth_date = form.birth_date.data
        appointment.phone = form.phone.data
        appointment.email = form.email.data
        appointment.address = form.address.data
        appointment.preferred_date = form.preferred_date.data
        appointment.visa_type = form.visa_type.data
        appointment.notes = form.notes.data

        db.session.commit()

        log_action(current_user.id, 'update_appointment',
                  details=f'Randevu güncellendi #{appointment.id}',
                  ip_address=request.remote_addr)

        flash('Randevu bilgileri güncellendi.', 'success')
        return redirect(url_for('user_appointments_by_country', country_id=appointment.country_id))

    return render_template('user/appointment_form.html',
                           form=form,
                           appointment=appointment,
                           mode='edit')


@app.route('/user/appointments/<int:apt_id>/delete', methods=['POST'])
@login_required
def user_appointment_delete(apt_id):
    """Kullanıcı randevu silme"""
    appointment = Appointment.query.get_or_404(apt_id)

    if appointment.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Bu işlem için yetkiniz yok.'}), 403

    if not appointment.can_delete():
        return jsonify({'success': False, 'message': 'Bu randevu mevcut durumu nedeniyle silinemez.'}), 400

    db.session.delete(appointment)
    db.session.commit()

    log_action(current_user.id, 'delete_appointment',
              details=f'Randevu silindi #{appointment.id}',
              ip_address=request.remote_addr)

    return jsonify({'success': True, 'message': 'Randevu silindi.'})


@app.route('/user/appointments/<int:apt_id>/update-request', methods=['GET', 'POST'])
@login_required
def user_appointment_update_request(apt_id):
    """Düzenlenemeyen randevular için güncelleme talebi oluştur"""
    appointment = Appointment.query.get_or_404(apt_id)

    if appointment.user_id != current_user.id:
        flash('Bu randevu için talep oluşturma yetkiniz yok.', 'danger')
        return redirect(url_for('user_appointments'))

    if appointment.can_edit():
        flash('Bu randevuyu doğrudan düzenleyebilirsiniz.', 'info')
        return redirect(url_for('user_appointment_edit', apt_id=apt_id))

    existing_request = (UpdateRequest.query
                        .filter_by(user_id=current_user.id,
                                   appointment_id=apt_id,
                                   status='Bekliyor')
                        .first())
    if existing_request:
        flash('Bu randevu için bekleyen bir talebiniz zaten var.', 'info')
        return redirect(url_for('user_appointments'))

    form = UpdateRequestForm()

    if form.validate_on_submit():
        update_request = UpdateRequest(
            user_id=current_user.id,
            appointment_id=apt_id,
            request_type='update',
            request_data=None,
            reason=form.reason.data
        )
        db.session.add(update_request)
        db.session.commit()

        log_action(current_user.id, 'create_update_request',
                  details=f'Randevu #{apt_id} için güncelleme talebi',
                  ip_address=request.remote_addr)

        # Yöneticiye mail bildirimi gönder
        try:
            subject = "Randevu Güncelleme Talebi"
            message = f"""
            <p><strong>Danışman:</strong> {current_user.full_name} (@{current_user.username})</p>
            <p><strong>Talep Tipi:</strong> <span style="color: #f59e0b;">Güncelleme</span></p>
            <p><strong>Randevu ID:</strong> #{appointment.id}</p>
            <p><strong>Başvuran:</strong> {appointment.applicant_name} {appointment.applicant_surname}</p>
            <p><strong>Ülke:</strong> {appointment.country.flag_emoji} {appointment.country.name}</p>
            <p><strong>Gerekçe:</strong> {update_request.reason}</p>
            """
            send_admin_notification(subject, message, action_type='warning')
        except Exception as e:
            print(f"Mail gönderme hatası: {e}")

        flash('Güncelleme talebiniz iletildi. Yönetici en kısa sürede değerlendirecektir.', 'success')
        return redirect(url_for('user_appointments'))

    return render_template('user/appointment_request.html',
                           form=form,
                           appointment=appointment)

@app.route('/user/appointments/<int:apt_id>/delete-request', methods=['POST'])
@login_required
def user_appointment_delete_request(apt_id):
    """Silme talebi oluştur"""
    appointment = Appointment.query.get_or_404(apt_id)
    
    if appointment.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Bu randevu için talep oluşturma yetkiniz yok'}), 403
    
    if appointment.can_delete():
        return jsonify({'success': False, 'message': 'Bu randevuyu doğrudan silebilirsiniz'}), 400
    
    # Bekleyen talep var mı kontrol et
    existing_request = (UpdateRequest.query
                        .filter_by(user_id=current_user.id,
                                   appointment_id=apt_id,
                                   request_type='delete',
                                   status='Bekliyor')
                        .first())
    if existing_request:
        return jsonify({'success': False, 'message': 'Bu randevu için bekleyen bir silme talebiniz zaten var'}), 400
    
    reason = request.form.get('reason', '').strip()
    if not reason:
        return jsonify({'success': False, 'message': 'Silme nedeni gereklidir'}), 400
    
    delete_request = UpdateRequest(
        user_id=current_user.id,
        appointment_id=apt_id,
        request_type='delete',
        request_data=None,
        reason=reason
    )
    db.session.add(delete_request)
    db.session.commit()
    
    log_action(current_user.id, 'create_delete_request',
              details=f'Randevu #{apt_id} için silme talebi: {reason}',
              ip_address=request.remote_addr)
    
    # Yöneticiye mail bildirimi gönder
    try:
        subject = "Randevu Silme Talebi"
        message = f"""
        <p><strong>Danışman:</strong> {current_user.full_name} (@{current_user.username})</p>
        <p><strong>Talep Tipi:</strong> <span style="color: #dc3545;">Silme</span></p>
        <p><strong>Randevu ID:</strong> #{appointment.id}</p>
        <p><strong>Başvuran:</strong> {appointment.applicant_name} {appointment.applicant_surname}</p>
        <p><strong>Ülke:</strong> {appointment.country.flag_emoji} {appointment.country.name}</p>
        <p><strong>Gerekçe:</strong> {reason}</p>
        """
        send_admin_notification(subject, message, action_type='danger')
    except Exception as e:
        print(f"Mail gönderme hatası: {e}")
    
    return jsonify({
        'success': True,
        'message': 'Silme talebiniz gönderildi. Yönetici en kısa sürede değerlendirecektir.'
    })

# ============================================================================
# ADMIN - REQUEST MANAGEMENT
# ============================================================================

@app.route('/admin/requests')
@login_required
def admin_requests():
    """Güncelleme/Silme talepleri listesi"""
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok.', 'danger')
        return redirect(url_for('dashboard'))
    
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    status_filter = request.args.get('status', 'all')
    type_filter = request.args.get('request_type', 'all')
    
    query = UpdateRequest.query
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    if type_filter != 'all':
        query = query.filter_by(request_type=type_filter)
    
    requests_paginated = query.order_by(UpdateRequest.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    # İstatistikler
    pending_count = UpdateRequest.query.filter_by(status='Bekliyor').count()
    approved_count = UpdateRequest.query.filter_by(status='Onaylandı').count()
    rejected_count = UpdateRequest.query.filter_by(status='Reddedildi').count()
    
    return render_template('admin/requests.html',
                         requests=requests_paginated,
                         status_filter=status_filter,
                         type_filter=type_filter,
                         pending_count=pending_count,
                         approved_count=approved_count,
                         rejected_count=rejected_count)

@app.route('/admin/requests/<int:req_id>/details', methods=['GET'])
@login_required
def admin_request_details(req_id):
    """Talep detaylarını getir"""
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    req = UpdateRequest.query.get_or_404(req_id)
    
    return jsonify({
        'success': True,
        'request': {
            'id': req.id,
            'request_type': req.request_type,
            'reason': req.reason,
            'status': req.status,
            'admin_note': req.admin_note,
            'created_at': req.created_at.strftime('%d.%m.%Y %H:%M'),
            'appointment': {
                'id': req.appointment.id,
                'applicant_name': req.appointment.applicant_name,
                'applicant_surname': req.appointment.applicant_surname,
                'country': req.appointment.country.name
            },
            'user': {
                'full_name': req.user.full_name,
                'username': req.user.username
            }
        }
    })

@app.route('/admin/requests/<int:req_id>/approve', methods=['POST'])
@login_required
def admin_request_approve(req_id):
    """Talebi onayla ve işlemi gerçekleştir"""
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    req = UpdateRequest.query.get_or_404(req_id)
    
    if req.status != 'Bekliyor':
        return jsonify({'success': False, 'message': 'Bu talep zaten işlenmiş'}), 400
    
    admin_note = request.form.get('admin_note', '').strip()
    
    # Talebi onayla
    req.status = 'Onaylandı'
    req.admin_note = admin_note if admin_note else None
    req.processed_at = datetime.utcnow()
    req.processed_by = current_user.id
    
    # Talep tipine göre işlem yap
    if req.request_type == 'delete':
        # Randevuyu sil
        appointment = req.appointment
        db.session.delete(appointment)
        log_action(current_user.id, 'approve_delete_request',
                  details=f'Randevu #{appointment.id} silme talebi onaylandı ve randevu silindi',
                  ip_address=request.remote_addr)
        message = 'Silme talebi onaylandı ve randevu silindi'
    else:
        # Güncelleme talebi için - şimdilik sadece onaylıyoruz
        # Gerçek güncellemeleri yapmak için request_data alanına güncelleme verileri eklenmeli
        log_action(current_user.id, 'approve_update_request',
                  details=f'Randevu #{req.appointment.id} güncelleme talebi onaylandı',
                  ip_address=request.remote_addr)
        message = 'Güncelleme talebi onaylandı'
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': message
    })

@app.route('/admin/requests/<int:req_id>/reject', methods=['POST'])
@login_required
def admin_request_reject(req_id):
    """Talebi reddet"""
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Yetkiniz yok'}), 403
    
    req = UpdateRequest.query.get_or_404(req_id)
    
    if req.status != 'Bekliyor':
        return jsonify({'success': False, 'message': 'Bu talep zaten işlenmiş'}), 400
    
    admin_note = request.form.get('admin_note', '').strip()
    if not admin_note:
        return jsonify({'success': False, 'message': 'Red nedeni gereklidir'}), 400
    
    req.status = 'Reddedildi'
    req.admin_note = admin_note
    req.processed_at = datetime.utcnow()
    req.processed_by = current_user.id
    
    db.session.commit()
    
    log_action(current_user.id, 'reject_request',
              details=f'Randevu #{req.appointment.id} {req.request_type} talebi reddedildi: {admin_note}',
              ip_address=request.remote_addr)
    
    return jsonify({
        'success': True,
        'message': 'Talep reddedildi'
    })

# ============================================================================
# ERROR HANDLERS
# ============================================================================
# ADMIN - SYSTEM LOGS
# ============================================================================

@app.route('/admin/logs')
@login_required
def admin_logs():
    """Sistem logları listesi (gelişmiş filtreleme)"""
    if not current_user.is_admin:
        flash('Bu sayfaya erişim yetkiniz yok.', 'danger')
        return redirect(url_for('dashboard'))
    
    from models import SystemLog
    from utils import get_action_type_badge, get_action_type_icon, get_device_icon
    
    # Veritabanı migration kontrolü
    try:
        # Test query - yeni kolonları kontrol et
        test_log = SystemLog.query.first()
        if test_log and not hasattr(test_log, 'action_type'):
            raise AttributeError("action_type kolonu bulunamadı")
    except Exception as e:
        flash(f'⚠️ Veritabanı migration gerekli! Lütfen migration_add_log_fields.sql dosyasını çalıştırın. Hata: {str(e)}', 'danger')
        return redirect(url_for('dashboard'))
    
    page = request.args.get('page', 1, type=int)
    per_page_default = app.config.get('ITEMS_PER_PAGE', 25)
    per_page = request.args.get('per_page', per_page_default, type=int)
    per_page_choices = [25, 50, 100, 200]
    if per_page not in per_page_choices:
        per_page = per_page_default
    
    # Filtreler
    search = (request.args.get('q') or '').strip()
    user_id = request.args.get('user_id', type=int)
    action_type = request.args.get('action_type', 'all')
    device_type = request.args.get('device_type', 'all')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    ip_address = request.args.get('ip_address', '').strip()
    
    query = SystemLog.query
    
    # Filtre uygula
    filters = []
    
    if search:
        like = f"%{search}%"
        filters.append(or_(
            SystemLog.action.ilike(like),
            SystemLog.details.ilike(like),
            User.username.ilike(like),
            User.full_name.ilike(like)
        ))
    
    if user_id:
        filters.append(SystemLog.user_id == user_id)
    
    if action_type != 'all':
        filters.append(SystemLog.action_type == action_type)
    
    if device_type != 'all':
        filters.append(SystemLog.device_type == device_type)
    
    if ip_address:
        filters.append(SystemLog.ip_address.ilike(f"%{ip_address}%"))
    
    if date_from:
        try:
            start_date = datetime.strptime(date_from, '%Y-%m-%d')
            filters.append(SystemLog.created_at >= start_date)
        except ValueError:
            flash('Başlangıç tarihi geçerli formatta değil.', 'warning')
    
    if date_to:
        try:
            end_date = datetime.strptime(date_to, '%Y-%m-%d') + timedelta(days=1)
            filters.append(SystemLog.created_at < end_date)
        except ValueError:
            flash('Bitiş tarihi geçerli formatta değil.', 'warning')
    
    # Join with User for filtering and display
    query = query.outerjoin(User, SystemLog.user_id == User.id)
    
    if filters:
        query = query.filter(and_(*filters))
    
    # Sıralama
    query = query.order_by(SystemLog.created_at.desc())
    
    # Paginate
    logs = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # İstatistikler
    base_query = SystemLog.query
    if filters:
        base_query = base_query.outerjoin(User, SystemLog.user_id == User.id).filter(and_(*filters))
    
    action_types = ['login', 'logout', 'create', 'update', 'delete', 'view', 'other']
    action_counts = {}
    for at in action_types:
        action_counts[at] = base_query.filter(SystemLog.action_type == at).count()
    
    device_counts = {
        'Desktop': base_query.filter(SystemLog.device_type == 'Desktop').count(),
        'Mobile': base_query.filter(SystemLog.device_type == 'Mobile').count(),
        'Tablet': base_query.filter(SystemLog.device_type == 'Tablet').count(),
    }
    
    # Kullanıcı listesi
    users_list = User.query.filter_by(is_admin=False).order_by(User.full_name.asc()).all()
    
    filters_payload = {
        'q': search,
        'user_id': user_id if user_id else '',
        'action_type': action_type,
        'device_type': device_type,
        'ip_address': ip_address,
        'date_from': date_from or '',
        'date_to': date_to or '',
        'per_page': per_page
    }
    
    return render_template('admin/logs.html',
                           logs=logs,
                           users=users_list,
                           action_types=action_types,
                           filters=filters_payload,
                           per_page_choices=per_page_choices,
                           action_counts=action_counts,
                           device_counts=device_counts,
                           get_action_type_badge=get_action_type_badge,
                           get_action_type_icon=get_action_type_icon,
                           get_device_icon=get_device_icon)

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found_error(error):
    """404 - Sayfa bulunamadı"""
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """500 - İç sunucu hatası"""
    db.session.rollback()
    print(f"❌ 500 Hatası: {error}")
    import traceback
    traceback.print_exc()
    return render_template('errors/500.html'), 500

@app.errorhandler(403)
def forbidden_error(error):
    """403 - Yetkisiz erişim"""
    return render_template('errors/403.html'), 403

@app.errorhandler(Exception)
def handle_exception(error):
    """Tüm yakalanmamış hataları yakala"""
    db.session.rollback()
    print(f"❌ Yakalanmamış Hata: {error}")
    import traceback
    traceback.print_exc()
    
    # Log kaydı oluştur
    try:
        if current_user and current_user.is_authenticated:
            log_action(current_user.id, 'error',
                      details=f'Hata: {str(error)}',
                      ip_address=request.remote_addr)
    except Exception as log_error:
        print(f"Log kaydı oluşturulamadı: {log_error}")
    
    # 500 hata sayfasını göster
    return render_template('errors/500.html'), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # İlk admin oluştur
        admin = User.query.filter_by(username=app.config['ADMIN_USERNAME']).first()
        if not admin:
            admin = User(
                username=app.config['ADMIN_USERNAME'],
                email=app.config['ADMIN_EMAIL'],
                full_name='Sistem Yöneticisi',
                is_admin=True,
                is_active=True
            )
            admin.set_password(app.config['ADMIN_PASSWORD'])
            db.session.add(admin)
            db.session.commit()
            print(f"✓ İlk admin oluşturuldu: {app.config['ADMIN_USERNAME']}")
            print(f"✓ Şifre: {app.config['ADMIN_PASSWORD']}")
        
        # Örnek ülkeler ekle (sadece ilk kurulumda)
        if Country.query.count() == 0:
            sample_countries = [
                {'name': 'Amerika Birleşik Devletleri', 'code': 'USA', 'flag_emoji': '🇺🇸'},
                {'name': 'İngiltere', 'code': 'GBR', 'flag_emoji': '🇬🇧'},
                {'name': 'Almanya', 'code': 'DEU', 'flag_emoji': '🇩🇪'},
                {'name': 'Fransa', 'code': 'FRA', 'flag_emoji': '🇫🇷'},
                {'name': 'İtalya', 'code': 'ITA', 'flag_emoji': '🇮🇹'},
                {'name': 'İspanya', 'code': 'ESP', 'flag_emoji': '🇪🇸'},
                {'name': 'Kanada', 'code': 'CAN', 'flag_emoji': '🇨🇦'},
                {'name': 'Avustralya', 'code': 'AUS', 'flag_emoji': '🇦🇺'},
            ]
            
            for country_data in sample_countries:
                country = Country(**country_data)
                db.session.add(country)
            
            db.session.commit()
            print(f"✓ {len(sample_countries)} örnek ülke eklendi")
        
        print("\n" + "="*50)
        print("✓ Vize Randevu Sistemi Hazır!")
        print("="*50)
    print("\n🌐 Adres: http://localhost:5000")
    print(f"👤 Kullanıcı: {app.config['ADMIN_USERNAME']}")
    print(f"🔑 Şifre: {app.config['ADMIN_PASSWORD']}\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

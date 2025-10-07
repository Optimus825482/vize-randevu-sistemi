import io
import json
from datetime import datetime
from flask import send_file, request
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from models import Appointment, User, Country, db, SystemLog
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def create_excel_report(appointments, filename='randevu_raporu.xlsx'):
    """Excel rapor oluştur"""
    # Veriyi DataFrame'e dönüştür
    data = []
    for apt in appointments:
        data.append({
            'ID': apt.id,
            'Kullanıcı': apt.user.username,
            'Kullanıcı Ad Soyad': apt.user.full_name,
            'Ülke': apt.country.name,
            'Başvuran Ad': apt.applicant_name,
            'Başvuran Soyad': apt.applicant_surname,
            'Pasaport No': apt.passport_number,
            'Doğum Tarihi': apt.birth_date.strftime('%d.%m.%Y') if apt.birth_date else '',
            'Telefon': apt.phone,
            'E-posta': apt.email,
            'Vize Türü': apt.visa_type or '',
            'Tercih Edilen Tarih': apt.preferred_date.strftime('%d.%m.%Y') if apt.preferred_date else '',
            'Durum': apt.status,
            'Oluşturma Tarihi': apt.created_at.strftime('%d.%m.%Y %H:%M'),
            'Son Güncelleme': apt.updated_at.strftime('%d.%m.%Y %H:%M'),
        })
    
    df = pd.DataFrame(data)
    
    # Excel dosyası oluştur
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Randevular', index=False)
        
        # Sütun genişliklerini ayarla
        worksheet = writer.sheets['Randevular']
        for idx, col in enumerate(df.columns):
            max_length = max(
                df[col].astype(str).apply(len).max(),
                len(col)
            ) + 2
            worksheet.column_dimensions[chr(65 + idx)].width = min(max_length, 50)
    
    output.seek(0)
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename
    )

def create_pdf_report(appointments, filename='randevu_raporu.pdf'):
    """PDF rapor oluştur"""
    buffer = io.BytesIO()
    
    # PDF oluştur
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
    elements = []
    
    # Stil tanımla
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=30,
        alignment=1  # Center
    )
    
    # Başlık
    title = Paragraph("VİZE RANDEVU RAPORU", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    # Tarih
    date_text = f"Rapor Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
    elements.append(Paragraph(date_text, styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Tablo verisi
    data = [['ID', 'Kullanıcı', 'Ülke', 'Başvuran', 'Pasaport', 'Durum', 'Tarih']]
    
    for apt in appointments:
        data.append([
            str(apt.id),
            apt.user.username[:15],
            apt.country.name[:15],
            f"{apt.applicant_name[:10]} {apt.applicant_surname[:10]}",
            apt.passport_number[:15],
            apt.status,
            apt.created_at.strftime('%d.%m.%Y')
        ])
    
    # Tablo oluştur
    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f1f5f9')]),
    ]))
    
    elements.append(table)
    
    # PDF'i oluştur
    doc.build(elements)
    buffer.seek(0)
    
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )

def get_dashboard_stats(user=None):
    """Dashboard istatistiklerini al"""
    if user and not user.is_admin:
        # Kullanıcı istatistikleri
        stats = {
            'total_appointments': Appointment.query.filter_by(user_id=user.id).count(),
            'waiting': Appointment.query.filter_by(user_id=user.id, status='Bekleme').count(),
            'in_process': Appointment.query.filter_by(user_id=user.id, status='Süreç Başlatıldı').count(),
            'completed': Appointment.query.filter_by(user_id=user.id, status='Tamamlandı').count(),
            'cancelled': Appointment.query.filter_by(user_id=user.id, status='İptal').count(),
        }
        
        # Ülkelere göre dağılım
        stats['by_country'] = db.session.query(
            Country.name,
            db.func.count(Appointment.id)
        ).join(Appointment).filter(
            Appointment.user_id == user.id
        ).group_by(Country.name).all()
        
    else:
        # Admin istatistikleri
        stats = {
            'total_users': User.query.filter_by(is_admin=False).count(),
            'active_users': User.query.filter_by(is_admin=False, is_active=True).count(),
            'total_appointments': Appointment.query.count(),
            'waiting': Appointment.query.filter_by(status='Bekleme').count(),
            'in_process': Appointment.query.filter_by(status='Süreç Başlatıldı').count(),
            'completed': Appointment.query.filter_by(status='Tamamlandı').count(),
            'cancelled': Appointment.query.filter_by(status='İptal').count(),
            'total_countries': Country.query.filter_by(is_active=True).count(),
        }
        
        # Ülkelere göre dağılım
        stats['by_country'] = db.session.query(
            Country.name,
            db.func.count(Appointment.id)
        ).join(Appointment).group_by(Country.name).all()
        
        # Kullanıcılara göre dağılım (Top 5)
        stats['top_users'] = db.session.query(
            User.username,
            User.full_name,
            db.func.count(Appointment.id).label('count')
        ).join(Appointment).group_by(User.id).order_by(
            db.func.count(Appointment.id).desc()
        ).limit(5).all()
    
    return stats

def parse_user_agent(user_agent_string):
    """User-Agent string'ini parse et ve cihaz bilgilerini çıkar"""
    if not user_agent_string:
        return {
            'device_type': 'Unknown',
            'browser': 'Unknown',
            'os': 'Unknown'
        }
    
    ua = user_agent_string.lower()
    
    # Device Type
    if 'mobile' in ua or 'android' in ua or 'iphone' in ua:
        device_type = 'Mobile'
    elif 'tablet' in ua or 'ipad' in ua:
        device_type = 'Tablet'
    else:
        device_type = 'Desktop'
    
    # Browser
    if 'edg' in ua:
        browser = 'Edge'
    elif 'chrome' in ua and 'chromium' not in ua:
        browser = 'Chrome'
    elif 'firefox' in ua:
        browser = 'Firefox'
    elif 'safari' in ua and 'chrome' not in ua:
        browser = 'Safari'
    elif 'opera' in ua or 'opr' in ua:
        browser = 'Opera'
    elif 'msie' in ua or 'trident' in ua:
        browser = 'Internet Explorer'
    else:
        browser = 'Unknown'
    
    # Operating System
    if 'windows' in ua:
        if 'windows nt 10' in ua:
            os = 'Windows 10/11'
        elif 'windows nt 6.3' in ua:
            os = 'Windows 8.1'
        elif 'windows nt 6.2' in ua:
            os = 'Windows 8'
        elif 'windows nt 6.1' in ua:
            os = 'Windows 7'
        else:
            os = 'Windows'
    elif 'mac' in ua or 'darwin' in ua:
        if 'iphone' in ua:
            os = 'iOS'
        elif 'ipad' in ua:
            os = 'iPadOS'
        else:
            os = 'macOS'
    elif 'linux' in ua:
        if 'android' in ua:
            os = 'Android'
        else:
            os = 'Linux'
    elif 'cros' in ua:
        os = 'Chrome OS'
    else:
        os = 'Unknown'
    
    return {
        'device_type': device_type,
        'browser': browser,
        'os': os
    }

def log_action(user_id, action, action_type=None, details=None, ip_address=None, user_agent=None):
    """
    Gelişmiş sistem loglarını kaydet
    
    Args:
        user_id: Kullanıcı ID
        action: İşlem adı (login, create_appointment, etc.)
        action_type: İşlem tipi (login, logout, create, update, delete, view)
        details: Detaylı açıklama
        ip_address: IP adresi
        user_agent: User-Agent string
    """
    # IP adresini otomatik al
    if ip_address is None and request:
        ip_address = request.remote_addr
    
    # User agent'ı otomatik al
    if user_agent is None and request:
        user_agent = request.headers.get('User-Agent', '')
    
    # Action type'ı otomatik belirle
    if action_type is None:
        if 'login' in action.lower():
            action_type = 'login'
        elif 'logout' in action.lower():
            action_type = 'logout'
        elif 'create' in action.lower():
            action_type = 'create'
        elif 'update' in action.lower() or 'edit' in action.lower():
            action_type = 'update'
        elif 'delete' in action.lower():
            action_type = 'delete'
        elif 'view' in action.lower() or 'list' in action.lower():
            action_type = 'view'
        else:
            action_type = 'other'
    
    # User agent'ı parse et
    device_info = parse_user_agent(user_agent)
    
    # Log kaydı oluştur
    log = SystemLog(
        user_id=user_id,
        action=action,
        action_type=action_type,
        details=details,
        ip_address=ip_address,
        user_agent=user_agent[:500] if user_agent else None,  # Max 500 karakter
        device_type=device_info['device_type'],
        browser=device_info['browser'],
        os=device_info['os']
    )
    
    try:
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Log kaydetme hatası: {e}")

def get_action_type_badge(action_type):
    """Action type için badge class döndür"""
    badges = {
        'login': 'bg-success',
        'logout': 'bg-secondary',
        'create': 'bg-primary',
        'update': 'bg-warning',
        'delete': 'bg-danger',
        'view': 'bg-info',
        'other': 'bg-dark'
    }
    return badges.get(action_type, 'bg-secondary')

def get_action_type_icon(action_type):
    """Action type için ikon döndür"""
    icons = {
        'login': 'bi-box-arrow-in-right',
        'logout': 'bi-box-arrow-left',
        'create': 'bi-plus-circle',
        'update': 'bi-pencil-square',
        'delete': 'bi-trash',
        'view': 'bi-eye',
        'other': 'bi-three-dots'
    }
    return icons.get(action_type, 'bi-circle')

def get_device_icon(device_type):
    """Cihaz tipi için ikon döndür"""
    icons = {
        'Desktop': 'bi-display',
        'Mobile': 'bi-phone',
        'Tablet': 'bi-tablet',
        'Unknown': 'bi-question-circle'
    }
    return icons.get(device_type, 'bi-question-circle')

def send_admin_notification(subject, message, action_type='info'):
    """
    Yöneticiye e-posta bildirimi gönder
    
    Args:
        subject: E-posta konusu
        message: E-posta mesajı (HTML formatında olabilir)
        action_type: Bildirim tipi (info, warning, success, danger)
    """
    try:
        # E-posta ayarları
        sender_email = "vizal8254@gmail.com"
        sender_password = "rsyg yksq tecj meel"  # Gmail uygulama şifresi
        receiver_email = "vizal8254@gmail.com"  # Şimdilik kendine gönder
        
        # E-posta oluştur
        msg = MIMEMultipart('alternative')
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = f"[VİZE RANDEVU SİSTEMİ] {subject}"
        
        # HTML içerik
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #1e293b; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
                .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 8px 8px; }}
                .badge {{ display: inline-block; padding: 8px 16px; border-radius: 4px; font-weight: bold; margin: 10px 0; }}
                .badge-info {{ background: #0dcaf0; color: #000; }}
                .badge-warning {{ background: #ffc107; color: #000; }}
                .badge-success {{ background: #198754; color: #fff; }}
                .badge-danger {{ background: #dc3545; color: #fff; }}
                .message {{ background: white; padding: 20px; border-left: 4px solid #10b981; margin: 20px 0; border-radius: 4px; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔔 Sistem Bildirimi</h1>
                </div>
                <div class="content">
                    <p>Merhaba <strong>Yönetici</strong>,</p>
                    <div class="badge badge-{action_type}">
                        {subject}
                    </div>
                    <div class="message">
                        {message}
                    </div>
                    <p><strong>Tarih:</strong> {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</p>
                    <p>Detaylı bilgi için lütfen yönetim paneline giriş yapın.</p>
                    <div class="footer">
                        <p>Bu otomatik bir bildirimdir, lütfen yanıtlamayın.</p>
                        <p>© 2025 Vize Randevu Sistemi</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        # HTML kısmını ekle
        html_part = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(html_part)
        
        # E-postayı gönder
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        print(f"Bildirim gönderildi: {receiver_email}")
        
        return True
        
    except Exception as e:
        print(f"Admin bildirim hatası: {e}")
        return False

def send_new_user_credentials(user_email, username, password, full_name):
    """
    Yeni kullanıcıya giriş bilgilerini e-posta ile gönder
    
    Args:
        user_email: Kullanıcının e-posta adresi
        username: Kullanıcı adı
        password: Kullanıcı şifresi (düz metin)
        full_name: Kullanıcının tam adı
    
    Returns:
        bool: Başarılı ise True, hata oluşursa False
    """
    from flask import current_app
    
    print("=" * 70)
    print(f"📧 YENİ KULLANICI MAİL GÖNDERİMİ BAŞLIYOR")
    print("=" * 70)
    print(f"   ├─ Alıcı E-posta: {user_email}")
    print(f"   ├─ Kullanıcı Adı: {username}")
    print(f"   ├─ Tam Ad: {full_name}")
    print(f"   └─ Şifre Uzunluğu: {len(password)} karakter")
    
    try:
        # E-posta ayarlarını config'den al
        sender_email = current_app.config.get('MAIL_USERNAME', 'vizal8254@gmail.com')
        sender_password = current_app.config.get('MAIL_PASSWORD', 'rsyg yksq tecj meel')
        mail_server = current_app.config.get('MAIL_SERVER', 'smtp.gmail.com')
        mail_port = current_app.config.get('MAIL_PORT', 587)
        
        print(f"\n📮 SMTP Ayarları:")
        print(f"   ├─ Server: {mail_server}")
        print(f"   ├─ Port: {mail_port}")
        print(f"   ├─ Gönderen: {sender_email}")
        print(f"   └─ TLS: Aktif")
        
        # E-posta oluştur
        msg = MIMEMultipart('alternative')
        msg['From'] = sender_email
        msg['To'] = user_email
        msg['Subject'] = "Vize Randevu Sistemi - Giriş Bilgileriniz"
        
        # HTML içerik
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #10b981; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
                .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 8px 8px; }}
                .credentials {{ background: white; padding: 25px; border: 2px solid #10b981; border-radius: 8px; margin: 20px 0; }}
                .credential-item {{ margin: 15px 0; padding: 10px; background: #f1f5f9; border-radius: 4px; }}
                .credential-label {{ font-weight: bold; color: #1e293b; }}
                .credential-value {{ font-size: 18px; color: #059669; font-family: 'Courier New', monospace; }}
                .warning {{ background: #fef3c7; border-left: 4px solid #f59e0b; padding: 15px; margin: 20px 0; border-radius: 4px; }}
                .button {{ display: inline-block; background: #10b981; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; border-top: 1px solid #ddd; padding-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 Hoş Geldiniz!</h1>
                </div>
                <div class="content">
                    <p>Merhaba <strong>{full_name}</strong>,</p>
                    
                    <p>Vize Randevu Sistemi'ne kullanıcı olarak eklendiniz. Sisteme giriş yapmak için aşağıdaki bilgileri kullanabilirsiniz:</p>
                    
                    <div class="credentials">
                        <h3 style="color: #1e293b; margin-top: 0;">🔐 Giriş Bilgileriniz</h3>
                        
                        <div class="credential-item">
                            <span class="credential-label">Kullanıcı Adı:</span><br>
                            <span class="credential-value">{username}</span>
                        </div>
                        
                        <div class="credential-item">
                            <span class="credential-label">Şifre:</span><br>
                            <span class="credential-value">{password}</span>
                        </div>
                    </div>
                    
                    <div class="warning">
                        <strong>⚠️ Önemli Güvenlik Uyarısı:</strong>
                        <ul style="margin: 10px 0;">
                            <li>Bu bilgileri <strong>yalnızca bir kez</strong> gönderilmektedir</li>
                            <li>Şifrenizi güvenli bir yerde saklayın</li>
                            <li>İlk girişten sonra şifrenizi değiştirmeniz önerilir</li>
                            <li>Bu e-postayı kimseyle paylaşmayın</li>
                        </ul>
                    </div>
                    
                    <div style="text-align: center;">
                        <a href="#" class="button">Sisteme Giriş Yap →</a>
                    </div>
                    
                    <p style="margin-top: 30px;">Herhangi bir sorunuz olursa lütfen sistem yöneticinizle iletişime geçin.</p>
                    
                    <div class="footer">
                        <p><strong>Vize Randevu Sistemi</strong></p>
                        <p>Bu otomatik bir e-postadır, lütfen yanıtlamayın.</p>
                        <p>© 2025 Tüm hakları saklıdır.</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        # HTML kısmını ekle
        html_part = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(html_part)
        
        print(f"   ├─ SMTP bağlantısı kuruluyor...")
        
        # E-postayı gönder
        with smtplib.SMTP('smtp.gmail.com', 587, timeout=10) as server:
            print(f"   ├─ TLS başlatılıyor...")
            server.starttls()
            
            print(f"   ├─ Giriş yapılıyor...")
            server.login(sender_email, sender_password)
            
            print(f"   ├─ Mail gönderiliyor...")
            server.send_message(msg)
        
        print(f"✅ Kullanıcı giriş bilgileri başarıyla gönderildi: {user_email}")
        
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ SMTP Kimlik Doğrulama Hatası: {e}")
        print(f"   └─ Gmail uygulama şifresi geçersiz veya 2FA kapalı olabilir")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ SMTP Hatası: {e}")
        print(f"   └─ Mail sunucusu ile iletişim kurulamadı")
        return False
    except Exception as e:
        print(f"❌ Kullanıcı e-postası gönderme hatası: {e}")
        import traceback
        traceback.print_exc()
        return False

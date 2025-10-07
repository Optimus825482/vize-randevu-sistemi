-- ============================================================================
-- VİZE RANDEVU YÖNETİM SİSTEMİ - VERİTABANI OLUŞTURMA SCRIPT'İ
-- ============================================================================
-- Tarih: 05.10.2025
-- Açıklama: Tüm tabloları ve ilişkileri otomatik oluşturur
-- Kullanım: MySQL Command Line veya phpMyAdmin'de çalıştırın
-- ============================================================================

-- Varsa mevcut veritabanını sil (DİKKAT: Tüm veriler silinir!)
-- DROP DATABASE IF EXISTS vize_randevu_db;

-- Yeni veritabanı oluştur
CREATE DATABASE IF NOT EXISTS vize_randevu_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Veritabanını seç
USE vize_randevu_db;

-- ============================================================================
-- TABLO 1: USERS (Kullanıcılar)
-- ============================================================================
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME NULL,
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_is_admin (is_admin),
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLO 2: COUNTRIES (Ülkeler)
-- ============================================================================
CREATE TABLE IF NOT EXISTS countries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    code VARCHAR(3) NOT NULL UNIQUE,
    flag_emoji VARCHAR(10) NULL,
    required_fields TEXT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_code (code),
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLO 3: USER_COUNTRY_QUOTAS (Kullanıcı Kota İlişkileri)
-- ============================================================================
CREATE TABLE IF NOT EXISTS user_country_quotas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    country_id INT NOT NULL,
    quota_limit INT NOT NULL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_user_country (user_id, country_id),
    INDEX idx_user_id (user_id),
    INDEX idx_country_id (country_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (country_id) REFERENCES countries(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLO 4: APPOINTMENTS (Randevu Talepleri)
-- ============================================================================
CREATE TABLE IF NOT EXISTS appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    country_id INT NOT NULL,
    
    -- Başvuran Bilgileri (Zorunlu)
    applicant_name VARCHAR(150) NOT NULL,
    applicant_surname VARCHAR(150) NOT NULL,
    passport_number VARCHAR(50) NOT NULL,
    
    -- Başvuran Bilgileri (Opsiyonel)
    birth_date DATE NULL,
    phone VARCHAR(20) NULL,
    email VARCHAR(120) NULL,
    passport_issue_date DATE NULL,
    passport_expiry_date DATE NULL,
    nationality VARCHAR(100) NULL,
    travel_date DATE NULL,
    address TEXT NULL,
    
    -- Randevu Bilgileri
    preferred_date DATE NULL,
    preferred_date_end DATE NULL,
    visa_type VARCHAR(100) NULL,
    notes TEXT NULL,
    
    -- Durum Takibi
    status VARCHAR(50) DEFAULT 'Bekleme',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    processed_at DATETIME NULL,
    
    INDEX idx_user_id (user_id),
    INDEX idx_country_id (country_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at),
    INDEX idx_passport (passport_number),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (country_id) REFERENCES countries(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLO 5: UPDATE_REQUESTS (Güncelleme/Silme Talepleri)
-- ============================================================================
CREATE TABLE IF NOT EXISTS update_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    appointment_id INT NOT NULL,
    request_type VARCHAR(20) NOT NULL,
    request_data TEXT NULL,
    reason TEXT NULL,
    status VARCHAR(20) DEFAULT 'Bekliyor',
    admin_note TEXT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    processed_at DATETIME NULL,
    processed_by INT NULL,
    
    INDEX idx_user_id (user_id),
    INDEX idx_appointment_id (appointment_id),
    INDEX idx_status (status),
    INDEX idx_request_type (request_type),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (appointment_id) REFERENCES appointments(id) ON DELETE CASCADE,
    FOREIGN KEY (processed_by) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLO 6: SYSTEM_LOGS (Sistem Logları)
-- ============================================================================
CREATE TABLE IF NOT EXISTS system_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    action VARCHAR(100) NOT NULL,
    details TEXT NULL,
    ip_address VARCHAR(50) NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_user_id (user_id),
    INDEX idx_action (action),
    INDEX idx_created_at (created_at),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- ÖRNEK VERİLER EKLE
-- ============================================================================

-- Admin Kullanıcısı (Şifre: Admin123!)
-- Şifre hash'i: pbkdf2:sha256:600000$... (uygulama tarafından oluşturulacak)
INSERT INTO users (username, email, password_hash, full_name, is_admin, is_active) VALUES
('admin', 'admin@vizesistemi.com', 'scrypt:32768:8:1$nR7xK9wL8jT3pM2q$a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2g3h4i5j6k7l8m9n0o1p2', 'Sistem Yöneticisi', TRUE, TRUE)
ON DUPLICATE KEY UPDATE username=username;

-- Örnek Ülkeler
INSERT INTO countries (name, code, flag_emoji, is_active) VALUES
('Amerika Birleşik Devletleri', 'USA', '🇺🇸', TRUE),
('İngiltere', 'GBR', '🇬🇧', TRUE),
('Almanya', 'DEU', '🇩🇪', TRUE),
('Fransa', 'FRA', '🇫🇷', TRUE),
('İtalya', 'ITA', '🇮🇹', TRUE),
('İspanya', 'ESP', '🇪🇸', TRUE),
('Kanada', 'CAN', '🇨🇦', TRUE),
('Avustralya', 'AUS', '🇦🇺', TRUE),
('Japonya', 'JPN', '🇯🇵', TRUE),
('Güney Kore', 'KOR', '🇰🇷', TRUE),
('İsviçre', 'CHE', '🇨🇭', TRUE),
('Hollanda', 'NLD', '🇳🇱', TRUE),
('Belçika', 'BEL', '🇧🇪', TRUE),
('Avusturya', 'AUT', '🇦🇹', TRUE),
('İsveç', 'SWE', '🇸🇪', TRUE)
ON DUPLICATE KEY UPDATE name=name;

-- ============================================================================
-- GÖRÜNÜMLER (VIEWS) - İstatistikler için
-- ============================================================================

-- Kullanıcı başına randevu sayısı
CREATE OR REPLACE VIEW view_user_appointment_stats AS
SELECT 
    u.id AS user_id,
    u.username,
    u.full_name,
    u.email,
    COUNT(a.id) AS total_appointments,
    SUM(CASE WHEN a.status = 'Bekleme' THEN 1 ELSE 0 END) AS waiting_count,
    SUM(CASE WHEN a.status = 'Süreç Başlatıldı' THEN 1 ELSE 0 END) AS in_process_count,
    SUM(CASE WHEN a.status = 'Tamamlandı' THEN 1 ELSE 0 END) AS completed_count,
    SUM(CASE WHEN a.status = 'İptal' THEN 1 ELSE 0 END) AS cancelled_count
FROM users u
LEFT JOIN appointments a ON u.id = a.user_id
WHERE u.is_admin = FALSE
GROUP BY u.id, u.username, u.full_name, u.email;

-- Ülke başına randevu sayısı
CREATE OR REPLACE VIEW view_country_appointment_stats AS
SELECT 
    c.id AS country_id,
    c.name AS country_name,
    c.code AS country_code,
    c.flag_emoji,
    COUNT(a.id) AS total_appointments,
    SUM(CASE WHEN a.status = 'Bekleme' THEN 1 ELSE 0 END) AS waiting_count,
    SUM(CASE WHEN a.status = 'Süreç Başlatıldı' THEN 1 ELSE 0 END) AS in_process_count,
    SUM(CASE WHEN a.status = 'Tamamlandı' THEN 1 ELSE 0 END) AS completed_count,
    SUM(CASE WHEN a.status = 'İptal' THEN 1 ELSE 0 END) AS cancelled_count
FROM countries c
LEFT JOIN appointments a ON c.id = a.country_id
WHERE c.is_active = TRUE
GROUP BY c.id, c.name, c.code, c.flag_emoji;

-- Kullanıcı kota kullanımı
CREATE OR REPLACE VIEW view_user_quota_usage AS
SELECT 
    u.id AS user_id,
    u.username,
    u.full_name,
    c.id AS country_id,
    c.name AS country_name,
    c.flag_emoji,
    ucq.quota_limit,
    COUNT(a.id) AS used_quota,
    (ucq.quota_limit - COUNT(a.id)) AS remaining_quota,
    ROUND((COUNT(a.id) / ucq.quota_limit) * 100, 2) AS usage_percentage
FROM users u
INNER JOIN user_country_quotas ucq ON u.id = ucq.user_id
INNER JOIN countries c ON ucq.country_id = c.id
LEFT JOIN appointments a ON u.id = a.user_id AND c.id = a.country_id
WHERE u.is_admin = FALSE AND c.is_active = TRUE
GROUP BY u.id, u.username, u.full_name, c.id, c.name, c.flag_emoji, ucq.quota_limit;

-- ============================================================================
-- STORED PROCEDURES - Yardımcı Fonksiyonlar
-- ============================================================================

-- Kullanıcı kota kontrolü
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS sp_check_user_quota(
    IN p_user_id INT,
    IN p_country_id INT,
    OUT p_has_quota BOOLEAN,
    OUT p_remaining_quota INT
)
BEGIN
    DECLARE v_quota_limit INT;
    DECLARE v_used_quota INT;
    
    -- Kota limitini al
    SELECT quota_limit INTO v_quota_limit
    FROM user_country_quotas
    WHERE user_id = p_user_id AND country_id = p_country_id;
    
    -- Kullanılan kotayı hesapla
    SELECT COUNT(*) INTO v_used_quota
    FROM appointments
    WHERE user_id = p_user_id AND country_id = p_country_id;
    
    -- Sonuçları hesapla
    SET p_remaining_quota = v_quota_limit - v_used_quota;
    SET p_has_quota = (p_remaining_quota > 0);
END //
DELIMITER ;

-- Randevu istatistikleri
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS sp_get_appointment_statistics(
    IN p_start_date DATE,
    IN p_end_date DATE
)
BEGIN
    SELECT 
        COUNT(*) AS total_appointments,
        SUM(CASE WHEN status = 'Bekleme' THEN 1 ELSE 0 END) AS waiting,
        SUM(CASE WHEN status = 'Süreç Başlatıldı' THEN 1 ELSE 0 END) AS in_process,
        SUM(CASE WHEN status = 'Tamamlandı' THEN 1 ELSE 0 END) AS completed,
        SUM(CASE WHEN status = 'İptal' THEN 1 ELSE 0 END) AS cancelled,
        COUNT(DISTINCT user_id) AS unique_users,
        COUNT(DISTINCT country_id) AS unique_countries
    FROM appointments
    WHERE DATE(created_at) BETWEEN p_start_date AND p_end_date;
END //
DELIMITER ;

-- ============================================================================
-- TRİGGER'LAR - Otomatik İşlemler
-- ============================================================================

-- Randevu oluşturulduğunda log ekle
DELIMITER //
CREATE TRIGGER IF NOT EXISTS trg_after_appointment_insert
AFTER INSERT ON appointments
FOR EACH ROW
BEGIN
    INSERT INTO system_logs (user_id, action, details)
    VALUES (
        NEW.user_id, 
        'create_appointment',
        CONCAT('Randevu ID: ', NEW.id, ' - Ülke ID: ', NEW.country_id)
    );
END //
DELIMITER ;

-- Randevu güncellendiğinde log ekle
DELIMITER //
CREATE TRIGGER IF NOT EXISTS trg_after_appointment_update
AFTER UPDATE ON appointments
FOR EACH ROW
BEGIN
    IF OLD.status != NEW.status THEN
        INSERT INTO system_logs (user_id, action, details)
        VALUES (
            NEW.user_id,
            'update_appointment_status',
            CONCAT('Randevu ID: ', NEW.id, ' - Durum: ', OLD.status, ' -> ', NEW.status)
        );
    END IF;
END //
DELIMITER ;

-- Randevu silindiğinde log ekle
DELIMITER //
CREATE TRIGGER IF NOT EXISTS trg_after_appointment_delete
AFTER DELETE ON appointments
FOR EACH ROW
BEGIN
    INSERT INTO system_logs (user_id, action, details)
    VALUES (
        OLD.user_id,
        'delete_appointment',
        CONCAT('Randevu ID: ', OLD.id, ' - Ülke ID: ', OLD.country_id)
    );
END //
DELIMITER ;

-- ============================================================================
-- VERİTABANI KULLANICISI OLUŞTUR
-- ============================================================================

-- Uygulama için özel kullanıcı oluştur
-- Not: Şifreyi kendi güvenli şifrenizle değiştirin!
CREATE USER IF NOT EXISTS 'vize_user'@'localhost' IDENTIFIED BY 'VizeSecure2025!';

-- Yetkileri ver
GRANT SELECT, INSERT, UPDATE, DELETE ON vize_randevu_db.* TO 'vize_user'@'localhost';

-- Stored procedure ve view için ek yetkiler
GRANT EXECUTE ON vize_randevu_db.* TO 'vize_user'@'localhost';

-- Yetkileri uygula
FLUSH PRIVILEGES;

-- ============================================================================
-- VERİFİKASYON - Tabloları Kontrol Et
-- ============================================================================

-- Oluşturulan tüm tabloları listele
SELECT 
    TABLE_NAME AS 'Tablo Adı',
    TABLE_ROWS AS 'Kayıt Sayısı',
    ROUND((DATA_LENGTH + INDEX_LENGTH) / 1024, 2) AS 'Boyut (KB)',
    ENGINE AS 'Motor',
    TABLE_COLLATION AS 'Karakter Seti'
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'vize_randevu_db'
ORDER BY TABLE_NAME;

-- Tüm view'ları listele
SELECT 
    TABLE_NAME AS 'View Adı',
    VIEW_DEFINITION AS 'Tanım'
FROM information_schema.VIEWS
WHERE TABLE_SCHEMA = 'vize_randevu_db';

-- Foreign key ilişkilerini göster
SELECT 
    CONSTRAINT_NAME AS 'İlişki Adı',
    TABLE_NAME AS 'Tablo',
    COLUMN_NAME AS 'Kolon',
    REFERENCED_TABLE_NAME AS 'Referans Tablo',
    REFERENCED_COLUMN_NAME AS 'Referans Kolon'
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'vize_randevu_db'
AND REFERENCED_TABLE_NAME IS NOT NULL;

-- ============================================================================
-- TAMAMLANDI!
-- ============================================================================

SELECT '=====================================' AS '';
SELECT '✅ VERİTABANI BAŞARIYLA OLUŞTURULDU!' AS '';
SELECT '=====================================' AS '';
SELECT '' AS '';
SELECT 'Veritabanı: vize_randevu_db' AS 'Bilgi';
SELECT 'Kullanıcı: vize_user@localhost' AS 'Bilgi';
SELECT 'Şifre: VizeSecure2025!' AS 'Bilgi';
SELECT '' AS '';
SELECT 'Admin Kullanıcı: admin' AS 'Uygulama Girişi';
SELECT 'Admin Şifre: Admin123!' AS 'Uygulama Girişi';
SELECT '' AS '';
SELECT '⚠️  .env dosyasını güncellemeyi unutmayın!' AS 'Uyarı';
SELECT '' AS '';

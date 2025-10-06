-- ============================================================================
-- SİSTEM LOG TABLOSU GELİŞTİRME MİGRATION SCRIPT'İ
-- ============================================================================
-- Tarih: 06.01.2025
-- Açıklama: system_logs tablosuna yeni alanlar ekler
-- ============================================================================

USE vize_randevu_db;

-- Yeni kolonları ekle
ALTER TABLE system_logs 
ADD COLUMN IF NOT EXISTS action_type VARCHAR(50) AFTER action,
ADD COLUMN IF NOT EXISTS user_agent VARCHAR(500) AFTER ip_address,
ADD COLUMN IF NOT EXISTS device_type VARCHAR(50) AFTER user_agent,
ADD COLUMN IF NOT EXISTS browser VARCHAR(50) AFTER device_type,
ADD COLUMN IF NOT EXISTS os VARCHAR(50) AFTER browser;

-- Index'ler ekle (performans için)
CREATE INDEX IF NOT EXISTS idx_action_type ON system_logs(action_type);
CREATE INDEX IF NOT EXISTS idx_ip_address ON system_logs(ip_address);
CREATE INDEX IF NOT EXISTS idx_created_at ON system_logs(created_at);

-- Mevcut kayıtlar için action_type'ı otomatik belirle
UPDATE system_logs SET action_type = 
    CASE 
        WHEN action LIKE '%login%' THEN 'login'
        WHEN action LIKE '%logout%' THEN 'logout'
        WHEN action LIKE '%create%' THEN 'create'
        WHEN action LIKE '%update%' OR action LIKE '%edit%' THEN 'update'
        WHEN action LIKE '%delete%' THEN 'delete'
        WHEN action LIKE '%view%' OR action LIKE '%list%' THEN 'view'
        ELSE 'other'
    END
WHERE action_type IS NULL;

-- Başarı mesajı
SELECT '✅ system_logs tablosu başarıyla güncellendi!' AS 'Durum';
SELECT 'Yeni kolonlar: action_type, user_agent, device_type, browser, os' AS 'Eklenen Alanlar';
SELECT 'Yeni index\'ler oluşturuldu' AS 'Performans';

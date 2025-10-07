#!/bin/bash

# Railway'de migration çalıştırma scripti
echo "🚀 Railway Migration Başlatılıyor..."
echo ""

# Python ile migration'ı çalıştır
python migration_add_residence_city.py

# Çıkış kodu kontrol et
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Migration başarılı! Uygulama başlatılabilir."
    exit 0
else
    echo ""
    echo "❌ Migration başarısız!"
    exit 1
fi

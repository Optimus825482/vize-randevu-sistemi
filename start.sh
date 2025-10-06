#!/bin/bash
# Railway başlangıç scripti

echo "🚀 Railway deployment başlatılıyor..."

# Veritabanını başlat
echo "📊 Veritabanı kontrol ediliyor..."
python3.9 init_railway_db.py

# Exit kodunu kontrol et
if [ $? -eq 0 ]; then
    echo "✅ Veritabanı hazır!"
else
    echo "⚠️ Veritabanı kurulumunda sorun olabilir, ancak devam ediliyor..."
fi

# Uygulamayı başlat
echo "🌐 Uygulama başlatılıyor..."
exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 4 --timeout 120 --access-logfile - --error-logfile -

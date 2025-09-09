#!/bin/bash

# Tea Activity Reporter - API Başlatma Scripti

echo "🚀 Tea Activity Reporter API başlatılıyor..."
echo ""

# Python ve pip varlığını kontrol et
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 bulunamadı. Lütfen Python3 yükleyin."
    exit 1
fi

if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip bulunamadı. Lütfen pip yükleyin."
    exit 1
fi

# Gerekli bağımlılıkları yükle
echo "📦 Bağımlılıklar yükleniyor..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Bağımlılık yükleme hatası!"
    exit 1
fi

# API sunucusunu başlat
echo ""
echo "🌟 API sunucusu başlatılıyor..."
echo "📍 Erişim: http://localhost:8000"
echo "📚 Dokümantasyon: http://localhost:8000/docs"
echo ""
echo "🛑 Durdurmak için Ctrl+C basın"
echo ""

cd scripts
python app.py
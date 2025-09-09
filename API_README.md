# Tea Activity Reporter - Backend API

Bu proje cryptocurrency exchange verilerini toplayan ve analiz eden bir FastAPI backend API'sidir.

## 📁 Dizin Yapısı

```
scripts/
├── app.py                    # FastAPI ana uygulaması
├── fetchers/                 # Exchange API bağlantıları
│   ├── binance_fetcher.py   # Binance entegrasyonu
│   ├── bybit_fetcher.py     # Bybit entegrasyonu  
│   ├── okx_fetcher.py       # OKX entegrasyonu
│   └── coinbase_fetcher.py  # Coinbase entegrasyonu
└── analysis/                # Analiz modülleri
    └── analyzer.py          # Klines analiz fonksiyonları
```

## 🚀 Kurulum

```bash
# Bağımlılıkları yükle
pip install -r requirements.txt

# API sunucusunu başlat
cd scripts
python app.py
```

API http://localhost:8000 adresinde çalışacaktır.

## 📖 API Endpoints

### Ana Endpoint
- `GET /` - API durumu

### Exchange-Specific Endpoints
- `GET /binance/{token}` - Binance'den veri çek ve analiz et
- `GET /bybit/{token}` - Bybit'den veri çek ve analiz et  
- `GET /okx/{token}` - OKX'den veri çek ve analiz et
- `GET /coinbase/{token}` - Coinbase'den veri çek ve analiz et

### Karşılaştırma Endpoint
- `GET /analyze?token={token}` - Tüm exchange'lerde token analizi

## 💡 Kullanım Örnekleri

```bash
# Bitcoin verisi al (Binance)
curl http://localhost:8000/binance/BTC

# Ethereum karşılaştırmalı analiz
curl "http://localhost:8000/analyze?token=ETH"

# Specific exchange'de altcoin
curl http://localhost:8000/bybit/ADA
```

## 📊 Analiz Sonuçları

Her endpoint şu analiz verilerini döndürür:

```json
{
  "exchange": "binance",
  "token": "BTC", 
  "data": [...],  // Ham klines verisi
  "analysis": {
    "ortalama_kapanis": 30150.0,
    "en_yuksek_kapanis": 30900.0,
    "en_dusuk_kapanis": 29200.0,
    "ortalama_volume": 103.1,
    "toplam_volume": 515.5,
    "veri_sayisi": 100,
    "fiyat_degisimi_yuzdesi": 5.82
  }
}
```

## 🔧 Özelleştirme

### Fetcher Parametreleri
- **Binance**: `interval` (1m, 5m, 1h, 1d), `limit` (max 1000)
- **Bybit**: `interval` (1, 5, 60, 240, D), `limit` (max 200) 
- **OKX**: `bar` (1m, 1H, 1D), `limit` (max 300)
- **Coinbase**: `granularity` (60, 3600, 86400), `limit` (max 300)

### Yeni Exchange Ekleme
1. `scripts/fetchers/` altında yeni fetcher oluştur
2. `scripts/app.py` içinde endpoint ekle
3. Klines formatını standardize et

## 🛠️ Geliştirme

```bash
# Syntax kontrolü
python -m py_compile scripts/app.py

# Test çalıştır
python scripts/test_analyzer.py  # Mock data ile test
```

## 📈 Gelecek Özellikler

- [ ] AI Predictor modülü (`analysis/ai_predictor.py`)
- [ ] WebSocket real-time data
- [ ] Database entegrasyonu
- [ ] Rate limiting
- [ ] Caching mekanizması
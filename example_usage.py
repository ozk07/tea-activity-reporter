#!/usr/bin/env python3
"""
Tea Activity Reporter API - Örnek Kullanım Scripti

Bu script, API'nin nasıl kullanılacağını gösterir.
"""

import requests
import json
from time import sleep

API_BASE_URL = "http://localhost:8000"

def test_api_endpoint(endpoint, description):
    """API endpoint'ini test et"""
    print(f"🔍 Test: {description}")
    print(f"📡 Endpoint: {endpoint}")
    
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Başarılı! Status: {response.status_code}")
            
            # Analiz sonuçlarını göster
            if 'analysis' in data:
                analysis = data['analysis']
                print(f"📊 Analiz:")
                print(f"   • Ortalama Kapanış: {analysis.get('ortalama_kapanis', 'N/A')}")
                print(f"   • En Yüksek: {analysis.get('en_yuksek_kapanis', 'N/A')}")
                print(f"   • En Düşük: {analysis.get('en_dusuk_kapanis', 'N/A')}")
                print(f"   • Fiyat Değişimi: %{analysis.get('fiyat_degisimi_yuzdesi', 'N/A')}")
                print(f"   • Veri Sayısı: {analysis.get('veri_sayisi', 'N/A')}")
        else:
            print(f"❌ Hata! Status: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Bağlantı hatası! API sunucusu çalışıyor mu?")
        print("   Başlatmak için: ./start_api.sh")
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")
    
    print("-" * 50)
    sleep(1)  # Rate limiting için kısa bekleme

def main():
    """Ana test fonksiyonu"""
    print("🚀 Tea Activity Reporter API Test Scripti")
    print("=" * 50)
    
    # API durumunu kontrol et
    test_api_endpoint("/", "API Durum Kontrolü")
    
    # Farklı exchange'lerde test
    exchanges_and_tokens = [
        ("/binance/BTC", "Binance - Bitcoin"),
        ("/bybit/ETH", "Bybit - Ethereum"), 
        ("/okx/ADA", "OKX - Cardano"),
        ("/coinbase/DOGE", "Coinbase - Dogecoin")
    ]
    
    for endpoint, description in exchanges_and_tokens:
        test_api_endpoint(endpoint, description)
    
    # Karşılaştırmalı analiz testi
    test_api_endpoint("/analyze?token=BTC", "Tüm Exchange'lerde Bitcoin Karşılaştırması")
    
    print("🏁 Test tamamlandı!")
    print("\n💡 Not: Internet bağlantısı gerektirir ve API sunucusunun çalışıyor olması lazım.")
    print("   Sunucuyu başlatmak için: ./start_api.sh")

if __name__ == "__main__":
    main()
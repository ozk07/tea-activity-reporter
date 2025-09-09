def analyze_klines(klines):
    """
    Analyze klines data and return basic statistics.
    
    Args:
        klines: List of kline data where each item contains:
                [timestamp, open, high, low, close, volume, ...]
    
    Returns:
        dict: Analysis results including averages and extremes
    """
    if not klines or len(klines) == 0:
        return {
            "ortalama_kapanis": 0,
            "en_yuksek_kapanis": 0,
            "en_dusuk_kapanis": 0,
            "ortalama_volume": 0,
            "toplam_volume": 0,
            "veri_sayisi": 0,
            "fiyat_degisimi_yuzdesi": 0
        }
    
    # Extract close prices and volumes from klines
    closes = [float(item[4]) for item in klines]
    volumes = [float(item[5]) for item in klines]
    
    # Calculate basic statistics
    ortalama_kapanis = sum(closes) / len(closes) if closes else 0
    en_yuksek_kapanis = max(closes) if closes else 0
    en_dusuk_kapanis = min(closes) if closes else 0
    ortalama_volume = sum(volumes) / len(volumes) if volumes else 0
    toplam_volume = sum(volumes)
    
    # Calculate price change percentage (first to last)
    fiyat_degisimi_yuzdesi = 0
    if len(closes) > 1 and closes[0] != 0:
        fiyat_degisimi_yuzdesi = ((closes[-1] - closes[0]) / closes[0]) * 100
    
    return {
        "ortalama_kapanis": round(ortalama_kapanis, 8),
        "en_yuksek_kapanis": round(en_yuksek_kapanis, 8),
        "en_dusuk_kapanis": round(en_dusuk_kapanis, 8),
        "ortalama_volume": round(ortalama_volume, 8),
        "toplam_volume": round(toplam_volume, 8),
        "veri_sayisi": len(klines),
        "fiyat_degisimi_yuzdesi": round(fiyat_degisimi_yuzdesi, 2)
    }

def calculate_volatility(klines):
    """
    Calculate price volatility based on close prices.
    
    Args:
        klines: List of kline data
        
    Returns:
        float: Volatility as standard deviation of price changes
    """
    if not klines or len(klines) < 2:
        return 0
    
    closes = [float(item[4]) for item in klines]
    
    # Calculate price changes (returns)
    price_changes = []
    for i in range(1, len(closes)):
        if closes[i-1] != 0:
            change = (closes[i] - closes[i-1]) / closes[i-1]
            price_changes.append(change)
    
    if not price_changes:
        return 0
    
    # Calculate standard deviation
    mean_change = sum(price_changes) / len(price_changes)
    variance = sum((x - mean_change) ** 2 for x in price_changes) / len(price_changes)
    volatility = variance ** 0.5
    
    return round(volatility * 100, 4)  # Return as percentage
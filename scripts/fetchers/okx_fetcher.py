import requests
from typing import List, Dict, Any

def fetch_okx_data(token: str, bar: str = "1H", limit: int = 100) -> List[List]:
    """
    Fetch klines data from OKX API for the specified token.
    
    Args:
        token: Token symbol (e.g., 'BTC-USDT')
        bar: Kline interval ('1m', '3m', '5m', '15m', '30m', '1H', '2H', '4H', '6H', '12H', '1D')
        limit: Number of klines to retrieve (max 300)
    
    Returns:
        List of klines converted to Binance-compatible format:
        [timestamp, open, high, low, close, volume, close_time, 
         quote_asset_volume, number_of_trades, taker_buy_base_asset_volume, 
         taker_buy_quote_asset_volume, ignore]
    """
    base_url = "https://www.okx.com"
    endpoint = "/api/v5/market/candles"
    
    # Ensure token is in correct format (BTC-USDT format for OKX)
    if '-' not in token:
        token = f"{token.upper()}-USDT"
    else:
        token = token.upper()
    
    params = {
        'instId': token,
        'bar': bar,
        'limit': min(limit, 300)  # OKX max limit is 300
    }
    
    try:
        response = requests.get(f"{base_url}{endpoint}", params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if data['code'] != '0':
            raise Exception(f"OKX API error: {data['msg']}")
        
        klines_raw = data['data']
        
        # Convert OKX format to Binance-compatible format
        # OKX: [timestamp, open, high, low, close, volume, volCcy, volCcyQuote, confirm]
        # Binance: [timestamp, open, high, low, close, volume, close_time, ...]
        klines_converted = []
        for kline in klines_raw:
            timestamp = int(kline[0])
            open_price = kline[1]
            high_price = kline[2]
            low_price = kline[3]
            close_price = kline[4]
            volume = kline[5]
            quote_volume = kline[6] if len(kline) > 6 else "0"
            
            # Convert to Binance format
            converted_kline = [
                timestamp,              # timestamp
                open_price,            # open
                high_price,            # high
                low_price,             # low
                close_price,           # close
                volume,                # volume
                timestamp + 3600000,   # close_time (approximate, +1 hour for 1H interval)
                quote_volume,          # quote_asset_volume
                0,                     # number_of_trades (not available)
                "0",                   # taker_buy_base_asset_volume (not available)
                "0",                   # taker_buy_quote_asset_volume (not available)
                "0"                    # ignore
            ]
            klines_converted.append(converted_kline)
        
        # Reverse to match Binance order (oldest first)
        klines_converted.reverse()
        
        return klines_converted
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"OKX API error: {str(e)}")
    except ValueError as e:
        raise Exception(f"OKX data parsing error: {str(e)}")
    except KeyError as e:
        raise Exception(f"OKX response format error: {str(e)}")

def get_okx_ticker_price(token: str) -> Dict[str, Any]:
    """
    Get current ticker price from OKX.
    
    Args:
        token: Token symbol
        
    Returns:
        Dict containing price information
    """
    base_url = "https://www.okx.com"
    endpoint = "/api/v5/market/ticker"
    
    # Ensure token is in correct format
    if '-' not in token:
        token = f"{token.upper()}-USDT"
    else:
        token = token.upper()
    
    params = {'instId': token}
    
    try:
        response = requests.get(f"{base_url}{endpoint}", params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if data['code'] != '0':
            raise Exception(f"OKX API error: {data['msg']}")
        
        if not data['data']:
            raise Exception(f"Symbol {token} not found on OKX")
        
        ticker = data['data'][0]
        
        # Convert to Binance-compatible format
        return {
            'symbol': token.replace('-', ''),
            'price': ticker['last']
        }
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"OKX API error: {str(e)}")
    except ValueError as e:
        raise Exception(f"OKX data parsing error: {str(e)}")
    except KeyError as e:
        raise Exception(f"OKX response format error: {str(e)}")

def get_okx_instrument_info(token: str) -> Dict[str, Any]:
    """
    Get instrument information from OKX.
    
    Args:
        token: Token symbol
        
    Returns:
        Dict containing instrument information
    """
    base_url = "https://www.okx.com"
    endpoint = "/api/v5/public/instruments"
    
    # Ensure token is in correct format
    if '-' not in token:
        token = f"{token.upper()}-USDT"
    else:
        token = token.upper()
    
    params = {
        'instType': 'SPOT',
        'instId': token
    }
    
    try:
        response = requests.get(f"{base_url}{endpoint}", params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if data['code'] != '0':
            raise Exception(f"OKX API error: {data['msg']}")
        
        if not data['data']:
            raise Exception(f"Symbol {token} not found on OKX")
        
        return data['data'][0]
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"OKX API error: {str(e)}")
    except ValueError as e:
        raise Exception(f"OKX data parsing error: {str(e)}")
    except KeyError as e:
        raise Exception(f"OKX response format error: {str(e)}")

def get_okx_24h_stats(token: str) -> Dict[str, Any]:
    """
    Get 24h statistics from OKX.
    
    Args:
        token: Token symbol
        
    Returns:
        Dict containing 24h statistics
    """
    base_url = "https://www.okx.com"
    endpoint = "/api/v5/market/ticker"
    
    # Ensure token is in correct format
    if '-' not in token:
        token = f"{token.upper()}-USDT"
    else:
        token = token.upper()
    
    params = {'instId': token}
    
    try:
        response = requests.get(f"{base_url}{endpoint}", params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if data['code'] != '0':
            raise Exception(f"OKX API error: {data['msg']}")
        
        if not data['data']:
            raise Exception(f"Symbol {token} not found on OKX")
        
        return data['data'][0]
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"OKX API error: {str(e)}")
    except ValueError as e:
        raise Exception(f"OKX data parsing error: {str(e)}")
    except KeyError as e:
        raise Exception(f"OKX response format error: {str(e)}")
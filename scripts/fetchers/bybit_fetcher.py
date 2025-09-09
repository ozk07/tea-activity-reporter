import requests
from typing import List, Dict, Any

def fetch_bybit_data(token: str, interval: str = "60", limit: int = 100) -> List[List]:
    """
    Fetch klines data from Bybit API for the specified token.
    
    Args:
        token: Token symbol (e.g., 'BTCUSDT')
        interval: Kline interval in minutes ('1', '5', '15', '30', '60', '240', 'D')
        limit: Number of klines to retrieve (max 200)
    
    Returns:
        List of klines converted to Binance-compatible format:
        [timestamp, open, high, low, close, volume, close_time, 
         quote_asset_volume, number_of_trades, taker_buy_base_asset_volume, 
         taker_buy_quote_asset_volume, ignore]
    """
    base_url = "https://api.bybit.com"
    endpoint = "/v5/market/kline"
    
    # Ensure token is in correct format
    if not token.upper().endswith('USDT'):
        token = f"{token.upper()}USDT"
    else:
        token = token.upper()
    
    params = {
        'category': 'spot',  # For spot trading
        'symbol': token,
        'interval': interval,
        'limit': min(limit, 200)  # Bybit max limit is 200
    }
    
    try:
        response = requests.get(f"{base_url}{endpoint}", params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if data['retCode'] != 0:
            raise Exception(f"Bybit API error: {data['retMsg']}")
        
        klines_raw = data['result']['list']
        
        # Convert Bybit format to Binance-compatible format
        # Bybit: [startTime, open, high, low, close, volume, turnover]
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
                timestamp + 60000,     # close_time (approximate)
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
        raise Exception(f"Bybit API error: {str(e)}")
    except ValueError as e:
        raise Exception(f"Bybit data parsing error: {str(e)}")
    except KeyError as e:
        raise Exception(f"Bybit response format error: {str(e)}")

def get_bybit_ticker_price(token: str) -> Dict[str, Any]:
    """
    Get current ticker price from Bybit.
    
    Args:
        token: Token symbol
        
    Returns:
        Dict containing price information
    """
    base_url = "https://api.bybit.com"
    endpoint = "/v5/market/tickers"
    
    # Ensure token is in correct format
    if not token.upper().endswith('USDT'):
        token = f"{token.upper()}USDT"
    else:
        token = token.upper()
    
    params = {
        'category': 'spot',
        'symbol': token
    }
    
    try:
        response = requests.get(f"{base_url}{endpoint}", params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if data['retCode'] != 0:
            raise Exception(f"Bybit API error: {data['retMsg']}")
        
        if not data['result']['list']:
            raise Exception(f"Symbol {token} not found on Bybit")
        
        ticker = data['result']['list'][0]
        
        # Convert to Binance-compatible format
        return {
            'symbol': token,
            'price': ticker['lastPrice']
        }
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Bybit API error: {str(e)}")
    except ValueError as e:
        raise Exception(f"Bybit data parsing error: {str(e)}")
    except KeyError as e:
        raise Exception(f"Bybit response format error: {str(e)}")

def get_bybit_symbol_info(token: str) -> Dict[str, Any]:
    """
    Get symbol information from Bybit.
    
    Args:
        token: Token symbol
        
    Returns:
        Dict containing symbol information
    """
    base_url = "https://api.bybit.com"
    endpoint = "/v5/market/instruments-info"
    
    # Ensure token is in correct format
    if not token.upper().endswith('USDT'):
        token = f"{token.upper()}USDT"
    else:
        token = token.upper()
    
    params = {
        'category': 'spot',
        'symbol': token
    }
    
    try:
        response = requests.get(f"{base_url}{endpoint}", params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if data['retCode'] != 0:
            raise Exception(f"Bybit API error: {data['retMsg']}")
        
        if not data['result']['list']:
            raise Exception(f"Symbol {token} not found on Bybit")
        
        return data['result']['list'][0]
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Bybit API error: {str(e)}")
    except ValueError as e:
        raise Exception(f"Bybit data parsing error: {str(e)}")
    except KeyError as e:
        raise Exception(f"Bybit response format error: {str(e)}")
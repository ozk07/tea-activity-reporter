import requests
from typing import List, Dict, Any

def fetch_binance_data(token: str, interval: str = "1h", limit: int = 100) -> List[List]:
    """
    Fetch klines data from Binance API for the specified token.
    
    Args:
        token: Token symbol (e.g., 'BTCUSDT')
        interval: Kline interval (e.g., '1m', '5m', '1h', '1d')
        limit: Number of klines to retrieve (max 1000)
    
    Returns:
        List of klines in format: [timestamp, open, high, low, close, volume, close_time, 
                                  quote_asset_volume, number_of_trades, taker_buy_base_asset_volume, 
                                  taker_buy_quote_asset_volume, ignore]
    """
    base_url = "https://api.binance.com"
    endpoint = "/api/v3/klines"
    
    # Ensure token is in correct format (uppercase with USDT suffix if not present)
    if not token.upper().endswith('USDT'):
        token = f"{token.upper()}USDT"
    else:
        token = token.upper()
    
    params = {
        'symbol': token,
        'interval': interval,
        'limit': limit
    }
    
    try:
        response = requests.get(f"{base_url}{endpoint}", params=params)
        response.raise_for_status()
        
        klines_data = response.json()
        return klines_data
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Binance API error: {str(e)}")
    except ValueError as e:
        raise Exception(f"Binance data parsing error: {str(e)}")

def get_binance_symbol_info(token: str) -> Dict[str, Any]:
    """
    Get symbol information from Binance.
    
    Args:
        token: Token symbol
        
    Returns:
        Dict containing symbol information
    """
    base_url = "https://api.binance.com"
    endpoint = "/api/v3/exchangeInfo"
    
    # Ensure token is in correct format
    if not token.upper().endswith('USDT'):
        token = f"{token.upper()}USDT"
    else:
        token = token.upper()
    
    try:
        response = requests.get(f"{base_url}{endpoint}")
        response.raise_for_status()
        
        exchange_info = response.json()
        
        # Find symbol info
        for symbol_info in exchange_info['symbols']:
            if symbol_info['symbol'] == token:
                return symbol_info
                
        raise Exception(f"Symbol {token} not found on Binance")
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Binance API error: {str(e)}")
    except ValueError as e:
        raise Exception(f"Binance data parsing error: {str(e)}")

def get_binance_ticker_price(token: str) -> Dict[str, Any]:
    """
    Get current ticker price from Binance.
    
    Args:
        token: Token symbol
        
    Returns:
        Dict containing price information
    """
    base_url = "https://api.binance.com"
    endpoint = "/api/v3/ticker/price"
    
    # Ensure token is in correct format
    if not token.upper().endswith('USDT'):
        token = f"{token.upper()}USDT"
    else:
        token = token.upper()
    
    params = {'symbol': token}
    
    try:
        response = requests.get(f"{base_url}{endpoint}", params=params)
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Binance API error: {str(e)}")
    except ValueError as e:
        raise Exception(f"Binance data parsing error: {str(e)}")
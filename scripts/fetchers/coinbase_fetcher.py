import requests
from typing import List, Dict, Any
import time

def fetch_coinbase_data(token: str, granularity: int = 3600, limit: int = 100) -> List[List]:
    """
    Fetch klines data from Coinbase Pro API for the specified token.
    
    Args:
        token: Token symbol (e.g., 'BTC-USD')
        granularity: Kline interval in seconds (60, 300, 900, 3600, 21600, 86400)
        limit: Number of klines to retrieve (max 300)
    
    Returns:
        List of klines converted to Binance-compatible format:
        [timestamp, open, high, low, close, volume, close_time, 
         quote_asset_volume, number_of_trades, taker_buy_base_asset_volume, 
         taker_buy_quote_asset_volume, ignore]
    """
    base_url = "https://api.exchange.coinbase.com"
    endpoint = "/products/{}/candles".format(token)
    
    # Ensure token is in correct format (BTC-USD format for Coinbase)
    if '-' not in token:
        token = f"{token.upper()}-USD"
    else:
        token = token.upper()
    
    # Calculate start and end times for the desired number of candles
    end_time = int(time.time())
    start_time = end_time - (limit * granularity)
    
    params = {
        'start': start_time,
        'end': end_time,
        'granularity': granularity
    }
    
    try:
        response = requests.get(f"{base_url}/products/{token}/candles", params=params)
        response.raise_for_status()
        
        klines_raw = response.json()
        
        if isinstance(klines_raw, dict) and 'message' in klines_raw:
            raise Exception(f"Coinbase API error: {klines_raw['message']}")
        
        # Convert Coinbase format to Binance-compatible format
        # Coinbase: [timestamp, low, high, open, close, volume]
        # Binance: [timestamp, open, high, low, close, volume, close_time, ...]
        klines_converted = []
        for kline in klines_raw:
            timestamp = int(kline[0]) * 1000  # Convert to milliseconds
            low_price = str(kline[1])
            high_price = str(kline[2])
            open_price = str(kline[3])
            close_price = str(kline[4])
            volume = str(kline[5])
            
            # Convert to Binance format
            converted_kline = [
                timestamp,                      # timestamp
                open_price,                    # open
                high_price,                    # high
                low_price,                     # low
                close_price,                   # close
                volume,                        # volume
                timestamp + (granularity * 1000),  # close_time
                "0",                           # quote_asset_volume (not available)
                0,                             # number_of_trades (not available)
                "0",                           # taker_buy_base_asset_volume (not available)
                "0",                           # taker_buy_quote_asset_volume (not available)
                "0"                            # ignore
            ]
            klines_converted.append(converted_kline)
        
        # Sort by timestamp (oldest first) to match Binance order
        klines_converted.sort(key=lambda x: x[0])
        
        return klines_converted
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Coinbase API error: {str(e)}")
    except ValueError as e:
        raise Exception(f"Coinbase data parsing error: {str(e)}")
    except (KeyError, IndexError) as e:
        raise Exception(f"Coinbase response format error: {str(e)}")

def get_coinbase_ticker_price(token: str) -> Dict[str, Any]:
    """
    Get current ticker price from Coinbase Pro.
    
    Args:
        token: Token symbol
        
    Returns:
        Dict containing price information
    """
    base_url = "https://api.exchange.coinbase.com"
    
    # Ensure token is in correct format
    if '-' not in token:
        token = f"{token.upper()}-USD"
    else:
        token = token.upper()
    
    try:
        response = requests.get(f"{base_url}/products/{token}/ticker")
        response.raise_for_status()
        
        data = response.json()
        
        if 'message' in data:
            raise Exception(f"Coinbase API error: {data['message']}")
        
        # Convert to Binance-compatible format
        return {
            'symbol': token.replace('-', ''),
            'price': data['price']
        }
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Coinbase API error: {str(e)}")
    except ValueError as e:
        raise Exception(f"Coinbase data parsing error: {str(e)}")
    except KeyError as e:
        raise Exception(f"Coinbase response format error: {str(e)}")

def get_coinbase_product_info(token: str) -> Dict[str, Any]:
    """
    Get product information from Coinbase Pro.
    
    Args:
        token: Token symbol
        
    Returns:
        Dict containing product information
    """
    base_url = "https://api.exchange.coinbase.com"
    
    # Ensure token is in correct format
    if '-' not in token:
        token = f"{token.upper()}-USD"
    else:
        token = token.upper()
    
    try:
        response = requests.get(f"{base_url}/products/{token}")
        response.raise_for_status()
        
        data = response.json()
        
        if 'message' in data:
            raise Exception(f"Coinbase API error: {data['message']}")
        
        return data
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Coinbase API error: {str(e)}")
    except ValueError as e:
        raise Exception(f"Coinbase data parsing error: {str(e)}")

def get_coinbase_24h_stats(token: str) -> Dict[str, Any]:
    """
    Get 24h statistics from Coinbase Pro.
    
    Args:
        token: Token symbol
        
    Returns:
        Dict containing 24h statistics
    """
    base_url = "https://api.exchange.coinbase.com"
    
    # Ensure token is in correct format
    if '-' not in token:
        token = f"{token.upper()}-USD"
    else:
        token = token.upper()
    
    try:
        response = requests.get(f"{base_url}/products/{token}/stats")
        response.raise_for_status()
        
        data = response.json()
        
        if 'message' in data:
            raise Exception(f"Coinbase API error: {data['message']}")
        
        return data
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Coinbase API error: {str(e)}")
    except ValueError as e:
        raise Exception(f"Coinbase data parsing error: {str(e)}")
    except KeyError as e:
        raise Exception(f"Coinbase response format error: {str(e)}")

def list_coinbase_products() -> List[Dict[str, Any]]:
    """
    List all available products on Coinbase Pro.
    
    Returns:
        List of product information dictionaries
    """
    base_url = "https://api.exchange.coinbase.com"
    
    try:
        response = requests.get(f"{base_url}/products")
        response.raise_for_status()
        
        data = response.json()
        
        if isinstance(data, dict) and 'message' in data:
            raise Exception(f"Coinbase API error: {data['message']}")
        
        return data
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Coinbase API error: {str(e)}")
    except ValueError as e:
        raise Exception(f"Coinbase data parsing error: {str(e)}")
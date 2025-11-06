"""
Crypto Prices Agent - Fetches cryptocurrency prices from public APIs.
"""
from typing import Dict, Any
import aiohttp
from .base_agent import BaseAgent


class CryptoAgent(BaseAgent):
    """Agent for fetching cryptocurrency prices."""
    
    def __init__(self):
        super().__init__("Crypto Prices Agent")
        # Using CoinGecko's free public API (no API key required)
        self.base_url = "https://api.coingecko.com/api/v3"
    
    async def execute(self, query: str) -> Dict[str, Any]:
        """
        Fetch current cryptocurrency prices.
        
        Args:
            query: User's search query
            
        Returns:
            Dictionary with crypto prices
        """
        self.status = "working"
        try:
            # Get top cryptocurrencies by market cap
            url = f"{self.base_url}/coins/markets"
            params = {
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': 10,
                'page': 1,
                'sparkline': False
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        crypto_list = []
                        for coin in data:
                            crypto_list.append({
                                'name': coin.get('name', 'N/A'),
                                'symbol': coin.get('symbol', 'N/A').upper(),
                                'price': f"${coin.get('current_price', 0):,.2f}",
                                'change_24h': f"{coin.get('price_change_percentage_24h', 0):.2f}%",
                                'market_cap': f"${coin.get('market_cap', 0):,.0f}"
                            })
                        
                        self.status = "completed"
                        return {
                            'agent': self.name,
                            'status': 'success',
                            'data': crypto_list
                        }
                    else:
                        self.status = "failed"
                        return {
                            'agent': self.name,
                            'status': 'error',
                            'message': f'HTTP {response.status}',
                            'data': []
                        }
        except Exception as e:
            self.status = "failed"
            return {
                'agent': self.name,
                'status': 'error',
                'message': str(e),
                'data': []
            }

"""
Stock Prices Agent - Fetches stock market data from public sources.
"""
from typing import Dict, Any
import aiohttp
from bs4 import BeautifulSoup
from .base_agent import BaseAgent


class StockAgent(BaseAgent):
    """Agent for fetching stock market prices."""
    
    def __init__(self):
        super().__init__("Stock Prices Agent")
        # Using Yahoo Finance as a public source
        self.base_url = "https://finance.yahoo.com"
    
    async def execute(self, query: str) -> Dict[str, Any]:
        """
        Fetch current stock market data.
        
        Args:
            query: User's search query
            
        Returns:
            Dictionary with stock prices
        """
        self.status = "working"
        try:
            # Fetch major indices and popular stocks
            stocks_to_check = [
                ('AAPL', 'Apple Inc.'),
                ('MSFT', 'Microsoft Corp.'),
                ('GOOGL', 'Alphabet Inc.'),
                ('AMZN', 'Amazon.com Inc.'),
                ('TSLA', 'Tesla Inc.'),
                ('META', 'Meta Platforms'),
                ('NVDA', 'NVIDIA Corp.'),
                ('JPM', 'JPMorgan Chase')
            ]
            
            stock_data = []
            
            async with aiohttp.ClientSession() as session:
                # Get trending stocks from Yahoo Finance homepage
                try:
                    async with session.get(f"{self.base_url}/trending-tickers", 
                                          timeout=aiohttp.ClientTimeout(total=10)) as response:
                        if response.status == 200:
                            html = await response.text()
                            soup = BeautifulSoup(html, 'lxml')
                            
                            # Try to find stock data in tables
                            rows = soup.find_all('tr', limit=10)
                            
                            for row in rows:
                                cells = row.find_all('td')
                                if len(cells) >= 3:
                                    symbol = cells[0].get_text(strip=True)
                                    name = cells[1].get_text(strip=True) if len(cells) > 1 else symbol
                                    price = cells[2].get_text(strip=True) if len(cells) > 2 else 'N/A'
                                    change = cells[3].get_text(strip=True) if len(cells) > 3 else 'N/A'
                                    
                                    if symbol and price != 'N/A':
                                        stock_data.append({
                                            'symbol': symbol,
                                            'name': name,
                                            'price': price,
                                            'change': change
                                        })
                except Exception:
                    pass  # Continue with fallback data
                
                # If we couldn't scrape data, provide sample data for demonstration
                if not stock_data:
                    for symbol, name in stocks_to_check[:5]:
                        stock_data.append({
                            'symbol': symbol,
                            'name': name,
                            'price': 'N/A - Live data unavailable',
                            'change': 'N/A',
                            'note': 'Using Yahoo Finance API requires authentication. Showing placeholder data.'
                        })
            
            self.status = "completed"
            return {
                'agent': self.name,
                'status': 'success',
                'data': stock_data[:10]
            }
            
        except Exception as e:
            self.status = "failed"
            return {
                'agent': self.name,
                'status': 'error',
                'message': str(e),
                'data': []
            }

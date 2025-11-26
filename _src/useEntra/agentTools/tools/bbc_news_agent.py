"""
BBC News Agent - Fetches latest news from BBC News website.
"""
from typing import Dict, Any
import aiohttp
from bs4 import BeautifulSoup
from .base_agent import BaseAgent


class BBCNewsAgent(BaseAgent):
    """Agent for fetching BBC News articles."""
    
    def __init__(self):
        super().__init__("BBC News Agent")
        self.base_url = "https://www.bbc.com/news"
    
    async def execute(self, query: str) -> Dict[str, Any]:
        """
        Fetch latest news from BBC News.
        
        Args:
            query: User's search query
            
        Returns:
            Dictionary with news articles
        """
        self.status = "working"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'lxml')
                        
                        articles = []
                        # Find article headlines and links
                        headlines = soup.find_all('h2', {'data-testid': 'card-headline'}, limit=5)
                        
                        if not headlines:
                            # Fallback: try different selectors
                            headlines = soup.find_all('h3', class_='gs-c-promo-heading__title', limit=5)
                        
                        for headline in headlines:
                            link_tag = headline.find_parent('a')
                            if link_tag and link_tag.get('href'):
                                url = link_tag.get('href')
                                if not url.startswith('http'):
                                    url = 'https://www.bbc.com' + url
                                
                                articles.append({
                                    'title': headline.get_text(strip=True),
                                    'url': url
                                })
                        
                        # If still no articles found, try a more general approach
                        if not articles:
                            all_links = soup.find_all('a', href=True, limit=10)
                            for link in all_links:
                                title_text = link.get_text(strip=True)
                                if len(title_text) > 20 and '/news/' in link.get('href', ''):
                                    url = link.get('href')
                                    if not url.startswith('http'):
                                        url = 'https://www.bbc.com' + url
                                    articles.append({
                                        'title': title_text[:100],
                                        'url': url
                                    })
                                    if len(articles) >= 5:
                                        break
                        
                        self.status = "completed"
                        return {
                            'agent': self.name,
                            'status': 'success',
                            'data': articles[:5] if articles else [{'title': 'No articles found', 'url': self.base_url}]
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

"""
TechCrunch News Agent - Fetches latest tech news from TechCrunch.
"""
from typing import Dict, Any
import aiohttp
from bs4 import BeautifulSoup
from .base_agent import BaseAgent


class TechCrunchAgent(BaseAgent):
    """Agent for fetching TechCrunch news articles."""
    
    def __init__(self):
        super().__init__("TechCrunch Agent")
        self.base_url = "https://techcrunch.com"
    
    async def execute(self, query: str) -> Dict[str, Any]:
        """
        Fetch latest tech news from TechCrunch.
        
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
                        # Find article headlines
                        article_links = soup.find_all('a', class_='post-block__title__link', limit=5)
                        
                        if not article_links:
                            # Fallback: try different selectors
                            article_links = soup.find_all('h2', class_='post-block__title')
                        
                        for article_link in article_links:
                            if article_link.name == 'a':
                                title = article_link.get_text(strip=True)
                                url = article_link.get('href', '')
                            else:
                                # It's an h2, find the link inside
                                link_tag = article_link.find('a')
                                if link_tag:
                                    title = link_tag.get_text(strip=True)
                                    url = link_tag.get('href', '')
                                else:
                                    continue
                            
                            if title and url:
                                articles.append({
                                    'title': title,
                                    'url': url
                                })
                        
                        # Alternative approach if no articles found
                        if not articles:
                            all_articles = soup.find_all('article', limit=5)
                            for article in all_articles:
                                title_elem = article.find(['h2', 'h3'])
                                link_elem = article.find('a', href=True)
                                if title_elem and link_elem:
                                    articles.append({
                                        'title': title_elem.get_text(strip=True),
                                        'url': link_elem.get('href')
                                    })
                        
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

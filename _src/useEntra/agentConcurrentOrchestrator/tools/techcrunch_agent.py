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
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, headers=headers, timeout=aiohttp.ClientTimeout(total=15)) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'lxml')
                        
                        articles = []
                        
                        # Strategy 1: Try multiple modern TechCrunch selectors
                        selectors = [
                            # Modern TechCrunch structure
                            ('h2', {'class': lambda x: x and 'wp-block-post-title' in str(x)}),
                            ('h3', {'class': lambda x: x and 'loop-card__title' in str(x)}),
                            ('h2', {'class': lambda x: x and 'loop-card__title' in str(x)}),
                            # Older selectors
                            ('a', {'class': 'post-block__title__link'}),
                            ('h2', {'class': 'post-block__title'}),
                            # Generic fallbacks
                            ('h2', {'class': lambda x: x and 'title' in str(x).lower()}),
                            ('h3', {'class': lambda x: x and 'title' in str(x).lower()}),
                        ]
                        
                        for tag, attrs in selectors:
                            elements = soup.find_all(tag, attrs, limit=20)
                            if elements:
                                for elem in elements:
                                    title = None
                                    url = None
                                    
                                    # Get title and URL based on element type
                                    if elem.name == 'a':
                                        title = elem.get_text(strip=True)
                                        url = elem.get('href', '')
                                    else:
                                        # It's a heading, find the link
                                        link = elem.find('a', href=True)
                                        if not link:
                                            link = elem.find_parent('a', href=True)
                                        if not link:
                                            # Look for nearby link
                                            parent = elem.parent
                                            if parent:
                                                link = parent.find('a', href=True)
                                        
                                        if link:
                                            title = elem.get_text(strip=True)
                                            url = link.get('href', '')
                                    
                                    # Validate and add article
                                    if title and url and len(title) > 10:
                                        # Make sure URL is absolute
                                        if url.startswith('/'):
                                            url = f"{self.base_url}{url}"
                                        elif not url.startswith('http'):
                                            url = f"{self.base_url}/{url}"
                                        
                                        # Avoid duplicates
                                        if not any(a['url'] == url for a in articles):
                                            articles.append({
                                                'title': title,
                                                'url': url
                                            })
                                            
                                            if len(articles) >= 10:
                                                break
                                
                                if len(articles) >= 5:
                                    break
                        
                        # Strategy 2: Try finding all links with article-like structure
                        if len(articles) < 5:
                            all_links = soup.find_all('a', href=True, limit=100)
                            for link in all_links:
                                url = link.get('href', '')
                                # Filter for article URLs
                                if '/2024/' in url or '/2025/' in url or '/20' in url:
                                    title = link.get_text(strip=True)
                                    if title and len(title) > 20 and len(title) < 200:
                                        if url.startswith('/'):
                                            url = f"{self.base_url}{url}"
                                        
                                        if not any(a['url'] == url for a in articles):
                                            articles.append({
                                                'title': title,
                                                'url': url
                                            })
                                            
                                            if len(articles) >= 10:
                                                break
                        
                        # Strategy 3: Find article tags
                        if len(articles) < 5:
                            article_tags = soup.find_all('article', limit=20)
                            for article_tag in article_tags:
                                title_elem = article_tag.find(['h1', 'h2', 'h3', 'h4'])
                                link_elem = article_tag.find('a', href=True)
                                
                                if title_elem and link_elem:
                                    title = title_elem.get_text(strip=True)
                                    url = link_elem.get('href', '')
                                    
                                    if title and url and len(title) > 10:
                                        if url.startswith('/'):
                                            url = f"{self.base_url}{url}"
                                        
                                        if not any(a['url'] == url for a in articles):
                                            articles.append({
                                                'title': title,
                                                'url': url
                                            })
                                        
                                            if len(articles) >= 10:
                                                break
                        
                        self.status = "completed"
                        
                        if len(articles) >= 5:
                            return {
                                'agent': self.name,
                                'status': 'success',
                                'data': articles[:10],
                                'count': len(articles[:10])
                            }
                        elif articles:
                            # Return whatever we found, even if less than 5
                            return {
                                'agent': self.name,
                                'status': 'success',
                                'data': articles,
                                'count': len(articles),
                                'warning': f'Only found {len(articles)} articles (expected minimum 5)'
                            }
                        else:
                            # Return debug info if no articles found
                            return {
                                'agent': self.name,
                                'status': 'success',
                                'data': [{
                                    'title': 'No articles found - website structure may have changed',
                                    'url': self.base_url
                                }],
                                'count': 0,
                                'debug': 'Try updating the CSS selectors or run test_techcrunch_agent.py with debug mode'
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

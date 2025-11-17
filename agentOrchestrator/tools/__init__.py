"""
Package initialization for agents module.
"""
from .base_agent import BaseAgent
from .bbc_news_agent import BBCNewsAgent
from .techcrunch_agent import TechCrunchAgent
from .crypto_agent import CryptoAgent
from .stock_agent import StockAgent

__all__ = [
    'BaseAgent',
    'BBCNewsAgent',
    'TechCrunchAgent',
    'CryptoAgent',
    'StockAgent'
]

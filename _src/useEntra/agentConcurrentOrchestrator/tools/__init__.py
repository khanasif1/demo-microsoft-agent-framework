"""
Package initialization for agents module.
"""
from .base_agent import BaseAgent
from .bbc_news_agent import BBCNewsAgent
from .techcrunch_agent import TechCrunchAgent

__all__ = [
    'BaseAgent',
    'BBCNewsAgent',
    'TechCrunchAgent'
]

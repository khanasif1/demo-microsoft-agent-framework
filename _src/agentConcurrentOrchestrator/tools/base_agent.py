"""
Base Agent class for the Microsoft Agent Framework demo.
This provides the foundation for all specialized agents.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
import asyncio


class BaseAgent(ABC):
    """Abstract base class for all agents in the framework."""
    
    def __init__(self, name: str):
        """
        Initialize the base agent.
        
        Args:
            name: The name identifier for this agent
        """
        self.name = name
        self.status = "ready"
    
    @abstractmethod
    async def execute(self, query: str) -> Dict[str, Any]:
        """
        Execute the agent's main task.
        
        Args:
            query: The user's query/prompt
            
        Returns:
            Dictionary containing the agent's results
        """
        pass
    
    def get_status(self) -> str:
        """Return the current status of the agent."""
        return self.status

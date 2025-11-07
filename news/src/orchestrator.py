"""
Agent Orchestrator - Manages and coordinates multiple agents running in parallel.
"""
import asyncio
from typing import List, Dict, Any
from src.agents import BBCNewsAgent, TechCrunchAgent, CryptoAgent, StockAgent


class AgentOrchestrator:
    """Orchestrates multiple agents to execute tasks in parallel."""
    
    def __init__(self):
        """Initialize the orchestrator with all available agents."""
        self.agents = {
            'bbc_news': BBCNewsAgent(),
            'techcrunch': TechCrunchAgent(),
            'crypto': CryptoAgent(),
            'stocks': StockAgent()
        }
    
    async def execute_all_agents(self, query: str) -> Dict[str, Any]:
        """
        Execute all agents in parallel.
        
        Args:
            query: The user's query/prompt
            
        Returns:
            Dictionary containing results from all agents
        """
        # Create tasks for all agents
        tasks = []
        agent_names = []
        
        for name, agent in self.agents.items():
            tasks.append(agent.execute(query))
            agent_names.append(name)
        
        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Organize results
        organized_results = {}
        for name, result in zip(agent_names, results):
            if isinstance(result, Exception):
                organized_results[name] = {
                    'agent': self.agents[name].name,
                    'status': 'error',
                    'message': str(result),
                    'data': []
                }
            else:
                organized_results[name] = result
        
        return organized_results
    
    async def execute_specific_agents(self, query: str, agent_names: List[str]) -> Dict[str, Any]:
        """
        Execute specific agents in parallel.
        
        Args:
            query: The user's query/prompt
            agent_names: List of agent names to execute
            
        Returns:
            Dictionary containing results from specified agents
        """
        tasks = []
        selected_agents = []
        
        for name in agent_names:
            if name in self.agents:
                tasks.append(self.agents[name].execute(query))
                selected_agents.append(name)
        
        if not tasks:
            return {'error': 'No valid agents selected'}
        
        # Execute selected tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Organize results
        organized_results = {}
        for name, result in zip(selected_agents, results):
            if isinstance(result, Exception):
                organized_results[name] = {
                    'agent': self.agents[name].name,
                    'status': 'error',
                    'message': str(result),
                    'data': []
                }
            else:
                organized_results[name] = result
        
        return organized_results
    
    def get_available_agents(self) -> List[str]:
        """Return list of available agent names."""
        return list(self.agents.keys())

"""
Orchestrator for BBC News Agent using Azure AI Agent Framework.

This orchestrator integrates the BBC News Agent with Azure AI Agent Client
to provide intelligent news fetching and response capabilities.
"""

import asyncio
import os
from typing import Annotated, Dict, Any, List
from dotenv import load_dotenv
from pydantic import Field

from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

from tools.bbc_news_agent import BBCNewsAgent
from tools.crypto_agent import CryptoAgent

# Load environment variables
load_dotenv()


class AgentOrchestrator:
    """Orchestrator that manages Azure AI Agent and BBC News Agent integration."""
    
    def __init__(self):
        self.bbc_agent = BBCNewsAgent()
    
    async def get_bbc_news(
        self,
        query: Annotated[str, Field(description="The user's news query or topic of interest")]
    ) -> str:
        """
        Fetch BBC news articles based on the user's query.
        
        Args:
            query: User's news query or topic
            
        Returns:
            Formatted string with news articles
        """
        try:
            # Execute the BBC news agent
            result = await self.bbc_agent.execute(query)
            print(f"*********BBC agent result: {result}")
            if result['status'] == 'success' and result['data']:
                # Format the news articles for the AI agent
                news_text = f"Here are the latest BBC news articles:\n\n"
                for i, article in enumerate(result['data'][:5], 1):
                    news_text += f"{i}. **{article['title']}**\n"
                    news_text += f"   Link: {article['url']}\n\n"
                
                return news_text
            else:
                return f"Sorry, I couldn't fetch news at the moment. Error: {result.get('message', 'Unknown error')}"
                
        except Exception as e:
            return f"Error fetching news: {str(e)}"
    
    async def get_crypto_data(
        self,
        symbol: Annotated[str, Field(description="The cryptocurrency for top coins or specific coins")]
    ) -> str:
        """
        Fetch cryptocurrency data based on the user's query.
        
        Args:
            symbol: Cryptocurrency symbol or name (e.g., 'bitcoin', 'BTC')
            
        Returns:
            Formatted string with cryptocurrency data
        """
        try:
            print(f"Fetching crypto data for: {symbol}")
            # Initialize crypto agent if not already done
            if not hasattr(self, 'crypto_agent'):
                self.crypto_agent = CryptoAgent()
            
            # Execute the crypto agent
            result = await self.crypto_agent.execute(symbol)
            print(f"********************Crypto agent result: {result}")
            return result
                
        except Exception as e:
            return f"Error fetching crypto data: {str(e)}"

    async def get_agent_responses(self, topic: str = None) -> str:
        """
        Get a news summary from the Azure AI Agent.
        
        Args:
            topic: Optional topic to focus on
            
        Returns:
            AI-generated news summary
        """
        query = f" {topic}"
        print(f"Query to agent: {query}")
        async with (
            AzureCliCredential() as credential,
            AzureAIAgentClient(
                async_credential=credential,
                project_endpoint=os.getenv("AZURE_AI_PROJECT_ENDPOINT"),
                model_deployment_name=os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME"),
            ).create_agent(
                name="IntelligentAssistant",
                instructions="""You are a helpful BBC news & crypto currency assistant. Provide concise and informative 
                summaries of the news articles and crypto currency. Focus on the most important and relevant information.""",
                tools=[self.get_bbc_news,self.get_crypto_data]
            ) as agent,
        ):
            result = await agent.run(query)
            return result

async def main():
    """Main function to run the news orchestrator."""
    
    # Check if environment variables are set
    if not os.getenv("AZURE_AI_PROJECT_ENDPOINT"):
        print("Error: AZURE_AI_PROJECT_ENDPOINT not found in environment variables.")
        print("Please create a .env file with your Azure AI configuration.")
        return
    
    if not os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME"):
        print("Error: AZURE_AI_MODEL_DEPLOYMENT_NAME not found in environment variables.")
        print("Please create a .env file with your Azure AI configuration.")
        return
    # Get user input
    user_prompt = input("Enter your query (news topic or crypto symbol): ").strip()
    if not user_prompt:
        user_prompt = None
        print("No specific topic provided. Getting general news...")
    else:
        print(f"Searching for: {user_prompt}")

    orchestrator = AgentOrchestrator()
    summary = await orchestrator.get_agent_responses(user_prompt)
    print(f"\n=== News Summary ===\n{summary}")

if __name__ == "__main__":
    asyncio.run(main())
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

# Load environment variables
load_dotenv()


class NewsOrchestrator:
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
    
    async def run_interactive_session(self):
        """Run an interactive session with the Azure AI Agent."""
        print("=== BBC News Agent with Azure AI ===")
        print("Ask me about BBC news or any news-related topics!")
        print("Type 'quit' to exit.\n")
        
        # Create Azure AI Agent with news fetching capability
        async with (
            AzureCliCredential() as credential,
            AzureAIAgentClient(
                async_credential=credential,
                project_endpoint=os.getenv("AZURE_AI_PROJECT_ENDPOINT"),
                model_deployment_name=os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME"),
            ).create_agent(
                name="BBCNewsAssistant",
                instructions="""You are a helpful BBC news assistant. You can fetch the latest BBC news articles 
                and provide intelligent summaries, analysis, and answers about current events. When users ask 
                about news, always use the get_bbc_news function to get the latest articles. You can also 
                answer general questions about the news articles you've fetched.""",
                tools=self.get_bbc_news,
            ) as agent,
        ):
            while True:
                try:
                    user_input = input("You: ").strip()
                    
                    if user_input.lower() in ['quit', 'exit', 'bye']:
                        print("Goodbye!")
                        break
                    
                    if not user_input:
                        continue
                    
                    print("Assistant: ", end="", flush=True)
                    
                    # Stream the response
                    async for chunk in agent.run_stream(user_input):
                        if chunk.text:
                            print(chunk.text, end="", flush=True)
                    
                    print("\n")
                    
                except KeyboardInterrupt:
                    print("\nGoodbye!")
                    break
                except Exception as e:
                    print(f"\nError: {str(e)}")
    
    async def get_news_summary(self, topic: str = None) -> str:
        """
        Get a news summary from the Azure AI Agent.
        
        Args:
            topic: Optional topic to focus on
            
        Returns:
            AI-generated news summary
        """
        query = f"Get me the latest BBC news about {topic}" if topic else "Get me the latest BBC news"
        
        async with (
            AzureCliCredential() as credential,
            AzureAIAgentClient(
                async_credential=credential,
                project_endpoint=os.getenv("AZURE_AI_PROJECT_ENDPOINT"),
                model_deployment_name=os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME"),
            ).create_agent(
                name="BBCNewsAssistant",
                instructions="""You are a helpful BBC news assistant. Provide concise and informative 
                summaries of the news articles. Focus on the most important and relevant information.""",
                tools=self.get_bbc_news,
            ) as agent,
        ):
            result = await agent.run(query)
            return result


# Function tools for standalone usage
async def fetch_bbc_news_tool(
    query: Annotated[str, Field(description="The user's news query or 'latest' for recent news")]
) -> str:
    """Standalone tool function to fetch BBC news."""
    orchestrator = NewsOrchestrator()
    return await orchestrator.get_bbc_news(query)


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
    
    orchestrator = NewsOrchestrator()
    
    # Example usage options
    print("Choose an option:")
    print("1. Interactive chat session")
    print("2. Get news summary")
    print("3. Fetch raw news data")
    
    choice = input("Enter your choice (1-3): ").strip()
    
    if choice == "1":
        await orchestrator.run_interactive_session()
    elif choice == "2":
        topic = input("Enter a topic (or press Enter for general news): ").strip()
        topic = topic if topic else None
        summary = await orchestrator.get_news_summary(topic)
        print(f"\n=== News Summary ===\n{summary}")
    elif choice == "3":
        result = await orchestrator.bbc_agent.execute("latest")
        print(f"\n=== Raw BBC News Data ===")
        for i, article in enumerate(result.get('data', []), 1):
            print(f"{i}. {article.get('title', 'No title')}")
            print(f"   URL: {article.get('url', 'No URL')}\n")
    else:
        print("Invalid choice. Please run the script again.")


if __name__ == "__main__":
    asyncio.run(main())
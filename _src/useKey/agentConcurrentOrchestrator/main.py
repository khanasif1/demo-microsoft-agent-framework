
import asyncio
import os
from typing import Annotated, Dict, Any, List
from dotenv import load_dotenv
from pydantic import Field


from agent_framework.azure import AzureOpenAIChatClient
from azure.identity.aio import AzureCliCredential
from agent_framework import ChatMessage, ConcurrentBuilder

from tools.bbc_news_agent import BBCNewsAgent
from tools.techcrunch_agent import TechCrunchAgent

# Load environment variables
load_dotenv()
# ---- CONFIG ----
API_KEY = os.getenv("AZURE_AI_API_KEY")
ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
DEPLOYMENT_NAME = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME")
MODEL_NAME = DEPLOYMENT_NAME   # usually same for Azure OpenAI

class AgentOrchestrator:   

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
            print(f"*********BBC agent result : {len(result)}")
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
    
    async def get_technews_data(
        self,
        symbol: Annotated[str, Field(description="The user technology news for top technology trends and events")]
    ) -> str:
        """
        Fetch technews data based on the user's query.
        
        Args:
            symbol: Technology news topic or keyword (e.g., 'AI', 'blockchain')
            
        Returns:
            Formatted string with technews data
        """
        try:
            print(f"Fetching technews data for: {symbol}")
            # Initialize technews agent if not already done
            if not hasattr(self, 'technews_agent'):
                self.technews_agent = TechCrunchAgent()
            
            # Execute the technews agent
            result = await self.technews_agent.execute(symbol)
            print(f"********************TechNews agent result: {len(result)}")
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
        
        print(f"Query to agent: {topic}")

        # ---- CLIENT USING API KEY ----
        client = AzureOpenAIChatClient(
            api_key=API_KEY,
            endpoint=ENDPOINT,
            deployment_name=DEPLOYMENT_NAME,
            model=MODEL_NAME
        )

        bbcnews_agent = client.create_agent(
            instructions=(
                "You are a helpful BBC news assistant. Provide concise and informative "
                "summaries of the news articles. Focus on the most important and relevant information news space."
            ),
            tools=[self.get_bbc_news],
            name="bbcnews",
        )

        crypto_agent = client.create_agent(
            instructions=(
                "You are a helpful technology news assistant which uses techcrunch tool. You provide concise and informative about latest technology news"
                "summaries of the technology news. Focus on the most important and relevant information from the technology news space."
            ),
            tools=[self.get_technews_data],
            name="technologynews",
        )

        # 2) Build a concurrent workflow
        # Participants are either Agents (type of AgentProtocol) or Executors
        workflow = ConcurrentBuilder().participants([bbcnews_agent, crypto_agent]).build()

        # 3) Run with a single prompt and pretty-print the final combined messages
        events = await workflow.run(topic)
        outputs = events.get_outputs()


        if outputs:
            print("===== Final Aggregated Conversation (messages) =====")
            for output in outputs:
                messages: list[ChatMessage] | Any = output
                for i, msg in enumerate(messages, start=1):
                    name = msg.author_name if msg.author_name else "user"
                    print(f"{'-' * 60}\n\n{i:02d} [{name}]:\n{msg.text}")                        

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
    # user_prompt = input("Enter your query (news topic or crypto symbol): ").strip()
    # if not user_prompt:
    #     user_prompt = None
    #     print("No specific topic provided. Getting general news...")
    # else:
    #     print(f"Searching for: {user_prompt}")
    user_prompt = "Get me latest global news and technology trends and events"

    orchestrator = AgentOrchestrator()
    summary = await orchestrator.get_agent_responses(user_prompt)
  

if __name__ == "__main__":
    asyncio.run(main())
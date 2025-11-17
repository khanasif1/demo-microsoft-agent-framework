
import asyncio
import os
from typing import Annotated, Dict, Any, List
from dotenv import load_dotenv
from pydantic import Field

from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from agent_framework import ChatMessage, ConcurrentBuilder

# Load environment variables
load_dotenv()


class AgentOrchestrator:   
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
                # project_endpoint=os.getenv("AZURE_AI_PROJECT_ENDPOINT"),
                # model_deployment_name=os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME"),
                endpoint=os.getenv("AZURE_AI_PROJECT_ENDPOINT"),
                deployment_name=os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME"),
            ) as agentClient
        ):
            researcher = agentClient.create_agent(
                instructions=(
                    "You're an expert market and product researcher. Given a prompt, provide concise, factual insights,"
                    " opportunities, and risks."
                ),
                name="researcher",
            )

            marketer = agentClient.create_agent(
                instructions=(
                    "You're a creative marketing strategist. Craft compelling value propositions and target messaging"
                    " aligned to the prompt."
                ),
                name="marketer",
            )

            legal = agentClient.create_agent(
                instructions=(
                    "You're a cautious legal/compliance reviewer. Highlight constraints, disclaimers, and policy concerns"
                    " based on the prompt."
                ),
                name="legal",
            )

            # 2) Build a concurrent workflow
            # Participants are either Agents (type of AgentProtocol) or Executors
            workflow = ConcurrentBuilder().participants([researcher, marketer, legal]).build()

            # 3) Run with a single prompt and pretty-print the final combined messages
            events = await workflow.run("We are launching a new budget-friendly electric bike for urban commuters.")
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
    user_prompt = input("Enter your query (news topic or crypto symbol): ").strip()
    if not user_prompt:
        user_prompt = None
        print("No specific topic provided. Getting general news...")
    else:
        print(f"Searching for: {user_prompt}")

    orchestrator = AgentOrchestrator()
    summary = await orchestrator.get_agent_responses(user_prompt)
  

if __name__ == "__main__":
    asyncio.run(main())
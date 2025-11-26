import asyncio
from random import randint
from typing import Annotated

# from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from agent_framework import ChatMessage
from agent_framework.azure import AzureOpenAIChatClient
from pydantic import Field
from dotenv import load_dotenv
import os

"""
Azure AI Agent Basic Example

This sample demonstrates basic usage of AzureAIAgentClient to create agents with automatic
lifecycle management. Shows both streaming and non-streaming responses with function tools.
"""


# Load environment variables from .env file
load_dotenv()
# ---- CONFIG ----
API_KEY = os.getenv("AZURE_AI_API_KEY")
ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
DEPLOYMENT_NAME = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME")
MODEL_NAME = DEPLOYMENT_NAME   # usually same for Azure OpenAI

def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    return f"The weather in {location} is {conditions[randint(0, 3)]} with a high of {randint(10, 30)}°C."


async def non_streaming_example() -> None:
    """Example of non-streaming response (get the complete result at once)."""
    print("=== Non-streaming Response Example ===")

    # ---- CLIENT USING API KEY ----
    client = AzureOpenAIChatClient(
        api_key=API_KEY,
        endpoint=ENDPOINT,
        deployment_name=DEPLOYMENT_NAME,
        model=MODEL_NAME
    )

    # ---- CREATE AGENT ----
    agent = client.create_agent(
        name="WeatherAgent",
        instructions="You are a helpful weather agent.",
        tools=get_weather,
    )
    query = input("Enter your weather query:  (eg: What's the weather like in Seattle?)")  
    print(f"User: {query}")
    response = await agent.run(query)
    print(f"Agent: {response.text}\n")
    


async def streaming_example() -> None:
    """Example of streaming response (get results as they are generated)."""
    print("=== Streaming Response Example ===")

    # Since no Agent ID is provided, the agent will be automatically created
    # and deleted after getting a response
    # For authentication, run `az login` command in terminal or replace AzureCliCredential with preferred
    # authentication option.
# ---- CLIENT USING API KEY ----
    client = AzureOpenAIChatClient(
        api_key=API_KEY,
        endpoint=ENDPOINT,
        deployment_name=DEPLOYMENT_NAME,
        model=MODEL_NAME
    )

    # ---- CREATE AGENT ----
    agent = client.create_agent(
        name="WeatherAgent",
        instructions="You are a helpful weather agent.",
        tools=get_weather,
    )
    query = input("Enter your weather query:  (eg: What's the weather like in Portland?)")
    print(f"User: {query}")
    print("Agent: ", end="", flush=True)
    async for chunk in agent.run_stream(query):
        if chunk.text:
            print(chunk.text, end="", flush=True)
    print("\n")


async def main() -> None:
    print("=== Basic Azure AI Chat Client Agent Example ===")

    await non_streaming_example()
    # await streaming_example()


if __name__ == "__main__":
    asyncio.run(main())
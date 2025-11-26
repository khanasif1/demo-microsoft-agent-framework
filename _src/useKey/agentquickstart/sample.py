import os
import asyncio
from dotenv import load_dotenv

from agent_framework import ChatMessage
from agent_framework.azure import AzureOpenAIChatClient

# Load environment variables from .env
load_dotenv()

# ---- CONFIG ----
API_KEY = os.getenv("AZURE_AI_API_KEY")
ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
DEPLOYMENT_NAME = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME")
MODEL_NAME = DEPLOYMENT_NAME   # usually same for Azure OpenAI

# Validate env vars
assert API_KEY, "AZURE_AI_API_KEY missing in .env"
assert ENDPOINT, "AZURE_AI_PROJECT_ENDPOINT missing in .env"
assert DEPLOYMENT_NAME, "AZURE_AI_MODEL_DEPLOYMENT_NAME missing in .env"

# ---- CLIENT USING API KEY ----
client = AzureOpenAIChatClient(
    api_key=API_KEY,
    endpoint=ENDPOINT,
    deployment_name=DEPLOYMENT_NAME,
    model=MODEL_NAME
)

# ---- CREATE AGENT ----
agent = client.create_agent(
    name="my-agent",
    instructions="You are a helpful assistant."
)

# ---- RUN AGENT ----
async def main():
    response = await agent.run("Give me a fun fact.")
    print("MODEL RESPONSE:", response.text)

if __name__ == "__main__":
    asyncio.run(main())

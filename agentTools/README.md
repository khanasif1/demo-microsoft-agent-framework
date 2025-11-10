# Agent Web - BBC News with Azure AI Agent Framework

This folder contains an orchestrator that integrates the BBC News Agent with Azure AI Agent Framework to provide intelligent news fetching and AI-powered responses.

## 🏗️ Architecture

The orchestrator (`orchestrator.py`) combines:
- **BBC News Agent**: Fetches latest news from BBC News website
- **Azure AI Agent Client**: Provides intelligent AI responses using Azure's language models
- **Function Tools**: Allows the AI to call the BBC news fetching function when needed

## 📋 Features

1. **Interactive Chat Session**: Chat with an AI assistant that can fetch live BBC news
2. **News Summaries**: Get AI-generated summaries of current news
3. **Raw News Data**: Access the raw BBC news articles directly
4. **Streaming Responses**: Real-time AI responses as they're generated

## 🚀 Setup

### 1. Install Dependencies

Make sure you have the Microsoft Agent Framework installed:
```bash
pip install azure-ai-agent-framework
# or if using the development version
pip install -r ../requirements.txt
```

### 2. Environment Configuration

1. Copy the example environment file:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` with your Azure AI configuration:
   ```env
   AZURE_AI_PROJECT_ENDPOINT=https://your-project.eastus.api.azureml.ms
   AZURE_AI_MODEL_DEPLOYMENT_NAME=your-deployment-name
   ```

### 3. Azure Authentication

Ensure you're logged in to Azure CLI:
```bash
az login
```

## ▶️ How to Run

Run the orchestrator:
```bash
python orchestrator.py
```

Choose from the available options:

### Option 1: Interactive Chat Session
```
Choose an option:
1. Interactive chat session
2. Get news summary  
3. Fetch raw news data
Enter your choice (1-3): 1
```

Example conversation:
```
You: What's the latest news from BBC?
Assistant: I'll fetch the latest BBC news for you...

Here are the latest BBC news articles:

1. **Breaking: Major Political Development**
   Link: https://www.bbc.com/news/politics-12345

2. **Technology: New AI Breakthrough Announced**  
   Link: https://www.bbc.com/news/technology-67890

...

You: Can you summarize the political news?
Assistant: Based on the latest articles, the main political development involves...
```

### Option 2: News Summary
Get an AI-generated summary of current news:
```
Enter your choice (1-3): 2
Enter a topic (or press Enter for general news): technology

=== News Summary ===
Here's a summary of the latest technology news from BBC:
...
```

### Option 3: Raw News Data
Get the raw news articles without AI processing:
```
Enter your choice (1-3): 3

=== Raw BBC News Data ===
1. Breaking News: Important Event
   URL: https://www.bbc.com/news/...
```

## 🔧 Code Structure

### NewsOrchestrator Class

The main orchestrator class that manages the integration:

- `get_bbc_news()`: Function tool that the AI can call to fetch news
- `run_interactive_session()`: Interactive chat interface
- `get_news_summary()`: Generate AI summaries of news

### Function Tools

The orchestrator provides the AI agent with function tools:
```python
async def get_bbc_news(query: str) -> str:
    """Fetch BBC news articles based on user query"""
```

### Agent Configuration

The Azure AI Agent is configured with specific instructions:
```python
instructions="""You are a helpful BBC news assistant. You can fetch the latest BBC news articles 
and provide intelligent summaries, analysis, and answers about current events."""
```

## 🛠️ Customization

### Adding More News Sources

You can extend the orchestrator to include more news agents:

```python
from agents.techcrunch_agent import TechCrunchAgent
from agents.crypto_agent import CryptoAgent

class NewsOrchestrator:
    def __init__(self):
        self.bbc_agent = BBCNewsAgent()
        self.tech_agent = TechCrunchAgent()
        self.crypto_agent = CryptoAgent()
    
    async def get_tech_news(self, query: str) -> str:
        """Fetch TechCrunch news"""
        # Implementation here
```

### Modifying AI Instructions

Customize the AI agent's behavior:
```python
instructions="""You are a specialized financial news assistant. Focus on business and 
economic aspects of news stories. Provide analysis and context for financial implications."""
```

### Adding More Function Tools

Extend the agent with additional capabilities:
```python
tools=[self.get_bbc_news, self.get_tech_news, self.get_crypto_news]
```

## 🔍 Troubleshooting

### Common Issues

1. **Import Error: agent_framework.azure**
   ```bash
   pip install azure-ai-agent-framework
   ```

2. **Authentication Error**
   ```bash
   az login
   az account show
   ```

3. **Environment Variables Missing**
   - Check your `.env` file exists and has correct values
   - Verify Azure AI project endpoint and deployment name

4. **BBC News Fetching Issues**
   - The BBC News Agent uses web scraping and may need updates if BBC changes their website structure
   - Check your internet connection

### Getting Help

- Review the [Azure AI Agent Framework documentation](https://github.com/microsoft/agent-framework)
- Check the main quickstart example in `../quickstart/`
- Ensure your Azure AI project and model deployment are properly configured

## 📝 Next Steps

- Integrate with other news agents (TechCrunch, Crypto, Stock)
- Add news filtering and search capabilities
- Implement news categorization and tagging
- Create a web interface for the orchestrator
- Add news sentiment analysis
- Implement news archiving and history
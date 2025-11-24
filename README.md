# 🤖 Microsoft Agent Framework - Complete Learning Repository

A comprehensive repository featuring **hands-on code samples** and **step-by-step workshop materials** for building intelligent AI agents using the Microsoft Agent Framework with Azure AI services.

[![Azure AI](https://img.shields.io/badge/Azure-AI%20Foundry-0078D4?logo=microsoft-azure)](https://ai.azure.com)
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📖 What is Microsoft Agent Framework?

The **Microsoft Agent Framework** is a powerful Python library that enables developers to build intelligent AI agents capable of:

- 🧠 **Natural Language Understanding** - Process and understand user queries
- 🔧 **Function Calling** - Execute Python functions based on AI decisions
- 🔄 **Streaming Responses** - Real-time response generation
- 🤝 **Multi-Agent Orchestration** - Coordinate multiple specialized agents
- 🎯 **Workflow Management** - Build complex agent workflows with visualization
- ☁️ **Azure Integration** - Seamless integration with Azure AI services

The framework abstracts the complexity of AI orchestration, allowing you to focus on building powerful agent capabilities while it handles:
- Authentication and credential management
- Agent lifecycle management
- Concurrent execution patterns
- Event-driven workflows
- Response streaming and aggregation

---

## 🗂️ Repository Structure

This repository is organized into **two main sections**:

### 1️⃣ [`_src/`](./_src) - Code Samples

Four production-ready sample applications demonstrating different agent patterns:

| Sample | Description | Key Pattern | Difficulty |
|--------|-------------|-------------|------------|
| [**agentquickstart**](./_src/agentquickstart) | Basic agent with function calling | Simple Agent + Tools | 🟢 Beginner |
| [**agentConcurrentOrchestrator**](./_src/agentConcurrentOrchestrator) | Web chatbot with news fetching | Fan-Out/Fan-In + Web UI | 🟡 Intermediate |
| [**agentTools**](./_src/agentTools) | Multi-agent data orchestrator | Multi-Agent + AI Routing | 🟠 Intermediate |
| [**agentVisualization**](./_src/agentVisualization) | Advanced workflow patterns | Event-Driven + Visualization | 🔴 Advanced |

➡️ **[Explore Code Samples](./_src/README.md)**

### 2️⃣ [`workshop/`](./workshop) - Step-by-Step Learning

A comprehensive, hands-on workshop with 7 progressive modules (45-60 minutes):

| Module | Title | Duration | What You'll Do |
|--------|-------|----------|----------------|
| 0 | [Introduction](./workshop/index.html) | 5 min | Workshop overview and objectives |
| 1 | [Prerequisites](./workshop/prerequisites.html) | 10 min | Install Python, Azure CLI, and tools |
| 2 | [Environment Setup](./workshop/environment-setup.html) | 8 min | Create virtual environment |
| 3 | [Azure AI Setup](./workshop/azure-setup.html) | 12 min | Configure Azure AI Foundry |
| 4 | [Code Walkthrough](./workshop/code-walkthrough.html) | 10 min | Understand agent code |
| 5 | [Running the Agent](./workshop/running-app.html) | 10 min | Execute your first agent |
| 6 | [Troubleshooting](./workshop/troubleshooting.html) | As needed | Common issues and fixes |

➡️ **[Start Workshop](./workshop/index.html)** | **[Workshop Documentation](./workshop/README.md)**

---

## 🚀 Quick Start

### Option 1: Start with Workshop (Recommended for Beginners)

Perfect if you're new to Microsoft Agent Framework:

```bash
# 1. Clone the repository
git clone https://github.com/khanasif1/demo-microsoft-agent-framework.git
cd demo-microsoft-agent-framework

# 2. Open workshop in browser
start workshop/index.html  # Windows
open workshop/index.html   # macOS
xdg-open workshop/index.html  # Linux

# 3. Follow the step-by-step guide
```

The workshop will guide you through:
- ✅ Setting up your development environment
- ✅ Configuring Azure AI services
- ✅ Understanding agent code
- ✅ Running your first agent

### Option 2: Jump into Code Samples

If you're already familiar with the basics:

```bash
# 1. Clone and navigate
git clone https://github.com/khanasif1/demo-microsoft-agent-framework.git
cd demo-microsoft-agent-framework/_src

# 2. Choose a sample
cd agentquickstart  # Start here for basics

# 3. Set up environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
# source .venv/bin/activate  # macOS/Linux

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure Azure
az login
# Create .env with your Azure AI settings

# 6. Run the sample
python azure_ai_basic.py
```

---

## 📋 Prerequisites

Before you begin, ensure you have:

| Requirement | Version | Purpose |
|-------------|---------|---------|
| **Python** | 3.8+ | Runtime environment |
| **Azure CLI** | Latest | Authentication |
| **Azure Subscription** | Active | Access to Azure AI services |
| **Text Editor** | Any | VS Code recommended |

### Azure Setup Required

1. **Azure AI Foundry** - Create an AI Hub and Project at [ai.azure.com](https://ai.azure.com)
2. **Model Deployment** - Deploy GPT-4o, GPT-4o-mini, or GPT-3.5-turbo
3. **Connection Details** - Get your project endpoint and deployment name

**Need help?** Follow the [workshop's Azure Setup module](./workshop/azure-setup.html) for detailed instructions.

---

## 🎓 Learning Path

### For Complete Beginners

```
1. Workshop Module 0-6 → 2. agentquickstart → 3. agentConcurrentOrchestrator
```

**Time:** ~2 hours total

### For Developers with Basic Knowledge

```
1. agentquickstart → 2. agentConcurrentOrchestrator → 3. agentTools
```

**Time:** ~1.5 hours

### For Advanced Developers

```
1. agentTools → 2. agentVisualization → 3. Build your own!
```

**Time:** ~1 hour

---

## 🏗️ What You'll Build

### Sample 1: Weather Agent (Quickstart)
A simple agent that calls a Python function to get weather information.

```python
query = "What's the weather in Seattle?"
# Agent automatically calls get_weather("Seattle")
# Returns: "The weather in Seattle is sunny with a high of 22°C."
```

### Sample 2: News Chatbot (Concurrent Orchestrator)
A web-based chatbot that fetches news from BBC and TechCrunch concurrently.

```
User clicks "Fetch News" 
→ Dispatcher (Fan-Out) 
→ [BBC Agent || TechCrunch Agent] (Parallel)
→ Aggregator (Fan-In)
→ Combined results in web UI
```

### Sample 3: Multi-Domain Agent (Tools)
An intelligent orchestrator that routes queries to specialized agents.

```
Query: "Latest tech news and Bitcoin price"
→ AI decides to call: get_techcrunch_news() + get_crypto_data("bitcoin")
→ Returns: Combined tech news + cryptocurrency data
```

### Sample 4: Expert Workflow (Visualization)
Advanced workflow with Research, Marketing, and Legal expert agents.

```
Prompt: "Analyze product launch"
→ [Research Agent || Marketing Agent || Legal Agent]
→ Consolidated expert analysis + Workflow diagram
```

---

## 💡 Key Features Demonstrated

### Design Patterns
- ✅ **Function Calling** - AI agents call Python functions intelligently
- ✅ **Streaming Responses** - Real-time response generation
- ✅ **Fan-Out/Fan-In** - Concurrent execution with result aggregation
- ✅ **Multi-Agent Systems** - Specialized agents working together
- ✅ **Event-Driven Architecture** - Handler-based workflow execution
- ✅ **Workflow Visualization** - Mermaid and GraphViz diagrams

### Technologies
- **Microsoft Agent Framework** - Core agent capabilities
- **Azure AI Foundry** - Cloud AI infrastructure
- **FastAPI** - Modern web framework for APIs
- **BeautifulSoup** - Web scraping capabilities
- **asyncio** - Asynchronous programming
- **Pydantic** - Data validation and settings management

---

## 📁 Detailed Documentation

### Code Samples
Each sample includes comprehensive documentation:
- Architecture diagrams (Mermaid)
- Setup instructions
- Code walkthrough
- API references
- Troubleshooting guide

➡️ **[View All Samples](./_src/README.md)**

### Workshop Materials
The workshop includes:
- Step-by-step instructions
- Platform-specific commands
- Verification checkpoints
- Visual aids and code examples
- Common issues and solutions

➡️ **[View Workshop Guide](./workshop/README.md)**

---

## 🛠️ Environment Setup

### 1. Install Python Dependencies

```bash
pip install azure-ai-agent-framework
pip install azure-identity python-dotenv pydantic
```

### 2. Configure Azure Authentication

```bash
az login
az account show
```

### 3. Set Up Environment Variables

Create `.env` file in your sample directory:

```env
AZURE_AI_PROJECT_ENDPOINT=https://your-project.region.api.azureml.ms/discovery
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4o
```

---

## 🎯 Use Cases

This repository helps you build:

- 🤖 **Chatbots** - Conversational AI assistants
- 📰 **Data Aggregators** - Fetch and combine data from multiple sources
- 🔍 **Research Assistants** - Multi-agent information gathering
- 📊 **Analysis Tools** - Expert systems with specialized agents
- 🌐 **Web Applications** - AI-powered web services
- 🔄 **Workflow Automation** - Complex multi-step processes

---

## 🐛 Troubleshooting

### Common Issues

**Authentication Error**
```bash
az logout
az login
az account show
```

**Module Not Found**
```bash
pip install -r requirements.txt
```

**Environment Variables**
```bash
# Verify .env file exists and has correct format
# No spaces, no quotes
AZURE_AI_PROJECT_ENDPOINT=https://your-endpoint.com
```

➡️ **[Complete Troubleshooting Guide](./workshop/troubleshooting.html)**

---

## 📚 Additional Resources

### Official Documentation
- [Microsoft Agent Framework Docs](https://learn.microsoft.com/azure/ai-services/)
- [Azure AI Foundry](https://ai.azure.com)
- [Azure OpenAI Service](https://azure.microsoft.com/products/ai-services/openai-service)

### Learning Materials
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Python AsyncIO Guide](https://docs.python.org/3/library/asyncio.html)
- [Azure CLI Reference](https://learn.microsoft.com/cli/azure/)

---

## 🤝 Contributing

Contributions are welcome! Whether you want to:
- Add new sample applications
- Improve workshop content
- Fix bugs or typos
- Enhance documentation

Please feel free to open issues or submit pull requests.

### Development Setup

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/demo-microsoft-agent-framework.git
cd demo-microsoft-agent-framework

# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and test
# ...

# Commit and push
git add .
git commit -m "Description of changes"
git push origin feature/your-feature-name

# Open pull request on GitHub
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🌟 Getting Started Checklist

- [ ] Clone this repository
- [ ] Choose your learning path (Workshop or Code Samples)
- [ ] Install prerequisites (Python, Azure CLI)
- [ ] Set up Azure AI Foundry account
- [ ] Deploy a GPT model in Azure
- [ ] Configure environment variables
- [ ] Run your first agent
- [ ] Explore additional samples
- [ ] Build your own agent application

---

## 📞 Support

- **Issues**: [Open an issue](https://github.com/khanasif1/demo-microsoft-agent-framework/issues)
- **Discussions**: [GitHub Discussions](https://github.com/khanasif1/demo-microsoft-agent-framework/discussions)
- **Documentation**: Check the README files in each folder

---

## 🎉 What's Next?

After completing the workshop and exploring the samples:

1. **Build Your Own Agent** - Apply what you've learned to your use case
2. **Experiment with Patterns** - Try combining different agent patterns
3. **Integrate Real APIs** - Replace mock data with real services
4. **Deploy to Production** - Learn about production deployment strategies
5. **Share Your Work** - Contribute your agent back to the community

---

**Ready to build intelligent AI agents?** 

🚀 **[Start with the Workshop →](./workshop/index.html)**  
💻 **[Explore Code Samples →](./_src/README.md)**

---

**Built with ❤️ using Microsoft Agent Framework**

*Last Updated: November 2025*

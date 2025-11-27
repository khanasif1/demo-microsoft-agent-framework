#  Agent Tools - Multi-Agent Orchestrator

AI orchestrator that intelligently routes queries to specialized agents using Entra ID authentication.

---

##  Architecture

```mermaid
graph TB
    A[User Query] --> B[AI Orchestrator]
    B --> C{Analyze Intent}
    C -.->|News| D[BBC Agent]
    C -.->|News| E[TechCrunch Agent]
    C -.->|Crypto| F[Crypto Agent]
    C -.->|Stocks| G[Stock Agent]
    
    D --> H[Web Scraping]
    E --> H
    F --> I[CoinGecko API]
    G --> J[Yahoo Finance API]
    
    H --> K[Aggregated Results]
    I --> K
    J --> K
    K --> L[User Response]
    
    style B fill:#9333EA,stroke:#7C3AED,color:#fff
    style D fill:#34a853,stroke:#0f9d58,color:#fff
    style E fill:#34a853,stroke:#0f9d58,color:#fff
    style F fill:#34a853,stroke:#0f9d58,color:#fff
    style G fill:#34a853,stroke:#0f9d58,color:#fff
    style K fill:#A855F7,stroke:#9333EA,color:#fff
```

**Key Components:**
-  **AI Orchestrator** - Intelligently routes to specialized agents
-  **News Agents** - BBC & TechCrunch web scrapers
-  **Crypto Agent** - Real-time cryptocurrency data
-  **Stock Agent** - Stock market prices
-  **Entra ID Auth** - Azure CLI authentication (no keys needed)

---

##  Clone & Setup

### 1 Navigate to Solution

```bash
cd demo-microsoft-agent-framework/_src/useEntra/agentTools
```

### 2 Authenticate with Azure CLI

```bash
az login
az account show
```

### 3 Install Dependencies

>  **Full setup instructions:** See [Main README - Getting Started](../../README.md#-getting-started) for virtual environment and package installation.

Quick setup:
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows
pip install -r ../../requirements.txt
pip install aiohttp beautifulsoup4 lxml requests
```

### 4 Configure Environment

Create `.env` file with your Azure AI project endpoint:

```env
AZURE_AI_PROJECT_ENDPOINT=https://your-project.openai.azure.com/
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4o
```

>  **Authentication Details:** [Main README - useEntra Authentication](../../README.md#option-1-useentra-entra-id-authentication)

---

##  Run & Test

### Run the Orchestrator

```bash
python orchestrator.py
```

### Expected Output

```
 AI Orchestrator Active!

Query: "Latest tech news and Bitcoin price"

 Fetching from TechCrunch...
 Fetching crypto data...

Results:
[Tech articles and Bitcoin price displayed]
```

### Test Queries

Try these multi-domain prompts:
-  "Latest tech news"
-  "Bitcoin price"
-  "BBC news headlines"
-  "Latest tech news and crypto prices"
-  "Stock prices for MSFT"

---

##  What You'll Learn

-  Build multi-agent orchestration systems
-  AI-powered intelligent routing
-  Integrate multiple APIs (CoinGecko, Yahoo Finance)
-  Web scraping with BeautifulSoup
-  Extensible agent architecture
-  Azure CLI authentication

---

** Next Step:** Try [agentVisualization](../agentVisulaization) for advanced workflow patterns!

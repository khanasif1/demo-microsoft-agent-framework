# Microsoft Agent Framework Demo

A comprehensive Python application demonstrating the Microsoft Agent Framework with a web UI and backend. The application enables users to access BBC News, TechCrunch News, cryptocurrency prices, and stock prices through specialized agents that run in parallel.

## 🌟 Features

- **Multi-Agent Architecture**: Four specialized agents working in parallel
  - 📰 **BBC News Agent**: Fetches latest news from BBC News
  - 💻 **TechCrunch Agent**: Retrieves tech news from TechCrunch
  - ₿ **Crypto Agent**: Gets cryptocurrency prices from CoinGecko API
  - 📈 **Stock Agent**: Fetches stock market data

- **Parallel Execution**: All agents execute concurrently for faster results
- **Web-based UI**: Clean, modern interface built with HTML/CSS/JavaScript
- **RESTful API**: Flask-based backend with JSON endpoints
- **Real-time Data**: Scrapes public websites and APIs for current information

## 🏗️ Architecture

```
demo-microsoft-agent-framework/
│
├── app.py                      # Flask web application (backend)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
└── src/
    ├── agents/                 # Agent implementations
    │   ├── __init__.py
    │   ├── base_agent.py       # Abstract base agent class
    │   ├── bbc_news_agent.py   # BBC News scraper agent
    │   ├── techcrunch_agent.py # TechCrunch scraper agent
    │   ├── crypto_agent.py     # Cryptocurrency price agent
    │   └── stock_agent.py      # Stock market data agent
    │
    ├── orchestrator.py         # Agent coordination and parallel execution
    │
    ├── templates/              # HTML templates
    │   └── index.html          # Main UI page
    │
    └── static/                 # Static assets
        ├── styles.css          # Application styles
        └── script.js           # Frontend JavaScript
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Internet connection (for data scraping)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/khanasif1/demo-microsoft-agent-framework.git
   cd demo-microsoft-agent-framework
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Usage

### Starting the Application

Run the Flask application:

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Using the Web Interface

1. Open your web browser and navigate to `http://localhost:5000`
2. Enter your query in the text area (e.g., "Get me the latest news and market updates")
3. Select which agents you want to activate (all are selected by default)
4. Click "🚀 Execute Agents" button
5. View results from all agents displayed in organized sections

### API Endpoints

The application provides the following REST API endpoints:

#### 1. Get Available Agents
```http
GET /api/agents
```

Response:
```json
{
  "agents": ["bbc_news", "techcrunch", "crypto", "stocks"],
  "count": 4
}
```

#### 2. Execute Query
```http
POST /api/query
Content-Type: application/json

{
  "query": "latest news",
  "agents": ["bbc_news", "techcrunch"]  // optional
}
```

Response:
```json
{
  "query": "latest news",
  "status": "success",
  "results": {
    "bbc_news": {
      "agent": "BBC News Agent",
      "status": "success",
      "data": [...]
    },
    "techcrunch": {
      "agent": "TechCrunch Agent",
      "status": "success",
      "data": [...]
    }
  }
}
```

#### 3. Health Check
```http
GET /api/health
```

Response:
```json
{
  "status": "healthy",
  "agents_available": 4
}
```

## 🔧 Configuration

### Agent Customization

Each agent can be customized by modifying its respective file in `src/agents/`:

- **BBC News Agent** (`bbc_news_agent.py`): Modify `base_url` and scraping selectors
- **TechCrunch Agent** (`techcrunch_agent.py`): Adjust scraping logic for TechCrunch
- **Crypto Agent** (`crypto_agent.py`): Change API endpoint or add more cryptocurrencies
- **Stock Agent** (`stock_agent.py`): Modify stock symbols or data sources

### Adding New Agents

1. Create a new agent class inheriting from `BaseAgent`
2. Implement the `execute()` method
3. Register the agent in `src/orchestrator.py`
4. Update the UI in `src/templates/index.html` and `src/static/script.js`

Example:
```python
from src.agents.base_agent import BaseAgent

class CustomAgent(BaseAgent):
    def __init__(self):
        super().__init__("Custom Agent")
    
    async def execute(self, query: str):
        # Your implementation here
        return {
            'agent': self.name,
            'status': 'success',
            'data': []
        }
```

## 🧪 Testing

You can test individual agents using Python:

```python
import asyncio
from src.agents import BBCNewsAgent

async def test_agent():
    agent = BBCNewsAgent()
    result = await agent.execute("latest news")
    print(result)

asyncio.run(test_agent())
```

## 📝 Technical Details

### Key Technologies

- **Flask**: Web framework for the backend API
- **asyncio/aiohttp**: Asynchronous HTTP requests for parallel execution
- **BeautifulSoup4**: HTML parsing for web scraping
- **CoinGecko API**: Free cryptocurrency data API

### Agent Framework Principles

1. **Abstraction**: All agents inherit from a common `BaseAgent` class
2. **Asynchronous Execution**: Agents use async/await for non-blocking operations
3. **Parallel Processing**: Orchestrator runs multiple agents concurrently
4. **Error Handling**: Graceful degradation when individual agents fail
5. **Modularity**: Easy to add, remove, or modify agents

## 🔒 Security & Rate Limiting

- The application scrapes public websites; respect their terms of service
- No API keys are required for the demo, but rate limits may apply
- For production use, consider:
  - Implementing caching to reduce requests
  - Adding API keys for authenticated services
  - Setting up rate limiting on your endpoints
  - Using environment variables for sensitive configuration

## 🐛 Troubleshooting

### Common Issues

1. **Module not found errors**
   - Ensure you've installed all dependencies: `pip install -r requirements.txt`
   - Verify you're in the correct directory

2. **Web scraping failures**
   - Websites may change their structure; update selectors in agent files
   - Check your internet connection
   - Some sites may block automated requests

3. **Port already in use**
   - Change the port in `app.py`: `app.run(port=5001)`

4. **Timeout errors**
   - Increase timeout values in agent files
   - Check firewall settings

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues and questions, please open an issue on the GitHub repository.

## 🎓 Educational Purpose

This project is designed for educational purposes to demonstrate:
- Multi-agent system architecture
- Parallel processing in Python
- Web scraping techniques
- RESTful API design
- Modern web UI development

---

**Note**: This is a demonstration application. For production use, consider implementing proper error handling, logging, authentication, and monitoring.

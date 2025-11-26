# 🤖 AI News Orchestrator - Chatbot API & UI

A modern chatbot system using Microsoft Agent Framework with **Fan-Out/Fan-In** concurrent execution pattern to fetch news from multiple sources (BBC News & TechCrunch).

## 🏗️ Architecture

```
┌─────────────┐
│   Web UI    │ (Modern HTML5 + JavaScript)
└──────┬──────┘
       │ HTTP POST /api/fetch-news
       ▼
┌─────────────────────────────────────┐
│      FastAPI Backend (api.py)       │
└──────┬──────────────────┬───────────┘
       │ Fan-Out          │
       ▼                  ▼
┌──────────────┐   ┌──────────────┐
│  BBC News    │   │  TechCrunch  │
│    Agent     │   │    Agent     │
└──────┬───────┘   └──────┬───────┘
       │                  │
       └────────┬─────────┘
                │ Fan-In
                ▼
         ┌──────────────┐
         │  Aggregator  │
         └──────────────┘
```

## ✨ Features

- **🚀 One-Click News Fetching**: Single button to fetch news from multiple sources
- **⚡ Concurrent Execution**: Fan-Out/Fan-In pattern for parallel news fetching
- **📊 Visual Workflow**: Real-time workflow visualization showing agent execution
- **🎨 Modern UI**: Beautiful responsive design with gradient backgrounds
- **📰 Dual News Sources**: BBC News (global) + TechCrunch (technology)
- **🔄 Real-time Updates**: Live status updates during news fetching

## 📁 Project Structure

```
agentConcurrentOrchestrator/
├── api.py                      # FastAPI backend server
├── requirements.txt            # Python dependencies
├── .env                        # Azure configuration
├── static/
│   └── index.html             # Modern UI chatbot interface
└── tools/
    ├── bbc_news_agent.py      # BBC News scraper
    └── techcrunch_agent.py    # TechCrunch scraper
```

## 🛠️ Setup Instructions

### 1. Install Dependencies

```powershell
# Navigate to the project directory
cd C:\_code\personal_github\demo-microsoft-agent-framework\agentConcurrentOrchestrator

# Install Python packages
pip install -r requirements.txt
```

### 2. Configure Azure AI

Create or verify your `.env` file:

```env
AZURE_AI_PROJECT_ENDPOINT=https://your-project.region.api.azureml.ms
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4o
```

### 3. Authenticate with Azure

```powershell
az login
az account show
```

## ▶️ Running the Application

### Start the API Server

```powershell
python api.py
```

The server will start on `http://localhost:8000`

**You'll see:**
```
🚀 Starting News Orchestrator API Server...
📡 API will be available at: http://localhost:8000
📚 API docs at: http://localhost:8000/docs
🌐 Open UI at: http://localhost:8000
```

### Access the UI

Open your browser and navigate to:

```
http://localhost:8000
```

## 🎮 How to Use

1. **Open the UI** at `http://localhost:8000`
2. **Click the button**: "🚀 Fetch Latest News from All Sources"
3. **Watch the workflow visualization** with blinking active components:
   - 📡 **Dispatcher** (Fan-Out) - Blinks when dispatching
   - **Animated arrows** - Show data flow direction
   - 📰 **BBC News Agent** & 💻 **TechCrunch Agent** - Blink during concurrent execution
   - 🔀 **Aggregator** (Fan-In) - Blinks when combining results
4. **View the results** in two sections:
   - Left: BBC News articles (teal icon)
   - Right: TechCrunch technology news (purple icon)

## 🔌 API Endpoints

### Main Endpoint

**`POST /api/fetch-news`**

Fetches news from BBC and TechCrunch concurrently.

**Response:**
```json
{
  "status": "success",
  "bbc_news": [
    {
      "title": "Article Title",
      "url": "https://bbc.com/news/..."
    }
  ],
  "tech_news": [
    {
      "title": "Tech Article Title",
      "url": "https://techcrunch.com/..."
    }
  ],
  "workflow_info": {
    "pattern": "Fan-Out / Fan-In",
    "agents": ["BBC News Agent", "TechCrunch Agent"],
    "execution": "Concurrent (Parallel)",
    "bbc_count": 5,
    "tech_count": 5,
    "total_articles": 10
  }
}
```

### Other Endpoints

- **`GET /`** - Serves the UI
- **`GET /api`** - API information
- **`GET /health`** - Health check
- **`GET /docs`** - Interactive API documentation (Swagger UI)

## 🎨 UI Features

### Modern Material Design (Dark Mode)
- Material Design 3 principles with dark theme
- Google Material Icons for visual consistency
- Smooth animations and transitions
- Responsive layout (mobile-friendly)
- Card-based news display with elevation
- Real-time loading states

### Workflow Visualization with Active Component Highlighting
- Visual representation of Fan-Out/Fan-In pattern
- **Blinking animations** to show active components being processed
- **Animated arrows** indicating data flow between stages
- Real-time status updates with Material Icons
- Color-coded execution phases:
  - **Purple (#bb86fc)** - Dispatcher and Aggregator
  - **Teal (#03dac6)** - Active agents (BBC & TechCrunch)
- Stage-by-stage execution display

### News Display
- Two-column grid layout
- Article count badges
- Clickable links to full articles
- Smooth hover effects

## 🔧 Technical Details

### Backend (FastAPI)
- **Framework**: FastAPI (async web framework)
- **Agent Framework**: Microsoft Agent Framework
- **Authentication**: Azure CLI Credential
- **Concurrency**: asyncio.gather for parallel execution
- **CORS**: Enabled for frontend access

### Frontend (HTML/JavaScript)
- **Material Design 3**: Dark theme with Material Icons
- **Pure JavaScript**: No framework dependencies
- **Fetch API**: For HTTP requests
- **CSS3**: Modern styling with keyframe animations
- **Responsive**: Mobile and desktop support
- **Blinking Animations**: Active component highlighting during execution

### Fan-Out/Fan-In Pattern
1. **Dispatcher** sends requests to multiple agents
2. **Agents** execute concurrently (parallel)
3. **Aggregator** combines results from all agents
4. **Response** returns unified data to UI

## 🐛 Troubleshooting

### Port Already in Use
```powershell
# Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Azure Authentication Error
```powershell
az logout
az login
az account show
```

### No Articles Found
- Check internet connection
- Verify website accessibility
- Run `test_techcrunch_agent.py` with debug mode

### CORS Errors
- Ensure API is running on `http://localhost:8000`
- Check browser console for errors
- Verify CORS middleware is enabled in `api.py`

## 📊 Testing

### Test Individual Agents

```powershell
# Test TechCrunch agent
python test_techcrunch_agent.py

# Choose option 2 for quick test
# Choose option 4 for HTML debug mode
```

### Test API Directly

```powershell
# Using curl
curl -X POST http://localhost:8000/api/fetch-news

# Using Python
python -c "import requests; print(requests.post('http://localhost:8000/api/fetch-news').json())"
```

### View API Documentation

Open `http://localhost:8000/docs` for interactive Swagger UI

## 🚀 Deployment

### Local Development
```powershell
python api.py
```

### Production (with Gunicorn)
```powershell
pip install gunicorn
gunicorn api:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker (Optional)
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "api.py"]
```

## 📈 Performance

- **Concurrent Execution**: ~2-3 seconds for both sources
- **Sequential would take**: ~4-6 seconds
- **Speedup**: ~50% faster with parallel execution

## 🔐 Security Notes

- Store Azure credentials securely in `.env`
- Never commit `.env` to version control
- Use environment-specific configurations
- Enable authentication for production deployments

## 📝 Future Enhancements

- [ ] Add more news sources (CNN, Reuters, etc.)
- [ ] Implement caching for better performance
- [ ] Add search/filter functionality
- [ ] User preferences and favorites
- [ ] Real-time WebSocket updates
- [ ] Export news to PDF/Email
- [ ] News categories and tags
- [ ] Sentiment analysis

## 🤝 Contributing

Feel free to open issues or submit pull requests!

## 📄 License

MIT License

---

**Made with ❤️ using Microsoft Agent Framework**

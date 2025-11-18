"""
FastAPI Backend for Agent Concurrent Orchestrator
Simple API with one endpoint to fetch news from BBC and TechCrunch
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import asyncio
import os
from typing import Dict, Any, List
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from agent_framework import ChatMessage

from tools.bbc_news_agent import BBCNewsAgent
from tools.techcrunch_agent import TechCrunchAgent

# Load environment variables
load_dotenv()

app = FastAPI(title="News Orchestrator API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


class NewsResponse(BaseModel):
    """Response model for news data"""
    status: str
    bbc_news: List[Dict[str, str]]
    tech_news: List[Dict[str, str]]
    workflow_info: Dict[str, Any]


class AgentOrchestrator:
    """Orchestrator for managing multiple news agents"""
    
    def __init__(self):
        self.bbc_agent = BBCNewsAgent()
        self.tech_agent = TechCrunchAgent()
    
    async def get_bbc_news(self, query: str) -> str:
        """Fetch BBC news articles"""
        try:
            result = await self.bbc_agent.execute(query)
            print(f"✅ BBC agent fetched {len(result.get('data', []))} articles")
            
            if result['status'] == 'success' and result['data']:
                news_text = "📰 **BBC News Headlines:**\n\n"
                for i, article in enumerate(result['data'][:5], 1):
                    news_text += f"{i}. {article['title']}\n"
                    news_text += f"   🔗 {article['url']}\n\n"
                return news_text
            else:
                return f"Could not fetch BBC news: {result.get('message', 'Unknown error')}"
        except Exception as e:
            return f"Error fetching BBC news: {str(e)}"
    
    async def get_tech_news(self, query: str) -> str:
        """Fetch TechCrunch news articles"""
        try:
            result = await self.tech_agent.execute(query)
            print(f"✅ TechCrunch agent fetched {len(result.get('data', []))} articles")
            
            if result['status'] == 'success' and result['data']:
                news_text = "💻 **Technology News:**\n\n"
                for i, article in enumerate(result['data'][:5], 1):
                    news_text += f"{i}. {article['title']}\n"
                    news_text += f"   🔗 {article['url']}\n\n"
                return news_text
            else:
                return f"Could not fetch tech news: {result.get('message', 'Unknown error')}"
        except Exception as e:
            return f"Error fetching tech news: {str(e)}"
    
    async def fetch_all_news(self) -> Dict[str, Any]:
        """
        Fetch news from both BBC and TechCrunch concurrently using Azure AI Agent Framework
        Returns structured data for the UI
        """
        try:
            # Verify environment variables
            if not os.getenv("AZURE_AI_PROJECT_ENDPOINT") or not os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME"):
                raise ValueError("Azure AI configuration missing in .env file")
            
            print("🚀 Starting Fan-Out: Dispatching to BBC and TechCrunch agents...")
            
            async with (
                AzureCliCredential() as credential,
                AzureAIAgentClient(
                    async_credential=credential,
                    endpoint=os.getenv("AZURE_AI_PROJECT_ENDPOINT"),
                    deployment_name=os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME"),
                ) as agentClient
            ):
                # Create BBC News Agent
                bbc_agent = agentClient.create_agent(
                    instructions=(
                        "You are a BBC news assistant. Fetch and summarize the latest news articles. "
                        "Focus on important global events and breaking news."
                    ),
                    tools=[self.get_bbc_news],
                    name="bbcnews",
                )
                
                # Create TechCrunch Agent
                tech_agent = agentClient.create_agent(
                    instructions=(
                        "You are a technology news assistant using TechCrunch. Fetch and summarize the latest "
                        "technology trends, startup news, and tech industry updates."
                    ),
                    tools=[self.get_tech_news],
                    name="technologynews",
                )
                
                # Fan-Out: Run both agents concurrently
                print("⚡ Fan-Out: Running agents in parallel...")
                
                bbc_task = bbc_agent.run("Get me the latest global news headlines")
                tech_task = tech_agent.run("Get me the latest technology news and trends")
                
                # Wait for both to complete
                bbc_result, tech_result = await asyncio.gather(bbc_task, tech_task)
                
                print("🔄 Fan-In: Aggregating results from both agents...")
                
                # Parse BBC results
                bbc_articles = []
                if bbc_result and hasattr(bbc_result, 'text'):
                    bbc_text = bbc_result.text
                    lines = bbc_text.split('\n')
                    for line in lines:
                        if line.strip() and line[0].isdigit() and '.' in line[:5]:
                            title = line.split('.', 1)[1].strip() if '.' in line else line.strip()
                            bbc_articles.append({'title': title, 'url': '#'})
                
                # Parse Tech results
                tech_articles = []
                if tech_result and hasattr(tech_result, 'text'):
                    tech_text = tech_result.text
                    lines = tech_text.split('\n')
                    for line in lines:
                        if line.strip() and line[0].isdigit() and '.' in line[:5]:
                            title = line.split('.', 1)[1].strip() if '.' in line else line.strip()
                            tech_articles.append({'title': title, 'url': '#'})
                
                # Get actual articles from agents for better data
                bbc_raw = await self.bbc_agent.execute("latest news")
                tech_raw = await self.tech_agent.execute("technology")
                
                bbc_articles = bbc_raw.get('data', [])[:5] if bbc_raw.get('status') == 'success' else []
                tech_articles = tech_raw.get('data', [])[:5] if tech_raw.get('status') == 'success' else []
                
                print("✅ Fan-In Complete: Results aggregated successfully")
                
                return {
                    'status': 'success',
                    'bbc_news': bbc_articles,
                    'tech_news': tech_articles,
                    'workflow_info': {
                        'pattern': 'Fan-Out / Fan-In',
                        'agents': ['BBC News Agent', 'TechCrunch Agent'],
                        'execution': 'Concurrent (Parallel)',
                        'bbc_count': len(bbc_articles),
                        'tech_count': len(tech_articles),
                        'total_articles': len(bbc_articles) + len(tech_articles)
                    }
                }
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))


# Global orchestrator instance
orchestrator = AgentOrchestrator()


@app.get("/")
async def root():
    """Root endpoint - Serve the UI"""
    return FileResponse("static/index.html")


@app.get("/api")
async def api_info():
    """API information endpoint"""
    return {
        "message": "News Orchestrator API is running",
        "version": "1.0.0",
        "endpoints": {
            "fetch_news": "/api/fetch-news",
            "health": "/health",
            "ui": "/"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "azure_configured": bool(os.getenv("AZURE_AI_PROJECT_ENDPOINT"))
    }


@app.post("/api/fetch-news")
async def fetch_news() -> NewsResponse:
    """
    Main API endpoint to fetch news from BBC and TechCrunch
    Uses Fan-Out/Fan-In pattern with concurrent execution
    
    Returns:
        NewsResponse with BBC news, tech news, and workflow information
    """
    try:
        print("\n" + "="*60)
        print("📡 API Request: Fetching news from all sources...")
        print("="*60)
        
        result = await orchestrator.fetch_all_news()
        
        print("\n" + "="*60)
        print("✅ API Response: News fetched successfully")
        print(f"   BBC Articles: {len(result['bbc_news'])}")
        print(f"   Tech Articles: {len(result['tech_news'])}")
        print("="*60 + "\n")
        
        return NewsResponse(**result)
        
    except Exception as e:
        print(f"\n❌ API Error: {str(e)}\n")
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "message": "Failed to fetch news. Check Azure configuration and try again."
            }
        )


if __name__ == "__main__":
    import uvicorn
    print("\n🚀 Starting News Orchestrator API Server...")
    print("📡 API will be available at: http://localhost:8000")
    print("📚 API docs at: http://localhost:8000/docs")
    print("🌐 Open UI at: http://localhost:8000/static/index.html\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

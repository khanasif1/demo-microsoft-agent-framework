"""
Flask Web Application - Backend server for the Microsoft Agent Framework demo.
"""
from flask import Flask, render_template, request, jsonify
import asyncio
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.orchestrator import AgentOrchestrator

app = Flask(__name__, 
            template_folder='src/templates',
            static_folder='src/static')

# Initialize the orchestrator
orchestrator = AgentOrchestrator()


@app.route('/')
def index():
    """Serve the main UI page."""
    return render_template('index.html')


@app.route('/api/agents', methods=['GET'])
def get_agents():
    """Return list of available agents."""
    agents = orchestrator.get_available_agents()
    return jsonify({
        'agents': agents,
        'count': len(agents)
    })


@app.route('/api/query', methods=['POST'])
def process_query():
    """
    Process user query and execute agents in parallel.
    
    Expected JSON payload:
    {
        "query": "user's search query",
        "agents": ["bbc_news", "techcrunch", "crypto", "stocks"] (optional)
    }
    """
    try:
        data = request.get_json()
        query = data.get('query', '')
        selected_agents = data.get('agents', None)
        
        if not query:
            return jsonify({
                'error': 'Query parameter is required'
            }), 400
        
        # Execute agents
        if selected_agents:
            results = asyncio.run(orchestrator.execute_specific_agents(query, selected_agents))
        else:
            results = asyncio.run(orchestrator.execute_all_agents(query))
        
        return jsonify({
            'query': query,
            'results': results,
            'status': 'success'
        })
    
    except Exception as e:
        # Log the full error for debugging (in production, use proper logging)
        print(f"Error processing query: {e}")
        return jsonify({
            'error': 'An error occurred while processing your request',
            'status': 'error'
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'agents_available': len(orchestrator.get_available_agents())
    })


if __name__ == '__main__':
    print("Starting Microsoft Agent Framework Demo Application...")
    print("Navigate to http://localhost:5001 to access the UI")
    app.run(debug=False, host='0.0.0.0', port=5001)

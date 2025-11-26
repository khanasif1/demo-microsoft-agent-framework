# Azure AI Agent Framework - Quick Start

This quickstart demonstrates how to use the Microsoft Agent Framework with Azure AI services to create intelligent agents that can respond to user queries and execute function calls.

## 📋 Overview

The `azure_ai_basic.py` script showcases:
- Creating AI agents with automatic lifecycle management using `AzureAIAgentClient`
- Both streaming and non-streaming response patterns
- Function calling capabilities (weather information in this example)
- Authentication using Azure CLI credentials
- Environment variable configuration for Azure AI services

## 🏗️ Code Structure

### Main Components

1. **Weather Function Tool** (`get_weather`):
   - A sample function that simulates weather data retrieval
   - Demonstrates how to create function tools that agents can call
   - Uses type annotations and Pydantic Field for proper function description

2. **Non-Streaming Example** (`non_streaming_example`):
   - Shows how to get complete responses at once
   - Uses the `agent.run()` method
   - Ideal for scenarios where you need the full response before proceeding

3. **Streaming Example** (`streaming_example`):
   - Demonstrates real-time response streaming
   - Uses the `agent.run_stream()` method
   - Perfect for interactive applications where you want to show responses as they're generated

## 🚀 Prerequisites

### 1. Azure CLI Authentication

First, install Azure CLI and log in:

```bash
# Install Azure CLI (if not already installed)
# Windows: Download from https://aka.ms/installazurecliwindows
# Or via winget:
winget install -e --id Microsoft.AzureCLI

# Log in to Azure
az login

# (Optional) Set your subscription if you have multiple
az account set --subscription "your-subscription-id"
```

### 2. Azure AI Foundry Setup

Follow these steps to create an Azure AI Foundry project and deploy a model:

#### Step 1: Create Azure AI Foundry Hub
1. Go to [Azure AI Foundry](https://ai.azure.com/)
2. Click **"+ New project"**
3. Select **"Create a new hub"** if you don't have one
4. Fill in the required details:
   - **Hub name**: `my-ai-hub` (or your preferred name)
   - **Subscription**: Select your Azure subscription
   - **Resource group**: Create new or select existing
   - **Location**: Choose a region (e.g., East US, West Europe)
5. Click **"Create"**

#### Step 2: Create AI Project
1. Once the hub is created, click **"+ New project"**
2. Fill in project details:
   - **Project name**: `weather-agent-project`
   - **Hub**: Select the hub you just created
3. Click **"Create"**

#### Step 3: Deploy a Model
1. In your AI project, go to **"Model catalog"** or **"Deployments"**
2. Click **"+ Create deployment"** or **"Deploy model"**
3. Choose a model (recommended options):
   - **GPT-4o** (latest GPT-4 Omni model)
   - **GPT-4o mini** (faster, cost-effective option)
   - **GPT-3.5 Turbo** (budget-friendly option)
4. Configure deployment:
   - **Deployment name**: `gpt-4o-deployment` (or your choice)
   - **Model version**: Use the latest available
   - **Capacity**: Start with default settings
5. Click **"Deploy"**

#### Step 4: Get Connection Details
1. Go to your project **"Overview"** or **"Settings"**
2. Copy the **"Project endpoint"** (looks like: `https://your-project.eastus.api.azureml.ms`)
3. Note your **"Deployment name"** from the deployments page

### 3. Environment Configuration

Create a `.env` file in the quickstart directory with your Azure AI configuration:

```env
# Azure AI Project Configuration
AZURE_AI_PROJECT_ENDPOINT=https://your-project.eastus.api.azureml.ms
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4o-deployment


**Important**: 
- Replace `your-project.eastus.api.azureml.ms` with your actual project endpoint
- Replace `gpt-4o-deployment` with your actual deployment name
- Never commit the `.env` file to version control (it should be in `.gitignore`)

## 📦 Installation

1. **Install Python dependencies**:
   ```bash
   pip install -r ../requirements.txt
   ```

2. **Verify your `.env` file** is properly configured with your Azure AI settings

3. **Ensure Azure CLI authentication** is working:
   ```bash
   az account show
   ```

## ▶️ How to Run

1. **Navigate to the quickstart directory**:
   ```bash
   cd quickstart
   ```

2. **Run the example**:
   ```bash
   python azure_ai_basic.py
   ```

3. **Follow the prompts**:
   - The script will run two examples sequentially
   - For each example, enter a weather-related query when prompted
   - Example queries:
     - "What's the weather like in Seattle?"
     - "Tell me about the weather in Paris"
     - "How's the weather in Tokyo today?"

## 🔧 Example Output

```
=== Basic Azure AI Chat Client Agent Example ===
=== Non-streaming Response Example ===
Enter your weather query: What's the weather like in Seattle?
User: What's the weather like in Seattle?
Agent: I'll check the weather in Seattle for you.

The weather in Seattle is cloudy with a high of 18°C.

=== Streaming Response Example ===
Enter your weather query: What's the weather like in Portland?
User: What's the weather like in Portland?
Agent: Let me check the current weather conditions in Portland for you.

The weather in Portland is sunny with a high of 25°C.
```

## 🔍 Troubleshooting

### Common Issues

1. **Authentication Error**:
   ```
   az login
   ```

2. **Missing Environment Variables**:
   - Verify your `.env` file exists and has correct values
   - Check that environment variable names match exactly

3. **Model Deployment Not Found**:
   - Verify the deployment name in Azure AI Foundry
   - Ensure the model is successfully deployed and running

4. **Connection Issues**:
   - Check your internet connection
   - Verify the project endpoint URL is correct
   - Ensure your Azure subscription is active

### Getting Help

- Check the [Azure AI documentation](https://docs.microsoft.com/azure/ai-services/)
- Visit [Azure AI Foundry documentation](https://docs.microsoft.com/azure/ai-studio/)
- Review the [Microsoft Agent Framework documentation](https://github.com/microsoft/agent-framework)
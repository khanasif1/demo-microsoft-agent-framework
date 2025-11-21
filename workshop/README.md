# 🤖 Microsoft Agent Framework Workshop

A comprehensive, hands-on workshop for learning to build AI agents using the Microsoft Agent Framework. This workshop provides step-by-step guidance suitable for developers with basic Python knowledge.

## 📚 Workshop Overview

This workshop teaches you how to:
- Set up Azure AI Foundry for agent development
- Create AI agents that can call Python functions
- Understand streaming vs non-streaming responses
- Deploy and interact with GPT-based agents
- Troubleshoot common issues

**Duration:** 45-60 minutes  
**Level:** Beginner to Intermediate  
**Prerequisites:** Basic Python knowledge

## 🚀 Quick Start

### Option 1: View Online (Recommended)
Visit the workshop website: [GitHub Pages URL will be here after publishing]

### Option 2: Run Locally
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/demo-microsoft-agent-framework.git
cd demo-microsoft-agent-framework/workshop

# Open in browser
# Windows PowerShell
start index.html

# macOS
open index.html

# Linux
xdg-open index.html
```

## 📋 Workshop Modules

The workshop is divided into 7 progressive modules:

| Module | Title | Duration | Description |
|--------|-------|----------|-------------|
| 0 | [Introduction](index.html) | 5 min | Workshop overview and learning objectives |
| 1 | [Prerequisites](prerequisites.html) | 10 min | Install Python, Azure CLI, and required tools |
| 2 | [Environment Setup](environment-setup.html) | 8 min | Create virtual environment and install dependencies |
| 3 | [Azure AI Setup](azure-setup.html) | 12 min | Configure Azure AI Foundry and deploy GPT model |
| 4 | [Code Walkthrough](code-walkthrough.html) | 10 min | Understand the agent code structure |
| 5 | [Running the Agent](running-app.html) | 10 min | Execute and interact with your first agent |
| 6 | [Troubleshooting](troubleshooting.html) | As needed | Common issues and solutions |

## 🎯 Learning Objectives

By the end of this workshop, you will:

- ✅ Understand what AI agents are and how they work
- ✅ Set up Azure AI Foundry for agent development
- ✅ Create agents that call custom Python functions
- ✅ Implement both streaming and non-streaming responses
- ✅ Deploy and test AI agents locally
- ✅ Troubleshoot common agent development issues

## 🛠️ What You'll Build

You'll create a **Weather Agent** that:
- Accepts natural language weather queries
- Intelligently calls a Python function to get weather data
- Returns responses in natural language
- Demonstrates both streaming and non-streaming modes

**Example Interaction:**
```
User: What's the weather in Seattle?
Agent: The weather in Seattle is sunny with a high of 22°C.
```

## 📦 Prerequisites

Before starting the workshop, ensure you have:

- **Python 3.8+** installed on your system
- **Azure CLI** for authentication
- **Text editor** (VS Code recommended)
- **Azure account** with an active subscription
- **Internet connection** for Azure services

Detailed installation instructions are provided in [Module 1: Prerequisites](prerequisites.html).

## 🏗️ Workshop Structure

The workshop follows a proven pedagogical pattern inspired by AWS workshops:

- **Progressive Learning:** Each module builds on the previous one
- **Hands-On Activities:** Practical exercises in every module
- **Verification Steps:** Checkpoints to ensure success before moving forward
- **Troubleshooting:** Comprehensive guide for common issues
- **Visual Design:** Clean, professional interface with clear navigation

## 🎨 Features

- **Responsive Design:** Works on desktop, tablet, and mobile
- **Dark Mode:** Comfortable viewing experience
- **Code Highlighting:** Clear syntax highlighting for code blocks
- **Navigation Sidebar:** Easy access to all modules
- **Alert Boxes:** Important information highlighted
- **Progress Tracking:** Checklists to track your progress

## 📂 Workshop Files

```
workshop/
├── index.html              # Module 0: Introduction
├── prerequisites.html      # Module 1: Tool installation
├── environment-setup.html  # Module 2: Python environment
├── azure-setup.html        # Module 3: Azure AI configuration
├── code-walkthrough.html   # Module 4: Code explanation
├── running-app.html        # Module 5: Execute the agent
├── troubleshooting.html    # Module 6: Problem solving
├── README.md              # This file
└── assets/
    └── styles.css         # Workshop styling
```

## 🔧 Technologies Used

- **Frontend:** HTML5, CSS3 (Material Design inspired)
- **Backend:** Python 3.8+
- **Framework:** Microsoft Agent Framework (`azure-ai-agent-framework`)
- **Azure Services:** Azure AI Foundry, Azure OpenAI
- **Authentication:** Azure CLI credentials
- **Environment:** Python virtual environments

## 👥 Target Audience

This workshop is designed for:

- **Python Developers** wanting to learn AI agent development
- **Students** interested in practical AI applications
- **Technical Trainers** teaching AI agent concepts
- **Azure Users** exploring Azure AI capabilities
- **Beginners** with basic Python knowledge (no AI experience required)

## 📝 Workshop Flow

```
1. Prerequisites ➜ 2. Environment Setup ➜ 3. Azure Setup
                                              ↓
6. Troubleshooting ⬅ 5. Running Agent ⬅ 4. Code Walkthrough
```

Each module includes:
- Clear learning objectives
- Step-by-step instructions
- Code examples with explanations
- Verification checkpoints
- Navigation to next/previous modules

## 🚨 Troubleshooting

If you encounter issues during the workshop:

1. Check the [Troubleshooting module](troubleshooting.html)
2. Verify all prerequisites are met
3. Ensure environment variables are correctly set
4. Confirm Azure CLI authentication is active
5. Review error messages carefully

Common issues covered:
- Authentication errors
- Missing dependencies
- Configuration mistakes
- Network/connection problems
- Permission issues

## 🤝 Contributing

Contributions to improve the workshop are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Areas for Contribution
- Additional troubleshooting scenarios
- More code examples
- Translation to other languages
- Improved styling or UX
- Bug fixes and corrections

## 📄 License

This workshop is licensed under the [MIT License](../LICENSE).

## 🔗 Related Resources

- [Microsoft Agent Framework Documentation](https://learn.microsoft.com/azure/ai-services/)
- [Azure AI Foundry](https://ai.azure.com)
- [Azure OpenAI Service](https://azure.microsoft.com/products/ai-services/openai-service)
- [Python Official Documentation](https://docs.python.org/3/)
- [Azure CLI Documentation](https://learn.microsoft.com/cli/azure/)

## 📧 Support

For questions or issues:
- Open an issue in the GitHub repository
- Review the troubleshooting guide
- Check existing documentation

## 🎓 After the Workshop

Once you complete this workshop, explore:

1. **Advanced Examples:** Check the `news/` folder for multi-agent systems
2. **Custom Functions:** Create your own function tools
3. **Real APIs:** Replace mock data with actual API calls
4. **Conversation History:** Implement multi-turn conversations
5. **Production Deployment:** Learn to deploy agents in production

## 🌟 Acknowledgments

This workshop structure is inspired by:
- AWS Workshop Studio patterns
- Microsoft Learn modules
- Hands-on teaching methodologies

Built with ❤️ for developers learning AI agent development.

---

**Ready to start?** Open [index.html](index.html) or visit the workshop website!

# HUGO - Self-Hosted JARVIS-Style AI Operating System

HUGO is a fully self-hosted AI operating system inspired by JARVIS from Iron Man. It's not a chatbot—it's a true AI assistant capable of natural voice conversations, autonomous task execution, and multi-agent collaboration.

## Features

- **🎤 Natural Voice Conversations** - Wake word detection, real-time speech-to-text/text-to-speech
- **🧠 Long-term Memory** - ChromaDB for semantic memory, PostgreSQL for persistent storage
- **🤖 Multi-Agent System** - Chief Agent, Planner, Research, Coding, Browser, Memory, Automation, File, and Security agents
- **💻 Computer Control** - Desktop automation, application control, system monitoring
- **🌐 Browser Control** - Automated web browsing, research, information gathering
- **⚙️ Workflow Automation** - Complex task orchestration and scheduling
- **📚 Personal Knowledge Base** - Local document search, semantic retrieval
- **🚀 Self-Improvement** - Agent learning and optimization
- **📊 Desktop Dashboard** - Real-time monitoring and control interface
- **🔒 Fully Secure** - Completely self-hosted, no mandatory cloud dependencies

## Architecture

```
HUGO
├── Backend (FastAPI)
│   ├── Core Engine
│   ├── Multi-Agent System
│   ├── Voice System
│   ├── Memory System
│   ├── Automation Framework
│   └── API Endpoints
├── Frontend (React)
│   ├── Dashboard
│   ├── Voice Interface
│   ├── Memory Viewer
│   └── Agent Monitor
├── Local Models
│   ├── Ollama Integration
│   ├── GGUF Support
│   └── LM Studio Support
└── Infrastructure
    ├── Docker Compose
    ├── PostgreSQL
    ├── Redis
    └── ChromaDB
```

## Supported Models

- **Ollama** - Local model management (Llama 2, Mistral, etc.)
- **GGUF** - Direct GGUF file support
- **LM Studio** - Local model server
- **Custom Models** - Bring your own LLM

## Quick Start

### Prerequisites
- Docker & Docker Compose
- 16GB+ RAM recommended
- GPU support optional but recommended

### Installation

1. Clone the repository:
```bash
git clone https://github.com/cherrstreetinfo-beep/HUGO.git
cd HUGO
```

2. Run the installation script:
```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

3. Start HUGO:
```bash
docker-compose up -d
```

4. Access the dashboard:
```
http://localhost:3000
```

## Configuration

See `config/config.yaml` for detailed configuration options.

## Agents

- **Chief Agent (Hugo)** - Main orchestrator and decision maker
- **Planner Agent** - Task planning and decomposition
- **Research Agent** - Information gathering and analysis
- **Coding Agent** - Code generation and debugging
- **Browser Agent** - Web automation and navigation
- **Memory Agent** - Memory management and retrieval
- **Automation Agent** - System task execution
- **File Agent** - File system operations
- **Security Agent** - Security monitoring and threat detection

## API Documentation

See `/docs/API.md` for complete API reference.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Installation Guide](docs/INSTALLATION.md)
- [Configuration](docs/CONFIGURATION.md)
- [API Reference](docs/API.md)
- [Voice Setup](docs/VOICE.md)
- [Agent Development](docs/AGENTS.md)
- [Deployment](docs/DEPLOYMENT.md)

## Development

```bash
# Backend development
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py

# Frontend development
cd frontend
npm install
npm start
```

## License

MIT License - See LICENSE file

## Support

For issues, questions, and discussions, please open an issue on GitHub.

---

**HUGO** - Making AI assistants truly autonomous, secure, and capable.

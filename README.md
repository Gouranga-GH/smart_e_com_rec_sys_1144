# 🛍️ E-Commerce AI Recommendation System

A sophisticated AI-powered recommendation system built with Flask, RAG (Retrieval-Augmented Generation), and modern web technologies. This system provides intelligent product recommendations based on customer reviews and product data.

## 🌟 Features

- **🤖 AI-Powered Recommendations**: Uses RAG (Retrieval-Augmented Generation) for intelligent product suggestions
- **💬 Interactive Chat Interface**: Modern, responsive web UI with real-time chat functionality
- **📊 Product Database**: Comprehensive product reviews and ratings data
- **🎨 Beautiful UI**: Vibrant gradients, animations, and modern design
- **📈 Monitoring**: Integrated Prometheus and Grafana for application monitoring
- **🐳 Containerized**: Docker support for easy deployment
- **☸️ Kubernetes Ready**: Full Kubernetes deployment configuration
- **🔒 Secure**: Environment-based configuration management

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Flask Web     │    │   AstraDB       │    │   HuggingFace   │
│   Application   │◄──►│   Vector Store  │◄──►│   Embeddings    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Groq LLM      │    │   Prometheus    │    │   Grafana       │
│   (Llama 3.1)   │    │   Monitoring    │    │   Dashboard     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Docker and Docker Compose
- Kubernetes cluster (Minikube recommended)
- API keys for:
  - AstraDB
  - Groq API
  - HuggingFace

### 1. Clone and Setup

```bash
git clone <repository-url>
cd e_com_rec_sys_1144
```

### 2. Environment Configuration

Copy the environment template and configure your API keys:

```bash
cp env_template.txt .env
```

Edit `.env` with your API keys:

```env
ASTRA_DB_API_ENDPOINT=your_astra_db_endpoint
ASTRA_DB_APPLICATION_TOKEN=your_astra_db_token
ASTRA_DB_KEYSPACE=your_keyspace
GROQ_API_KEY=your_groq_api_key
HF_TOKEN=your_huggingface_token
FLASK_DEBUG=False
FLASK_PORT=5000
```

### 3. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode
pip install -e .
```

### 4. Data Ingestion

Run the data ingestion script to create embeddings:

```bash
python ecom/data_ingestion.py
```

### 5. Run the Application

```bash
python app.py
```

Visit `http://localhost:5000` to access the chat interface.

## 🐳 Docker Deployment

### Build and Run

```bash
# Build the Docker image
docker build -t ecom-recommender .

# Run the container
docker run -p 5000:5000 --env-file .env ecom-recommender
```

## ☸️ Kubernetes Deployment

### 1. Create Kubernetes Secrets

```bash
kubectl create secret generic ecom-secrets \
  --from-literal=ASTRA_DB_API_ENDPOINT="your_endpoint" \
  --from-literal=ASTRA_DB_APPLICATION_TOKEN="your_token" \
  --from-literal=ASTRA_DB_KEYSPACE="your_keyspace" \
  --from-literal=GROQ_API_KEY="your_groq_key" \
  --from-literal=HF_TOKEN="your_hf_token"
```

### 2. Deploy Application

```bash
# Deploy Flask application
kubectl apply -f flask-deployment.yaml

# Deploy Prometheus
kubectl create namespace monitoring
kubectl apply -f prometheus/

# Deploy Grafana
kubectl apply -f grafana/
```

### 3. Access Services

```bash
# Get service URLs
kubectl get services

# Access Grafana (NodePort 32000)
# Access Prometheus (NodePort 32001)
```

## 📊 Monitoring

### Prometheus Configuration

The system includes automatic metrics collection:

- **HTTP Request Counter**: Tracks total requests
- **Custom Metrics**: Application-specific metrics
- **Health Checks**: Liveness and readiness probes

### Grafana Dashboards

Access Grafana at `http://localhost:32000` (default credentials: admin/admin) to view:

- Request rates and response times
- Error rates and availability
- Custom application metrics

## 🎨 UI Features

### Modern Chat Interface

- **Responsive Design**: Works on desktop and mobile
- **Real-time Chat**: Instant AI responses
- **Beautiful Animations**: Smooth transitions and effects
- **Dark Theme**: Easy on the eyes with white text
- **Formatted Responses**: Rich text formatting with HTML support

### Interactive Elements

- **Typing Indicators**: Shows when AI is processing
- **Auto-scroll**: Automatically scrolls to new messages
- **Clear Chat**: Reset conversation functionality
- **Error Handling**: Graceful error messages

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `ASTRA_DB_API_ENDPOINT` | AstraDB API endpoint | Yes |
| `ASTRA_DB_APPLICATION_TOKEN` | AstraDB authentication token | Yes |
| `ASTRA_DB_KEYSPACE` | Database keyspace name | Yes |
| `GROQ_API_KEY` | Groq API key for LLM | Yes |
| `HF_TOKEN` | HuggingFace token for embeddings | Yes |
| `FLASK_DEBUG` | Flask debug mode | No |
| `FLASK_PORT` | Application port | No |

### Model Configuration

The system uses:
- **Embedding Model**: `BAAI/bge-base-en-v1.5`
- **LLM**: Groq Llama 3.1-8B-instant
- **Temperature**: 0.4 (configurable)

## 📁 Project Structure

```
e_com_rec_sys_1144/
├── app.py                          # Main Flask application
├── ecom/                           # Core application package
│   ├── __init__.py
│   ├── config.py                   # Configuration management
│   ├── data_ingestion.py          # Data processing and embeddings
│   ├── rag_chain.py               # RAG chain implementation
│   └── data_converter.py          # Data format conversion
├── templates/
│   └── index.html                 # Chat interface template
├── static/
│   └── style.css                  # Modern CSS styling
├── data/
│   └── ecom_product_review.csv    # Product review dataset
├── prometheus/                    # Prometheus configuration
├── grafana/                       # Grafana configuration
├── flask-deployment.yaml          # Kubernetes deployment
├── Dockerfile                     # Docker configuration
├── requirements.txt               # Python dependencies
└── setup.py                      # Package setup
```

## 🤖 AI Features

### RAG Implementation

- **Vector Search**: Semantic similarity search in product database
- **Context Retrieval**: Relevant product information extraction
- **LLM Integration**: Groq API for natural language responses
- **Conversation Memory**: Maintains chat history for context

### Response Formatting

- **HTML Support**: Rich text formatting
- **Markdown Conversion**: Automatic formatting of responses
- **Emoji Support**: Engaging visual elements
- **List Formatting**: Automatic bullet and numbered lists

## 🔍 Troubleshooting

### Common Issues

1. **Embedding Model Issues**
   ```bash
   python troubleshoot_embeddings.py
   ```

2. **Configuration Errors**
   - Check all environment variables are set
   - Verify API keys are valid
   - Ensure AstraDB connection is working

3. **Kubernetes Issues**
   ```bash
   kubectl logs deployment/flask-app
   kubectl describe pod <pod-name>
   ```

### Debug Mode

Enable debug mode for detailed logging:

```bash
export FLASK_DEBUG=True
python app.py
```

## 🚀 Performance

### Optimizations

- **Vector Caching**: Embeddings are cached for faster retrieval
- **Connection Pooling**: Efficient database connections
- **Resource Limits**: Kubernetes resource constraints
- **Health Checks**: Automatic failure detection

### Scaling

- **Horizontal Scaling**: Multiple replicas in Kubernetes
- **Load Balancing**: Kubernetes service load balancing
- **Resource Management**: CPU and memory limits

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main chat interface |
| `/get` | POST | AI chat response |
| `/metrics` | GET | Prometheus metrics |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Gouranga** - E-Commerce AI Recommendation System

---

⭐ **Star this repository if you find it helpful!** 
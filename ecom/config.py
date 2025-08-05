import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
    ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    ASTRA_DB_KEYSPACE = os.getenv("ASTRA_DB_KEYSPACE", "default_keyspace")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    HF_TOKEN = os.getenv("HF_TOKEN")  # Added for HuggingFace embeddings
    
    # Embedding models
    EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"  # BGE model for better embeddings
    
    RAG_MODEL = "llama-3.1-8b-instant"
    
    @classmethod
    def validate_config(cls):
        """Validate that required environment variables are set"""
        missing_vars = []
        if not cls.ASTRA_DB_API_ENDPOINT:
            missing_vars.append("ASTRA_DB_API_ENDPOINT")
        if not cls.ASTRA_DB_APPLICATION_TOKEN:
            missing_vars.append("ASTRA_DB_APPLICATION_TOKEN")
        if not cls.GROQ_API_KEY:
            missing_vars.append("GROQ_API_KEY")
        if not cls.HF_TOKEN:
            missing_vars.append("HF_TOKEN")
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
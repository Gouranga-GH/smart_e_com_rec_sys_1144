"""
Alternative data ingestion using local sentence-transformers
Use this if HuggingFace API is having issues
"""

from langchain_astradb import AstraDBVectorStore
from sentence_transformers import SentenceTransformer
from langchain.embeddings import HuggingFaceEmbeddings
from ecom.data_converter import DataConverter
from ecom.config import Config

class DataIngestorLocal:
    def __init__(self):
        # Use local sentence-transformers instead of HuggingFace API
        self.embedding = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}  # Use CPU to avoid GPU issues
        )

        self.vstore = AstraDBVectorStore(
            embedding=self.embedding,
            collection_name="ecom_database",
            api_endpoint=Config.ASTRA_DB_API_ENDPOINT,
            token=Config.ASTRA_DB_APPLICATION_TOKEN,
            namespace=Config.ASTRA_DB_KEYSPACE
        )

    def ingest(self, load_existing=True):
        if load_existing == True:
            return self.vstore
        
        docs = DataConverter("data/ecom_product_review.csv").convert()
        self.vstore.add_documents(docs)
        return self.vstore 
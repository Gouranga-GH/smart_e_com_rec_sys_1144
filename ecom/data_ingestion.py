from langchain_astradb import AstraDBVectorStore
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from ecom.data_converter import DataConverter
from ecom.config import Config

class DataIngestor:
    def __init__(self):
        self.embedding = HuggingFaceEndpointEmbeddings(
            model=Config.EMBEDDING_MODEL,
            huggingfacehub_api_token=Config.HF_TOKEN,
        )

        self.vstore = AstraDBVectorStore(
            embedding=self.embedding,
            collection_name="ecom_database",
            api_endpoint=Config.ASTRA_DB_API_ENDPOINT,
            token=Config.ASTRA_DB_APPLICATION_TOKEN,
            namespace=Config.ASTRA_DB_KEYSPACE
        )

    def ingest(self,load_existing=True):
        if load_existing==True:
            return self.vstore
        
        docs = DataConverter("data/ecom_product_review.csv").convert()

        self.vstore.add_documents(docs)

        return self.vstore


if __name__ == "__main__":
    print("Starting data ingestion process...")
    print("Loading television reviews and creating embeddings...")
    
    try:
        # Initialize the data ingestor
        ingestor = DataIngestor()
        
        # Run ingestion with load_existing=False to create new embeddings
        print("Creating embeddings for television reviews...")
        vector_store = ingestor.ingest(load_existing=False)
        
        print("Data ingestion completed successfully!")
        print(f"Embeddings created and stored in AstraDB collection: ecom_database")
        
    except Exception as e:
        print(f"Error during data ingestion: {e}")
        print("Make sure your .env file has all required API keys:")
        print("   - ASTRA_DB_API_ENDPOINT")
        print("   - ASTRA_DB_APPLICATION_TOKEN") 
        print("   - HF_TOKEN")
        print("   - GROQ_API_KEY")
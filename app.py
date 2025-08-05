from flask import render_template,Flask,request,Response
from prometheus_client import Counter,generate_latest
from ecom.data_ingestion import DataIngestor
from ecom.rag_chain import RAGChainBuilder
from ecom.config import Config

from dotenv import load_dotenv
load_dotenv()

REQUEST_COUNT = Counter("http_requests_total" , "Total HTTP Request")

def create_app():

    app = Flask(__name__)

    # Validate configuration
    try:
        Config.validate_config()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("Please set the required environment variables in your .env file")
        return None

    try:
        vector_store = DataIngestor().ingest(load_existing=True)
        rag_chain = RAGChainBuilder(vector_store).build_chain()
    except Exception as e:
        print(f"Error initializing RAG system: {e}")
        print("Please check your API keys and database connection")
        return None

    @app.route("/")
    def index():
        REQUEST_COUNT.inc()
        return render_template("index.html")
    
    @app.route("/get" , methods=["POST"])
    def get_response():
        try:
            user_input = request.form["msg"]

            response = rag_chain.invoke(
                {"input" : user_input},
                config={"configurable" : {"session_id" : "user-session"}}
            )["answer"]

            return response
        except Exception as e:
            return f"Error processing request: {str(e)}"
    
    @app.route("/metrics")
    def metrics():
        return Response(generate_latest(), mimetype="text/plain")
    
    return app

if __name__=="__main__":
    app = create_app()
    if app:
        app.run(host="0.0.0.0",port=5000,debug=True)
    else:
        print("Failed to create app due to configuration errors")

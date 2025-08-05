from langchain_groq import ChatGroq
from langchain.chains import create_history_aware_retriever,create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from ecom.config import Config

class RAGChainBuilder:
    def __init__(self,vector_store):
        self.vector_store=vector_store
        self.model = ChatGroq(model=Config.RAG_MODEL , temperature=0.8)
        self.history_store={}

    def _get_history(self,session_id:str) -> BaseChatMessageHistory:
        if session_id not in self.history_store:
            self.history_store[session_id] = ChatMessageHistory()
        return self.history_store[session_id]
    
    def build_chain(self):
        retriever = self.vector_store.as_retriever(search_kwargs={"k":3})

        context_prompt = ChatPromptTemplate.from_messages([
            ("system", """Given the chat history and user question, rewrite it as a natural, standalone question that helps find relevant product information from our database.

Focus on:
- Product names, brands, or models mentioned
- Specific features or characteristics being asked about
- Price ranges or budget considerations
- Use cases and scenarios
- Customer review sentiments and experiences
- Any specific requirements or preferences mentioned

Make the question conversational and focused on finding relevant information."""),
            MessagesPlaceholder(variable_name="chat_history"), 
            ("human", "{input}")  
        ])

        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a friendly and knowledgeable AI assistant for an e-commerce platform. You help customers find the perfect products by sharing insights from customer reviews and product information.

Your personality:
- Be conversational, warm, and helpful
- Use natural language and friendly tone
- Show enthusiasm when you have great recommendations
- Be empathetic to customer needs
- Use emojis occasionally to make responses more engaging

When you have relevant product information from the context, share it enthusiastically and provide detailed recommendations. If you don't have specific information about a product, you can provide general advice and suggestions based on your knowledge, but always be honest about what you know and don't know.

CONTEXT: {context}

QUESTION: {input}

Be helpful, informative, and engaging in your responses!"""),
            MessagesPlaceholder(variable_name="chat_history"), 
            ("human", "{input}")  
        ])

        history_aware_retriever = create_history_aware_retriever(
            self.model , retriever , context_prompt
        )

        question_answer_chain = create_stuff_documents_chain(
            self.model , qa_prompt
        )

        rag_chain = create_retrieval_chain(
            history_aware_retriever,question_answer_chain
        )

        return RunnableWithMessageHistory(
            rag_chain,
            self._get_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )




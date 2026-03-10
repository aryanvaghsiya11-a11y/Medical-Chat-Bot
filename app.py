from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from pinecone import Pinecone
from langchain_google_genai import GoogleGenerativeAI
from langchain_classic.chains import create_retrieval_chain, create_history_aware_retriever
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from src.prompt import system_prompt
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

embeddings = download_hugging_face_embeddings()

index_name = "medicalbot"

# Connect to Pinecone using v3 client directly
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(index_name)

# Custom retriever that queries Pinecone directly
from langchain_core.retrievers import BaseRetriever
from typing import List
from pydantic import Field

class PineconeRetriever(BaseRetriever):
    """Custom retriever using Pinecone client directly."""
    embeddings_model: object = Field(default=None)
    pinecone_index: object = Field(default=None)
    top_k: int = 3

    class Config:
        arbitrary_types_allowed = True

    def _get_relevant_documents(self, query: str) -> List[Document]:
        query_embedding = self.embeddings_model.embed_query(query)
        results = self.pinecone_index.query(
            vector=query_embedding,
            top_k=self.top_k,
            include_metadata=True
        )
        documents = []
        for match in results['matches']:
            metadata = match.get('metadata', {})
            page_content = metadata.pop('text', metadata.pop('page_content', ''))
            documents.append(Document(page_content=page_content, metadata=metadata))
        return documents

retriever = PineconeRetriever(
    embeddings_model=embeddings,
    pinecone_index=index,
    top_k=3
)

from langchain_classic.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder

llm = GoogleGenerativeAI(model="models/gemini-2.5-flash")

# Memory 1: Contextualize question prompt
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)

# Memory 2: Answer question prompt
qa_system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise.\n\n"
    "{context}"
)
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

# Global chat history (for demonstration purposes - single session)
chat_history = []


@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    global chat_history
    msg = request.form["msg"]
    input_text = msg
    print("User Input:", input_text)
    
    response = rag_chain.invoke({
        "input": input_text,
        "chat_history": chat_history
    })
    
    answer = response["answer"]
    print("Response:", answer)
    
    # Update chat history with the current turn
    chat_history.extend([
        ("human", input_text),
        ("assistant", answer)
    ])
    
    return str(answer)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
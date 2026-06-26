# services/query_service.py
import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser 
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_mistralai import MistralAIEmbeddings

load_dotenv()


CHROMA_DIR = "./data/chroma_db"


embeddings = MistralAIEmbeddings(model="mistral-embed")


def search_and_generate_answer(question: str) -> dict:
    """
    Queries ChromaDB for relevant context chunks, packages them into a clean prompt,
    and invokes the Mistral model to return a context-aware answer.
    """
    
    if not os.path.exists(CHROMA_DIR):
        raise FileNotFoundError(
            "Vector database is empty or the path is incorrect. Please ingest a document first."
        )

    
    db = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    
   
    retriever = db.as_retriever(search_kwargs={"k": 3})
    relevant_docs = retriever.invoke(question)

   
    context = "\n\n".join([doc.page_content for doc in relevant_docs])

  
    llm = HuggingFaceEndpoint(
        repo_id="meta-llama/Llama-3.1-8B-Instruct",
        task="text-generation",
        max_new_tokens=512,
        do_sample=False,
    )
    chat_model = ChatHuggingFace(llm=llm)

    
    messages = [
        SystemMessage(
            content=(
                "You are an advanced AI research assistant. Answer the user's question "
                "using ONLY the following retrieved context blocks. If the answer cannot "
                "be found in the context, say that you do not know the answer.\n\n"
                f"Context:\n{context}"
            )
        ),
        HumanMessage(content=question),
    ]

    
    chain = chat_model | StrOutputParser()
    clean_answer = chain.invoke(messages)

    
    sources = [doc.metadata.get("source", "Unknown Source") for doc in relevant_docs]

   
    return {
        "answer": clean_answer,
        "sources": list(set(sources)),  
    }
import os
import faiss
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from config import Config


def initialize_vector_store():
    """
    Initializes and returns a FAISS vector store.
    This function sets up the Ollama embeddings with the specified model and base URL, 
    creates a FAISS index and initializes the FAISS vector store.
    If a local vector store with the name does not 
    exist, it saves a new one. Otherwise, it loads the existing vector store from 
    the local storage.
    Returns:
        FAISS: The initialized FAISS vector store.
    """
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text", base_url="http://localhost:11434")
    single_vector = embeddings.embed_query("this is some text data")
    index = faiss.IndexFlatL2(len(single_vector))
    db_name = Config.FAISS_DB_NAME
    vector_store = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )
    if not os.path.exists(f"./{db_name}"):
        vector_store.save_local(db_name)
    else:
        vector_store = FAISS.load_local(
            db_name, embeddings=embeddings, allow_dangerous_deserialization=True)

    return vector_store


def process_and_store_file(file, vectore_store: FAISS):
    """
    Processes a file and stores its contents in a FAISS vector store.
    Args:
        file (str): The path to the file to be processed.
        vectore_store (FAISS): An instance of the FAISS vector store.
    Returns:
        None
    """
    loader = PyMuPDFLoader(file)
    pages = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(pages)

    vectore_store.add_documents(documents=chunks)
    vectore_store.save_local("test_db")


def ask_question(question, vector_store: FAISS):
    """
    Asks a question to the vector store and retrieves an answer using a language model.
    This function performs the following steps:
    1. Searches the vector store for similar documents based on the input question.
    2. Uses a retriever to fetch relevant context from the vector store.
    3. Constructs a prompt for the language model using the retrieved context and the input question.
    4. Invokes the language model to generate an answer based on the constructed prompt.
    Args:
        question (str): The question to be asked.
        vector_store (FAISS): An instance of the FAISS vector store used for searching and retrieving documents.
    Returns:
        str: The answer generated by the language model.
    """
    search_results = vector_store.search(question, search_type="similarity")
    retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={
                                          'k': 3, 'fetch_k': 100, 'lambda_mult': 1})
    model = ChatOllama(
        model="llama3.2:1b",
        base_url="http://localhost:11434"
    )
    prompt = """
    You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know.
    Make sure your answer is relevant to the question and it is answered from the context only.
    Question: {question} 
    Context: {context} 
    Answer:
    """
    prompt = ChatPromptTemplate.from_template(prompt)

    def format_docs(search_results):
        """
        Format the search results as a string. 
        This function is used because rag_chain exptects a runnable
        """
        return "\n\n".join([result.page_content for result in search_results])

    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | model
        | StrOutputParser()
    )

    answer = rag_chain.invoke(question)

    return answer

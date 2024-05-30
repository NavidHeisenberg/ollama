from langchain_community.document_loaders import OnlinePDFLoader
from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community import embeddings
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA
from langchain_community.embeddings import OllamaEmbeddings
import sys
import os
# import pdfminer
# import pdfminer.high_level

class SuppressStdout:
    def __enter__(self):
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr

# load the pdf and split it into chunks
loader = OnlinePDFLoader("https://d18rn0p25nwr6d.cloudfront.net/CIK-0001813756/975b>data = loader.load()

from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)

# Switched GPT4AllEmbedding with OllamaEmbeddings
with SuppressStdout():
    vectorstore = Chroma.from_documents(
        documents=all_splits,
        embedding=embeddings.ollama.OllamaEmbeddings(model="nomic-embed-text"),
    )

while True:
    query = input("\nQuery: ")
    if query == "exit":
        break
    if query.strip() == "":
        continue

    # Prompt
    template = """Use the following pieces of context to answer the question at the>    If you don't know the answer, just say that you don't know, don't try to make u>    Use three sentences maximum and keep the answer as concise as possible.
    {context}
    Question: {question}
    Helpful Answer:"""
    QA_CHAIN_PROMPT = PromptTemplate(
        input_variables=["context", "question"],
        template=template,
    )

    llm = Ollama(model="llama3:8b", callback_manager=CallbackManager([StreamingStdO>    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
    )

    result = qa_chain({"query": query})

#reading our pdfs

from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyPDFDirectoryLoader


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)
loader = PyPDFDirectoryLoader("docs")
documents = loader.load()

print(len(documents))


chunks = text_splitter.split_documents(documents)
print(chunks[0].metadata)

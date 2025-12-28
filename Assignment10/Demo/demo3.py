from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


loader = PyPDFLoader("resume-001.pdf")

documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(documents)
for i, chunk in enumerate(texts):
    print(f"Chunk {i+1}:\n{chunk.page_content}\n")

    
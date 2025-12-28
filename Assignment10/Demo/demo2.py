from langchain_text_splitters import CharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

#texts_splitter = CharacterTextSplitter(chunk_size=150,
#                                    chunk_overlap=20,
#                                    separator=" ")



texts_splitter = RecursiveCharacterTextSplitter(chunk_size=150,
                                                chunk_overlap=20,
                                                separators=["\n\n", "\n", " ", ""])

text=["""A computer is a machine that can be programmed to automatically carry out sequences of arithmetic or logical operations (computation). Modern digital electronic computers  functions"""]

chunks = texts_splitter.split_text(text[0])
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}:\n{chunk}\n")
    

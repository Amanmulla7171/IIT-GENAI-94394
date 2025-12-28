from langchain.embeddings import init_embeddings

embed_model = init_embeddings(
    model="text-embedding-nomic-embed-text-v1.5",
    provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="null key",
    check_embedding_ctx_length=False
)

texts = ["Hello world", "Bonjour le monde"]
embeddings = embed_model.embed_documents(texts)

for text, embedding in zip(texts, embeddings):
    print(f"Text: {text}\nEmbedding: {embedding}\n")
    
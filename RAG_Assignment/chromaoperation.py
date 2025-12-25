import chromadb
from embeddin import get_embeddings  

db = chromadb.PersistentClient(path="./knowledge_base")
collection = db.get_or_create_collection("resumes")


def add_resume_to_db(resume_id, texts, metadata_list, embeddings):
    """
    Add multiple chunks for a resume.
    - resume_id: string for candidate resume
    - texts: list of chunk strings
    - metadata_list: list of dicts, same length as texts
      each metadata must include at least {'resume_id': resume_id, 'chunk_index': i}
    """
    

    ids = [f"{resume_id}_chunk_{i}" for i in range(len(texts))]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        metadatas=metadata_list,
        documents=texts,
    )


def search_resumes(query_text, n_results=5):
    """
    Search similar chunks for a job description.
    - query_text: raw text of job description
    Returns raw Chroma result dict.
    """
    # Embed query text
    query_embedding = get_embeddings([query_text])[0]

    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )
    # result has keys: ids, documents, metadatas, distances [web:32][web:33]
    return result


def delete_resume_from_db(resume_id):
    """
    Delete all chunks for a given resume_id using metadata filter.
    """
    collection.delete(where={"resume_id": {"$eq": resume_id}})

def get_resume_intro(resume_id):
    results = collection.get(
        where={"resume_id": resume_id}
    )

    documents = results.get("documents", [])
    metadatas = results.get("metadatas", [])

    for doc, meta in zip(documents, metadatas):
        if meta.get("chunk_index") == 0:
            return doc

    return ""







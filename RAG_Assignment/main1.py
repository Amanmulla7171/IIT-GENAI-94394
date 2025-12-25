import os
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage

from pdfoperation import load_pdf_resume, split_resume_text
from embeddin import get_embeddings
from chromaoperation import (
    add_resume_to_db,
    search_resumes,
    get_resume_intro,
    delete_resume_from_db,
    
       
)


load_dotenv()

if "llm" not in st.session_state:
    st.session_state.llm = init_chat_model(
        model="openai/gpt-oss-120b",
        model_provider="openai",
        base_url="https://api.groq.com/openai/v1",
        api_key=os.getenv("GROQ_API_KEY"),
    )

llm = st.session_state.llm


if "resumes" not in st.session_state:
    st.session_state.resumes = []

if "show_manage" not in st.session_state:
    st.session_state.show_manage = False

if "show_all_resumes" not in st.session_state:
    st.session_state.show_all_resumes = False



def deduplicate_and_rank(docs, metas, dists):
    """
    Strict ATS-style deduplication:
    - One resume = one result
    - First (best-ranked) chunk wins
    """
    seen_resumes = set()
    unique_results = []

    for doc, meta, dist in zip(docs, metas, dists):
        resume_id = meta.get("resume_id")

        if not resume_id:
            continue

        if resume_id in seen_resumes:
            continue  # 🚫 block duplicates forever

        seen_resumes.add(resume_id)

        unique_results.append({
            "doc": doc,
            "meta": meta,
            "dist": dist
        })

    return unique_results



def explain_match(job_description: str, resume_chunk: str) -> str:
    messages = [
        SystemMessage(
            content=(
                "You are an HR AI assistant. "
                "Explain clearly and professionally why a resume matches the job."
            )
        ),
        HumanMessage(
            content=(
                f"Job Description:\n{job_description}\n\n"
                f"Resume Snippet:\n{resume_chunk}\n\n"
                "Explain in 3–4 concise bullet points."
            )
        ),
    ]

    response = llm.invoke(messages)
    return response.content


st.set_page_config(
    page_title="AI Resume Shortlisting System",
    layout="wide",
)

st.title("AI Resume Shortlisting System")
st.caption(
    "Upload resumes, index them using embeddings + ChromaDB, "
    "and shortlist candidates with AI explanations."
)


with st.sidebar:
    st.header("Resume Management")

    uploaded_pdf = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"],
    )

    if uploaded_pdf:
        temp_path = f"./temp_{uploaded_pdf.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_pdf.getbuffer())

        if st.button("Index Resume", use_container_width=True):
            try:
                resume_text, meta = load_pdf_resume(temp_path)
                chunks = split_resume_text(resume_text)

                texts = [f"search_document: {c}" for c in chunks]
                embeddings = get_embeddings(texts)

                resume_id = Path(uploaded_pdf.name).stem

                metadatas = [
                    {
                        "resume_id": resume_id,
                        "source": meta["source"],
                        "page_count": meta["page_count"],
                        "chunk_index": i,
                    }
                    for i in range(len(chunks))
                ]

                add_resume_to_db(
                    resume_id=resume_id,
                    texts=chunks,
                    metadata_list=metadatas,
                    embeddings=embeddings,
                )

                st.session_state.resumes.append(
                    {"resume_id": resume_id, "source": meta["source"]}
                )

                st.success(f"Resume **{resume_id}** indexed successfully.")

            except Exception as e:
                st.error(str(e))

    if st.button("Manage Resumes", use_container_width=True):
        st.session_state.show_manage = not st.session_state.show_manage
    if st.button("View All Resumes", use_container_width=True):
        st.session_state.show_all_resumes = True


if st.session_state.show_manage:
    st.subheader("Indexed Resumes")

    if not st.session_state.resumes:
        st.info("No resumes indexed yet.")
    else:
        for resume in st.session_state.resumes:
            col1, col2 = st.columns([5, 1])

            with col1:
                st.write(
                    f"**Resume ID:** {resume['resume_id']}  \n"
                    f"**Source:** {resume['source']}"
                )

            with col2:
                if st.button("Delete", key=resume["resume_id"]):
                    delete_resume_from_db(resume["resume_id"])
                    st.session_state.resumes.remove(resume)
                    st.success("Resume deleted.")
                    st.rerun()

if st.session_state.show_all_resumes:
    st.subheader("All Resumes in Database")

    try:
        all_data = search_resumes("", n_results=100)

        metas = all_data["metadatas"][0]

        if not metas:
            st.info("No resumes found in database.")
        else:
            seen = set()
            for meta in metas:
                rid = meta["resume_id"]
                if rid not in seen:
                    seen.add(rid)
                    st.write(
                        f"Resume ID: {rid}  |  "
                        f"Source:{meta.get('source')}  |  "
                        f"Total Chunks: {meta.get('chunk_index') + 1}"
                    )

    except Exception as e:
        st.error(str(e))


st.divider()


st.subheader("Shortlist Candidates")

job_description = st.text_area(
    "Paste Job Description",
    height=220,
)
max_results = st.slider(
    "Number of candidates to shortlist",
    min_value=1,
    max_value=20,
    value=5,
)


if st.button("Shortlist Candidates"):
    if not job_description.strip():
        st.warning("Please enter a job description.")
    else:
        try:
            results = search_resumes(job_description, n_results=max_results )


            docs = results["documents"][0]
            metas = results["metadatas"][0]
            dists = results["distances"][0]

            grouped_results = deduplicate_and_rank(docs, metas, dists)
            final_results = grouped_results[:max_results]


            if not docs:
                st.info("No matching resumes found.")
            else:
                for i, item in enumerate(final_results, start=1):

                    resume_id = item["meta"]["resume_id"]
                    dist = item["dist"]
                    doc = item["doc"]

                    st.subheader(f"Candidate Match {i}")
                    st.write(f"Resume ID: {resume_id}")
                    st.write(f"Relevance Score: {1 - dist:.2f}")

                    with st.expander("Candidate Contact & Profile"):
                        st.write(get_resume_intro(resume_id) or "Not available")

                    with st.expander("Matching Skills / Experience"):
                        st.write(doc)

                    with st.expander("AI Explanation"):
                        st.write(explain_match(job_description, doc))   

        except Exception as e:
            st.error(str(e))

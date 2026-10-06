"""Bare-bones RAG chatbot that answers questions about the documents in DATA_DIR."""

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from google.genai import errors as genai_errors
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.google_genai import GoogleGenAI

DATA_DIR = Path("data/handbook")
LLM_MODEL = "gemini-2.5-flash"
EMBED_MODEL = "BAAI/bge-small-en-v1.5"

load_dotenv()


def get_api_key():
    """Return GEMINI_API_KEY, or show an error and stop the app if it is missing."""
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        st.error(
            "GEMINI_API_KEY was not found. Create a `.env` file in the same "
            "folder as app.py with the line `GEMINI_API_KEY=your-key-here`, "
            "then restart the app."
        )
        st.stop()
    return api_key


def validate_data_dir():
    """Stop the app with a clear message if DATA_DIR is missing, not a folder, or empty."""
    if not DATA_DIR.exists():
        st.error(
            f"Data folder not found. The app expected a folder at "
            f"`{DATA_DIR.resolve()}`. Create it and add your documents, "
            f"then restart the app."
        )
        st.stop()

    if not DATA_DIR.is_dir():
        st.error(
            f"`{DATA_DIR}` exists but is a file, not a folder. Replace it "
            f"with a folder that contains your documents, then restart the app."
        )
        st.stop()

    # Hidden files such as .DS_Store are ignored: they are not documents.
    documents = [
        p for p in DATA_DIR.iterdir() if p.is_file() and not p.name.startswith(".")
    ]
    if not documents:
        st.error(
            f"The data folder `{DATA_DIR}` has no documents in it. Add at "
            f"least one file (for example a PDF), then restart the app."
        )
        st.stop()


@st.cache_resource
def get_query_engine(api_key):
    """Load the models, index the documents in DATA_DIR, and return a query engine.

    Cached, so this runs once instead of on every rerun. It contains no
    st.error / st.stop calls; it raises and the caller decides what to show.
    """
    Settings.llm = GoogleGenAI(model=LLM_MODEL, api_key=api_key)
    Settings.embed_model = HuggingFaceEmbedding(model_name=EMBED_MODEL)

    documents = SimpleDirectoryReader(str(DATA_DIR)).load_data()
    index = VectorStoreIndex.from_documents(documents)
    return index.as_query_engine()


st.title("Bare Bones RAG Chatbot")

# Fail fast: the app can't do anything without a key and documents.
api_key = get_api_key()
validate_data_dir()

# Fail fast: indexing can still fail after the checks above pass.
try:
    query_engine = get_query_engine(api_key)
except ValueError as e:
    st.error(
        f"Couldn't read the documents in `{DATA_DIR}`. Check that the files "
        f"are supported and not corrupt, then restart the app. Details: {e}"
    )
    st.stop()
except OSError as e:
    st.error(
        f"Couldn't load the embedding model `{EMBED_MODEL}`. The first run "
        f"downloads it, so check your internet connection and restart the "
        f"app. Details: {e}"
    )
    st.stop()
except Exception as e:
    st.error(f"Couldn't build the search index, so the app can't start. Details: {e}")
    st.stop()

prompt = st.chat_input("Ask me anything...")
if prompt:
    st.write(f"User: {prompt}")
    # Fallback: one failed question shouldn't take down the app, so no st.stop().
    try:
        response = query_engine.query(prompt)
    except genai_errors.APIError as e:
        if e.code == 429:
            st.error("Gemini's rate limit was reached. Wait a minute and ask again.")
        elif e.code in (400, 401, 403):
            st.error(
                "Gemini rejected the request. Check that the GEMINI_API_KEY "
                f"in your `.env` is valid, then restart the app. Details: {e}"
            )
        else:
            st.error(f"Gemini returned an error. Please try again. Details: {e}")
    except Exception as e:
        st.error(
            "Couldn't get an answer for that question. Check your internet "
            f"connection and try again. Details: {e}"
        )
    else:
        st.write(f"Bot response: {response.response}")
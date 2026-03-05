import os
import glob as glob_module

import numpy as np
import gradio as gr
from sentence_transformers import SentenceTransformer
from huggingface_hub import InferenceClient


# ---------------------------------------------------------------------------
# Load & chunk documents
# ---------------------------------------------------------------------------

def load_documents(docs_dir="docs"):
    docs = []
    for path in glob_module.glob(f"{docs_dir}/**/*.md", recursive=True):
        with open(path) as f:
            docs.append({"path": path, "content": f.read()})
    if os.path.exists("readme.md"):
        with open("readme.md") as f:
            docs.append({"path": "readme.md", "content": f.read()})
    return docs


def chunk_text(text, chunk_size=400, overlap=50):
    """Split text into overlapping chunks by paragraph."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current, current_len = [], 0
    for para in paragraphs:
        words = para.split()
        if current_len + len(words) > chunk_size and current:
            chunk_text_str = "\n\n".join(current)
            chunks.append(chunk_text_str)
            # carry-over overlap words into the next chunk
            tail = chunk_text_str.split()[-overlap:]
            current = [" ".join(tail)]
            current_len = len(tail)
        current.append(para)
        current_len += len(words)
    if current:
        chunks.append("\n\n".join(current))
    return chunks


print("Loading documents...")
_documents = load_documents()
all_chunks = []
for doc in _documents:
    for chunk in chunk_text(doc["content"]):
        all_chunks.append({"text": chunk, "source": doc["path"]})
print(f"  {len(all_chunks)} chunks from {len(_documents)} files")


# ---------------------------------------------------------------------------
# Embed chunks at startup
# ---------------------------------------------------------------------------

print("Embedding chunks (this may take a moment)...")
_embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
_chunk_texts = [c["text"] for c in all_chunks]
_embeddings = _embedder.encode(_chunk_texts, show_progress_bar=False)
_embeddings = _embeddings / np.linalg.norm(_embeddings, axis=1, keepdims=True)
print("  Done.")


# ---------------------------------------------------------------------------
# Retrieval
# ---------------------------------------------------------------------------

def retrieve(query: str, top_k: int = 3) -> list[dict]:
    q = _embedder.encode([query])
    q = q / np.linalg.norm(q)
    scores = (_embeddings @ q.T).squeeze()
    top_idx = np.argsort(scores)[::-1][:top_k]
    return [all_chunks[i] for i in top_idx]


# ---------------------------------------------------------------------------
# Mistral via HF Inference API
# ---------------------------------------------------------------------------

HF_TOKEN = os.environ.get("HF_TOKEN")
_client = InferenceClient("mistralai/Mistral-7B-Instruct-v0.3", token=HF_TOKEN)

SYSTEM_TEMPLATE = """\
You are a helpful assistant for technical blog writing. You help software engineers \
write clear, compelling, and well-structured technical blog posts.

Answer the user's question using the context below. If the context doesn't contain \
enough information, answer from general knowledge and say so briefly.

--- CONTEXT ---
{context}
--- END CONTEXT ---"""


def chat(message: str, history: list) -> str:
    chunks = retrieve(message)
    context = "\n\n---\n\n".join(c["text"] for c in chunks)

    messages = [{"role": "system", "content": SYSTEM_TEMPLATE.format(context=context)}]
    for turn in history:
        messages.append({"role": "user",      "content": turn[0]})
        messages.append({"role": "assistant", "content": turn[1]})
    messages.append({"role": "user", "content": message})

    response = ""
    for token in _client.chat_completion(messages, max_tokens=600, stream=True):
        delta = token.choices[0].delta.content
        if delta:
            response += delta
            yield response


# ---------------------------------------------------------------------------
# Gradio UI
# ---------------------------------------------------------------------------

demo = gr.ChatInterface(
    fn=chat,
    title="Technical Blog Writing Assistant",
    description=(
        "Ask anything about writing technical blog posts — templates, structure, "
        "openings, code examples, common pitfalls, AI prompting strategies, and more."
    ),
    examples=[
        "What blog template should I use for a debugging story?",
        "What are the most common pitfalls when writing technical posts?",
        "How do I write a strong opening for a performance case study?",
        "Give me a prompt to get AI help drafting a before/after refactoring post.",
        "How should I structure the metrics section of a post?",
    ],
    cache_examples=False,
)

if __name__ == "__main__":
    demo.launch()

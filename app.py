"""
Semantic PDF Reader - Main Streamlit Application
AI-powered document search system using sentence embeddings and cosine similarity.
Supports custom PDF upload and 🚀 Demo Mode.
Built by roshni-choudhary.
"""

import time
import pandas as pd
import streamlit as st

# Custom modules
import pdf_processor
import embeddings
import search
import database
import sample_data

# Page Configuration
st.set_page_config(
    page_title="Semantic PDF Reader",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Bootstrap-inspired Styling
BOOTSTRAP_STYLE = """
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hero Header */
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem 2.5rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        font-weight: 700;
        font-size: 2.2rem;
        margin-bottom: 0.5rem;
        color: #ffffff;
    }
    .main-header p {
        font-size: 1.05rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Instruction Steps */
    .step-box {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 1rem 1.25rem;
        text-align: center;
        height: 100%;
    }
    .step-number {
        background-color: #2a5298;
        color: white;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    .step-title {
        font-weight: 600;
        color: #212529;
        margin-bottom: 0.25rem;
    }
    .step-desc {
        font-size: 0.85rem;
        color: #6c757d;
    }

    /* Bootstrap Card Styling */
    .result-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 5px solid #2a5298;
        border-radius: 8px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .result-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    /* Bootstrap Badges */
    .badge-similarity {
        background-color: #28a745;
        color: white;
        font-weight: 600;
        padding: 0.35em 0.75em;
        border-radius: 20px;
        font-size: 0.88rem;
        display: inline-block;
    }
    .badge-similarity-medium {
        background-color: #ffc107;
        color: #212529;
        font-weight: 600;
        padding: 0.35em 0.75em;
        border-radius: 20px;
        font-size: 0.88rem;
        display: inline-block;
    }
    .badge-page {
        background-color: #e9ecef;
        color: #495057;
        font-weight: 500;
        padding: 0.35em 0.65em;
        border-radius: 6px;
        font-size: 0.85rem;
        display: inline-block;
        margin-right: 0.5rem;
    }
    .badge-rank {
        background-color: #1e3c72;
        color: white;
        font-weight: 600;
        padding: 0.35em 0.65em;
        border-radius: 6px;
        font-size: 0.85rem;
        display: inline-block;
        margin-right: 0.5rem;
    }
    
    /* Banner for Demo Mode */
    .demo-banner {
        background-color: #e8f4f8;
        border: 1px solid #b8daff;
        border-radius: 8px;
        padding: 0.75rem 1.25rem;
        margin-bottom: 1rem;
        color: #004085;
        font-size: 0.95rem;
    }

    /* Footer */
    .app-footer {
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
        color: #6c757d;
        font-size: 0.9rem;
    }
</style>
"""

st.markdown(BOOTSTRAP_STYLE, unsafe_allow_html=True)


# Cache Model Loading for Streamlit Performance
@st.cache_resource
def get_model():
    return embeddings.load_model()


def main():
    # Ensure database directory is initialized
    database.init_db()

    # Sidebar UI
    with st.sidebar:
        st.image("https://img.icons8.com/isometric/96/search-property.png", width=64)
        st.title("Semantic PDF Reader")
        st.caption("AI-Powered Document Search System")
        st.markdown("---")

        st.subheader("🎯 Mode Selection")
        app_mode = st.radio(
            "Select Operating Mode:",
            ["🚀 Try Demo Mode", "📂 Upload Custom PDF"],
            index=0,
            help="Demo Mode lets you test the AI search instantly using a sample document."
        )

        st.markdown("---")
        st.subheader("⚙️ Search Settings")
        top_k = st.slider("Top Results (K)", min_value=1, max_value=5, value=3)
        show_score = st.checkbox("Show Similarity Score", value=True)
        similarity_threshold = st.slider(
            "Min Similarity Threshold (%)",
            min_value=0,
            max_value=100,
            value=10,
            step=5
        ) / 100.0

        st.markdown("---")
        st.markdown("### 💡 Tech Stack")
        st.markdown("""
        - **UI**: Streamlit + Bootstrap Styling
        - **PDF Parser**: PyPDF
        - **ML Model**: `all-MiniLM-L6-v2`
        - **Vector Metric**: Cosine Similarity
        - **Storage**: SQLite
        """)

        st.markdown("---")
        st.caption("👤 Built by **roshni-choudhary**")

    # Main Hero Banner
    st.markdown("""
    <div class="main-header">
        <h1>🔍 Semantic PDF Reader</h1>
        <p>AI document search that understands meaning, context, and intent — not just exact keywords.</p>
    </div>
    """, unsafe_allow_html=True)

    # 3-Step Quick Guide
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.markdown("""
        <div class="step-box">
            <div class="step-number">1</div>
            <div class="step-title">Load Document</div>
            <div class="step-desc">Upload a PDF or select Demo Mode with sample policy text.</div>
        </div>
        """, unsafe_allow_html=True)
    with col_s2:
        st.markdown("""
        <div class="step-box">
            <div class="step-number">2</div>
            <div class="step-title">Ask Question</div>
            <div class="step-desc">Enter any natural language query in plain English.</div>
        </div>
        """, unsafe_allow_html=True)
    with col_s3:
        st.markdown("""
        <div class="step-box">
            <div class="step-number">3</div>
            <div class="step-title">View Ranked Results</div>
            <div class="step-desc">Explore AI-ranked text matches with similarity scores.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Navigation Tabs
    tab_search, tab_history = st.tabs([
        "📄 Document Search",
        "📜 Search History"
    ])

    with tab_search:
        render_search_tab(app_mode, top_k, show_score, similarity_threshold)

    with tab_history:
        render_history_tab()

    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="app-footer">
        Semantic PDF Reader | Built by <strong>roshni-choudhary</strong>
    </div>
    """, unsafe_allow_html=True)


def render_search_tab(app_mode: str, top_k: int, show_score: bool, threshold: float):
    pages = []
    chunks = []
    doc_name = ""

    if app_mode == "🚀 Try Demo Mode":
        st.markdown("""
        <div class="demo-banner">
            🚀 <strong>Demo Mode Active:</strong> Loaded sample document <code>company_policy.pdf</code>.
            Click a sample query below or type your own question!
        </div>
        """, unsafe_allow_html=True)

        doc_name = sample_data.SAMPLE_DOCUMENT_NAME
        pages = sample_data.SAMPLE_PAGES
        chunks = pdf_processor.chunk_text(pages, chunk_size=300, overlap=50)

    else:
        st.subheader("1. Upload PDF Document")
        uploaded_file = st.file_uploader(
            "Choose a PDF file to process",
            type=["pdf"],
            help="Upload standard text-based PDF documents."
        )

        if not uploaded_file:
            st.info("👆 Please upload a PDF file to begin semantic search, or switch to '🚀 Try Demo Mode' in the sidebar.")
            return

        doc_name = uploaded_file.name
        with st.spinner("Extracting text from PDF..."):
            pages = pdf_processor.extract_text_from_pdf(uploaded_file)
            chunks = pdf_processor.chunk_text(pages, chunk_size=400, overlap=80)

        if not chunks:
            st.error("⚠️ No text could be extracted from this PDF. It might be scanned or image-based.")
            return

    # Document Statistics Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📄 Document Name", doc_name[:25])
    with col2:
        st.metric("📑 Total Pages", len(pages))
    with col3:
        st.metric("🧩 Text Chunks", len(chunks))

    # Text Preview Expander
    with st.expander("👁️ View Document Text Preview"):
        preview_text = "\n\n".join([f"--- Page {p['page']} ---\n{p['text']}" for p in pages])
        st.text_area("Extracted Content", preview_text, height=180, disabled=True)

    st.markdown("---")

    # Load Model & Cache Vector Embeddings
    model = get_model()

    file_id = f"{doc_name}_{len(chunks)}"
    if "current_file_id" not in st.session_state or st.session_state.current_file_id != file_id:
        with st.status("Generating vector embeddings using `all-MiniLM-L6-v2`...", expanded=True) as status:
            start_time = time.time()
            chunk_texts = [c["text"] for c in chunks]
            chunk_embeddings = embeddings.generate_chunk_embeddings(model, chunk_texts)
            st.session_state.current_file_id = file_id
            st.session_state.chunk_embeddings = chunk_embeddings
            st.session_state.chunks = chunks
            elapsed = round(time.time() - start_time, 2)
            status.update(label=f"✅ Ready! Encoded {len(chunks)} chunks in {elapsed}s.", state="complete")

    chunk_embeddings = st.session_state.chunk_embeddings
    cached_chunks = st.session_state.chunks

    # Search Query Section
    st.subheader("2. Semantic Search")

    # Quick Demo Queries
    if app_mode == "🚀 Try Demo Mode":
        st.write("💡 **Quick Demo Questions (Click to test):**")
        q_cols = st.columns(len(sample_data.SAMPLE_QUERIES))
        for idx, sample_q in enumerate(sample_data.SAMPLE_QUERIES):
            with q_cols[idx]:
                if st.button(f"🔍 {sample_q}", key=f"demo_btn_{idx}"):
                    st.session_state.search_input_val = sample_q

    default_val = st.session_state.get("search_input_val", "")
    query = st.text_input(
        "Enter your question in natural language:",
        value=default_val,
        placeholder="e.g., What is the refund policy? or How many days of leave are allowed?",
        help="Search based on meaning rather than exact keyword match."
    )

    if query:
        # Generate query embedding
        query_vector = embeddings.generate_query_embedding(model, query)

        # Compute cosine similarity
        sim_scores = search.compute_cosine_similarity(query_vector, chunk_embeddings)

        # Rank results
        results = search.rank_search_results(
            cached_chunks,
            sim_scores,
            top_k=top_k,
            threshold=threshold
        )

        # Log to SQLite DB history
        top_preview = results[0]["text"] if results else "No matches found"
        top_score_val = results[0]["score"] if results else 0.0
        database.save_search_history(
            document_name=doc_name,
            search_query=query,
            top_match_preview=top_preview,
            top_score=top_score_val
        )

        st.markdown(f"### 🎯 Results for: *\"{query}\"*")

        if not results:
            st.warning("No sections matched your query above the set similarity threshold.")
            return

        for rank, res in enumerate(results, 1):
            score_pct = res["similarity_percentage"]
            badge_class = "badge-similarity" if score_pct >= 40 else "badge-similarity-medium"
            badge_html = f'<span class="{badge_class}">Similarity: {score_pct}%</span>' if show_score else ''

            st.markdown(f"""
            <div class="result-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                    <div>
                        <span class="badge-rank">Rank #{rank}</span>
                        <span class="badge-page">Page {res['page']}</span>
                    </div>
                    {badge_html}
                </div>
                <p style="font-size: 1.05rem; color: #212529; line-height: 1.6; margin-bottom: 0;">
                    "{res['text']}"
                </p>
            </div>
            """, unsafe_allow_html=True)


def render_history_tab():
    st.subheader("📜 Search History")
    st.caption("Records of previous document searches stored locally in SQLite database.")

    col_btn, _ = st.columns([1, 4])
    with col_btn:
        if st.button("🗑️ Clear History", type="secondary"):
            database.clear_search_history()
            st.success("Search history cleared!")
            st.rerun()

    history = database.get_search_history(limit=25)

    if not history:
        st.info("No search history recorded yet. Perform a search to see entries logged here.")
        return

    df = pd.DataFrame(history)
    df.rename(columns={
        "id": "ID",
        "document_name": "Document",
        "search_query": "Query",
        "top_match_preview": "Top Match Snippet",
        "top_score": "Top Score",
        "timestamp": "Timestamp"
    }, inplace=True)

    df["Top Score"] = df["Top Score"].apply(lambda x: f"{round(x * 100, 1)}%")

    st.dataframe(df, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()

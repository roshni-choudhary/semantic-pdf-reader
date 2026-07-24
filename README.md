# 📄 Semantic PDF Reader

An intuitive, lightweight **AI-Powered Document Search System** built with **Python**, **Streamlit**, and **Sentence-Transformers**.

Search PDF documents using natural language based on **semantic meaning and intent** instead of exact keyword matching.

---

## 🚀 Live Demo & Deployment

- **GitHub Repository:** [https://github.com/roshni-choudhary/semantic-pdf-reader](https://github.com/roshni-choudhary/semantic-pdf-reader)
- **Try Demo Mode:** Built-in sample company policy document for instant testing without uploading files.

---

## 🌟 Key Features

- **🚀 1-Click Demo Mode**: Built-in sample document (`company_policy.pdf`) and sample questions for instant demos.
- **📄 Custom PDF Upload**: Fast text extraction page-by-page using `pypdf`.
- **🧩 Smart Text Chunking**: Splits text into clean overlapping chunks preserving page numbers.
- **🧠 Semantic Embeddings**: Generates 384-dimensional vector representations using `all-MiniLM-L6-v2`.
- **📐 Cosine Similarity Ranking**: Computes vector similarity using NumPy dot product and L2 normalization.
- **🎨 Polished Bootstrap UI**: Result cards, rank badges (`Rank #1`), percentage similarity badges (`88%`), and document statistics.
- **📜 Search History Persistence**: Uses SQLite database (`documents.db`) to record past queries and top results.

---

## 💡 Example Usage

**User Query:**
> *"What is the refund policy?"*

**Matched Result:**
> *"Customers can return purchased items within 30 days of purchase for a full refund if accompanied by the original receipt."*
> **Similarity:** `88.5%`

**User Query:**
> *"How many days of leave are allowed?"*

**Matched Result:**
> *"Full-time employees are entitled to 20 days of paid annual leave per calendar year."*
> **Similarity:** `84.2%`

---

## 🧠 How Semantic Search Works

Standard keyword search looks for exact character matches (e.g., searching "refund" fails if the text says "reimbursement" or "returns").

Semantic search converts text into dense numerical vector representations called **embeddings**:

```text
PDF Document / Sample Policy
            │
            ▼
    pypdf / Text Processor
    (Extracts text & splits into chunks)
            │
            ▼
SentenceTransformer ('all-MiniLM-L6-v2')
            │
            ▼
384-Dimensional Vector Embeddings
            │
            ▼
User Search Query ──► Query Embedding Vector
            │
            ▼
Cosine Similarity Calculation
(Measures angle between Query Vector and Chunk Vectors)
            │
            ▼
Ranked Result Cards with % Match Badges
```

### 1. Vector Embeddings (`all-MiniLM-L6-v2`)
The model maps sentences into a 384-dimensional vector space where semantically similar sentences are positioned close to each other.

### 2. Cosine Similarity Formula
Cosine similarity measures the cosine of the angle between two vectors $\mathbf{A}$ and $\mathbf{B}$:

$$\text{Cosine Similarity} = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|} = \frac{\sum_{i=1}^{n} A_i B_i}{\sqrt{\sum_{i=1}^{n} A_i^2} \sqrt{\sum_{i=1}^{n} B_i^2}}$$

- **Value = 1.0 (100%):** Identical semantic meaning.
- **Value = 0.0 (0%):** Unrelated meaning.

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend/UI** | Streamlit + Bootstrap CSS | Web application layout & styling |
| **PDF Processing** | `pypdf` | Extracting raw text from PDF pages |
| **Machine Learning** | `sentence-transformers` | Sentence embedding model (`all-MiniLM-L6-v2`) |
| **Vector Math** | `numpy` | Fast matrix dot-product cosine similarity |
| **Data Handling** | `pandas` | Search history table display |
| **Database** | `sqlite3` | Local persistent search history storage |

---

## 📁 Project Structure

```text
semantic-pdf-reader/
│
├── app.py              # Main Streamlit UI & app orchestration
├── pdf_processor.py    # PDF text extraction, cleaning & chunking logic
├── embeddings.py       # SentenceTransformer model loading & vector generation
├── search.py           # Cosine similarity math & result ranking
├── database.py         # SQLite connection & search history persistence
├── sample_data.py       # Sample policy text & demo questions
├── create_sample_pdf.py # Script to generate test PDF file
├── sample_test_document.pdf # Generated PDF for testing
├── requirements.txt    # Python dependencies for deployment
├── README.md           # Documentation
├── .gitignore          # Git ignore configuration
│
├── database/
│   └── documents.db    # SQLite database (auto-created on startup)
│
└── assets/
    └── sample_test_document.pdf
```

---

## 💻 Local Installation & Run Guide

### 1. Prerequisites
- Python 3.9 or higher installed.

### 2. Clone Repository
```bash
git clone https://github.com/roshni-choudhary/semantic-pdf-reader.git
cd semantic-pdf-reader
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Application
```bash
streamlit run app.py
```
The application will launch at `http://localhost:8501`.

---

## 📜 License
MIT License. Free for learning, modification, and project showcase.

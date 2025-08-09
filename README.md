# 🎭 Thriller Game AI Agent — Web & Notebook Versions

A **narrative-driven thriller** where players interact with a dynamic **Narrator Agent** that generates immersive, suspenseful storylines — and secretly consults a **Research Agent** for accurate real-world facts when needed.

Built to run in:

- **Jupyter Notebook** (development / prototyping)
- **Gradio web app** (interactive browser experience with meta endpoints)
- **Streamlit web app** (interactive browser experience with sidebar tools and example actions)

---

## 🧠 Core Concept

> The player never speaks to the Research Agent directly. The Narrator orchestrates all in-world responses, seamlessly weaving research into the narrative to preserve immersion and tone.

---

## 🕹️ Features

### **Narrator Agent**

- Generates rich, scene-by-scene storytelling with pacing and dramatic tension.
- Recognizes when external factual knowledge is needed and triggers background research.
- Maintains a consistent thriller tone while integrating facts naturally.

### **Research Agent**

- Activated **only** by the Narrator Agent.
- Can access web search or other factual sources (e.g., history, symbols, locations).
- Returns concise factual summaries for in-story use.

### **Game Systems**

- **Game Log** — Tracks events, discoveries, and decisions.
- **Research Log** — Stores all research queries and results.
- **Inventory** — Add/remove items dynamically.
- **Save/Load** — (Planned) Persist and restore game state.
- **Extensible Tooling** — Easily add new tool functions for other agents.

---

## 📌 Example Narrative Flow

**User Input:**

> What is the symbol on the floor? It looks like a spiral with a triangle.

**Narrator Output (internal trigger):**

```
[[RESEARCH: spiral with triangle symbol occult meaning]]
```

**Research Agent Response:**

> This symbol resembles the Triquetra, a pagan emblem representing the cycle of life, death, and rebirth.

**Final Narrator Response:**

> The symbol isn’t random — it’s an ancient triquetra. Your skin tingles as you realize this place may be tied to something far older... and darker.

---

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Core AI:** `openai` or compatible async chat model API (e.g., `litellm`)
- **UI Frameworks:**
  - **Gradio** — Clean Blocks layout, custom theme, example inputs, manifest/robots/sitemap endpoints.
  - **Streamlit** — Sidebar tools, example buttons, auto-scroll toggle, clean chat interface.
- **Async Support:** `nest_asyncio`
- **Environment Management:** `python-dotenv`
- **Optional Web Search:** SerpAPI, Tavily, or custom API integration.

---

## 🌐 Web App Versions

### **Gradio Version**

- Styled with a clean Soft theme and custom CSS.
- **Example Actions:** “Look around”, “Inventory”, “Open the door”, “Run outside”.
- **Meta Endpoints Provided:**
  - `/manifest.json` — PWA manifest.
  - `/robots.txt` — Crawler rules.
  - `/sitemap.xml` — Sitemap for SEO.
- Optional favicon support.

Run:

```bash
pip install -r requirements.txt
python app_gradio_webapp.py
```

Then open: `http://127.0.0.1:7860`

---

### **Streamlit Version**

- Sidebar with:
  - Game description & version info
  - API key status
  - Clear chat button
  - Auto-scroll toggle
  - Clickable example prompts
- Styled header/footer and in-chat assistant/user messages.
- Designed for both local play and easy deployment.

Run:

```bash
pip install streamlit python-dotenv nest-asyncio
python -m streamlit run app_streamlit_webapp.py
```

---

## 📓 Notebook Version

For development and prototyping, you can run the Jupyter notebook:

```bash
jupyter notebook notebooks/ThrillerGameAgent.ipynb
```

- Fully contains agent definitions and tools.
- Great for quick iteration and debugging.

---

## 📁 File Structure

```
.
├── thriller_module.py             # Core agents & tool functions
├── app_gradio_webapp.py           # Gradio UI implementation
├── app_streamlit_webapp.py        # Streamlit UI implementation
├── notebooks/
│   └── ThrillerGameAgent.ipynb    # Development/prototype notebook
├── resources/
│   └── openaiApiKey.env           # API key storage
├── requirements.txt
├── README.md
```

---

## 🔑 Environment Setup

1. Create a `openaiApiKey.env` file or use the provided `openaiApiKey.env_example`:

```
OPENAI_API_KEY=sk-...
```

2. Update the `load_dotenv(dotenv_path=...)` path if your `.env` location differs.

---

## 🚀 Deployment Notes

- **Gradio**: Suitable for quick demos and public links via `share=True`.
- **Streamlit**: Good for dashboards and more structured UIs; easily deployable on Streamlit Cloud.
- **Production**: For a public game, secure API keys and consider adding database-backed save/load.

---

## 🧩 Next Steps

- Implement persistent save/load via JSON or SQLite.
- Add an **Inventory Panel** in the Streamlit sidebar.
- Support branching storylines with player stats.
- Package agents into a lightweight backend service.

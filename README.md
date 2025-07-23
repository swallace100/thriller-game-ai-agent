# 🎭 Thriller Game AI Agent

A narrative-driven thriller game powered by AI agents, where players interact with a dynamic **Narrator Agent** that weaves suspenseful storylines — and secretly consults a **Research Agent** for accurate real-world facts when needed.

> 🧠 The player never interacts with the research agent directly. The narrator handles all in-world responses, maintaining immersion and tone while integrating researched knowledge only when necessary.

---

## 🕹️ Features

- **Narrator Agent**:

  - Responds to player input with rich story progression
  - Controls pacing, tone, and dramatic tension
  - Detects when real-world information is needed and triggers research behind the scenes

- **Research Agent**:

  - Activated only by the narrator
  - Uses AI or web tools to search factual information (e.g., history, symbols, psychology, places)
  - Feeds back concise data to the narrator to integrate into the story

- **Orchestrator**:
  - Central controller that:
    - Handles user input
    - Routes requests to the narrator
    - Detects special `[[RESEARCH: ...]]` tokens in narrator output
    - Retrieves research results and re-prompts the narrator for a final response

---

## 📌 Example Flow

**User Input**:

> What is the symbol on the floor? It looks like a spiral with a triangle.

**Narrator Output**:

> `[[RESEARCH: spiral with triangle symbol occult meaning]]`

**Research Agent Response**:

> This symbol resembles the Triquetra, a pagan emblem representing the cycle of life, death, and rebirth.

**Final Narrator Response**:

> The symbol isn’t random — it's an ancient triquetra. Your skin tingles as you realize this place may be tied to something far older... and darker.

---

## 🛠️ Tech Stack

- Python 3.10+
- `openai` or compatible async chat model API (e.g., `litellm`)
- (Optional) Web search integration via SerpAPI, Tavily, or custom tool
- No LangChain or LangGraph dependencies — intentionally lightweight for full control

---

## 🚧 Planned Features

- Game log tracking with timestamps
- Optional memory (conversation history)
- Web-based UI using Gradio or Streamlit
- Inventory system and branching decision trees
- Save/load game state

---

## 📁 File Structure (planned)

.
├── main.py # Orchestrator logic and game loop
├── agents.py # Narrator and Research agent definitions
├── tools.py # Research tool interface (Web API, mock, etc.)
├── game_log.py # Game log tracking (optional)
├── README.md

---

## 🧩 How to Run

### Not yet implemented. Use the notebook at ./notebooks/ThrillerGameAgent.ipynb for current features.

1. Clone the repo
2. Set up your OpenAI or compatible API key
3. Run the main script:

```bash
python main.py\
```

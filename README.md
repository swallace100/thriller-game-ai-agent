# Thriller Game 🎭

A near-future text thriller powered by an AI Narrator Agent. Experience an interactive story through natural language commands and responses.

## 🚀 Features

- Interactive text-based gameplay
- AI-powered narrative responses
- Inventory management system
- Game state tracking
- Multiple user interfaces (Gradio & Streamlit)
- Clean, production-ready code structure

## 📁 Project Structure

```
agent-code/
├── game/
│   ├── __init__.py
│   ├── api.py              # Core game API functions
│   ├── state.py            # Game state management
│   ├── tools.py            # Function tools for agents
│   ├── content.py          # Game story and content
│   ├── config.py           # Configuration settings
│   └── agents/
│       ├── __init__.py
│       └── narrator.py     # Narrator agent implementation
├── app_gradio.py          # Gradio web interface
├── app_streamlit.py       # Streamlit web interface
├── .env                   # Environment variables (create this)
└── requirements.txt       # Project dependencies
```

## 🛠️ Setup

1. Clone the repository
2. Create a virtual environment:

```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your-api-key-here
```

## 🎮 Running the Game

You can run the game using either the Gradio or Streamlit interface:

### Gradio Interface

```bash
python app_gradio.py
```

Then open http://127.0.0.1:7860 in your browser.

### Streamlit Interface

```bash
python streamlit run app_streamlit.py
```

Then open http://localhost:8501 in your browser.

## 🎯 How to Play

Try these example commands:

- "Look around"
- "Inventory"
- "Open the door"
- "Run outside"

## 💻 Technology Stack

- Python 3.x
- OpenAI GPT Models
- Gradio
- Streamlit
- OpenAI Agents Framework

## 🔑 Environment Variables

Required environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key
- `APP_URL`: (Optional) Custom URL for deployment

## 📝 License

This project is licensed under the MIT License:

```
MIT License

Copyright (c) 2025 Thriller Game

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## ⚠️ Note

Remember to never commit your API keys or sensitive information to version control.

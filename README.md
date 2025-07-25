# Minerva Chatbot

Minerva is a web-based chatbot application built with Flask, SQLAlchemy, and LangChain. It leverages large language models (LLMs) via MistralAI or Replicate to generate conversational responses, storing user and conversation history in a SQLite database.

## Features

- Web interface for chatting with an LLM-powered bot
- User and conversation management with persistent memory
- Supports both MistralAI and Replicate LLMs (see `Minerva_bot.py` and `lamma.py`)
- Clean HTML responses suitable for direct webpage rendering

## Project Structure

```
key.py                  # Stores API keys
lamma.py                # Flask app using Replicate Llama 3 model
Minerva_bot.py          # Flask app using MistralAI model
practice.py             # Alternate Flask app (MistralAI)
req.txt                 # Python dependencies
instance/learning.db    # SQLite database (auto-created)
templates/index.html    # Web UI template
```

## Setup

1. **Clone the repository** and navigate to the project directory.

2. **Install dependencies:**
   ```sh
   pip install -r req.txt
   ```

3. **Set up API keys:**
   - Edit [`key.py`](key.py) and add your MistralAI API key.
   - For Replicate, ensure the API token is set in [`lamma.py`](lamma.py).

4. **Run the application:**
   - To use MistralAI:
     ```sh
     python Minerva_bot.py
     ```
   - To use Replicate Llama 3:
     ```sh
     python lamma.py
     ```
   - Or use [`practice.py`](practice.py) for a similar MistralAI setup.

5. **Access the web interface:**
   - Open [http://localhost:5000](http://localhost:5000) in your browser.

## Usage

- Enter your User ID, Conversation ID, and prompt in the web interface.
- The chatbot will respond with a valid HTML snippet, suitable for direct embedding in web pages.
- Conversation history is stored per user and conversation.

## Notes

- The database (`learning.db`) is created automatically in the `instance/` directory.
- The application expects valid API keys for MistralAI and/or Replicate.
- All responses are formatted as HTML for easy integration.

## License

This project is for educational and demonstration purposes.

---

**Files referenced:**
- [`key.py`](key.py)
- [`lamma.py`](lamma.py)
- [`Minerva_bot.py`](Minerva_bot.py)
- [`practice.py`](practice.py)
- [`req.txt`](req.txt)
-

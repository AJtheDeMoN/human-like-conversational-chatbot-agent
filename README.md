# Kai - A Human-Like Conversational AI

This project is a backend service for Kai, a modular and emotionally intelligent chatbot designed for user-facing platforms.

## Key Features

- **Human-Like Interaction:** Adapts tone based on user input and emotional context.
- **Persistent Memory:** Utilizes a ChromaDB vector store to remember conversations across sessions.
- **Context-Aware:** Employs a RAG (Retrieval-Augmented Generation) pipeline with a relevance filter to ensure coherent conversations.
- **Modular Architecture:** Built with FastAPI, separating API logic, chatbot core, and memory management.

## Tech Stack

- **Backend:** Python, FastAPI
- **AI Model:** Google Gemini API (gemini-1.5-flash)
- **Database:** ChromaDB (Vector Store)

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone [your-repo-url]
    cd kai_backend
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You'll need to create a `requirements.txt` file by running `pip freeze > requirements.txt` in your backend terminal.)*

3.  **Set up environment variables:**
    Create a `.env` file in the root directory and add your API key:
    ```
    GOOGLE_API_KEY="your_gemini_api_key"
    ```
4.  **Run the server:**
    ```bash
    uvicorn main:app --reload
    ```
The API will be available at `http://127.0.0.1:8000`.

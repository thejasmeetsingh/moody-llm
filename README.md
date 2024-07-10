# Moody LLM

Moody LLM is an interactive chat application where a Language Model's mood keeps changing, allowing users to receive varied responses based on the LLM's current mood. The project is designed to simulate conversations with a moody AI, providing a unique and dynamic user experience.

![](./assets/overview.png)

# Functionality

## Backend:

**API Endpoints:**

- `/user_id/`: Generates and returns a UUID.
- `/history/{user_id}/`: Returns the chat message history list (latest on top) based on the given `user_id` in the URL path.

**WebSocket Endpoint:**

- `/chat/{user_id}/`: Receives the user message, generates the LLM response based on its mood, and returns the response through the socket to the user.

**Mood-Based Responses:**
The LLM's responses are based on different moods, configured through a `ChatPromptTemplate` that dictates the type of response. A mood mapper (dictionary) is used in the backend to determine the LLM's mood randomly for each response. This ensures a varied and engaging interaction experience.

## Frontend:

- On application load, checks for a userID in `sessionStorage`. If not found, it calls the API to fetch a userID and saves it in `sessionStorage`.
- The userID is used to fetch chat message history.
- Users can type their messages in an input field, which are sent to the LLM via a websocket connection.
- A typing effect simulates real-time message generation.
- Each LLM response includes a "mood" indicator, displayed with different colors to easily highlight the LLM's current mood.

# Getting Started

## Prerequisites:

1. [Supabase](https://supabase.com/) Account:
    - Create an account on Supabase and set up a table.
    - Obtain the Supabase Key and Supabase URL from the Supabase dashboard.
    - Configure these details in the backend `.env` file.
    
    **Table Schema:**
    ```
    id UUID PRIMARY KEY
    created_at TIMESTAMPZ NOT NULL
    user_id UUID NOT NULL
    message JSON NOT NULL
    ```

2. Ollama Installation:
    - [Install](https://ollama.com/download) Ollama on your system.
    - Once installed, Run the following commands:
    ```sh
    ollama pull llama3
    ollama serve
    ```

## Steps:

- **Backend:**
    1. Navigate to the backend folder.
    2. Install requirements: `pip install -r requirements.txt`
    3. Run the backend services: `fastapi run dev`

    Access backend services at: http://localhost:8000/

- **Frontend:**
    1. Navigate to the frontend folder.
    2. Install libraries: `npm install`
    3. Run the frontend app: `npm run dev`

    Access the frontend app at: http://localhost:5173/

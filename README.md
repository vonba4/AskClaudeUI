# AskClaudeUI
UI to use Ask Claude via the API

## Description

AskClaudeUI is a simple web application that allows users to interact with the Ask Claude API (Anthropic Claude) through a minimalist user interface. The application consists of a Python FastAPI backend and a lightweight HTML frontend.

## Functionality

- **Prompt Submission:**  
  Users can enter a prompt/question in a text area on the web page and submit it.

- **Model Selection:**  
  The application fetches the available Claude models from the API and displays them in a dropdown. The currently selected model is loaded from the config and shown as the default. Users can change the model at any time, and the selection is saved to the config file.

- **API Integration:**  
  The backend receives the prompt and forwards it to the Ask Claude API using the selected model and API key.

- **Response Display:**  
  The application extracts the main text content from the API response and displays it in a read-only text box on the web page, preserving line breaks.

- **Processing Indicator:**  
  When a prompt is submitted, a "Processing..." message with animated dots is shown until the response is received.

- **Configuration:**  
  The API key and model are stored in a config file (not tracked by git for security).

## How it Works

1. User enters a prompt in the web form and clicks "Submit".
2. The frontend sends the prompt to the FastAPI backend via a POST request.
3. The backend sends the prompt to the Ask Claude API and receives a response.
4. The backend extracts the relevant text from the response and sends it back to the frontend.
5. The frontend displays the answer to the user in a text box.
6. Users can select a different Claude model from the dropdown, which updates the backend configuration.

This application provides a quick and easy way to interact with the Ask Claude API from your browser. Start web server in in VS code: uvicorn main:app --reload --port 8080 and access in browser via localhost:8080.

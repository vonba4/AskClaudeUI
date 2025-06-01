# AskClaudeUI
UI to use Ask Claude via the API

## Description

AskClaudeUI is a simple web application that allows users to interact with the Ask Claude API (Anthropic Claude) through a user-friendly interface. The application consists of a Python FastAPI backend and a minimal HTML frontend.

## Functionality

- **Prompt Submission:**  
  Users can enter a prompt/question in a text area on the web page and submit it.

- **API Integration:**  
  The backend receives the prompt and forwards it to the Ask Claude API using the configured model and API key.

- **Response Display:**  
  The application extracts the main text content from the API response and displays it directly on the web page for the user.

- **Configuration:**  
  The API key and model are stored in a `config.json` file (not tracked by git for security).

## How it Works

1. User enters a prompt in the web form and clicks "Submit".
2. The frontend sends the prompt to the FastAPI backend via a POST request.
3. The backend sends the prompt to the Ask Claude API and receives a response.
4. The backend extracts the relevant text from the response and sends it back to the frontend.
5. The frontend displays the answer to the user.

This application provides a quick and easy way to interact with the Ask Claude API from your browser.

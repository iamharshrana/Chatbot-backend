
# FastAPI Chatbot Backend

This repository contains a FastAPI-based backend for a chatbot that interacts with the LangFlow API. It handles both HTTP and WebSocket connections, allowing for real-time chat functionality. The chatbot can be integrated with a front-end to provide interactive responses.

## Features

- **REST API**: Handles chat messages via HTTP POST requests.
- **WebSocket Support**: Enables real-time, bidirectional communication.
- **CORS Enabled**: Allows cross-origin requests from different domains.
- **LangFlow API Integration**: Sends and receives messages via the LangFlow API.
- **Environment Variable Support**: Sensitive information like API URLs and Flow IDs are managed through a `.env` file.

## Setup

### Prerequisites

- Python 3.7+
- FastAPI
- `requests` library for API communication
- `python-dotenv` for managing environment variables

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/iamharshrana/Chatbot-backend.git
   cd Chatbot-backend
   ```

2. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with the following variables:

   ```bash
   BASE_API_URL=<Your LangFlow API Base URL>
   FLOW_ID=<Your Flow ID>
   ```

### Running the Application

You can start the FastAPI application by running:

```bash
uvicorn main:app --reload
```

The server will run at `http://127.0.0.1:8000` by default.

## Environment Variables

This project uses a `.env` file to store the LangFlow API URL and Flow ID. Ensure that you create the `.env` file before running the application.

Example `.env` file:

```env
BASE_API_URL=https://your-langflow-api-url
FLOW_ID=your-flow-id
```

## License

This project is licensed under the MIT License.

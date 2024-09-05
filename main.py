from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from typing import Optional

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow only your front-end domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Define a request model
class ChatRequest(BaseModel):
    message: str

# Define a response model
class ChatResponse(BaseModel):
    response: str

# LangFlow API configuration
BASE_API_URL = "http://35.176.125.157:7860"
FLOW_ID = "e9aab95c-d25d-4036-93f2-bb39cc06b477"

def run_flow(message: str,
             endpoint: str = FLOW_ID,
             output_type: str = "chat",
             input_type: str = "chat",
             tweaks: Optional[dict] = None) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param endpoint: The ID or the endpoint name of the flow
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/api/v1/run/{endpoint}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    if tweaks:
        payload["tweaks"] = tweaks

    response = requests.post(api_url, json=payload)
    
    # Print the status code and content for debugging
    print("Response Status Code:", response.status_code)
    # print("Response Content:", response.text)

    return response.json()

def extract_message(response_data: dict) -> str:
    """
    Extract the chatbot message from the LangFlow API response.

    :param response_data: The JSON response from the LangFlow API
    :return: The chatbot message
    """
    try:
        # Navigate through the nested structure
        message_data = response_data.get('outputs', [])[0].get('outputs', [])[0].get('results', {}).get('message', {})
        message_text = message_data.get('text', 'No response found')
        return message_text
    except Exception as e:
        print(f"Error extracting message: {e}")
        return 'No response found'

# Endpoint to handle the chatbot request
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Get a response from the LangFlow API
        response_data = run_flow(request.message)
        
        # Extract the chatbot reply from the response data
        chatbot_response = extract_message(response_data)
        
        return ChatResponse(response=chatbot_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket endpoint for real-time chat
@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()  # Accept the WebSocket connection
    try:
        while True:
            data = await websocket.receive_text()  # Wait for a message from the client
            response_data = run_flow(data)  # Process the message
            chatbot_response = extract_message(response_data)  # Extract the response
            await websocket.send_text(chatbot_response)  # Send the response back
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")

# Basic route for testing
@app.get("/")
async def root():
    return {"message": "Chatbot API is running"}
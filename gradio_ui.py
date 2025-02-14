import os
import gradio as gr
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Validate API key
if not API_KEY:
    raise ValueError("❌ API_KEY is missing! Please check your .env file.")

# Configure Google Gemini API
genai.configure(api_key=API_KEY)

# Function to generate a dynamic response from the AI model
def handle_user_query(msg, chat_history):
    """Handles user messages and generates AI response dynamically."""
    
    try:
        # Initialize Google AI Model
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(msg)

        # Ensure response is valid
        bot_reply = response.text if response and hasattr(response, 'text') else "🤖 Sorry, I didn't understand that."

        # Append user query & bot response to chat history
        chat_history.append((msg, bot_reply))

    except Exception as e:
        chat_history.append((msg, f"⚠️ Error: {str(e)}"))

    return '', chat_history  # Return empty input & updated chat history

# Creating Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("### 🤖 AI Chatbot - Powered by BRICK WEB STUDIO ")
    chatbot = gr.Chatbot(label="AI Chatbot")
    msg = gr.Textbox(placeholder="Type your message here and press Enter...")
    clear = gr.ClearButton([msg, chatbot])

    msg.submit(
        handle_user_query,
        [msg, chatbot],
        [msg, chatbot]
    )

# Launch Gradio App
if __name__ == "__main__":
    demo.queue()
    demo.launch()
from django.shortcuts import render
from django.http import JsonResponse
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google Generative AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the environment.")

genai.configure(api_key=GEMINI_API_KEY)

# Initialize the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

# Django view for the chatbot
def chatBot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        try:
            # Start a chat session
            chat_session = model.start_chat(
                history=[
                    {"role": "user", "parts": ["Hi!"]},
                    {"role": "model", "parts": ["Hello! How can I assist you?"]},
                ]
            )
            # Send the user's message
            response = chat_session.send_message(message)
            reply = response.text.strip()
        except Exception as e:
            reply = "Sorry, I couldn't process your request. Please try again later."
            print(f"Error: {e}")

        return JsonResponse({'message': message, 'response': reply})
    
    # Render the chatbot template
    return render(request, "chatbot.html")

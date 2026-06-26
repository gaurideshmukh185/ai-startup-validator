import os
import dotenv
import google.generativeai as genai

# Load API key from .env file
dotenv.load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=api_key)

# Use a working model from the available list
model = genai.GenerativeModel("models/gemini-2.5-flash")

# Ask a question
response = model.generate_content("What is a startup? Explain in 2 sentences.")

# Print the response
print("\n--- Gemini Response ---")
print(response.text)

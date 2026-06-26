import os
import dotenv
import google.generativeai as genai
import json

# Load API key
dotenv.load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Use working model
model = genai.GenerativeModel("models/gemini-2.5-flash")

# The same startup idea for all prompts
idea = "An AI-powered note-taking app that automatically organizes your thoughts"

print("=" * 60)
print("PROMPT ENGINEERING COMPARISON")
print("=" * 60)

# PROMPT 1: Vague
print("\n1. PROMPT 1 (Vague):")
print('"Analyze this idea: ' + idea + '"')
print("-" * 40)
response1 = model.generate_content("Analyze this idea: " + idea)
print("Response:")
print(response1.text)

input("\nPress Enter to continue to Prompt 2...")

# PROMPT 2: Better (with role)
print("\n2. PROMPT 2 (Better):")
print('"You are a startup expert. Analyze: ' + idea + '"')
print("-" * 40)
response2 = model.generate_content("You are a startup expert. Analyze: " + idea)
print("Response:")
print(response2.text)

input("\nPress Enter to continue to Prompt 3...")

# PROMPT 3: Best (with JSON format)
print("\n3. PROMPT 3 (Best):")
print('"You are a startup expert. Analyze this idea: ' + idea + '. Return ONLY valid JSON in this format: {"verdict": "good/bad", "score": 0-100, "reason": "short explanation"}"')
print("-" * 40)
response3 = model.generate_content("You are a startup expert. Analyze this idea: " + idea + ". Return ONLY valid JSON in this format: {'verdict': 'good/bad', 'score': 0-100, 'reason': 'short explanation'}")
print("Response:")
print(response3.text)

print("\n" + "=" * 60)
print("KEY LESSON: Specifying JSON format gives you structured, usable data!")
print("=" * 60)

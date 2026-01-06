import google.generativeai as genai
import os

# Paste your ACTUAL key here
API_KEY = "AIzaSyAEvmxF7DZmmGC9zNjTMbjn1knFAsgZa9Y" 
genai.configure(api_key=API_KEY)

print("Searching for available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error: {e}")
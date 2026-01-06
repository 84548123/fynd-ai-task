import google.generativeai as genai

# PASTE YOUR NEW KEY BELOW INSIDE THE QUOTES
NEW_KEY = "AIzaSyAEvmxF7DZmmGC9zNjTMbjn1knFAsgZa9Y"

genai.configure(api_key=NEW_KEY)

try:
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content("Are you working?")
    print("SUCCESS: " + response.text)
except Exception as e:
    print("FAILURE: " + str(e))
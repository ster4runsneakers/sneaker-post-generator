import os
from dotenv import load_dotenv
import google.generativeai as genai
from flask import Flask, render_template, request
import re # Εισάγουμε μια νέα βιβλιοθήκη για την επεξεργασία κειμένου

# --- Αρχικοποίηση ---
app = Flask(__name__)

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Η συνάρτηση που καλεί την AI (παραμένει ίδια)
def call_ai(sneaker_name, language, tone):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Create a complete social media post for the "{sneaker_name}" sneaker.
    The tone of the post should be **{tone}**.

    Please provide the following in the {language} language, using these exact headers:
    HOOKS:
    [List of 3 hooks here]

    CAPTION:
    [The caption text here]

    HASHTAGS:
    [List of 5 hashtags here]
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error"

# ΝΕΑ ΣΥΝΑΡΤΗΣΗ για να "κόβει" το κείμενο
def parse_ai_response(text):
    if text == "Error":
        return {"hooks": "Error", "caption": "Error", "hashtags": "Error"}
    
    # Χρησιμοποιούμε απλή λογική για να βρούμε τα σημεία που μας ενδιαφέρουν
    hooks = text.split("HOOKS:")[1].split("CAPTION:")[0].strip()
    caption = text.split("CAPTION:")[1].split("HASHTAGS:")[0].strip()
    hashtags = text.split("HASHTAGS:")[1].strip()

    return {
        "hooks": hooks,
        "caption": caption,
        "hashtags": hashtags
    }

# --- Ορισμός Σελίδων (Routes) ---
@app.route('/', methods=['GET', 'POST'])
def home():
    ai_result_parts = None
    if request.method == 'POST':
        sneaker_name_from_form = request.form['sneaker_name']
        language_from_form = request.form['language']
        tone_from_form = request.form['tone']
        
        # 1. Παίρνουμε το ενιαίο κείμενο από την AI
        raw_text_result = call_ai(sneaker_name_from_form, language_from_form, tone_from_form)
        # 2. Το "κόβουμε" στα κομμάτια του
        ai_result_parts = parse_ai_response(raw_text_result)
    
    # Στέλνουμε στο HTML τα κομμάτια ξεχωριστά
    return render_template('index.html', result=ai_result_parts)

if __name__ == '__main__':
    app.run(debug=True)
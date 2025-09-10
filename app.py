import os
from dotenv import load_dotenv
import google.generativeai as genai
from flask import Flask, render_template, request

# --- Αρχικοποίηση ---
app = Flask(__name__)

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Η συνάρτηση τώρα δέχεται και τον τόνο ως παράμετρο
def generate_post_for_sneaker(sneaker_name, language, tone):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Το prompt τώρα περιλαμβάνει και τη μεταβλητή του τόνου
    prompt = f"""
    Create a complete social media post for the "{sneaker_name}" sneaker.
    The tone of the post should be **{tone}**.

    Please provide the following in the {language} language:
    1.  Three (3) different, catchy hooks.
    2.  One (1) engaging caption.
    3.  Five (5) relevant hashtags.

    Structure the response clearly.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Παρουσιάστηκε σφάλμα κατά την επικοινωνία με την AI."

# --- Ορισμός Σελίδων (Routes) ---
@app.route('/', methods=['GET', 'POST'])
def home():
    ai_result = None
    if request.method == 'POST':
        # Παίρνουμε όλες τις τιμές από τη φόρμα
        sneaker_name_from_form = request.form['sneaker_name']
        language_from_form = request.form['language']
        tone_from_form = request.form['tone']
        
        # Καλούμε την AI δίνοντας και τις τρεις παραμέτρους
        ai_result = generate_post_for_sneaker(sneaker_name_from_form, language_from_form, tone_from_form)
    
    return render_template('index.html', result=ai_result)

# Αυτό χρειάζεται για να τρέξει η εφαρμογή
if __name__ == '__main__':
    app.run(debug=True)
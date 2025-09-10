import os
from dotenv import load_dotenv
import google.generativeai as genai
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename # Νέα βιβλιοθήκη για ασφαλή ονόματα αρχείων

# --- Αρχικοποίηση ---
UPLOAD_FOLDER = 'uploads' # Ονομα φακέλου για τις εικόνες
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'} # Επιτρεπόμενοι τύποι αρχείων

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Δημιουργούμε τον φάκελο uploads αν δεν υπάρχει
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# ... οι συναρτήσεις call_ai και parse_ai_response παραμένουν ακριβώς ίδιες ...
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

def parse_ai_response(text):
    if text == "Error":
        return {"hooks": "Error", "caption": "Error", "hashtags": "Error"}
    try:
        hooks = text.split("HOOKS:")[1].split("CAPTION:")[0].strip()
        caption = text.split("CAPTION:")[1].split("HASHTAGS:")[0].strip()
        hashtags = text.split("HASHTAGS:")[1].strip()
        return {"hooks": hooks, "caption": caption, "hashtags": hashtags}
    except IndexError:
        return {"hooks": text, "caption": "Could not parse.", "hashtags": "Could not parse."}

# --- Ορισμός Σελίδων (Routes) ---
@app.route('/', methods=['GET', 'POST'])
def home():
    ai_result_parts = None
    if request.method == 'POST':
        # Παίρνουμε τα δεδομένα κειμένου από τη φόρμα
        sneaker_name_from_form = request.form['sneaker_name']
        language_from_form = request.form['language']
        tone_from_form = request.form['tone']

        # ΝΕΟ ΚΟΜΜΑΤΙ: Διαχείριση των εικόνων
        uploaded_files = request.files.getlist('images')
        for file in uploaded_files:
            if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                print(f"Saved file: {filename}") # Τυπώνουμε στο terminal για επιβεβαίωση

        # Η κλήση στην AI παραμένει ίδια προς το παρόν
        raw_text_result = call_ai(sneaker_name_from_form, language_from_form, tone_from_form)
        ai_result_parts = parse_ai_response(raw_text_result)
    
    return render_template('index.html', result=ai_result_parts)

if __name__ == '__main__':
    app.run(debug=True)
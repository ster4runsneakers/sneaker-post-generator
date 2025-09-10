import os
from dotenv import load_dotenv
import google.generativeai as genai

# Φορτώνει τα "μυστικά" από το αρχείο .env
load_dotenv()

# --- Ρυθμίσεις ---
# Διαβάζει το κλειδί με ασφαλή τρόπο από το περιβάλλον
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Δημιουργούμε το μοντέλο AI
model = genai.GenerativeModel('gemini-1.5-flash', transport='rest')

# --- Δυναμική Ερώτηση στον Χρήστη ---
sneaker_name = input("Για ποιο sneaker θέλεις να δημιουργήσω περιεχόμενο; ")

# --- Prompt ---
prompt = f"""
Δημιούργησε μια ολοκληρωμένη δημοσίευση για social media για το sneaker "{sneaker_name}".

Παρακαλώ, δώσε μου τα παρακάτω στα Ελληνικά:
1.  Τρία (3) διαφορετικά, πιασάρικα hooks.
2.  Μία (1) ενδιαφέρουσα λεζάντα (caption).
3.  Πέντε (5) σχετικά hashtags.

Δόμησε την απάντηση με ξεκάθαρο τρόπο.
"""

# --- Επικοινωνία με την ΑΙ & Απάντηση ---
response = model.generate_content(prompt)

# Τυπώνουμε την απάντηση της ΑΙ.
print("---")
print("Η ολοκληρωμένη πρόταση της AI είναι:")
print(response.text)
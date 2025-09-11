import os
import requests
from dotenv import load_dotenv

# Φορτώνουμε τα κλειδιά από το .env
load_dotenv()

PEXELS_API_URL = "https://api.pexels.com/v1/audio/search"
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

print("--- Ξεκινά το τεστ σύνδεσης με το Pexels ---")

if not PEXELS_API_KEY:
    print("ΣΦΑΛΜΑ: Δεν βρέθηκε το PEXELS_API_KEY. Έλεγξε το αρχείο .env.")
else:
    print("Το PEXELS API Key βρέθηκε επιτυχώς.")
    
    headers = {
        "Authorization": PEXELS_API_KEY
    }
    params = {
        "query": "upbeat",
        "per_page": 5
    }

    try:
        print(f"Προσπάθεια σύνδεσης στο: {PEXELS_API_URL}")
        response = requests.get(PEXELS_API_URL, headers=headers, params=params)
        response.raise_for_status() # Ελέγχει για σφάλματα (π.χ. 4xx, 5xx)

        print(f"Επιτυχής σύνδεση! Status Code: {response.status_code}")
        print("--- Απάντηση από το Pexels ---")
        print(response.json())

    except requests.exceptions.RequestException as e:
        print("\n!!! ΑΠΕΤΥΧΕ Η ΣΥΝΔΕΣΗ !!!")
        print(f"Λεπτομέρειες σφάλματος: {e}")

print("\n--- Το τεστ ολοκληρώθηκε ---")
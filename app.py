import os
import requests
import random
from flask import Flask, render_template, request, redirect, url_for, jsonify
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# --- Ρυθμίσεις για Cloudinary ---
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

# --- Ρυθμίσεις για APIs ---
SHOTSTACK_API_URL = "https://api.shotstack.io/stage/render"
SHOTSTACK_API_KEY = os.getenv("SHOTSTACK_API_KEY")
PEXELS_API_URL = "https://api.pexels.com/v1/audio/search"
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")


# --- ΝΕΑ ΣΥΝΑΡΤΗΣΗ: Βρίσκει μουσική από το Pexels ---
def get_music_from_pexels(category="background"):
    """
    Ψάχνει για μουσική στο Pexels API με βάση μια κατηγορία.
    """
    if not PEXELS_API_KEY:
        print("Σφάλμα: Δεν βρέθηκε το PEXELS_API_KEY.")
        return None
        
    headers = {
        "Authorization": PEXELS_API_KEY
    }
    params = {
        "query": category,
        "per_page": 50
    }
    try:
        response = requests.get(PEXELS_API_URL, headers=headers, params=params)
        response.raise_for_status()
        results = response.json().get("audio_files", [])
        if results:
            track = random.choice(results)
            # Το Pexels επιστρέφει το link απευθείας
            return track.get('link')
    except requests.exceptions.RequestException as e:
        print(f"Σφάλμα κατά την κλήση στο Pexels API: {e}")
        return None
    return None


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        uploaded_images = request.files.getlist("images")
        platform_choice = request.form.get('platform')
        if not uploaded_images or uploaded_images[0].filename == '':
            return "Παρακαλώ επιλέξτε τουλάχιστον μία φωτογραφία."
        image_urls = []
        for image in uploaded_images:
            try:
                upload_result = cloudinary.uploader.upload(image)
                image_urls.append(upload_result['secure_url'])
            except Exception as e:
                return f"Σφάλμα κατά το ανέβασμα της εικόνας: {e}"
        clips = []
        clip_length = 2.5
        start_time = 0
        for url in image_urls:
            clip = {
                "asset": {"type": "image", "src": url},
                "start": start_time,
                "length": clip_length,
                "effect": "zoomIn",
                "transition": {"in": "fade", "out": "fade"}
            }
            clips.append(clip)
            start_time += clip_length
        if platform_choice == 'vertical':
            width, height = 1080, 1920
            music_category = "upbeat"
        else:
            width, height = 1080, 1080
            music_category = "cinematic"
            
        # --- ΑΛΛΑΓΗ: Παίρνουμε τη μουσική από το Pexels ---
        music_url = get_music_from_pexels(music_category)
        
        timeline = {
            "background": "#000000",
            "tracks": [{"clips": clips}]
        }
        if music_url:
            timeline["soundtrack"] = {
                "src": music_url,
                "effect": "fadeInFadeOut"
            }

        output = {"format": "mp4", "size": {"width": width, "height": height}}
        payload = {"timeline": timeline, "output": output}
        headers = {
            "Content-Type": "application/json",
            "x-api-key": SHOTSTACK_API_KEY
        }
        try:
            response = requests.post(SHOTSTACK_API_URL, json=payload, headers=headers)
            response.raise_for_status()
            render_id = response.json()["response"]["id"]
            return redirect(url_for('status', render_id=render_id))
        except requests.exceptions.RequestException as e:
            error_message = response.text if 'response' in locals() else str(e)
            return f"Σφάλμα επικοινωνίας με το Shotstack API: {error_message}"
    return render_template('index.html')


# --- Οι άλλες διαδρομές παραμένουν ίδιες ---
@app.route('/status/<render_id>')
def status(render_id):
    return render_template('status.html', render_id=render_id)

@app.route('/get-status/<render_id>')
def get_status(render_id):
    status_url = f"{SHOTSTACK_API_URL}/{render_id}"
    headers = {"x-api-key": SHOTSTACK_API_KEY}
    try:
        response = requests.get(status_url, headers=headers)
        response.raise_for_status()
        data = response.json()["response"]
        if data["status"] == "failed":
            return jsonify({
                "status": "failed",
                "url": None,
                "error": data.get("error", "Άγνωστο σφάλμα από το Shotstack")
            })
        return jsonify({
            "status": data["status"],
            "url": data.get("url")
        })
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "failed", "error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
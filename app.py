from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        uploaded_image = request.files['image']
        platform_choice = request.form.get('platform')

        # Ορίζουμε τις ρυθμίσεις του βίντεο με βάση την επιλογή (vertical ή square)
        if platform_choice == 'vertical':
            # Κάθετο βίντεο για TikTok, Instagram Reels, YouTube Shorts, Pinterest
            width = 1080
            height = 1920
            duration = 15  # seconds
            platform_name = "TikTok / Instagram Reel / YouTube Short / Pinterest"
        
        elif platform_choice == 'square':
            # Τετράγωνο βίντεο για Facebook Feed
            width = 1080
            height = 1080
            duration = 30 # seconds
            platform_name = "Facebook Post"

        else:
            # Προεπιλογή σε περίπτωση σφάλματος
            width = 1080
            height = 1080
            duration = 20 # seconds
            platform_name = "Default"

        # (Εδώ θα μπει η λογική για την κλήση στο Shotstack API)

        # Προς το παρόν, επιστρέφουμε μια σελίδα επιβεβαίωσης
        return f"<h1>Έτοιμο για Δημιουργία!</h1>" \
               f"<p><b>Επιλεγμένη Μορφή:</b> {platform_name}</p>" \
               f"<p><b>Όνομα Αρχείου:</b> {uploaded_image.filename}</p>" \
               f"<p><b>Ρυθμίσεις Βίντεο:</b> {width}x{height}, Διάρκεια: {duration}s</p>"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
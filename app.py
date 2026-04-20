from flask import Flask, request, jsonify
from flask_cors import CORS
import requests, re, os

app = Flask(__name__)
CORS(app)

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.json.get('url')
    if not url.startswith('http'): url = 'https://' + url
    try:
        res = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        emails = list(set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', res.text)))
        return jsonify({"emails": [e for e in emails if not e.lower().endswith(('.png', '.jpg'))]})
    except:
        return jsonify({"emails": []})

if __name__ == "__main__":
    # This line is critical for the cloud to work
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

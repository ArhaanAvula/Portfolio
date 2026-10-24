from flask import Flask, request, jsonify
import lightgbm as lgb
import numpy as np
import logging
from urllib.parse import urlparse
import re
from flask_cors import CORS

suspicious_words = ['login', 'secure', 'account', 'update', 'free', 'verify', 'webscr']
suspicious_tlds = ['.xyz', '.top', '.club', '.online', '.info', '.biz']

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
CORS(app)

# Load the trained model
model = lgb.Booster(model_file='lightgbm_model_advanced.txt')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    app.logger.info(f"Received JSON: {data}")
    
    if 'url' not in data:
        return jsonify({'error': 'Missing "url" in request'}), 400

    url = data['url']
    app.logger.info(f"URL to predict: {url}")

    # Feature extraction (basic example, not full feature set!)
    url_length = len(url)
    num_dots = url.count('.')
    has_https = int(urlparse(url).scheme == 'https')
    has_ip = 1 if re.match(r'^\d+\.\d+\.\d+\.\d+$', urlparse(url).netloc) else 0
    count_at = url.count('@')
    count_question = url.count('?')
    count_percent = url.count('%')
    count_slashes = urlparse(url).path.count('/')
    count_equal = url.count('=')
    count_suspicious_words = sum(word in url.lower() for word in suspicious_words)
    domain = urlparse(url).netloc
    domain_length = len(domain)
    count_subdomains = max(len(domain.split('.')) - 2, 0)
    hyphen_in_domain = 1 if '-' in domain else 0
    count_digits = sum(c.isdigit() for c in url)
    count_letters = sum(c.isalpha() for c in url)
    count_special_chars = sum(url.count(c) for c in ['#', '&', '~', '$', '!', '*'])
    ends_with_slash = 1 if url.endswith('/') else 0
    at_in_path = 1 if '@' in urlparse(url).path else 0
    subdirectory_depth = len([p for p in urlparse(url).path.split('/') if p]) - 1
    digit_ratio = count_digits / url_length if url_length > 0 else 0
    suspicious_tld = 1 if any(domain.endswith(tld) for tld in suspicious_tlds) else 0
    
    # Format for LightGBM
    features = np.array([[
    has_ip, has_https, count_at, count_question, count_percent,
    count_slashes, count_equal, count_suspicious_words, domain_length,
    count_subdomains, hyphen_in_domain, url_length, count_digits,
    count_letters, count_special_chars, ends_with_slash, at_in_path,
    subdirectory_depth, digit_ratio, suspicious_tld
]])

    prediction = model.predict(features)
    is_scam = prediction[0] > 0.36

    return jsonify({'prediction': bool(is_scam)})

if __name__ == '__main__':
    app.run(debug=True)





# from flask import Flask, request, jsonify
# import lightgbm as lgb
# import numpy as np
# import sys
# import logging

# app = Flask(__name__)

# logging.basicConfig(level=logging.DEBUG)

# # Load the pre-trained LightGBM model, don't use joblib
# model = lgb.Booster(model_file='lightgbm_model_advanced.txt')

# @app.route('/predict', methods=['POST'])
# def predict():
#     app.logger.info(f"Received JSON: {data}")
#     data = request.get_json()  # JSON should contain: { "url": "http://..." }
#     print(data)
#     print("Received data:", data)
#     url = data['url']

#     # Feature extraction (same as in training)
#     url_length = len(url)
#     num_dots = url.count('.')
#     has_https = int('https' in url.lower())

#     # Format features for model prediction/add ALL features
#     features = np.array([[url_length, num_dots, has_https]])

#     # Make prediction using the trained model
#     prediction = model.predict(features)

#     # Return the prediction result as JSON
#     is_scam = (prediction[0]) > 0.36 # Convert to True/False
#     return jsonify({'prediction': bool(is_scam)})

# if __name__ == '__main__':
#     app.run(debug=True)
"""
Flask API of the SMS Spam detection model model.
"""
import os
import joblib
from flask import Flask, jsonify, request
from flasgger import Swagger
import pandas as pd
import sys
import requests

from text_preprocessing import prepare, _extract_message_len, _text_process

sys.modules['__main__']._text_process = _text_process
sys.modules['__main__']._extract_message_len = _extract_message_len

app = Flask(__name__)
swagger = Swagger(app)

MODEL_DIR = os.getenv("MODEL_DIR", "app/models")
MODEL_VERSION = os.getenv("MODEL_VERSION", "model-6")
MODEL_PATH = f"{MODEL_DIR}/{MODEL_VERSION}/model.joblib"
PREPROCESSOR_PATH = f"{MODEL_DIR}/{MODEL_VERSION}/preprocessor.joblib"
MODEL_REPO = os.getenv('MODEL_REPO', 'doda25-team18/model-service')

def download_model():
    """
    Downloads the model file from GitHub releases if it does not exist locally.
    Notes:
    - AI tools were used to assist in writing this function.
    """
    model_dir = os.path.dirname(MODEL_PATH)
    os.makedirs(model_dir, exist_ok=True)

    base_url = f'https://github.com/doda25-team18/model-service/releases/download/{MODEL_VERSION}'


    for filename in ['model.joblib', 'preprocessor.joblib']:
        url = f'{base_url}/{filename}'
        filepath = os.path.join(model_dir, filename)
        resp = requests.get(url)

        if resp.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(resp.content)
            print(f"Downloaded {filename}")
        else:
            raise Exception(f"Failed to download {filename}: HTTP {resp.status_code}")

# Check if model exists - otherwise download the model
if os.path.exists(MODEL_PATH) and os.path.exists(PREPROCESSOR_PATH):
    print(f"Model found in volume: {MODEL_PATH}, using it...")
else:
    print(f"Model not found in volume: {MODEL_DIR}, downloading {MODEL_VERSION}...")
    download_model()

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict whether an SMS is Spam.
    ---
    consumes:
      - application/json
    parameters:
        - name: input_data
          in: body
          description: message to be classified.
          required: True
          schema:
            type: object
            required: sms
            properties:
                sms:
                    type: string
                    example: This is an example of an SMS.
    responses:
      200:
        description: "The result of the classification: 'spam' or 'ham'."
    """
    input_data = request.get_json()
    sms = input_data.get('sms')
    processed_sms = prepare(sms)
    model = joblib.load(MODEL_PATH)
    prediction = model.predict(processed_sms)[0]

    res = {
        "result": prediction,
        "classifier": "decision tree",
        "sms": sms
    }
    print(res)
    return jsonify(res)

if __name__ == '__main__':
    #clf = joblib.load('output/model.joblib')
    app.run(host="0.0.0.0", port=8081, debug=True)
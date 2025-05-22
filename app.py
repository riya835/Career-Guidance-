from flask_cors import CORS
from flask import Flask, request, jsonify
import numpy as np
import pickle
from keras.models import load_model

app = Flask(_name_)
CORS(app, resources={r"/": {"origins": ""}})

# Load the trained FNN model
model = load_model("career_fnn_model.h5")

# Load the scaler and label encoders
with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

with open("label_encoders.pkl", "rb") as f:
    label_encoders = pickle.load(f)

@app.route('/')
def home():
    return "Flask is working!"

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    try:
        # Get the user answers sent as JSON
        user_answers = request.get_json()
        if not user_answers:
            return jsonify({"error": "No data received"}), 400

        # Convert user answers to a format that the model expects (a feature vector)
        feature_vector = np.array([user_answers.get(str(i), 0) for i in range(17)]).reshape(1, -1)

        # Normalize the feature vector using the scaler
        feature_vector = scaler.transform(feature_vector)

        # Predict the career role using the trained model
        predicted_role = model.predict(feature_vector)
        role_index = np.argmax(predicted_role, axis=1)[0]
        predicted_role_name = label_encoders["Role"].inverse_transform([role_index])[0]

        # Return the predicted career role as a JSON response
        return jsonify({"role": predicted_role_name})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if _name_ == '_main_':
    app.run(debug=True)
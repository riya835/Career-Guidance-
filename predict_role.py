import numpy as np
from keras.models import load_model
import pickle

# Load the preprocessed data and label encoders
data = np.load("career_data.npz")
X_test = data["X_test"]

with open("label_encoders.pkl", "rb") as f:
    label_encoders = pickle.load(f)

# Load the trained model
model = load_model("career_fnn_model.h5")

# Make predictions on the test set (or any other sample data)
sample_input = X_test[0].reshape(1, -1)  # Reshape the input if needed
predicted_role = label_encoders["Role"].inverse_transform(np.argmax(model.predict(sample_input), axis=1))

# Print the predicted role
print(f"Predicted Role for sample input: {predicted_role[0]}")
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from sklearn.metrics import accuracy_score
import pickle

# Load the preprocessed dataset
data = np.load("career_data.npz")
X_train, X_test, y_train, y_test = data["X_train"], data["X_test"], data["y_train"], data["y_test"]

# Load the saved scaler and label encoders
with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

with open("label_encoders.pkl", "rb") as f:
    label_encoders = pickle.load(f)

# Define the model
model = Sequential()

# Input layer: Number of input neurons should match the number of features
model.add(Dense(64, input_dim=X_train.shape[1], activation='relu'))

# Hidden layer: You can experiment with the number of neurons
model.add(Dense(32, activation='relu'))

# Output layer: Use softmax activation for multi-class classification
model.add(Dense(len(label_encoders["Role"].classes_), activation='softmax'))

# Compile the model
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Evaluate the model on the test set
y_pred = np.argmax(model.predict(X_test), axis=1)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Save the trained model
model.save("career_fnn_model.h5")

# Predict on some test data (optional)
sample_input = X_test[0].reshape(1, -1)  # Reshape the input if needed
predicted_role = label_encoders["Role"].inverse_transform(np.argmax(model.predict(sample_input), axis=1))
print(f"Predicted Role: {predicted_role[0]}")
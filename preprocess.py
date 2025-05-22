import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pickle

# Load dataset
file_path = "C:/Users/khand/OneDrive/Desktop/softcomputing/dataset9000.csv"
df = pd.read_csv(file_path)

# Handle missing values
df.dropna(inplace=True)

# Encode categorical columns
label_encoders = {}
for column in df.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le

# Separate features (X) and target (y)
X = df.drop(columns=["Role"])  # Ensure "Role" is correct
y = df["Role"]

# Encode target labels
le_role = LabelEncoder()
y = le_role.fit_transform(y)
label_encoders["Role"] = le_role  # Save label encoder for later use

# Normalize numerical features
scaler = StandardScaler()
X = scaler.fit_transform(X)  # Scale the entire dataset before splitting

# Split dataset properly
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Save encoders and scaler for later use
with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

with open("label_encoders.pkl", "wb") as f:
    pickle.dump(label_encoders, f)

# Save preprocessed data
np.savez("career_data.npz", X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test)

print("✅ Dataset preprocessing complete. Files saved!")

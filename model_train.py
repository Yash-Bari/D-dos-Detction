import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load the dataset
df = pd.read_csv(r"modified_cicddos2019_dataset.csv")  # Replace "your_dataset.csv" with the path to your dataset

# Preprocessing: assuming the dataset has already been preprocessed and cleaned

# Split the data into features (X) and target (y)
X = df.drop(["Label", "Class"], axis=1)  # Assuming "Label" and "Class" are the target columns
y = df["Class"]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the model
model = RandomForestClassifier()

# Train the model
model.fit(X_train, y_train)

# Make predictions on the testing data
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Save the trained model
joblib.dump(model, "ddos_detection_model.pkl")  # Replace "ddos_detection_model.pkl" with your desired filename

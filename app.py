import joblib
import pandas as pd
from flask import Flask, request, render_template, jsonify
import json

app = Flask(__name__)

# Load the trained model
model = joblib.load("ddos_detection_model.pkl")

# Define a route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Endpoint to receive network traffic data and make predictions
@app.route('/predict', methods=['POST'])
def predict():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})

    file = request.files['file']
    
    # Check if the file is empty
    if file.filename == '':
        return jsonify({'error': 'Empty file uploaded'})

    # Check if the file is a JSON file
    if file and file.filename.endswith('.json'):
        try:
            # Load the JSON data from file
            json_data = json.load(file)
            
            # Convert the JSON data into a DataFrame
            input_data = pd.DataFrame([json_data])
            
            # Ensure proper data transformation
            # Handle missing features if necessary
            # Ensure correct data types
            
            # Make sure input_data contains all required features
            # If input_data has fewer features than expected, you can add dummy values for missing features
            if input_data.shape[1] < 78:
                # Add dummy values for missing features
                missing_features = set(['Protocol', 'Flow Duration', 'Total Fwd Packets', 'Total Backward Packets', 'Fwd Packets Length Total', 'Bwd Packets Length Total', 'Fwd Packet Length Max', 'Fwd Packet Length Min', 'Fwd Packet Length Mean', 'Fwd Packet Length Std', 'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Bwd Packet Length Mean', 'Bwd Packet Length Std', 'Flow Bytes/s', 'Flow Packets/s', 'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min', 'Fwd IAT Total', 'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min', 'Bwd IAT Total', 'Bwd IAT Mean', 'Bwd IAT Std', 'Bwd IAT Max', 'Bwd IAT Min', 'Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd URG Flags', 'Bwd URG Flags', 'Fwd Header Length', 'Bwd Header Length', 'Fwd Packets/s', 'Bwd Packets/s', 'Packet Length Min', 'Packet Length Max', 'Packet Length Mean', 'Packet Length Std', 'Packet Length Variance', 'FIN Flag Count', 'SYN Flag Count', 'RST Flag Count', 'PSH Flag Count', 'ACK Flag Count', 'URG Flag Count', 'CWE Flag Count', 'ECE Flag Count', 'Down/Up Ratio', 'Avg Packet Size', 'Avg Fwd Segment Size', 'Avg Bwd Segment Size', 'Fwd Avg Bytes/Bulk', 'Fwd Avg Packets/Bulk', 'Fwd Avg Bulk Rate', 'Bwd Avg Bytes/Bulk', 'Bwd Avg Packets/Bulk', 'Bwd Avg Bulk Rate', 'Subflow Fwd Packets', 'Subflow Fwd Bytes', 'Subflow Bwd Packets', 'Subflow Bwd Bytes', 'Init Fwd Win Bytes', 'Init Bwd Win Bytes', 'Fwd Act Data Packets', 'Fwd Seg Size Min', 'Active Mean', 'Active Std', 'Active Max', 'Active Min', 'Idle Mean', 'Idle Std', 'Idle Max', 'Idle Min']) - set(input_data.columns)
                for feature in missing_features:
                    input_data[feature] = 0  # You may need to adjust this depending on the data and model requirements
            
            # Make predictions using the trained model
            prediction = model.predict(input_data)
            
            # Return the prediction as JSON response
            return jsonify({'prediction': prediction.tolist()})
        
        except Exception as e:
            return jsonify({'error': 'Error processing file: {}'.format(str(e))})

    else:
        return jsonify({'error': 'Invalid file format. Please upload a JSON file'})

if __name__ == '__main__':
    app.run(debug=True)

import os
import numpy as np
import pandas as pd
from flask import Flask, request, render_template
from sklearn.preprocessing import MinMaxScaler
from werkzeug.utils import secure_filename
import pickle

# Initialize the Flask App
app = Flask(__name__)

# Helper function to load the model
def load_model(file_path):
    try:
        with open(file_path, 'rb') as file:
            model = pickle.load(file)
        return model
    except FileNotFoundError:
        print(f"File {file_path} not found. Please check the file path and try again.")
        return None

# Load the trained model
model_path = os.path.join(os.path.dirname(__file__), 'stress.pkl')
stress_model = load_model(model_path)

if stress_model is None:
    raise FileNotFoundError(f"Model file not found at {model_path}")

# Home route
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# Login route
@app.route('/login')
def login():
    return render_template('login.html')

# Upload route
@app.route('/upload')
def upload():
    return render_template('upload.html')

# Preview route to display uploaded CSV data
@app.route('/preview', methods=["POST"])
def preview():
    if request.method == 'POST':
        dataset = request.files['datasetfile']
        df = pd.read_csv(dataset, encoding='unicode_escape')
        df.set_index('Id', inplace=True)
        return render_template("preview.html", df_view=df)

# Prediction route (GET and POST)
@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    return render_template('prediction.html')

# Predict route for handling prediction requests
@app.route('/predict', methods=['POST'])
def predict():
    int_features = [x for x in request.form.values()]
    final_features = [np.array(int_features)]
    result = stress_model.predict(final_features)[0]

    # Mapping result to stress levels
    stress_levels = {
        0: "Low/Normal",
        1: "Medium Low",
        2: "Medium",
        3: "Medium High",
        4: "High"
    }
    prediction_text = stress_levels.get(result, "Unknown")

    return render_template('prediction.html', prediction_text=prediction_text)

# Performance route
@app.route('/performance')
def performance():
    return render_template('performance.html')

# Chart route
@app.route('/chart')
def chart():
    return render_template('chart.html')

if __name__ == "__main__":
    app.run(debug=True)

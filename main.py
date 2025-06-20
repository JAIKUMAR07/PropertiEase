import pandas as pd
import numpy as np
import pickle
from flask import Flask, render_template, request
import os

# Initialize Flask app
app = Flask(__name__)

# Load data
try:
    data = pd.read_csv('Cleaned_data.csv')
except FileNotFoundError:
    print("👉 'Cleaned_data.csv' not found. Please ensure it's in the same directory.")
    exit()

# Load trained model
try:
    pipe = pickle.load(open('RidgeModel.pkl', 'rb'))
except FileNotFoundError:
    print("👉 'RidgeModel.pkl' not found. Please ensure it's in the same directory.")
    exit()

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/buy')
def buy():
    return render_template('buy.html')

@app.route('/estimate_cost')
def estimate_cost():
    locations = sorted(data['location'].unique())
    return render_template('prediction.html', locations=locations)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        location = request.form.get('location')
        bhk = int(request.form.get('bhk'))
        bath = int(request.form.get('bath'))
        sqft = float(request.form.get('total_sqft'))
        balcony = int(request.form.get('balcony'))

        input_data = pd.DataFrame([[location, sqft, bath, bhk, balcony]],
                                  columns=['location', 'total_sqft', 'bath', 'bhk', 'balcony'])

        prediction = pipe.predict(input_data)[0] * 1e5

        return render_template('result.html', price=prediction)

    except Exception as e:
        return f"⚠️ Prediction failed: {e}"

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True, port=5001)

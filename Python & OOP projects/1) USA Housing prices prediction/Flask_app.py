from flask import Flask, request, render_template
import joblib
import numpy as np
import pandas as pd


data = pd.read_csv("house_sales.csv", sep = '\t')
y = data['AdjSalePrice']

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods = ['POST'])

def predict():

    # Load saved model
    model = joblib.load('Housing_prices_predictor.pkl')

    # Get input variables from form
    SqFtLot = request.form['SqFtLot']
    SqFtTotLiving = request.form['SqFtTotLiving']
    SqFtFinBasement = request.form['SqFtFinBasement']
    Bathrooms = request.form['Bathrooms']
    Bedrooms = request.form['Bedrooms']
    YrRenovated = request.form['YrRenovated']
    TrafficNoise = request.form['TrafficNoise']
    LandVal = request.form['LandVal']
    ImpsVal = request.form['ImpsVal']
    NewConstruction_encoded = request.form['NewConstruction_encoded']

    # Make prediction
    y_pred_all = model.predict([[SqFtLot, SqFtTotLiving, SqFtFinBasement, Bathrooms, Bedrooms, YrRenovated, TrafficNoise, LandVal, ImpsVal, NewConstruction_encoded]])


    # Compute the mean and standard deviation of the target variable in the original data
    adj_saleprice_mean = np.mean(y)
    adj_saleprice_std = np.std(y)

    # Reverse the scaling of the predicted values
    y_pred_all_original_scale = y_pred_all * adj_saleprice_std + adj_saleprice_mean

    # Round the predicted values to the nearest integer
    y_pred_all_original_scale = np.round(y_pred_all_original_scale)
    
    # Return result to user
    return render_template('index.html', prediction_text = 'Predicted House Price: ${:,.2f}'.format(y_pred_all[0]))


if __name__ == '__main__':
    app.run(debug = True)

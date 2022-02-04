#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 18:25:59 2022

@author: aakashdeorukhkar
"""

from flask import Flask,render_template,request
import jsonify
import requests
import joblib
import numpy as np
import sklearn
import pandas as pd

app = Flask(__name__)

#Loading the XGBoost Model 

xgbmodel = joblib.load('spotifyXGB')

@app.route("/")
def Home():
    return render_template('main.html')

@app.route("/predict", methods=['POST'])
def predict():
    print("Im here")
    if request.method == 'POST':
        danceability = float(request.form['danceability'])
        energy=float(request.form['energy'])
        key=int(request.form['key'])
        loudness = float(request.form['loudness'])
        mode =request.form['mode']
        if(mode=='Major'):
            mode=1
        else:
            mode=0
        speechiness = float(request.form['speechiness'])
        acousticness=float(request.form['acousticness'])
        instrumentalness = float(request.form['instrumentalness'])
        liveness=float(request.form['liveness'])
        valence = float(request.form['valence'])
        tempo=float(request.form['tempo'])
        duration_ms = int(request.form['duration_ms'])
        time_signature = int(request.form['time_signature'])
        chorus_hit = float(request.form['chorus_hit'])
        sections = int(request.form['sections'])
        
        input_variables = pd.DataFrame([[danceability,energy,key,loudness,mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo,duration_ms,time_signature,chorus_hit,sections]])
        
        prediction = xgbmodel.predict(input_variables)
        output = int(prediction[0])
        print(output)
        if output==1:
            return render_template('main.html',prediction_texts="I see this song on Billboard Hot 100 list")
        else:
            return render_template('main.html', prediction_texts="You have your own audience. You are not mainstream!")
    else:
        return render_template('main.html',prediction_texts="Something went wrong!")

# training data did not have the following fields: danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, duration_ms, time_signature, chorus_hit, sections
# FLASK_APP=app.py flask run

if __name__=='__main__':
    app.run(port=5000,debug=True)
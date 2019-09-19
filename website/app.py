#importing libraries
import os
import numpy as np
import flask
import pickle
from flask import Flask, render_template, request
import pandas as pd

#creating instance of the class
app=Flask(__name__)

#to tell flask what url shoud trigger the function index()
@app.route('/')
@app.route('/index')
def index():
    return flask.render_template('index.html')

#preprocessing function
def InputPreproc(to_predict_df):
    print(to_predict_df.columns)
    to_predict_df = to_predict_df.astype({'HomeGame': 'int32', 'TeamScore': 'int32', 'OppScore': 'int32', 'Down': 'int32', 'Distance': 'int32',  'YardLine': 'int32'})

    #to_predict_df['HomeGame'] = to_predict_df.HomeGame.astype('int32')
    print('HomeGame')
    to_predict_df['Score_diff'] = to_predict_df.TeamScore - to_predict_df.OppScore
    print('Score_diff')
    to_predict_df['Down'] = to_predict_df.Down
    to_predict_df['ToGo'] = to_predict_df.Distance
    to_predict_df['Distance_to_goal'] = pd.np.where(to_predict_df.Side == '50', (50 - to_predict_df.YardLine) + 50, to_predict_df.YardLine)
    times = to_predict_df.Time.str.split(':', expand = True)
    to_predict_df['Time_dec'] = times[0].astype('float64') + (times[1].astype('float64')/60)

    to_predict_df['Time_left_in_game'] = pd.np.where(to_predict_df.Quarter == 1, 45 + to_predict_df['Time_dec'], pd.np.where(to_predict_df.Quarter == 2, 30 + to_predict_df['Time_dec'], pd.np.where(to_predict_df.Quarter == 3, 15 + to_predict_df['Time_dec'], to_predict_df['Time_dec'])))
    out = to_predict_df[['Down', 'ToGo', 'HomeGame', 'Score_diff', 'Distance_to_goal', 'Time_left_in_game']]
    return(out)


#prediction function
def ValuePredictor(to_predict_processed):
    loaded_model = pickle.load(open("Models/Run_Pass_XGB.pkl","rb"))
    result = loaded_model.predict_proba(to_predict_processed)
    print(result)
    result = result[0,1]
    print(result)
    return result


@app.route('/result',methods = ['POST'])
def result():
    if request.method == 'POST':
        to_predict_dict = request.form.to_dict()
        print(to_predict_dict)
        to_predict_df = pd.DataFrame([to_predict_dict])
        print(to_predict_df)
        to_predict_processed = InputPreproc(to_predict_df)
        result = ValuePredictor(to_predict_processed)
        
        if result > .5:
            prediction='Pass'
        else:
            prediction='Run'
        
        #passProb = round(result, 3) 
        passProb = round(result * 100, 1)
            
        return render_template("result.html",
        prediction=prediction, 
        passProb = passProb, 
        HomeGame = to_predict_df.HomeGame[0], 
        TeamScore = to_predict_df.TeamScore[0],
        OppScore = to_predict_df.OppScore[0],
        Quarter = to_predict_df.Quarter[0],
        Time = to_predict_df.Time[0],
        Side = to_predict_df.Side[0],
        Down = to_predict_df.Down[0],
        Distance = to_predict_df.Distance[0],
        YardLine = to_predict_df.YardLine[0]
        )

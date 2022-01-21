from flask import Flask, render_template, url_for, flash, redirect,session, request
import pandas as pd
import numpy as np
import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import json
app = Flask(__name__)
app.config['SECRET_KEY'] ="Kaya"

@app.route('/')
def test():
    dates = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    hr_zone_fig_list_json = []
    labels_matrix = []
    values_matrix = []
    specs_matrix =[]
    patient_id = 27

    for i in dates:
        # Read each file date wise
        path = "/Users/shehjarsadhu/Desktop/UniversityOfRhodeIsland/Graduate/ResearchWBL/My_Thesis/careportal-flaskapp/care-portal-thesis-sub/PatientID_" +str(patient_id) + "/HR_ACT_Resample_40Hz_PID_" + str(patient_id) + "_" + str(i) + "_Date_ID_HR.csv"
        print(path)
        df_hr_zone = pd.read_csv(path)
        labels = ['level. < 60%',' 55%-75%','75%-90%.','90%-105%','105%-120%','120%-130%','>120%',"No classification"]
        values = [df_hr_zone[df_hr_zone.HR_ACT_ZONE_MORE == 0].shape[0],df_hr_zone[df_hr_zone.HR_ACT_ZONE_MORE == 1].shape[0],df_hr_zone[df_hr_zone.HR_ACT_ZONE_MORE == 2].shape[0],df_hr_zone[df_hr_zone.HR_ACT_ZONE_MORE == 3].shape[0],df_hr_zone[df_hr_zone.HR_ACT_ZONE_MORE == 4].shape[0],df_hr_zone[df_hr_zone.HR_ACT_ZONE_MORE == 5].shape[0],df_hr_zone[df_hr_zone.HR_ACT_ZONE_MORE == 6].shape[0],df_hr_zone[df_hr_zone.HR_ACT_ZONE_MORE == -1].shape[0]]
        labels_matrix.append(labels)
        values_matrix.append(values)
        specs_matrix.append([{"type": "pie"}])
    fig = make_subplots(rows=len(labels_matrix), cols=1, specs=specs_matrix)
    for idx, (i, j) in enumerate(zip(labels_matrix, values_matrix)):
        if idx != 0:
            print(idx, "Lables \n",i, "values \n",j)
            fig.add_trace(go.Pie(labels=i, values=j, hole=.3
                    ,name="Pie CHart of HR based Activity Zones"), row=idx, col=1)
    fig.update_layout(title="HR activity Zones",height=5000, width=1000)
    hr_zone_fig =  json.dumps(fig, cls = plotly.utils.PlotlyJSONEncoder)

    return render_template('test.html',hr_zone_fig=hr_zone_fig)
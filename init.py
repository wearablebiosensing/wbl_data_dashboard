#####################################
# Author: Shehjar Sadhu.            
# Project: Care- l.            
# Date: Updated Sept1st 2021 from Pi   
#####################################
import os
import json
from typing import Dict
from flask import Flask, render_template, url_for, flash, redirect,session, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import plotly
from flask_login import UserMixin
from flask_login import login_user, current_user, logout_user, login_required
import pandas as pd
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
from utils.hr_features import *
import time
app = Flask(__name__)
app.config['SECRET_KEY'] ="Kaya"
# Set database instances
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database/careportal-dev-hr.db'
app.config['RECAPTCHA_USE_SSL']= False
#Site key: 6LcijG0cAAAAACKIXc3CVPuEfvl6pf2dFERY7gNU
# Seceret Key 6LcijG0cAAAAAG38qeW2Ay0Y4bOSBN8ZmvSigNLm

app.config['RECAPTCHA_PUBLIC_KEY']= '6LcijG0cAAAAACKIXc3CVPuEfvl6pf2dFERY7gNU'
app.config['RECAPTCHA_PRIVATE_KEY']='6LcijG0cAAAAAG38qeW2Ay0Y4bOSBN8ZmvSigNLm'
app.config['RECAPTCHA_OPTIONS'] = {'theme':'white'}
# Create a db instance.
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
# Init log in manager for flask app.
login_manager = LoginManager(app)
login_manager.login_view = 'login'
root_pi = "/var/www/html/web"
p_27 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
p_34 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
p_52 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
p_53 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
p_75 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
p_80 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
p_88 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
p_90 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
p_106 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
p_118 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
p_129 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
p_131 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
# Returns a list of Dates based on Date ID.
def get_dates(patient_id):
    date_id_list = []
    if patient_id == 27:
        date_id_list = p_27
    elif patient_id == 34:
        date_id_list = p_34
    elif patient_id == 52:
        date_id_list = p_52
    elif patient_id == 53:
        date_id_list = p_53
    elif patient_id == 75:
        date_id_list = p_75
    elif patient_id == 80:
        date_id_list = p_80
    elif patient_id == 88:
        date_id_list = p_88
    elif patient_id == 90:
        date_id_list = p_90
    elif patient_id == 106:
        date_id_list = p_106
    elif patient_id == 118:
        date_id_list = p_118
    elif patient_id == 129:
        date_id_list = p_129
    elif patient_id == 131:
        date_id_list = p_131
    return date_id_list

class user_doctor(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    email = db.Column(db.String(1000),nullable=False)
    password = db.Column(db.String(600),nullable=False)

class user_patient(db.Model):
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user_doctor.id'),nullable=False)
    acc_path = db.Column(db.String(10000),nullable=False)
    hr_path = db.Column(db.String(10000),nullable=False)

# This import is here because of variable defined above are needed in forms .py
from forms import RegisterFormDoctors, LogInFormDoctors,DateDropDown_form

# To filter by Hour and Date&Time. Give it a dataset for one day only apply that filter before feeding.
def unique_time_stamps(df):
    time_stamp_list = [] # get the unique time stamps int he paricular df.
    for idx,val in enumerate(df["Time"]):
        #print("TS: ",val,val[11:13])
        time_stamp_list.append(val[11:13])
    return np.unique(np.array(time_stamp_list))

@login_manager.user_loader
def load_user(user_id):
    return user_doctor.query.get(int(user_id))
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/about')
def about():
    return render_template('about.html')
# Registers the doctors and inserts their information in the database
@app.route('/registerdoctor',methods = ["GET", "POST"])
def register_doctors():
    form = RegisterFormDoctors()
    # If form is valid print a message and redirect the users to the log in page
    if form.validate_on_submit():
        # Generate the hased the password using bcrypt API .
        pass_hash = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        # Create a new user instance.
        user = user_doctor(email=form.email.data, password=pass_hash)
        db.session.add(user)
        db.session.commit()
        flash(f"Account is created for {form.name.data}!","success")
        return redirect(url_for("login_doctors"))
    #Else redirect back to the register page.
    return render_template('register_doctors.html',form=form)

@app.route('/logindoctor',methods = ["POST", "GET"])
def login_doctors():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LogInFormDoctors()
    print("user_doctor :",user_doctor.query.all())
    user = user_doctor.query.filter_by(email=form.email.data).first()
    #user_p = user_doctor.query.filter_by(password=form.email.data).first()
    # print("USER: ",user.columns.keys())
    print("Form FIelds = ",form.validate_on_submit())
    # Check is the fields in the form are valid.
    if form.validate_on_submit():
        print("user = ",form.email.data)
        # print("PSS: ",user.password, form.password.data)
        # If they are valid then check if the user exists in the database and check if they entered the correct password.
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f"Logged in {form.email.data}","success")
            return redirect(url_for("home"))        
        #Else display error message.
        else:
            flash(f"Not logged in","danger")
    return render_template('login_doctors.html', title='login',form=form)

@app.route('/signout')
def signout():
    logout_user()
    return redirect(url_for("home"))


# Calculates HR features for a particular patient, plots the HR feaure values like RR interval,SSDRR.
@app.route('/patient/<int:patient_id>', methods=['GET', 'POST'])
@login_required
def patient(patient_id):
    graphs = []
    day = []
    print("patient(): patient_id",patient_id)
    patientId = user_patient.query.get(patient_id)
    #path =  os.getcwd()  + patientId.hr_path
    print("patient(): From DB Before Conversion",patientId.id)
    patientId = patientId.id
    if patientId == 1:
        patientId = 27
    elif patientId  == 2: 
        patientId = 34
    elif patientId  == 3:
        patientId = 52
    elif patientId  == 4:
        patientId = 53
    elif patientId  == 5:
        patientId = 75
    elif patientId  == 6:
        patientId = 80
    elif patientId  == 7:
        patientId = 88
    elif patientId  == 8:
        patientId = 90
    elif patientId  == 9:
        patientId = 106   
    elif patientId  == 10:
        patientId = 118    
    elif patientId  == 10:
        patientId = 129    
    elif patientId  == 11:
        patientId = 131  
    elif patientId  == 12:
        patientId = 584   
    print("patient(): After Conversion",patientId)
    date_id_list = get_dates(patientId)
    # Unique dates from a particular patient.
    dates = date_id_list
    # wtf forms displays the forms on the web page
    form = DateDropDown_form()
    # Gets the unique avaliable dates from a patient.
    form.date.choices = [(date) for date in dates]
    #print("date list: ",dates)
    #print("selected date:  ",form.date.data)
    # Read from plotly json file and put it in. 
    stats_hr_json_path =  "./static/plotlycharts/PatientID_"+ str(patientId)+"/hr_stats_pid_" + str(patientId) +".json" #"./static/plotlycharts/PatientID_"+str(27) + "/hr_stats_pid_" + str(27) + ".json"                
    patient_resuorce = "./static/hl7_FHIR/patient_resource.json"
    with open(stats_hr_json_path, "r") as json_file:
        hr_stats = json.load(json_file)
    with open(patient_resuorce, "r") as json_file:
        patient_resuorce_json = json.load(json_file)
    print("patient_resuorce_json: \n",patient_resuorce_json["name"])
    family_name = patient_resuorce_json["name"][0]["family"]
    given_name  = patient_resuorce_json["name"][0]["given"][0]
    gender = patient_resuorce_json["gender"]
    max_d = hr_stats["max"][int(form.date.data)]
    min_d = hr_stats["min"][int(form.date.data)]
    std_d = round(hr_stats["std"][int(form.date.data)],2)
    mean_d = round(hr_stats["mean"][int(form.date.data)],2)

    file_name_hr = "plotlycharts/pid_27_did_"+ str(form.date.data) +"raw_hr.png"
    print("file_name_hr: ",file_name_hr) 
    hourly_average = plotly.io.read_json("./static/plotlycharts/PatientID_" + str(patientId) + "/"+ str(patientId) + "_DateId_"+ str(form.date.data) + "hourly_average.json")#"./static/plotlycharts/27_DateId_"+str(form.date.data)+"hourly_average.json")
    hourly_average_json = json.dumps(hourly_average, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template( 
        'patient.html', patientId = patientId,dates=dates,form = form,submitted_date=form.date.data,max_d=max_d,min_d=min_d,mean_d=mean_d,std_d=std_d,selected_date=str(form.date.data),file_name_hr=file_name_hr,hourly_average_json=hourly_average_json,family_name=family_name,given_name=given_name,gender=gender)

# Displays Activity Level Data for patient selected. Get the patient ID from route.
@app.route('/patient/<int:patient_id>/activity', methods=['GET', 'POST'])
@login_required
def activity_levels(patient_id,methods=['GET', 'POST']):
     patientId = user_patient.query.get(patient_id)
     print("activity_levels: ",patientId)
     path =  os.getcwd()  + patientId.acc_path
     date_id_list = get_dates(27)
     # Unique dates from a particular patient.
     dates = date_id_list #df['Date'].unique()
     print("Acc Dates:",dates)
     # wtf forms displays the forms on the web page
     form = DateDropDown_form()
     # Gets the unique avaliable dates from a patient.
     form.date.choices = [(date) for date in dates]
     print("date list: ",dates)
     print("selected date:  ",form.date.data)
     f_json = plotly.io.read_json("./static/plotlycharts/plotly_hr_zone_27date_id0_barchart.json")
     bar_chart = json.dumps(f_json, cls=plotly.utils.PlotlyJSONEncoder)
     f_json_hr = plotly.io.read_json( "./static/plotlycharts/pid_27_did_" + str(form.date.data) + "_piplot_activity.json")
     hr_pi_chart = json.dumps(f_json_hr, cls=plotly.utils.PlotlyJSONEncoder)
     stats_hr_json_path = "./static/plotlycharts/hr_stats_pid_" + str(27) + ".json"                
     with open(stats_hr_json_path, "r") as json_file:
         hr_stats = json.load(json_file)
     hr_activity_d_list = hr_stats["HR_Activity"][int(form.date.data)]
     return render_template('activity_level.html',patientId=patientId,form=form,dates=dates,hr_pi_chart=hr_pi_chart,selected_date=str(form.date.data),hr_activity_d_list=hr_activity_d_list)

# To display pi chart of overall patient progress.
@app.route('/patient/<int:patient_id>/overall', methods=['GET', 'POST'])
@login_required
def overall_patient_progress(patient_id,methods=['GET', 'POST']):
     patientId = user_patient.query.get(patient_id)
     print("Overall Patient Progress: ",patient_id)
     print("Before from DB Completion",patientId.id)
     patientId = patientId.id
     if patientId == 1:
         patientId = 27
     elif patientId  == 2:
         patientId = 34
     elif patientId  == 3:
         patientId = 52
     elif patientId  == 4:
         patientId = 53
     elif patientId  == 5:
         patientId = 75
     elif patientId  == 6:
         patientId = 80
     elif patientId  == 7:
         patientId = 88
     elif patientId  == 8:
         patientId = 90
     elif patientId  == 9:
         patientId = 106   
     elif patientId  == 10:
         patientId = 118    
     elif patientId  == 10:
         patientId = 129    
     elif patientId  == 11:
         patientId = 131  
     elif patientId  == 12:
         patientId = 584
     print("After Completion",patientId)
     date_id_list = get_dates(patientId)
     start_time_plot = time.time()
     bar_plot_list = []
     hr_zone_fig_list_json = []
     labels_matrix = []
     values_matrix = []
     specs_matrix =[]
     fig_bar_list = []
     form = DateDropDown_form()
     # Gets the unique avaliable dates from a patient.
    #  form.date.choices = [(date) for date in date_id_list]
     print("date list: ",date_id_list,"Length dates: ",len(date_id_list))
     print("selected date:  ",form.date.data)
     colors= ["#a8fa74","#5eda38","#fbda35","#f17304","#fc978d","#eb250e","#b41904"]
     json_fig_l = []
     stats_hr_json_path =  "./static/plotlycharts/PatientID_" + str(patientId)+"/hr_stats_pid_" + str(patientId) + ".json"                
     #f_json = plotly.io.read_json( "./static/plotlycharts/PatientID_" + str(patientId)+"/plotly_hr_zone_"+ str(patientId) + "_pichart_1_7.json")
     #f_json2 = plotly.io.read_json( "./static/plotlycharts/PatientID_" + str(patientId)+"/plotly_hr_zone_"+ str(patientId) + "_pichart_8_15.json")
     #json_fig = json.dumps(f_json, cls=plotly.utils.PlotlyJSONEncoder)
     #json_fig2 = json.dumps(f_json2, cls=plotly.utils.PlotlyJSONEncoder)
    #  bar_list = []
     with open(stats_hr_json_path, "r") as json_file:
         hr_stats = json.load(json_file)
     max_dates_hr_list = []
     min_dates_hr_list = []
     average_dates_hr_list = []
     print("Length of dates",hr_stats["dates"])
     for i in range(0,len(hr_stats["dates"])):
         max_d = hr_stats["max"][i]
         min_d = hr_stats["min"][i]
         avg_d = hr_stats["mean"][i]
         max_dates_hr_list.append(max_d)
         min_dates_hr_list.append(min_d)
         average_dates_hr_list.append(avg_d)
     print("Date List: ",len(date_id_list))
     return render_template("over_all_patients.html",patientId=patientId,
                            form =form,date_id_list=date_id_list,
                            hr_stats = hr_stats,
                            #json_fig=json_fig,json_fig2=json_fig2,
                            selected_date = str(form.date.data),
                            all_zipped = zip(max_dates_hr_list,min_dates_hr_list,date_id_list,average_dates_hr_list))

# To display pi chart of overall patient progress.
@app.route('/patient/<int:patient_id>/hrv', methods=['GET', 'POST'])
@login_required
def hrv(patient_id,methods=['GET', 'POST']):
     patientId = user_patient.query.get(patient_id)
     print("Overall Patient Progress: ",patient_id)
    #  patient_id = 27
     date_id_list = get_dates(27)
     start_time_plot = time.time()
     bar_plot_list = []
     hr_zone_fig_list_json = []
     labels_matrix = []
     values_matrix = []
     specs_matrix =[]
     fig_bar_list = []
     colors= ["#a8fa74","#5eda38","#fbda35","#f17304","#fc978d","#eb250e","#b41904"]
     start_read_time = time.time()
     path = "/Users/shehjarsadhu/Desktop/UniversityOfRhodeIsland/Graduate/ResearchWBL/My_Thesis/careportal-flaskapp/care-portal-thesis-sub/PatientID_" +str(27) + "/HR_ACT_Resample_40Hz_PID_" + str(27) + "_" + str(0) + "_Date_ID_HR.csv"
     print(path)
     df_hr_zone = pd.read_csv(path)
     hrv_hourly,new_ts = calculate_hourly_hrv(df_hr_zone)
     print("HRV Length: ",hrv_hourly)
     #hrv_hourly,new_ts
     fig_hrv = go.Figure()
     fig_hrv.add_trace(go.Scatter(
        x=new_ts,
        y=hrv_hourly,))
     return render_template("hrv.html",patientId=patientId,fig_hrv=fig_hrv,date_id_list=date_id_list)

# Params: dataframe that. 
# Returns a list of hourly HRV avaliable for that particular day. and the time stamp.
def calculate_hourly_hrv(df):
    times = unique_time_stamps(df)
    hrv_hourly = []
    new_ts = df["Time"].str.split(" ", n = 1, expand = True)
    for ts in times: # Time Filter.
        df = df[new_ts[1].str.startswith(ts)]
        df_date_time = df[new_ts[1].str.startswith(ts)]
        print("HRV Date and time: ",df_date_time.head())
        sdrr = df_date_time["Heart.Rate..BPM."].diff()
        print("sdrr = ",sdrr)
        hrv = np.sqrt(sdrr.sum()/len(df))
        hrv_hourly.append(hrv)
    return hrv_hourly,new_ts

@app.route('/view_patients')
@login_required
def view_patients():
    patients = user_patient.query.order_by(user_patient.id.asc())
    return render_template('patients.html', patients = patients)
##########################
# Care Well Study Data   #
##########################

 # 1. Read data from google sheets directly.
sheet_id = "1yVeplaUTfh1F_CGDEJkGaL3EyNy7NiXN7J29Gl2kSNg"
sheet_name ="InitialAssessment" # Can change different sheets.
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
carewell_df = pd.read_csv(url)
@app.route('/carewell_dashboard/<string:patient_id>')
@login_required
def carewell_dashboard(patient_id):
    carewell_df_p= carewell_df[carewell_df["PatientID"]==patient_id]
    yes_counter = 0
    no_counter = 0
    for i in carewell_df_p["Response"]:
        print("Response",i)
        if i == "Yes":
            yes_counter +=1
        elif i == "No":
            no_counter +=1
    pi_chart_list = [yes_counter/carewell_df_p.shape[0]*100,no_counter/carewell_df_p.shape[0]*100]
    # 2. Get Patient ID based on device id. 
    # 3. Viz Initial Assessment data in (1) Piechart for yes / no.
    return render_template('carewell_dashboard.html',pi_chart_list=pi_chart_list)

@app.route('/view_carewell_patients')
@login_required
def view_carewell_patients():   
    patients_carewell = carewell_df["PatientID"].unique()
    print("CAREWELL PARTIENTS=",patients_carewell[1:])
    return render_template('patients_carewell.html', patients = patients_carewell[1:])




    

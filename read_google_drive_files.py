from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pandas as pd
def google_drive_file_read():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth() # client_secrets.json need to be in the same directory as the script
    drive = GoogleDrive(gauth)
    fileList = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    
    # fileList = drive.ListFile({'q': "'2mavWSQhVfr7GnX2JHa45Qd43bTaYCHXE' in parents and trashed=false"}).GetList()

    # ED EAR - HR Datafolder - List of all HR files using google drive folder.
    # fileList = drive.ListFile({'q': "'1AS0qLFTTF9RFRDMW-fIVXnKjFYC2JV-m' in parents and trashed=false"}).GetList()
    print(fileList)
    for file in fileList:
        print("file_title ,file_id - ",file['title'],file['id'])
        fileList_pid = drive.ListFile({'q': "{{file['id']}} in parents and trashed=false"}).GetList()
        for i in fileList_pid:
            print(i)
        #sheet_id = file['id']
        #sheet_name =file['title'].split(".")[0] # Can change different sheets.
        #url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        #print("Reading File for :",file['title'].split(".")[0] )
        #carewell_df = pd.read_csv(url)
google_drive_file_read()
# Kaya Data ID 1AcTwPf5GwDdrM8vzwh6-EaJ8b-doBfk0
# google_drive_file_read("1AcTwPf5GwDdrM8vzwh6")









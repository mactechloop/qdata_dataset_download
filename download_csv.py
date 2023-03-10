import json
import csv
import pandas as pd
import firebase_admin
from firebase_admin import db
import streamlit as st
import sys
import re
from pathlib import Path

downloads_path = str(Path.home() / "Downloads")

@st.cache
def convert_df(df, ftr):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    df.replace(ftr, inplace=True)
    return df.to_csv(index=False).encode('utf-8')


def listToString(s):

    str1 = ""

    for ele in s:
        str1 += ele
 
    return str1

if firebase_admin._DEFAULT_APP_NAME not in firebase_admin._apps:
    cred_obj = firebase_admin.credentials.Certificate('qdataapp-firebase.json')
    firebase_admin.initialize_app(cred_obj, {
    'databaseURL':"https://qdataapp-default-rtdb.firebaseio.com/"
    })

st.title('Download Dataset Qdata')



activities=['SENSORY EVALUATION', 'ANY OTHER']
option=st.selectbox('Selection option:',activities)

if(option == 'SENSORY EVALUATION'):
    user_id = st.text_input('User Id')
    unique_id = st.text_input('Unique Id')

    if(st.button('Proceed')):

        ref2 = db.reference("/Users/" + user_id +"/Questionnaires/" + unique_id + "/CollectedData/")
        a = ref2.get()
        ll = (len(a.values()))
        # print(type(a.values()))
        xx = (list(a.values()))

        ap = []
        ar = []
        ga = []
        pe = []
        sa = []
        ta = []
        tx = []

        gen_ll = (list(xx))

        for i in range(len(gen_ll)):
            ml  = (gen_ll[i].values())

            count = 0
            for i in ml:
                i = i.replace('[', '')
                i = i.replace(']', '')
                i = i.replace(' ', '')
                my_ml = i.split(',')
                if(count == 0):
                    for j in range(len(my_ml)):
                        ap.append((my_ml[j]))
                elif(count == 1):
                    for j in range(len(my_ml)):
                        ar.append((my_ml[j]))
                elif(count == 2):
                    for j in range(len(my_ml)):
                        ga.append((my_ml[j]))
                elif(count == 3):
                    for j in range(len(my_ml)):
                        pe.append((my_ml[j]))
                elif(count == 4):
                    for j in range(len(my_ml)):
                        sa.append(my_ml[j])
                elif(count == 5):
                    for j in range(len(my_ml)):
                        ta.append((my_ml[j]))
                else:
                    for j in range(len(my_ml)):
                        tx.append((my_ml[j]))


                count += 1

        my_df = pd.DataFrame(columns=['Panelist', 'Sample', 'Text', 'Texture', 'Appearance', 'Aroma', 'General Acceptability'])
        my_df['Appearance'] = ap
        my_df['Aroma'] = ar
        my_df['General Acceptability'] = ga
        my_df['Panelist'] = pe
        my_df['Sample'] = sa
        my_df['Text'] = ta
        my_df['Texture'] = tx

        # my_df.to_csv('data.csv', index=False, index_label=False)
        ftr = {
            'A' : 1,
            'B' : 2,
            'C' : 3,
            'D' : 4,
            'E' : 5,
            'F' : 6,
            'G' : 7,
            'H' : 8,
            'I' : 9,
            'J' : 10,
            'K' : 11
        }
        aaaa = convert_df(my_df, ftr)

        file_name = 'Qdata'+'('+unique_id+').csv'

        if(st.download_button(
            label="Download CSV File",
            data=aaaa,
            file_name=file_name,
            mime='text/csv',
        )):
            st.success('Downloaded Successfully')


elif(option == 'ANY OTHER'):

    user_id = st.text_input('User Id')
    unique_id = st.text_input('Unique Id')

    if(st.button('Proceed')):
        ref2 = db.reference("/Users/" + user_id +"/Questionnaires/" + unique_id + "/CollectedData/")
        my_json = ref2.get()

        with open('data.json', 'w') as json_file:
            json.dump(my_json, json_file)

        json_file = open("data.json")
        dic = json.load(json_file)
        print(dic)

        arr = []

        for item in dic:
            arr.append(dic[item])

        jsonString = json.dumps(arr)

        df = pd.read_json(jsonString)
        ftr = {
            'A' : 1,
            'B' : 2,
            'C' : 3,
            'D' : 4,
            'E' : 5,
            'F' : 6,
            'G' : 7,
            'H' : 8,
            'I' : 9,
            'J' : 10,
            'K' : 11
        }
        aaaa = convert_df(df, ftr)

        file_name = 'Qdata'+'('+unique_id+').csv'

        if(st.download_button(
            label="Download CSV File",
            data=aaaa,
            file_name=file_name,
            mime='text/csv',
        )):
                st.success('Downloaded Successfully')

elif option == 'REPLACE ALPHABETS':
    try:
        uploadedFile = st.file_uploader('datasetqdata', type=['csv','xlsx'],accept_multiple_files=False,key="fileUploader")
        try:
            df=pd.read_csv(uploadedFile, error_bad_lines=True, warn_bad_lines=False)
        except:
            try:
                df = pd.read_excel(uploadedFile)
            except:      
                df=pd.DataFrame()

       
        ftr = {
            'A' : 1,
            'B' : 2,
            'C' : 3,
            'D' : 4,
            'E' : 5,
            'F' : 6
        }
        aa = convert_df(df, ftr)
        # aa.replace(ftr, inplace=True)

        file_name = 'Qdata'+'('+uploadedFile.name[:-4].strip()+').csv'

        if(st.download_button(
            label="Download CSV File",
            data=aa,
            file_name=file_name,
            mime='text/csv',
        )):
                st.success('Downloaded Successfully')

    except:
        st.info('Upload Dataset')

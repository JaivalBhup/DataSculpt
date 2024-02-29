import os
import tkinter as tk
from tkinter import filedialog
import pandas as pd
from tsfresh import extract_features, select_features
import numpy as np
import shutil
import json
from sklearn.preprocessing import MinMaxScaler,LabelEncoder
from threading import Thread
import re



def main():
    # def threadFunc(msg):
    #     Thread(target=showMsg, args=(msg), daemon=True).start()

    # def showMsg(msg):
    #     text_widget.insert(1.0, msg)
    def dirSelectedPressed(dir):
        if selecteddir.get() == dir:
            selecteddir.set('')
            dirSelected.set(False)
            file_widget.delete(1.0, tk.END)
        else:
            selecteddir.set(dir)
            dirSelected.set(True)
            file_widget.delete(1.0, tk.END)
            file_widget.insert(1.0, "Selected Data Source: "+selecteddir.get())
    
    def ts_extract_features():
        text_widget.delete(1.0, tk.END)
        extractedObject = {}
        current = []
        settings = { 
                    "median":None,
                    "mean": None,
                    "variance":None,
                    "maximum": None,
                    "minimum": None,
                    "linear_trend":[{'attr':'pvalue'},{'attr':'rvalue'},{'attr':'intercept'},{'attr':'slope'},{'attr':'stderr'}]
                }
        #os.path.isdir to check for directory
        sd = selecteddir.get()
        if sd=='': return
        # Loop Through every Subject
        for subject in os.listdir('./data/'+sd):
           if subject[0] == '.': continue
           extractedObject[subject] = {}
           current.append('./data/'+sd+"/"+subject)
           mainDf = pd.DataFrame()
           extracted_features = pd.DataFrame()
           # Loop through every directory
           for dir in os.listdir('./data/'+sd+'/'+subject):
               if dir[0] == '.': continue
               extractedObject[subject][dir] = []
               df = pd.DataFrame()
            #    threadFunc("Extracting features from: "+subject+" -> "+dir+"...\n")
               #Loop through every file inside
               for file in os.listdir('./data/'+sd+'/'+subject+'/'+dir):
                   if file[0] == '.': continue
                   #Create File name
                   currentFile = './data/'+sd+'/'+subject+'/'+dir+"/"+file
                   extractedObject[subject][dir].append(currentFile)
                   data = pd.read_csv(currentFile)
                   object_cols = data.select_dtypes(include=['object'])

                   # Label encoder for every object type in our data
                   le = LabelEncoder()
                   for col in object_cols.columns:
                       data[col] = le.fit_transform(data[col])
                   #Seperate column names for conflicting column names
                   newCols = []
                   for col in data.columns:
                       if col == 'TimeStamp(epoch)': 
                           newCols.append('TimeStamp(epoch)')
                           continue
                       newCols.append(dir+"_"+col)
                       
                   data.columns = newCols
                   #Append all the dataframes into one for same file type 
                   df = df.append(data)
               #Extract features with timestamp id and sort by time stamp
               extracted_features = extract_features(df, column_id='TimeStamp(epoch)', column_sort='TimeStamp(epoch)', default_fc_parameters=settings)
               extracted_features = extracted_features.rename_axis('TimeStamp(epoch)')
            #    extracted_features.to_csv('./extracted/tsfresh_extract_'+subject+"_"+dir+".csv")
               # Merge all the extracted feature into one big dataframe
               if not mainDf.empty:
                    mainDf = mainDf.merge(extracted_features, on="TimeStamp(epoch)", how='outer')
               else:
                    mainDf = extracted_features
           #Save that dataframe
           mainDf.to_csv('./extracted/tsfresh_extract_'+subject+".csv")
            
                
        # print(extractedObject)

    #main window
    root = tk.Tk()
    root.title("DataSculpt")
    selecteddir = tk.StringVar(master=root)
    dirSelected = tk.BooleanVar(master=root)
    top_frame = tk.Frame(root)
    top_frame.pack(side=tk.TOP)
    file_frame = tk.Frame(root)
    file_frame.pack(side=tk.TOP)
    sub_frame = tk.Frame(root)
    sub_frame.pack(side=tk.TOP)
    for dir in os.listdir("./data/"):
        if len(dir.split(".")) == 1:
            file_button = tk.Button(file_frame, text=dir,name=dir, command=lambda dir=dir: dirSelectedPressed(dir))
            file_button.pack(side='left', padx=5, pady=10)
    file_widget = tk.Text(root, height=5, width=40)
    file_widget.pack(expand=True)
    extract_button = tk.Button(top_frame, text="Extract data (TSFresh)", command=ts_extract_features)
    extract_button.pack(side='left', padx=5, pady=10)
    text_widget = tk.Text(root)
    text_widget.pack(expand=True, fill=tk.BOTH)

    root.mainloop()

if __name__ == "__main__":
    main()
import os
import tkinter as tk
from tkinter import filedialog
import pandas as pd
from tsfresh import extract_features, select_features
import numpy as np
import shutil
import json
from sklearn.preprocessing import MinMaxScaler,LabelEncoder
import re

def main():
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
        ans = []
        settings = { 
                    "length": None,
                    "large_standard_deviation": [{"r": 0.05}, {"r": 0.1}]
                }
        #os.path.isdir to check for directory
        sd = selecteddir.get()
        for subject in os.listdir('./data/'+sd):
           if subject[0] == '.': continue
           extractedObject[subject] = {}
           current.append('./data/'+sd+"/"+subject)
           for dir in os.listdir('./data/'+sd+'/'+subject):
               if dir[0] == '.': continue
               extractedObject[subject][dir] = []
               df = pd.DataFrame()
               text_widget.insert(1.0, "Extracting features from: "+subject+" -> "+dir+"...\n")

               for file in os.listdir('./data/'+sd+'/'+subject+'/'+dir):
                   
                   if file[0] == '.': continue
                   

                   currentFile = './data/'+sd+'/'+subject+'/'+dir+"/"+file
                   extractedObject[subject][dir].append(currentFile)
                   data = pd.read_csv(currentFile)
                   object_cols = data.select_dtypes(include=['object'])
                   # Apply label encoding to object columns
                   le = LabelEncoder()
                   for col in object_cols.columns:
                       data[col] = le.fit_transform(data[col])
                   segement_id = int(re.sub("[A-Za-z]","",file.split('.')[0]))
                   data['segement_id'] = segement_id
                   df = df.append(data)
               extracted_features = extract_features(df, column_id='segement_id', column_sort='TimeStamp(epoch)', default_fc_parameters=settings)
               extracted_features = extracted_features.rename_axis('segement_id')
               extracted_features.to_csv('./extracted/tsfresh_extract_'+subject+"_"+dir+".csv")
                
        print(extractedObject)
        

    def create_file_buttons():
        for widget in file_frame.winfo_children():
            widget.destroy()  # Clear previously created file buttons
        for file in os.listdir("./imported_files/"):
            file_button = tk.Button(file_frame, text=file, command=lambda file=file: fileSelectedPressed(file))
            file_button.pack(side='left', padx=5, pady=10)


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
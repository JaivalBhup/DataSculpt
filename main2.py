import os
import tkinter as tk
from tkinter import filedialog
import pandas as pd
from tsfresh import extract_features, select_features
import numpy as np
import shutil
import json
from sklearn.preprocessing import MinMaxScaler
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
        extractedObject = {}
        current = []
        ans = []
        #os.path.isdir to check for directory
        sd = selecteddir.get()
        for dir in os.listdir('./data/'+sd):
           extractedObject[dir] = {}
           current.append('./data/'+sd+"/"+dir)
        while len(current) > 0:
            cur = current.pop(0)
            if len(cur.split('/')[-1].split('.')) == 1:
                for dirorfile in os.listdir(cur):
                    current.append(cur+'/'+dirorfile)
            elif cur.split('.')[-1] == 'csv':
                ans.append(cur)
        
        #Currently only for balance (DONOT RUNNNNN)
        df = pd.DataFrame()
        for file in ans:
            print(file)
            data = pd.read_csv(file)
            segement_id = int(re.sub("[A-Za-z]","",file.split('/')[-1].split('.')[0]))
            data['segement_id'] = segement_id
		    #drops NaN rows and columns 
            #Identify non number columns
            #Label encoder on those columns
            df = df.append(data)
        
        extracted_features = extract_features(df, column_id='segement_id', column_sort='TimeStamp(epoch)')
        extracted_features = extracted_features.rename_axis('segement_id')
        print(extracted_features)
        extracted_features.to_csv('outFile_'+file.split('/')[-1])

    def features_extract_features():
        extractedObject = {}
        current = []
        ans = []
        #os.path.isdir to check for directory
        sd = selecteddir.get()
        for dir in os.listdir('./data/'+sd):
           extractedObject[dir] = {}
           current.append('./data/'+sd+"/"+dir)
        while len(current) > 0:
            cur = current.pop(0)
            if len(cur.split('/')[-1].split('.')) == 1:
                for dirorfile in os.listdir(cur):
                    current.append(cur+'/'+dirorfile)
            elif cur.split('.')[-1] == 'csv':
                ans.append(cur)
        
        for file in ans:
            print(file)
            data = pd.read_csv(file)
		    #drops NaN rows and columns 
            #Identify non number columns
            #Label encoder on those columns
            data.dropna(inplace=True)
            data = data.select_dtypes(include='number')
            file_obj = {}
            for column in data.columns:

                if column == 'TimeStamp(epoch)': continue
                scaler = MinMaxScaler()
                data_scaled = scaler.fit_transform(data[column].values.reshape(-1, 1))
                # Extract features (replace with your desired features)
                mean = data_scaled.mean()
                std = data_scaled.std()
                max_val = data_scaled.max()
                min_val = data_scaled.min()

                extracted_features = [mean,std, max_val,min_val]
                extracted_features = extracted_features
                file_obj[column] = extracted_features
            
            curObj = extractedObject
            itt = file.split('/')[3:]
            while itt:
                curItt = itt.pop(0)
                if curObj.get(curItt):
                    curObj = curObj.get(curItt)
                    if curItt.split('.')[-1]!='csv':
                        continue
                    curObj[curItt] = file_obj
                    
                else:
                    if curItt.split('.')[-1]=='csv':
                        curObj[curItt] = file_obj
                    else:
                        curObj[curItt] = {}
                        curObj = curObj[curItt]
        
        json_object = json.dumps(extractedObject, indent=4)
        with open("test.json", "w") as outfile:
            outfile.write(json_object)
                        

            
        text_widget.delete(1.0,tk.END)
        text_widget.insert(1.0,extractedObject)

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
    
    extract_button = tk.Button(top_frame, text="Extract data (TSFresh)", command=ts_extract_features)
    extract_button.pack(side='left', padx=5, pady=10)
    reg_extract_button = tk.Button(top_frame, text="Extract data (NOT TSFresh)", command=features_extract_features)
    reg_extract_button.pack(side='left', padx=5, pady=10)


    file_widget = tk.Text(root, height=5, width=40)
    file_widget.pack(expand=True)

    text_widget = tk.Text(root)
    text_widget.pack(expand=True, fill=tk.BOTH)

    root.mainloop()

if __name__ == "__main__":
    main()
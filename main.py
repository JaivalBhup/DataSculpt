import os
import tkinter as tk
from tkinter import filedialog
import pandas as pd
from tsfresh import extract_features 
import numpy as np
import shutil

def main():
    
    def browse_file():
        try:
            file_path = filedialog.askopenfilename()
            if file_path:
            # Open the selected file for reading
                with open(file_path, 'r') as file:
                # Read the contents of the file
                    # file_contents = file.read()
                    # text_widget.delete(1.0, tk.END)
                    # text_widget.insert(1.0, file_contents)
                    shutil.copyfile(file.name,'./imported_files/'+file.name.split('/')[-1])
                    create_file_buttons()
        except Exception as e:
            text_widget.delete(1.0, tk.END)
            text_widget.insert(1.0, e)
                

    def fileSelectedPressed(file):
        if selectedFile.get() == file:
            selectedFile.set('')
            fileSelected.set(False)
            file_widget.delete(1.0, tk.END)
        else:
            selectedFile.set(file)
            fileSelected.set(True)
            file_widget.delete(1.0, tk.END)
            file_widget.insert(1.0, "Selected File: "+selectedFile.get())

    def ts_extract_features():
        if fileSelected.get():

            data = pd.read_csv('./imported_files/'+selectedFile.get())

            #drops NaN rows and columns
            data.dropna(inplace=True)
            data = data.select_dtypes(include='number')

            #extracts features
            extracted_features = extract_features(data,column_id = 'cases',column_sort = None)
            features_array = str(extracted_features.columns)
            text_widget.delete(1.0,tk.END)
            text_widget.insert(1.0,features_array)



    def bin_data():
         if fileSelected.get():

            data = pd.read_csv('./imported_files/'+selectedFile.get())
            #Disretizes all numeric columns
            for column in data.select_dtypes(include = 'number'):
                column_data = data[column].values
            
            #sets number of bins
            num_bins = 100
            bins = np.linspace(min(column_data), max(column_data), num_bins + 1)
            #Discretize
            discretized_values = np.digitize(column_data, bins)
            bin_column_name = f'{column}_bin'
            data[bin_column_name] = discretized_values
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, data)


    def readfile():
         if fileSelected.get():

            data = pd.read_csv('./imported_files/'+selectedFile.get())
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, data)

    def create_file_buttons():
        for widget in file_frame.winfo_children():
            widget.destroy()  # Clear previously created file buttons
        for file in os.listdir("./imported_files/"):
            file_button = tk.Button(file_frame, text=file, command=lambda file=file: fileSelectedPressed(file))
            file_button.pack(side='left', padx=5, pady=10)





    #main window
    root = tk.Tk()
    selectedFile = tk.StringVar(master=root)
    fileSelected = tk.BooleanVar(master=root)
    root.title("DataSculpt")

    top_frame = tk.Frame(root)
    top_frame.pack(side=tk.TOP)
    
    browse_button = tk.Button(top_frame, text="Choose your file", command=browse_file)
    browse_button.pack(side='left', padx=5, pady=10)

    read_button = tk.Button(top_frame, text="Read File", command=readfile)
    read_button.pack(side='left', padx=5, pady=10)

    extract_button = tk.Button(top_frame, text="Extract data (TSFresh)", command=ts_extract_features)
    extract_button.pack(side='left', padx=5, pady=10)

    bin_button = tk.Button(top_frame, text="Discretization (Binning)", command=bin_data)
    bin_button.pack(side='left', padx=5, pady=10)

    file_frame = tk.Frame(root)
    file_frame.pack(side=tk.TOP)
    for file in os.listdir("./imported_files/"):
        file_button = tk.Button(file_frame, text=file, command=lambda file=file: fileSelectedPressed(file))
        file_button.pack(side='left', padx=5, pady=10)


    file_widget = tk.Text(root, height=5, width=40)
    file_widget.pack(expand=True)

    text_widget = tk.Text(root)
    text_widget.pack(expand=True, fill=tk.BOTH)

    root.mainloop()

if __name__ == "__main__":
    main()

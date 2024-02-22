import tkinter as tk
from tkinter import filedialog
import pandas as pd
from tsfresh import extract_features 
import numpy as np





def main():



    def browse_file():
        try:
            file_path = filedialog.askopenfilename()
            if file_path:
            # Open the selected file for reading
                with open(file_path, 'r') as file:
                # Read the contents of the file
                    file_contents = file.read()
                    text_widget.delete(1.0, tk.END)
                    text_widget.insert(1.0, file_contents)
            else:   
                file_label.config(text="No file selected")
        except Exception as e:
            text_widget.delete(1.0, tk.END)
            text_widget.insert(1.0, e)
                



    def ts_extract_features():
        
        file_path = filedialog.askopenfilename()
        if file_path:

            data = pd.read_csv(file_path)

            #drops NaN rows and columns
            data.dropna(inplace=True)
            data = data.select_dtypes(include='number')

            #extracts features
            extracted_features = extract_features(data,column_id = 'cases',column_sort = None)
            features_array = str(extracted_features.columns)
            text_widget.delete(1.0,tk.END)
            text_widget.insert(1.0,features_array)



    def bin_data():
        file_path = filedialog.askopenfilename()
        if file_path:

            bin_data = pd.read_csv(file_path)
            #Disretizes all numeric columns
            for column in bin_data.select_dtypes(include = 'number'):
                column_data = bin_data[column].values
            
            #sets number of bins
            num_bins = 100
            bins = np.linspace(min(column_data), max(column_data), num_bins + 1)


            #Discretize
            discretized_values = np.digitize(column_data, bins)

            bin_column_name = f'{column}_bin'
            bin_data[bin_column_name] = discretized_values
    

            

            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, bin_data)









    #main window
    root = tk.Tk()
    root.title("DataSculpt")

    # Top Label

    file_label = tk.Label(root, text="Test")
    file_label.pack(pady=10)

    # Our Button
    browse_button = tk.Button(root, text="Choose your file", command=browse_file)
    browse_button.pack(pady=10)


    extract_button_TSFresh = tk.Button(root,text = "extract data (TSFresh)", command= ts_extract_features)
    extract_button_TSFresh.pack(pady=10)

    bin_button = tk.Button(root, text="discretization(binning)", command=bin_data)
    bin_button.pack(pady=10)




    # Data Display (Simple text widget for now)
    text_widget = tk.Text(root)
    text_widget.pack(expand=True, fill=tk.BOTH)



    root.mainloop()

if __name__ == "__main__":
    main()

import tkinter as tk
from tkinter import filedialog
import pandas as pd
import tsfel

#Merging everything
def browse_file():
    global file_path #path directory is global as we will need it later to derive the discrete stats
    file_path = filedialog.askopenfilename()
    if file_path:
        # Open the selected file for reading
        with open(file_path, 'r') as file:
            # Read the contents of the file
            file_contents = file.read()
            #Display the file contents in a text widget
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, file_contents)
    else:
        file_label.config(text="No file selected")

#main window
root = tk.Tk()
root.title("DataSculpt")

# Top Label
file_label = tk.Label(root, text="Test")
file_label.pack(pady=10)

# Our Button
browse_button = tk.Button(root, text="Choose your file", command=browse_file)
browse_button.pack(pady=10)

# Data Display (Simple text widget for now)
text_widget = tk.Text(root)
text_widget.pack(expand=True, fill=tk.BOTH)

def mytsfel():
    #load the file the user selected as a csv file
    df = pd.read_csv(file_path)
    if browse_file:
        #Retrieves a pre-defined feature configuration file to extract all available features
        cfgfile = tsfel.get_features_by_domain()

        #Drop all columns that contain string elements
        #For example, the code below is unique to the mock time-series dataset I tested my code on
        #df = df.drop(["Country", "Status"], axis = 1)

        #Also, drop all null values of the csv file
        df.dropna(inplace=True)

        # Extract features using the tsfel package
        X = tsfel.time_series_features_extractor(cfgfile, df, fs=50, window_size=250)
        text_widget.delete(1.0,tk.END)
        text_widget.insert(1.0,X)
        print('\nExtracted arrays:')
        print(X) #will print the discrete features onto th

#Adds a button to the main window that calls the command that extracts the discrete values from the time series using the tsfel package
#Will read the extracted info onto the window and terminal
extract_button = tk.Button(root, text = 'Extract data', command = mytsfel)
extract_button.pack(pady=10)

root.mainloop() #infinite loop until the window is closed

import tkinter as tk
from tkinter import filedialog

def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        # Open the selected file for reading
        with open(file_path, 'r') as file:
            # Read the contents of the file
            file_contents = file.read()
        # Display the file contents in a text widget
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

root.mainloop() #infinite loop until the window is closed

#FOR THE NEXT CODE TO RUN, WE MUST CLOSE THE WINDOW THAT READS THE FILE SELECTED BY THE USER

#load the file the user selected as a csv file
df = pd.read_csv(file_path)
#Retrieves a pre-defined feature configuration file to extract all available features
cfgfile = tsfel.get_features_by_domain()

#Drop all columns that contain string elements
#For example, the code below is unique to the mock time-series dataset I tested my code on
#df = df.drop(["Country", "Status"], axis = 1)

#Also, drop all null values of the csv file
df.dropna(inplace=True)

# Extract features using the tsfel package
X = tsfel.time_series_features_extractor(cfgfile, df, fs=50, window_size=250)
print(X) #will print the discrete features onto the terminal

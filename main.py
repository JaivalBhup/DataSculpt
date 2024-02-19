import tkinter as tk
from tkinter import filedialog
import pandas as pd
from tsfresh import extract_features 




def main():
    def browse_file():
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



    def ts_extract_features():
        file_path = filedialog.askopenfilename()
        if file_path:

            data = pd.read_csv(file_path)
            extracted_features = extract_features(data,column_id = "sensor_id",column_sort = "time_stamp")
            features_array = str(extracted_features.columns)
            text_widget.delete(1.0,tk.END)
            text_widget.insert(1.0,features_array)

            print("\nExtracted features:")
            print(features_array)



    #main window
    root = tk.Tk()
    root.title("DataSculpt")

    # Top Label
    file_label = tk.Label(root, text="Test")
    file_label.pack(pady=10)

    # Our Button
    browse_button = tk.Button(root, text="Choose your file", command=browse_file)
    browse_button.pack(pady=10)

    extract_button = tk.Button(root,text = "extract data", command= ts_extract_features)
    extract_button.pack(pady=10)

    # Data Display (Simple text widget for now)
    text_widget = tk.Text(root)
    text_widget.pack(expand=True, fill=tk.BOTH)



    root.mainloop()

if __name__ == "__main__":
    main()

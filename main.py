import tkinter as tk
from tkinter import filedialog
import pandas as pd
# Merging everything
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

root.mainloop()

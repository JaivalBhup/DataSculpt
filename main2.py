import os
import tkinter as tk
from FeaturesExtraction.tsfresh_extract import process_and_extract_features as ts_process_and_extract_features

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
        sd = selecteddir.get()
        if sd=='': return
        print(ts_process_and_extract_features(sd))

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
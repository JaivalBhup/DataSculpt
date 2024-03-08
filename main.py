import os
import tkinter as tk
from tsfresh_extract import process_and_extract_features as ts_process_and_extract_features
from tsfel_extract import process_and_extract_features as tsfel_process_and_extract_features

#REMEMBER TO CHANGE ALL PATH DIRECTORIES IN MY CODE TO YOUR DISTINCT PATH DIRECTORY

def main():
    def make_file_button(dir):
        button = tk.Button(
            file_frame, text=dir, name=dir, command=lambda dir=dir: dirSelectedPressed(dir)
        )
        button.config(bg="lightgrey", activebackground="lightblue")  # Set default and active colors
        return button
    
    root = tk.Tk()
    root.title("DataSculpt")

    # Use grid for more structured layout
    top_frame = tk.Frame(root)
    top_frame.grid(row=1, column=0, columnspan=2)  # Span across both columns
    file_frame = tk.Frame(root)
    file_frame.grid(row=2, column=0, sticky=tk.N+tk.S) 
    # dir_frame = tk.Frame(root)
    # dir_frame.grid(row=1, column=0, sticky=tk.N+tk.S)  # Stick to top and bottom
    dir_frame = tk.Frame(root)
    dir_frame.grid(row=3, column=0, sticky=tk.N+tk.S)  # Expand as needed

    selecteddir = tk.StringVar(master=root)
    dirSelected = tk.BooleanVar(master=root)
    selectedFeatures = tk.StringVar(master=root)
    for dir in os.listdir("C:/Users/jamir\Downloads/2024 - CS multimodal data/"):
        if len(dir.split(".")) == 1:
            file_button = make_file_button(dir)
            file_button.pack(side='left',padx=5, pady=10) 
    file_widget = tk.Text(root, height=5, width=40)
    file_widget.grid(row=4,rowspan=2, column=0, sticky=tk.N+tk.S+tk.W)  # Stick to top, bottom, and left
    text_widget = tk.Text(root)
    text_widget.grid(row=5, column=1, sticky=tk.N+tk.S+tk.E+tk.W)  # Expand in both directions
    def ts_extract_features():
        text_widget.delete(1.0, tk.END)
        text_widget.insert(1.0, 'Extracting Features ....')
        dirArray = selectedFeatures.get().split(',')
        sd = selecteddir.get()
        if sd=='': return
        if dirArray[0] == '':return
        objj = ts_process_and_extract_features(sd, dirArray)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(1.0, f'''Files Extracted:\n {', '.join(objj['extractedFiles'])}\n\n Features: {str(objj['features'])}''')

    #NOW IMPLEMENTING TSFFEL EXTRACT FEATURES
    def tsfel_extract_features():
        text_widget.delete(1.0, tk.END)
        text_widget.insert(1.0, 'Extracting Features ....')
        dirArray = selectedFeatures.get().split(',')
        sd = selecteddir.get()
        if sd=='': return
        if dirArray[0] == '':return
        objj = tsfel_process_and_extract_features(sd, dirArray)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(1.0, f'''Files Extracted:\n {', '.join(objj['extractedFiles'])}\n\n Features: {str(objj['features'])}''')


    extract_button = tk.Button(top_frame, text="Extract data (TSFresh)", command=ts_extract_features)
    extract_button.pack(side='left', padx=5, pady=10)

    extract_button1 = tk.Button(top_frame, text="Extract data (TSFel)", command=tsfel_extract_features)
    extract_button1.pack(side='right', padx=5, pady=10)

    def make_dir_buttons(data):
        robj = {"subjects":[], "dirs":[]}
        gotdirs = False
        for sub in os.listdir('C:/Users/jamir/Downloads/2024 - CS multimodal data/'+data):
            if sub[0] != '.': robj["subjects"].append(sub)
            if gotdirs: continue
            for dir in os.listdir('C:/Users/jamir/Downloads/2024 - CS multimodal data/'+data+'/'+sub):

                if dir[0] != '.':
                    robj["dirs"].append(dir)
                    gotdirs = True
                    button = tk.Button(
                        dir_frame, text=dir, name=dir.lower(), command=lambda dir=dir: updatedDirs(dir)
                    )
                    button.config(bg="lightgrey", activebackground="lightblue")  # Set default and active colors
                    button.pack(side='left',padx=5, pady=10) 
        selectedFeatures.set(",".join(robj["dirs"]))
        return robj

    def updatedDirs(dir):
        dirArray = selectedFeatures.get().split(',')
        if len(dirArray)>=1 and dirArray[0] != '':
            if dir in dirArray:
                dirArray.remove(dir)
            else: 
                dirArray.append(dir)
            selectedFeatures.set(','.join(dirArray))
            file_widget.delete(3.0, tk.END)
            file_widget.insert(3.0, f'''\nFeatures Extracted on: \n {", ".join(dirArray)}''')
        else:
            selectedFeatures.set(dir)
            file_widget.delete(3.0, tk.END)
            file_widget.insert(3.0, f'''\nFeatures Extracted on: \n {dir}''')

        

    def dirSelectedPressed(dir):
        if selecteddir.get() == dir:
            selecteddir.set('')
            dirSelected.set(False)
            file_widget.delete(1.0, tk.END)
        else:
            selecteddir.set(dir)
            obj = make_dir_buttons(dir)
            dirSelected.set(True)
            file_widget.delete(1.0, tk.END)
            file_widget.insert(1.0, f'''Subjects Found: \n {", ".join(obj['subjects'])}\n''')
            file_widget.insert(3.0, f'''Features Extracted on: \n {", ".join(obj['dirs'])}''')

    root.mainloop()

if __name__ == "__main__":
    main()

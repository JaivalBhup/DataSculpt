import tkinter as tk
from tkinter import filedialog
import pandas as pd
from tsfresh import extract_features 
import numpy as np
import tsfel



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
                


    def write_dict_to_text_file(dictionary, filename):
        with open(filename, 'w') as file:
            for key, value in dictionary.items():
                file.write(f'{key}: {value}\n')


    def ts_extract_features():
        file_path = filedialog.askopenfilename()
        if file_path:
            data = pd.read_csv(file_path)
            dict_data = {}

            for column in data.select_dtypes(include='number').columns:
            # Extract features for each numeric column
                extracted_features = extract_features(data, column_id=column, column_sort=None)
                features_array = str(extracted_features.columns)
                dict_data[column] = features_array


            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, dict_data)
            write_dict_to_text_file(dict_data,"ts_dictionary.txt")




    def tsfel_extract_features():
        file_path = filedialog.askopenfilename()
        if file_path:
            data = pd.read_csv(file_path)
            dict_data = {}

            for column in data.select_dtypes(include='number').columns:
                # Extract features for each numeric column using tsfel
                cfgfile = tsfel.get_features_by_domain()
                X = tsfel.time_series_features_extractor(cfgfile, data[column])
                features_array = str(X.columns)
                dict_data[column] = features_array

            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, dict_data)
            write_dict_to_text_file(dict_data, "tsfel_dictionary.txt")
    
    def merge_data():
        file_path1 = filedialog.askopenfilename()
        df1 = pd.read_csv(file_path1)

        file_path2 = filedialog.askopenfilename()
        df2 = pd.read_csv(file_path2)

    
    # Merge the DataFrames
        merged_df = pd.merge(df1, df2, how='outer') 

        mergeFilePath = "/Users/brandonbautista/CSProject/DataSculpt/merged.csv"

        merged_df.to_csv(mergeFilePath, index=False)





    def merge_merge(dict1, dict2):
        merged_dict = dict1.copy()  # Make a copy of dict1 to avoid modifying it directly
        merged_dict.update(dict2)   # Update merged_dict with the key-value pairs from dict2
        return merged_dict
    


    def merge_dictionaries():
        file1_path = filedialog.askopenfilename()
        file2_path = filedialog.askopenfilename()

        # Initialize dictionaries to store the contents of the files
        dict1 = {}
        dict2 = {}

        # Read the contents of the first file and populate dict1
        with open(file1_path, 'r') as file1:
            # Read the contents of the file
            file1_content = file1.read()
            # Extract key and value pairs from the content
            pairs = file1_content.split('\n')
            for pair in pairs:
                if ':' in pair:
                    key, value = pair.split(': ')
                    dict1[key.strip()] = value.strip()

        # Read the contents of the second file and populate dict2
        with open(file2_path, 'r') as file2:
            # Read the contents of the file
            file2_content = file2.read()
            # Extract key and value pairs from the content
            pairs = file2_content.split('\n')
            for pair in pairs:
                if ':' in pair:
                    key, value = pair.split(': ')
                    dict2[key.strip()] = value.strip()

        # Merge the two dictionaries
        merged_dict = merge_merge(dict1,dict2)
        write_dict_to_text_file(merged_dict, "mergedDict.txt")


        # Display the merged dictionary
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, merged_dict)


    def bin_data():
        csv_file = "/Users/brandonbautista/CSProject/DataSculpt/merged.csv"
        df = pd.read_csv(csv_file)
        df_discretized = pd.DataFrame()
        
        # Loop through each column
        for column in df.columns:
            # Check if the column contains numerical values
            if pd.api.types.is_numeric_dtype(df[column]):
                # Calculate the average of the column
                avg = df[column].mean()
                
                # Define the number of bins based on the column's average
                num_bins = int(avg)
                
                # Discretize values using equal-width binning
                bins = pd.cut(df[column], bins=num_bins, labels=[f'Bin_{i+1}' for i in range(num_bins)])
                
                # Add the discretized values as a new column to the DataFrame
                df_discretized[f'{column}_discrete'] = bins.astype(str)
            else:
                # If the column does not contain numerical values, keep it unchanged
                df_discretized[column] = df[column]
        

        # Save the DataFrame with discretized values into a new CSV file
        output_csv_file = '/Users/brandonbautista/CSProject/DataSculpt/discrete.csv'
        df_discretized.to_csv(output_csv_file, index=False)




    #stupid
    def discretize_merged_dictionary():
    # Get the path to the merged dictionary file
        file_path = filedialog.askopenfilename()

    # Check if a file was selected
        if file_path:
            num_bins = 3
            discretized_dict = {}

        # Read the content of the merged dictionary file
            with open(file_path, 'r') as file:
            # Iterate through each line in the file
                for line in file:
                # Split each line into key and value
                    parts = line.strip().split(': ')
                    if len(parts) == 2:
                        key, feature_list = parts
                    # Convert feature list to a list of strings
                        feature_list = feature_list.strip()[1:-1].split(', ')
                    # Initialize a list to store discretized feature names
                        discretized_feature_list = []

                    # Iterate through each feature name in the feature list
                        for feature_name in feature_list:
                        # Apply binning to discretize the feature name
                            bins = np.linspace(0, 1, num_bins + 1)
                            discretized_value = np.digitize(hash(feature_name), bins)

                        # Append the discretized value to the list
                            discretized_feature_list.append(discretized_value)

                    # Store the discretized feature list in the discretized dictionary
                        discretized_dict[key] = discretized_feature_list

        # Write the discretized dictionary to a text file
            write_dict_to_text_file(discretized_dict, "discrete.txt")
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, discretized_dict)
        




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

    extract_button_tsfel = tk.Button(root,text = "extract data (TSFEL)", command= tsfel_extract_features)
    extract_button_tsfel.pack(pady=10)

 
    merge_button = tk.Button(root,text = "Merge",command=merge_data)
    merge_button.pack(pady=15)

    bin_button = tk.Button(root,text = 'Discrete', command=bin_data)
    bin_button.pack(pady=10)


    merge_dictionary_button = tk.Button(root, text="Merge_dictionaries", command=merge_dictionaries)
    merge_dictionary_button.pack(pady=10)




    # Data Display (Simple text widget for now)
    text_widget = tk.Text(root)
    text_widget.pack(expand=True, fill=tk.BOTH)



    root.mainloop()

if __name__ == "__main__":
    main()

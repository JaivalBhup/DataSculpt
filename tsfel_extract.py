import os
import re
import pandas as pd
from tsfel import calc_features, get_features_by_domain
import numpy as np
from sklearn.preprocessing import LabelEncoder
from pathlib import Path

def process_folder(folderlink, dir, settings):
	sett = get_features_by_domain(domain=None, json_path=None)

	combined_files = pd.DataFrame()
	for file in os.listdir(folderlink):
		if file[0] == '.': continue
		currentFile = folderlink+"/"+file
		data = pd.read_csv(currentFile)
		object_cols = data.select_dtypes(include=['object'])
		# Label encoder for every object type in our data
		le = LabelEncoder()
		for col in object_cols.columns:
			data[col] = le.fit_transform(data[col])
		#Seperate column names for conflicting column names
		newCols = []
		for col in data.columns:
			if col == 'TimeStamp(epoch)': 
				newCols.append('TimeStamp(epoch)')
				continue
			newCols.append(dir+"_"+col)
			
		data.columns = newCols
		segement_id = file
		data['segement_id'] = segement_id
		#print(data)
		#Append all the dataframes into one for same file type 
		#combined_files = combined_files.append(data)
		cols = [combined_files, data]
		combined_files = pd.concat(cols, ignore_index=True)
		combined_files1 = combined_files.values.tolist()
		#combined_files = pd.DataFrame(combined_files.T.reshape(2, -1), columns=combined_files.columns)
	
	extracted_features = calc_features(wind_sig=combined_files1, dict_features=sett, fs=None, kwargs='TimeStamp(epoch)')
	extracted_features = extracted_features.rename_axis('segement_id')

	print(settings)
	return extracted_features
	

def process_and_extract_features(dataFolder, featuresArray):
	output_dir = Path('C:/Users/jamir/Downloads/extracted')
	output_dir.mkdir(parents=True, exist_ok=True)
	extractedFiles = []
	features=[]
	#THINKING ABOUT CHANGING THE SETTINGS
	settings = { 
				'calc_median':'calc_median',
				'calc_mean':'calc_mean',
				'calc_var':'calc_var',
				'calc_max':'calc_max',
				'calc_min':'calc_min'
			}
	#os.path.isdir to check for directory
	
	# Loop Through every Subject
	for subject in os.listdir('C:/Users/jamir/Downloads/2024 - CS multimodal data/'+dataFolder):
		if subject[0] == '.': continue
		mainDf = pd.DataFrame()
		extracted_features = pd.DataFrame()

		# Loop through every directory
		for dir in os.listdir('C:/Users/jamir/Downloads/2024 - CS multimodal data/'+dataFolder+'/'+subject):
			if dir[0] == '.': continue
			if dir not in featuresArray: continue
			extracted_features = process_folder('C:/Users/jamir/Downloads/2024 - CS multimodal data/'+dataFolder+'/'+subject+"/"+dir, dir,settings)
			# Merge all the extracted feature into one big dataframe
			features = extracted_features.columns
			extracted_features.to_csv('C:/Users/jamir/Downloads/extracted/tsfel_extract_'+subject+'_'+dir+'.csv')
			extractedFiles.append('tsfel_extract_'+subject+'_'+dir+".csv")

			#if not mainDf.empty:
			#	mainDf = mainDf.merge(extracted_features, on="segement_id", how='outer')
			#else:
			#	mainDf = extracted_features
		#Save that dataframe
		#features = mainDf.columns
		#mainDf.to_csv("C:/Users/jamir/Downloads/extracted/tsfel_extract_"+subject+".csv")
		#extractedFiles.append('tsfel_extract_'+subject+".csv")

	return {"extractedFiles":extractedFiles, 'features': features}

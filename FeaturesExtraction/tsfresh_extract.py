import os
import re
import pandas as pd
from tsfresh import extract_features, select_features
import numpy as np
from sklearn.preprocessing import LabelEncoder
from pathlib import Path

def process_folder(folderlink, dir, settings, segement_by_file=False):
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
		if segement_by_file:
			segement_id = int(re.sub("[A-Za-z]","",file.split('.')[0]))
		else:
			data['segement_id'] = dir
		#Append all the dataframes into one for same file type 
		combined_files = combined_files.append(data)
	extracted_features = extract_features(combined_files, column_id='segement_id', column_sort='TimeStamp(epoch)', default_fc_parameters=settings)
	extracted_features = extracted_features.rename_axis('segement_id')
	return extracted_features
	

def process_and_extract_features(dataFolder):
	output_dir = Path('./extracted')
	output_dir.mkdir(parents=True, exist_ok=True)
	extractedFiles = []
	settings = { 
				"median":None,
				"mean": None,
				"variance":None,
				"maximum": None,
				"minimum": None,
				"linear_trend":[{'attr':'pvalue'},{'attr':'rvalue'},{'attr':'intercept'},{'attr':'slope'},{'attr':'stderr'}]
			}
	#os.path.isdir to check for directory
	
	# Loop Through every Subject
	for subject in os.listdir('../data/'+dataFolder):
		if subject[0] == '.': continue
		mainDf = pd.DataFrame()
		extracted_features = pd.DataFrame()
		# Loop through every directory
		for dir in os.listdir('../data/'+dataFolder+'/'+subject):
			if dir[0] == '.': continue
			extracted_features = process_folder('../data/'+dataFolder+'/'+subject+"/"+dir, dir,settings)
			# Merge all the extracted feature into one big dataframe
			if not mainDf.empty:
				mainDf = mainDf.merge(extracted_features, on="segement_id", how='outer')
			else:
				mainDf = extracted_features
		#Save that dataframe
		mainDf.to_csv('./extracted/tsfresh_extract_'+subject+".csv")
		extractedFiles.append('tsfresh_extract_'+subject+".csv")

	return extractedFiles
	
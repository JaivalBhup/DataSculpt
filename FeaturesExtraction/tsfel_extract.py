import os
import re
import pandas as pd
from tsfel import calc_features, get_features_by_domain, time_series_features_extractor
import numpy as np
from sklearn.preprocessing import LabelEncoder
from pathlib import Path

def process_folder(folderlink, dir, settings):
	sett = get_features_by_domain(domain='statistical', json_path=None)

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
		data.drop(['TimeStamp(epoch)'], axis=1, inplace=True)
		extracted_features =   calc_features(wind_sig=data, dict_features=sett, fs=None)
	# extracted_features =   time_series_features_extractor(dict_features=sett, signal_windows= data,fs=None)
		extracted_features.insert(0, 'segement_id',file)
		cols = [combined_files, extracted_features]
		combined_files = pd.concat(cols, ignore_index=True)



	return combined_files
	

def process_and_extract_features(dataFolder, featuresArray):
	output_dir = Path('./extracted')
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
	for subject in os.listdir('./data/'+dataFolder):
		if subject[0] == '.': continue
		mainDf = pd.DataFrame()
		extracted_features = pd.DataFrame()

		# Loop through every directory
		for dir in os.listdir('./data/'+dataFolder+'/'+subject):
			if dir[0] == '.': continue
			if dir not in featuresArray: continue
			extracted_features = process_folder('./data/'+dataFolder+'/'+subject+"/"+dir, dir,settings)
			# Merge all the extracted feature into one big dataframe
			features = extracted_features.columns
			extracted_features.to_csv('./extracted/tsfel_extract_'+subject+'_'+dir+'.csv')
			extractedFiles.append('tsfel_extract_'+subject+'_'+dir+".csv")
	return {"extractedFiles":extractedFiles, 'features': features}
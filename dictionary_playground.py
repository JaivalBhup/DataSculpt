import tkinter as tk
from tkinter import filedialog
import pandas as pd
from tsfresh import extract_features 
import numpy as np
import csv
 
filename ="timeseries.csv"
 
# opening the file using "with"
# statement
with open(filename, 'r') as data:
  for line in csv.DictReader(data):
      print(line)
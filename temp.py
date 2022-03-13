import pandas as pd
import csv
dataframe = csv.reader('css.csv')
with open("css.csv", "r") as f:
    csv_reader = csv.DictReader(f)
    for i in csv_reader:
        print(i['full_name'])
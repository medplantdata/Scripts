import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

file = '/home/school/masters/Scripts/APG_IV/data-apg4-master/apg4.txt'
df = pd.DataFrame(columns=['Scientific Name', 'Taxon Rank'])
rows = []

with open(file, 'r') as f:
    lines = f.readlines()
    for line in lines:
        split_line = line.split()
        rows.append({'Scientific Name': split_line[0], 'Taxon Rank': split_line[1]})

df = pd.DataFrame(rows)
df.to_csv('apg4_data.csv', index=False)
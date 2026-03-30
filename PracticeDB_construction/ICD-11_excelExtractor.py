import numpy
import pandas as pd

# //////////////////////////////////////////////////////////////////////////////////make the ICD-11 codes neurological only
path = "PracticeDB_construction/SimpleTabulation-ICD-11-MMS-en.xlsx"

df = pd.read_excel(path)
dfPsychoological = df.loc[3565:4493]
dfNeurological = df.loc[4580:5468]

dfBoth = pd.concat([dfPsychoological, dfNeurological], ignore_index=True)
dfBoth.to_csv("/home/school/masters/Scripts/PracticeDB_construction/ICD-11_6_8.csv", index=False)
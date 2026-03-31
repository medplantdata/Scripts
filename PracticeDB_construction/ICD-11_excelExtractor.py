import numpy
import pandas as pd

# ///extracting the ICD-11 codes for neurological and psycological disorders to ICD-11_6_8.csv, which will be used to create the PracticeDB for neurological and psychological disorders
"""path = "PracticeDB_construction/SimpleTabulation-ICD-11-MMS-en.xlsx"

df = pd.read_excel(path)
dfPsychoological = df.loc[3565:4493]
dfNeurological = df.loc[4580:5468]

dfBoth = pd.concat([dfPsychoological, dfNeurological], ignore_index=True)
dfBoth.to_csv("/home/school/masters/Scripts/PracticeDB_construction/ICD-11_6_8.csv", index=False)"""

# extracting a list of all the disorders in the ICD-11_6_8.csv removing the 4th level .something codes and saving it to ICD-11NoPointLevel
path = "PracticeDB_construction/ICD-11_6_8.csv"
df = pd.read_csv(path)
dfNoPointLevel = pd.DataFrame(columns=df.columns)

mask = ~(df['Code'].astype(str).str.contains(r'\.')) | df['Code'].isna()
dfNoPointLevel = df[mask]
dfNoPointLevel.to_csv("/home/school/masters/Scripts/PracticeDB_construction/ICD-11NoPointLevel.csv", index=False)



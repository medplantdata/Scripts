import pandas as pd


# extracts a managable (first 10 rows) dataset from the original excel file and also extracts the unique neurological diseases and saves them in a txt file
"""path = "/home/school/masters/Scripts/PracticeDB_construction/Disease-Drug_associations.xlsx"
df = pd.read_excel(path, header=0)
print(df.head())

dfManageable = df.head(10)
dfUniqueNeurologicalDiseases = pd.DataFrame(df['Disease_Name'].unique())

dfUniqueNeurologicalDiseases.to_csv("/home/school/masters/Scripts/PracticeDB_construction/UniqueNeurologicalDiseases.txt", index=False)

dfManageable.to_csv("/home/school/masters/Scripts/PracticeDB_construction/Disease-Drug_associations_manageable.csv", index=False)   
"""
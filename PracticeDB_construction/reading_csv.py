import pandas as pd

path = "/home/school/masters/Scripts/PracticeDB_construction/Disease-Drug_associations.xlsx"
df = pd.read_excel(path, header=0)
print(df.head())

dfManageable = df.head(10)
dfUniqueNeurologicalDiseases = pd.DataFrame(df['Disease_Name'].unique())

dfUniqueNeurologicalDiseases.to_csv("/home/school/masters/Scripts/PracticeDB_construction/UniqueNeurologicalDiseases.txt", index=False)

dfManageable.to_csv("/home/school/masters/Scripts/PracticeDB_construction/Disease-Drug_associations_manageable.csv", index=False)   
import pandas as pd

path = "/home/school/masters/Scripts/PracticeDB_construction/Drug-Target_associations.xlsx"

df = pd.read_excel(path)

dfManageable = df.head(50)

dfManageable.to_csv("/home/school/masters/Scripts/PracticeDB_construction/Drug-Target_associations_manageable.csv", index=False)
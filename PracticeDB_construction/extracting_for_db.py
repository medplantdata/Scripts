import pandas as pd

# extracts the data fromICD-11NoPointLevel and creates a table of diseases that uses a materialized path strategy to 
# represent the hierarchy of diseases. The table is then saved as a csv file.
"""
path = "/home/school/masters/Scripts/PracticeDB_construction/ICD-11NoPointLevel.csv"
df = pd.read_csv(path)

simplified_df = df[['Code', 'Title']].copy()
simplified_df.dropna(subset=['Title'], inplace=True)
#print(simplified_df.head())

codedOnly_df = simplified_df.dropna(subset=['Code'])
#print(codedOnly_df.head(10))
"""
"""
Does not work because of the way the data is structured. The path is not correctly constructed because the hierarchy is not properly represented in the data. The code needs to be modified to correctly construct the path based on the hierarchy of the diseases.
paths = []

for code, title in simplified_df.itertuples(index=False):
    if (title[:5] != '- - -'):
        path = ''
    if pd.isna(code):
        path = path + '/' + title
    else:
        paths.append(path)

codedOnly_df['Path'] = paths
print(codedOnly_df.head(20))

codedOnly_df.to_csv('/home/school/masters/Scripts/PracticeDB_construction/diseases_with_materialized_paths.csv', index=False)
"""
# retrying to take ICD-11NoPointLevel and create something that can go in the DB with matrialized paths but this time
# using the blockID to identify when things are related

big_df = pd.read_csv("/home/school/masters/Scripts/PracticeDB_construction/ICD-11NoPointLevel.csv")

df = big_df[['Code', 'Title', 'BlockId']].copy()

icd = []

for code, title, BlockId in df.itertuples(index=False):
    name = str(title)
    name = name.lstrip('- ')
    if 'L1' in str(BlockId):
        head = name
        path = head + '/'
    elif 'L2' in str(BlockId):
        path = head + '/' + name + '/'
    elif pd.isna(BlockId) and not pd.isna(code):
        path = path + name + '/'
        entry = [code, name, path]
        icd.append(entry)
    

icd_df = pd.DataFrame(icd, columns=['Code', 'Title', 'Path'])

icd_df.to_csv('/home/school/masters/Scripts/PracticeDB_construction/diseases_with_materialized_paths.csv', index=False)
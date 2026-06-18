import pubchempy as pcp
import pandas as pd
import time
# attempt 1 worked well but there were a few errors
"""df = pd.read_csv('/home/school/masters/Scripts/ANPDB/anpdb_compounds_for_db.csv')

cids = {}

def progress_bar(count, total):
    bar_length = 40
    filled_length = int(bar_length * count // total)
    bar = '#' * filled_length + '-' * (bar_length - filled_length)
    print(f'\rProgress: |{bar}| {count}/{total} ({(count/total)*100:.2f}%)', end='')
errors = []
counter = 0

for inchi_key in df['inchi_key']:
    time.sleep(0.5)
    counter += 1
    try:
        compounds = pcp.get_compounds(inchi_key, 'inchikey')
        if compounds:
            compound = compounds[0]
            cids[inchi_key] = (compound.cid)
            print(f"Compound: {compound.iupac_name}, PubMed IDs: {compound.cid}")
            progress_bar(counter, len(df['inchi_key']))
        else:
            print(f"No compound found for InChIKey: {inchi_key}")
            errors.append(inchi_key)
    except Exception as e:
        print(f"Error processing InChIKey {inchi_key}: {e}")
        errors.append(inchi_key)

df['cids'] = df['inchi_key'].map(cids)

df_retry = df[df['cids'].isnull()]

for inchi_key in df_retry['inchi_key']:
    time.sleep(0.5)
    counter += 1
    try:
        compounds = pcp.get_compounds(inchi_key, 'inchikey')
        if compounds:
            compound = compounds[0]
            cids[inchi_key] = (compound.cid)
            print(f"Compound: {compound.iupac_name}, PubMed IDs: {compound.cid}")
            progress_bar(counter, len(df['inchi_key']))
        else:
            print(f"No compound found for InChIKey: {inchi_key}")
            errors.append(inchi_key)
    except Exception as e:
        print(f"Error processing InChIKey {inchi_key}: {e}")
        errors.append(inchi_key)


df['cids'] = df['inchi_key'].map(cids)
emergency_save = pd.DataFrame({'inchi_key': df['inchi_key'], 'cids': df['cids']})
emergency_save.to_csv('/home/school/masters/Scripts/ANPDB/cid dictionary.csv', index=False)
df.to_csv('/home/school/masters/Scripts/ANPDB/anpdb_compounds_for_db.csv', index=False)
print(f"Errors for InChIKeys: {', '.join(errors)}"):"""

# trying again for empty in case the issue was the server timeout
"""df = pd.read_csv('/home/school/masters/Scripts/ANPDB/anpdb_compounds_for_db.csv')

errors = []

for inchi, cid in df[['inchi_key', 'cids']].values:
    if pd.isna(cid):
        time.sleep(0.4)        
        try:
            df.loc[df['inchi_key'] == inchi, 'cids'] = pcp.get_compounds(inchi, 'inchikey')[0].cid
            print('Getting CID for', inchi)
        except:
            errors.append(inchi)
            print('Error getting CID for', inchi)

df.to_csv('/home/school/masters/Scripts/ANPDB/anpdb_compounds_for_db_v2.csv', index=False)
print(f"Errors for InChIKeys: {', '.join(errors)}")"""

# find longest smile/inchi/inchikey for the VARCHAR
"""
df = pd.read_csv('/home/school/masters/Scripts/ANPDB/anpdb_compounds_for_db.csv')

max = 0
bigSmile = ''
for name in df['cas']:
    length = len(str(name))
    if length > max:
        max = length
        bigSmile = name

print(f"{max} is the longest and is for {bigSmile}")"""

# fixing fact that the cids are as .0 
"""df = pd.read_csv('/home/school/masters/Scripts/ANPDB/anpdb_compounds_for_db.csv')

df['cids'] = (df['cids'].astype(str).str.replace(r'\.0$', '', regex=True))

df.to_csv('/home/school/masters/Scripts/ANPDB/anpdb_compounds_for_db.csv', index=False)"""

# fixing inconsistant comma usage causing fields to be added incorrectly to DB
import csv
df = pd.read_csv('/home/school/masters/Scripts/ANPDB/anpdb_compounds_for_db.csv')

for col in ['name', 'synonyms', 'coconut_id', 'cas']:
    if col in df.columns:
        df[col] = df[col].astype(str)

df.to_csv(
    '/home/school/masters/Scripts/ANPDB/anpdb_compounds_for_dbclean.csv',
    index=False,
    quoting=csv.QUOTE_ALL  
)
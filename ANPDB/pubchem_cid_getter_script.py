import pubchempy as pcp
import pandas as pd
import time

df = pd.read_csv('/home/school/masters/Scripts/ANPDB/anpdb_compounds_for_db.csv')

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
print(f"Errors for InChIKeys: {', '.join(errors)}")
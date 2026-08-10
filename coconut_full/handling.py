import pandas as pd
import pubchempy as pcp
import time

"""
#decreasing size
df = pd.read_csv('/home/school/masters/Scripts/coconut_full/coconut_full.csv')

entry = []

for coconut_id, canonical_smiles, standard_inchi, standard_inchi_key, name, organisms, synonyms, cas in df[['identifier', 'canonical_smiles', 'standard_inchi', 'standard_inchi_key', 'name', 'organisms', 'synonyms', 'cas']].values:
    entry.append([coconut_id, canonical_smiles, standard_inchi, standard_inchi_key, name, organisms, synonyms, cas])

shorter_df = pd.DataFrame(entry, columns=['coconut_id', 'canonical_smiles', 'standard_inchi', 'standard_inchi_key', 'name', 'organisms', 'synonyms', 'cas'])

shorter_df.to_csv('/home/school/masters/Scripts/coconut_full/coconut_managebale.csv', index=False)

print(df.head)
"""


# removing the already in DB compounds and assigning name
"""
df = pd.read_csv('/home/school/masters/Scripts/coconut_full/coconut_managebale.csv')
in_db_df = pd.read_csv('/home/school/masters/Scripts/ANPDB/compound_stuff/anpdb_compounds_for_dbclean.csv')

in_db = set(in_db_df['coconut_id'])

df = df[~df['coconut_id'].isin(in_db)]

df.to_csv('/home/school/masters/Scripts/coconut_full/new_compounds.csv')
"""

#giving compound cids
"""
def progress_bar(count, total):
    bar_length = 40
    filled_length = int(bar_length * count // total)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    print(f'\rProgress: |{bar}| {count}/{total} ({(count/total)*100:.2f}%)', end='')

df = pd.read_csv('/home/school/masters/Scripts/coconut_full/coconut_managebale.csv')

df['cid'] = None
err = []
count = 0
length = len(df)

for idx, row in df[df['cid'].isna()].iterrows():
    inchi = row['standard_inchi']
    try:
        compound = pcp.get_compounds(inchi, 'inchi')
        cid = compound[0].cid 
        df.at[idx, 'cid'] = cid
        progress_bar(count, length)
    except Exception as e:
        print(f"Error retrieving compound for InChI {inchi}: {e}")
        err.append([inchi,str(e)])
    count += 1
    time.sleep(0.2)
    if count % 1000 == 0:
        df.to_csv('/home/school/masters/Scripts/coconut_full/coconut_with_cids.csv', index=False)
        error_df = pd.DataFrame(err, columns=['standard_inchi', 'error'])
        error_df.to_csv('/home/school/masters/Scripts/coconut_full/errors_for_cids.csv', index=False)



error_df = pd.DataFrame(err, columns=['standard_inchi', 'error'])
error_df.to_csv('/home/school/masters/Scripts/coconut_full/errors.csv', index=False)
df.to_csv('/home/school/masters/Scripts/coconut_full/coconut_with_cids.csv', index=False)

#script that gets cids and handles bad gateway error

def progress_bar(count, total):
    bar_length = 40
    filled_length = int(bar_length * count // total)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    print(f'\rProgress: |{bar}| {count}/{total} ({(count/total)*100:.2f}%)', end='')

df = pd.read_csv('/home/school/masters/Scripts/coconut_full/coconut_managebale.csv')

df['cid'] = None
err = []
count = 0
length = len(df)

for idx, row in df[df['cid'].isna()].iterrows():
    inchi = row['standard_inchi']
    inchi_key = row['standard_inchi_key']
    smiles = row['canonical_smiles']
    try:
        compound = pcp.get_compounds(inchi, 'inchi')
        cid = compound[0].cid 
        df.at[idx, 'cid'] = cid
        progress_bar(count, length)
    except Exception as e:
        while 'PubChem HTTP Error 502 Bad Gateway' in str(e):
            print(f"Bad Gateway error for InChI {inchi}. Retrying...")
            time.sleep(5) 
            try:
                compound = pcp.get_compounds(inchi, 'inchi')
                cid = compound[0].cid 
                df.at[idx, 'cid'] = cid
                progress_bar(count, length)
            except Exception as e:
                print(f"Error retrieving compound for InChI {inchi} after retry: {e}")
                err.append([inchi,str(e)])
        else:
            try:
                compound = pcp.get_compounds(smiles, 'smiles')
                cid = compound[0].cid 
                df.at[idx, 'cid'] = cid
                progress_bar(count, length)
            except Exception as e:
                try:
                    compound = pcp.get_compounds(inchi_key, 'inchikey')
                    cid = compound[0].cid 
                    df.at[idx, 'cid'] = cid
                    progress_bar(count, length)
                except Exception as e:
                    print(f"Error retrieving compound for InChI {inchi} after retry: {e}")
                    err.append([inchi,str(e)])
                    print(f"Error retrieving compound for InChI {inchi}: {e}")
                    err.append([inchi,str(e)])
    count += 1
    time.sleep(0.2)
    if count % 1000 == 0:
        df.to_csv('/home/school/masters/Scripts/coconut_full/coconut_with_cids.csv', index=False)
        error_df = pd.DataFrame(err, columns=['standard_inchi', 'error'])
        error_df.to_csv('/home/school/masters/Scripts/coconut_full/errors_for_cids.csv', index=False)



error_df = pd.DataFrame(err, columns=['standard_inchi', 'error'])
error_df.to_csv('/home/school/masters/Scripts/coconut_full/errors.csv', index=False)
df.to_csv('/home/school/masters/Scripts/coconut_full/coconut_with_cids.csv', index=False)
"""

df = pd.read_csv('/home/school/masters/Scripts/coconut_full/coconut_managebale.csv')

df = df[['coconut_id','standard_inchi','standard_inchi_key','canonical_smiles']]

df.to_csv('/home/school/masters/Scripts/coconut_full/compounds_for_wonko.csv',index=False)

"""import time
import pandas as pd
import pubchempy as pcp
def get_cid(input,type):
    for k in range(5):
        try:
            compound = pcp.get_compounds(input,type)
            if compound:
                cid = compound[0].cid
                return cid
            else:
                return None
        except Exception as e:
            error_msg = str(e)
            if '502' in error_msg or 'bad gateway' in error_msg.lower() or 'timeout' in error_msg.lower():
                time.sleep(5)
            else:
                return str(e)
    return 'retry not sucessful'
       
def progress_bar(count, total):
    bar_length = 40
    filled_length = int(bar_length * count // total)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    out = f'\rProgress: |{bar}| {count}/{total} ({(count/total)*100:.2f}%)'
    return out

coconut_in = '/home/school/masters/Scripts/coconut_full/coconut_managebale.csv'
err_out = '/home/school/masters/Scripts/coconut_full/errors_for_cids.csv'
progress_out = '/home/school/masters/Scripts/coconut_full/progress_for_cids.csv'
results_out = '/home/school/masters/Scripts/coconut_full/coconut_with_cids.csv'

df = pd.read_csv(coconut_in)

df['cid'] = None
err = []
count = 1
length = len(df)

for idx, row in df.iterrows():
    inchi = row['standard_inchi']
    inchi_key = row['standard_inchi_key']
    smiles = row['canonical_smiles']

    cid = get_cid(inchi,'inchi')
    prog = progress_bar(count, length)

    if isinstance(cid,int):
        df.at[idx, 'cid'] = cid
    else:
        cid = get_cid(smiles,'smiles')
        if isinstance(cid,int):
            df.at[idx, 'cid'] = cid
        else:
            cid = get_cid(inchi_key,'inchikey')
            if isinstance(cid,int):
                df.at[idx, 'cid'] = cid
            else:
                err.append([inchi,cid])
    time.sleep(0.2)
    count += 1

    if count % 1000 == 0:
        df.to_csv(results_out, index=False)
        error_df = pd.DataFrame(err, columns=['standard_inchi', 'error'])
        error_df.to_csv(err_out,index=False)
        prog_df = pd.DataFrame([prog], columns=['Progress'])
        prog_df.to_csv(progress_out, index=False)
    prog_df = pd.DataFrame([prog], columns=['Progress'])
    print(prog)

df.to_csv(results_out,index=False)
error_df = pd.DataFrame(err, columns=['standard_inchi', 'error'])
error_df.to_csv(err_out,index=False)
prog_df = pd.DataFrame([prog], columns=['Progress'])
prog_df.to_csv(progress_out, index=False)"""
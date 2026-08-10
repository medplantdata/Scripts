import time
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

coconut_in = '/nlustre/users/nathanc/compounds_for_wonko.csv'
err_out = '/nlustre/users/nathanc/errors_for_cids.csv'
progress_out = '/nlustre/users/nathanc/progress_for_cids.csv'
results_out = '/nlustre/users/nathanc/coconut_with_cids.csv'

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
prog_df.to_csv(progress_out, index=False)
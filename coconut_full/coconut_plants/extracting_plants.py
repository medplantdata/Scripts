import pandas as pd
import sys
# extracts coconut_id and organism 
plant_file = '/home/school/masters/Scripts/wcvp_dwca/wcvp_taxon.csv'
input_file_path = '/home/school/masters/Scripts/coconut_full/coconut_full.csv'
error_path = ''
output_path = ''

# getting the coconut_id and organism from the coconut_full.csv file to send to the checkilist thingy
"""
df = pd.read_csv(input_file_path)
entries = []

for idx, row in df.iterrows():
    coconut_id = row['identifier']
    orgs = row['organisms']
    if pd.isna(orgs) == False:
        organisms = orgs.split('|')
        clean_organisms = [organism.strip() for organism in organisms]
        for organism in clean_organisms:
            entries.append([coconut_id,organism])

coconut_organisms= pd.DataFrame(entries, columns=['coconut_id','scientificName'])
print('finished plant sep')
coconut_organisms.to_csv('/home/school/masters/Scripts/coconut_full/coconut_organisms.csv', index=False)
"""


# code below was supposed to check the names against the WCVP but but I decided to do this differently
"""
seperated_plants_df = pd.DataFrame(entries,columns=['coconut_id','plant_name_from_coconut'])
plant_df = pd.read_csv(plant_file, sep= '|')

entries = []
entry = []
errors = []

for idx, row in seperated_plants_df.iterrows():
    full_name = row['plant_name_from_coconut']
    full_name = full_name.strip()
    genus = full_name.split()[0]
    species = full_name.split()[1]
    coconut_id = seperated_plants_df['coconut_id']


    if plant_df['scientfiicname'].str.lower().isin([full_name.lower()]):
        plant_row = plant_df.loc(plant_df['scientfiicname'] == full_name)
        if plant_row['taxonomicstatus'] == 'accepted':
            for idx, row in plant_row.iterrows():
                entry = [coconut_id,full_name,row['taxonid']]
        elif pd.isna(plant_row['acceptedusagenameid']):
            errors = [coconut_id, full_name, 'the name was not relateable to a proper ID via the WCVP']
        else:
            accepted_id = plant_row['acceptedusagenameid']
            accepted_row = plant_df.loc[plant_df['taxonid'] == accepted_id]
            entry = [coconut_id,full_name,accepted_row['taxonid']] 
    else:
        print(full_name)
        errors = [coconut_id, full_name, 'WCVP does not have a synonym for this one']
        sys.exit()

df_with_accepted_names = pd.DataFrame(entries, columns = ['coconut_id', 'coconut_name', 'accepted_id'])
"""


# pulling non plantae from coconut plants and deduplicating on the origional name from coconut_full.csv
"""
df = pd.read_csv('/home/school/masters/Scripts/coconut_full/checklist_matched_organisms.tsv',sep='\t')

entries = []
for row in df.itertuples(index=False):
    if row.kingdom == 'Plantae':
        entries.append(row)

old_len = len(df)
formatted = f"{old_len:,}".replace(",", " ")
print(f"The file sent had 1 267 087 entires and the one that came back has {old_len} (there are lots of dups still 
      in theory not just because of plant synonyms but because the same plants are repeated)")

df_plants = pd.DataFrame(entries, 
                         columns=['original_coconut_id','original_scientificName','matchType','matchIssues','ID','rank',
                                  'scientificName','authorship','status','acceptedID','acceptedScientificName',
                                  'acceptedAuthorship','kingdom','phylum','class','order','family','genus','classification'])

new_len = len(df_plants)
formatted = f"{new_len:,}".replace(",", " ")
print(f'The plants only (not deduplicated) is {formatted}')

df_plants.drop_duplicates('original_scientificName',inplace=True)

new_len = len(df_plants)
formatted = f"{new_len:,}".replace(",", " ")
print(f'The plants now with origional name deduplications removed is {formatted}')

df_plants.to_csv('/home/school/masters/Scripts/coconut_full/coconut_plants_still_needs_synonym_deduplication.csv', index=False)
"""

"""
# seeing what the options are for some of the ranks to fin what to excclude

df = pd.read_csv('/home/school/masters/Scripts/coconut_full/coconut_plants/coconut_plants_still_needs_synonym_deduplication.csv')

match_types = df['matchType'].unique()
match_issues = df['matchIssues'].unique()

print(f'Types of matches are: {match_types}')
print(f'Types of match issues are: {match_issues}')
"""


# making a script that seperates the plants that worked so I can deduplicate on synonyms and assign accepted names
"""
df = pd.read_csv('/home/school/masters/Scripts/coconut_full/coconut_plants/coconut_plants_still_needs_synonym_deduplication.csv')

df.drop(columns=['original_coconut_id'],inplace=True)

entries = []
naughty_names = []

for row in df.itertuples(index=False):
    if (row.matchType not in ['ambiguous','higherrank']) and pd.isna(row.matchIssues):
        entries.append(row)
    else:
        naughty_names.append(row)

column_names = df.columns

worked_df = pd.DataFrame(entries, columns=column_names)
worked_df.to_csv('/home/school/masters/Scripts/coconut_full/coconut_plants/to_be_deduplicated_validated_plants.csv',index=False)

no_df = pd.DataFrame(naughty_names,columns=column_names)
no_df.to_csv('/home/school/masters/Scripts/coconut_full/coconut_plants/checklist_error_plants.csv',index=False)
"""

# script to count mismatches in scientific names between my checklist and the WCVP checklist (31 Aug)
"""
coco_df = pd.read_csv('/home/school/masters/Scripts/coconut_full/coconut_plants/to_be_deduplicated_validated_plants.csv')
wcvp_df1 = pd.read_csv('/home/school/masters/Scripts/wcvp_dwca/wcvp_taxon.csv', sep='|')


wcvp_df1['name'] = None

wcvp_df = wcvp_df1[['scientfiicname','name']].copy()
wcvp_df1['scientfiicname'] = wcvp_df1['scientfiicname'].str.strip()



for idx, row in wcvp_df.iterrows():
    if len(str(row.scientfiicname).split()) > 1:
        genus = row.scientfiicname.split()[0]
        species = row.scientfiicname.split()[1]
        name = f'{genus} {species}'
        name = name.replace('-', '')
        wcvp_df.at[idx,'name'] = name
    
        

wvcp_set = set(wcvp_df['name'].str.lower())

match_count = 0
mismatch_count = 0


entries = []
for row in coco_df.itertuples(index=False):
    name = row.scientificName if pd.isna(row.acceptedScientificName) else row.acceptedScientificName

    name = name.replace('-', '')

    if len(str(name).split()) > 1:
        genus = name.split()[0]
        species = name.split()[1]
        name = f'{genus} {species}'

    if isinstance(name, str):
        name = name.strip().lower()
    else:
        print(f'No name found for row: {row}')

    if name in wvcp_set:
        match_count+=1
    else:
        mismatch_count+=1
        entries.append([row.originalScientificName, row.acceptedScientificName, row.scientificName])


mismatch_df = pd.DataFrame(entries, columns=['original_scientificName', 'accepted_scientificName', 'scientificName'])
mismatch_df.to_csv('/home/school/masters/Scripts/coconut_full/coconut_plants/plants_not_in_WCVP.csv', index=False)
print(f'{match_count} matches')
print(f'{mismatch_count} mismatches')
"""

#NOT USED >>>>>dereplicating the gbif matched plants from coconut then adding names as synonyms for POWO matching (31 Aug)
"""
def clean_name(name):
    if isinstance(name, str):
        name = name.strip().lower()
        name = name.replace('-', '')
        if len(str(name).split()) > 1:
            genus = name.split()[0]
            species = name.split()[1]
            name = f'{genus} {species}'
        return name
    else:
        return None

gbif = pd.read_csv('/home/school/masters/Scripts/coconut_full/coconut_plants/to_be_deduplicated_validated_plants(matches_to_coconut).csv')

entries = []
ID_set = set()
count = 0
for idx, row in gbif.iterrows():
    synonyms = ''
    if not row.ID in ID_set:
        count+=1
        ID_set.add(row.ID)
        if pd.isna(row.acceptedID):
            name = row.scientificName
            gbif_taxon_key = row.ID
            cleaned_name = clean_name(name)
        else:
            name = row.acceptedScientificName
            cleaned_name = clean_name(name)
            gbif_taxon_key = row.acceptedID
            synonyms = f'{row.scientificName} ({row.ID})'

        entries.append([count,cleaned_name,name,gbif_taxon_key,synonyms])
print('deduplication complete')   
deduplicated_df = pd.DataFrame(entries, columns=['count','cleaned_name','scientificName','gbif_taxon_key','synonyms'])

wcvp = pd.read_csv('/home/school/masters/Scripts/wcvp_dwca/wcvp_taxon.csv', sep='|')

entries = []
count = 0

for idx, row in wcvp.iterrows():
    name = clean_name(row.scientfiicname)
    if name in deduplicated_df['cleaned_name'].values:
        count += 1
        gbif_taxon_key = deduplicated_df.loc[deduplicated_df['cleaned_name'] == name, 'gbif_taxon_key'].values[0]
        synonyms = deduplicated_df.loc[deduplicated_df['cleaned_name'] == name, 'synonyms'].values[0]
        taxon_id = row.taxonid
        family = row.family
        scientific_name = row.scientfiicname
        scientific_name_authorship = row.scientfiicnameauthorship
        taxonomic_status = row.taxonomicstatus
        acceptednameusageid = row.acceptednameusageid
        parentnameusageid = row.parentnameusageid
        originalnameusageid = row.originalnameusageid
        namepublishedin = row.namepublishedin
        scientificnameid = row.scientificnameid
        dynamicproperties = row.dynamicproperties
        references = row.references
        entries.append([count,gbif_taxon_key,family,scientific_name,scientific_name_authorship,taxonomic_status,acceptednameusageid,parentnameusageid,originalnameusageid,namepublishedin,scientificnameid,dynamicproperties,references])
        if count % 10000 == 0:
            print(count)
        
df = pd.DataFrame(entries,columns=["count", "gbif_taxon_key", "family", "scientific_name", "scientific_name_authorship", "taxonomic_status", "acceptednameusageid", "parentnameusageid", "originalnameusageid", "namepublishedin", "scientificnameid", "dynamicproperties", "references"])
df.to_csv('/home/school/masters/Scripts/coconut_full/coconut_plants/dereplicated_powo_matched_plants.csv', index=False)
"""

# Not used deduplication of checklisted plants from coconut  (1 Sep)
"""
def clean_name(name):
    if isinstance(name, str):
        name = name.strip().lower()
        name = name.replace('-', '')
        if len(str(name).split()) > 1:
            genus = name.split()[0]
            species = name.split()[1]
            name = f'{genus} {species}'
        return name
    else:
        return None

gbif_df = pd.read_csv('/home/school/masters/Scripts/coconut_full/coconut_plants/to_be_deduplicated_validated_plants(matches_to_coconut).csv')

entry=[]
for idx, row in gbif_df.iterrows():
    if pd.isna(row.acceptedID):
        gbif_taxon_key = row.id
        accepted_name = row.scientificName
        synonym = None
    else: 
        gbif_taxon_key = row.acceptedID
        accepted_name = row.acceptedScientificName
        synonym = f'{row.scientificName} ({row.ID})'
    entry.append([gbif_taxon_key,accepted_name,synonym])

columns = ['gbif_taxon_key','scientific_name','synonym']
df = pd.DataFrame(entry, columns=columns)

df = df.groupby('gbif_taxon_key',as_index=False).agg(
    scientific_name=('scientific_name','first'),
    synonyms=('synonym', lambda x: list(pd.unique(x.dropna())))
)
"""

# the following is gonna take very long and is kinda broken and is not used
"""
df_wcvp = pd.read_csv('/home/school/masters/Scripts/wcvp_dwca/wcvp_taxon.csv', sep='|')
for id, row in df.iterrows():
    name = clean_name(row.scientificName)
    if name in df_wcvp[clean_name[df_wcvp['scientfiicname']]]:
        wvcp_row = df_wcvp.loc[clean_name(df_wcvp['scientfiicname'])==name]
        wvcp_id = wvcp_row.taxon_id
        family = wvcp_row.family
        powo_scientific_name = wvcp_row.scientfiicname
        scientific_name_authorship = wvcp_row.scientfiicnameauthorship
        taxonomic_status = wvcp_row.taxonomicstatus
        acceptednameusageid = wvcp_row.acceptednameusageid
        parentnameusageid = wvcp_row.parentnameusageid
        originalnameusageid = wvcp_row.originalnameusageid
        namepublishedin = wvcp_row.namepublishedin
        scientificnameid = wvcp_row.scientificnameid
        dynamicproperties = wvcp_row.dynamicproperties
        references = wvcp_row.references
        df.at[id,'gbif_taxon_key'] = wvcp_id
        df.at[id,'family'] = family
        df.at[id,'scientific_name'] = powo_scientific_name
        df.at[id,'scientific_name_authorship'] = scientific_name_authorship
        df.at[id,'taxonomic_status'] = taxonomic_status
        df.at[id,'acceptednameusageid'] = acceptednameusageid
        df.at[id,'parentnameusageid'] = parentnameusageid
        df.at[id,'originalnameusageid'] = originalnameusageid
        df.at[id,'namepublishedin'] = namepublishedin
        df.at[id,'scientificnameid'] = scientificnameid
        df.at[id,'dynamicproperties'] = dynamicproperties
        df.at[id,'references'] = references

df.to_csv('/home/school/masters/Scripts/coconut_full/coconut_plants/dereplicated_powo_matched_plants.csv', index=False)
"""

"""
# making a smaller version of the wcvp using the coconut checklisted plants (1 Sep)
def clean_name(name): # cleans the names 
    if isinstance(name, str):
        name = name.strip().lower()
        name = name.replace('-', '')
        if len(str(name).split()) > 1:
            genus = name.split()[0]
            species = name.split()[1]
            name = f'{genus} {species}'
        return name
    else:
        return None

df_wcvp = pd.read_csv('/home/school/masters/Scripts/wcvp_dwca/wcvp_taxon.csv', sep='|')
gbif_df = pd.read_csv('/home/school/masters/Scripts/coconut_full/coconut_plants/to_be_deduplicated_validated_plants(matches_to_coconut).csv')

wcvp = df_wcvp.copy()
gbif = gbif_df.copy()

print(gbif.columns.tolist())
print(wcvp.columns.tolist())

gbif=gbif.drop(columns=['matchType', 'matchIssues', 'rank', 'authorship', 'status', 'acceptedAuthorship', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'classification'])
wcvp=wcvp.drop(columns=['genus', 'specificepithet', 'nomenclaturalstatus'])

print('dropped uneccesary columns')

wcvp['cleaned_name'] = wcvp['scientfiicname'].map(clean_name)
gbif['cleaned_name'] = gbif['scientificName'].map(clean_name)
print('merging now')



df = gbif.merge(wcvp, how='inner', on='cleaned_name',validate='m:m')

df.to_csv('/home/school/masters/Scripts/coconut_full/coconut_plants/merged_gbif_wcvp.csv')
"""

# now taaking the merge file and deduplicationg while handling variants and synonyms

import pandas as pd
import requests
# creating a junction table that will link the compound ID to a npclassifier class id, superclass id and then pathway id
"""compoundsdf = pd.read_csv('/home/school/masters/Scripts/ANPDB/anpdb_plants.csv')

classdf = pd.read_csv('/home/school/masters/Scripts/NpClassifier_ClassyFire/NpClassifierClassesDB.csv')
classdict = dict(zip(classdf['class'], classdf['class_id']))
entry =[]

url = 'https://npclassifier.gnps2.org/classify?smiles=<smiles string>'

error =[]
for coconut_id, smiles, classname in compoundsdf[['identifier','canonical_smiles','np_classifier_class']].values:
    if pd.isna(classname):
        r = requests.get(url.replace('<smiles string>', smiles), timeout=10)
        r.raise_for_status()
        data = r.json()
        try:
            class_id = classdict[data['class']]
            entry.append((coconut_id, class_id, data['class']))
            print(f"Processed: {coconut_id} it is a {data['class']}")
        except KeyError:
            entry.append((coconut_id, None, None))
            error.append(f"Error for {coconut_id}")
    else:
        entry.append((coconut_id, classdict[classname], classname))
junction1 = pd.DataFrame(entry, columns=['compound_id', 'class_id', 'class'])

print(error)

print(junction1.head())
"""

# So due to the fact that the coconut entries are incomplete I am going to use the API and reclassify the stuff

dfcompounds  = pd.read_csv('ANPDB/anpdb_compounds_for_dbclean.csv')
dfpathways   = pd.read_csv('/home/school/masters/Scripts/NpClassifier_ClassyFire/NpClassifierPathwaysDB.csv')
dfsuperclass = pd.read_csv('/home/school/masters/Scripts/NpClassifier_ClassyFire/NpClassifierSuperclassesDB.csv')
dfclasses    = pd.read_csv('/home/school/masters/Scripts/NpClassifier_ClassyFire/NpClassifierClassesDB.csv')

def progress_bar(count, length):
    bar_length = 40
    filled_length = int(bar_length * count // length)
    bar = '#' * filled_length + '-' * (bar_length - filled_length)
    print(f'\rProgress: |{bar}| {count}/{length} ({(count/length)*100:.2f}%)', end='')

url = 'https://npclassifier.gnps2.org/classify?smiles=<smiles string>'

r = requests.get(url.replace('<smiles string>', 'CCC1=NC=CN=C1C(C)=O'), timeout=10)
r.raise_for_status()
data = r.json()
print(data)
print(data['class_results'])
counter = 0
errors = []
entry_pathway = []
entry_superclass = []
entry_class = []
for coconutid, smiles in dfcompounds[['identifier','canonical_smiles']].values:
    counter += 1
    try:
        r = requests.get(url.replace('<smiles string>', smiles))
        r.raise_for_status()
        data = r.json()
        classres      = data['class_results']
        superclassres = data['superclass_results']
        pathwayres    = data['pathway_results']
        
        classid = dfclasses[dfclasses['class'] == classres[0]]['class_id']
        entry_class.append((coconutid, classid))

        for superclass in superclassres:
            superclassid = dfsuperclass[dfsuperclass['superclass'] == superclass]['superclass_id']
            entry_superclass.append((coconutid, superclassid))

        for pathway in pathwayres:
            pathwayid = dfpathways[dfpathways['pathway'] == pathway]['pathway_id']
            entry_pathway.append((coconutid, pathwayid))
        print(f"Processed: {coconutid}")
        progress_bar(counter, len(dfcompounds['identifier']))
    except:
        errors.append(f"Error for {coconutid}")

junction1 = pd.DataFrame(entry_class, columns=['compound_id', 'class_id'])
junction2 = pd.DataFrame(entry_superclass, columns=['compound_id', 'superclass_id'])
junction3 = pd.DataFrame(entry_pathway, columns=['compound_id', 'pathway_id'])

junction1.to_csv('/home/school/masters/Scripts/ANPDB/anpdb_compound_class_junction.csv', index=False)
junction2.to_csv('/home/school/masters/Scripts/ANPDB/anpdb_compound_superclass_junction.csv', index=False)
junction3.to_csv('/home/school/masters/Scripts/ANPDB/anpdb_compound_pathway_junction.csv', index=False)

print(errors)



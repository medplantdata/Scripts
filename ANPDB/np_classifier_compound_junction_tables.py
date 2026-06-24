import pandas as pd
import requests
# creating a junction table that will link the compound ID to a npclassifier class id, superclass id and then pathway id
compoundsdf = pd.read_csv('/home/school/masters/Scripts/ANPDB/anpdb_plants.csv')

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

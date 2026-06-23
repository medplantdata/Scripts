import pandas as pd
import requests
# creating a junction table that will link the compound ID to a npclassifier class id
compoundsdf = pd.read_csv('/home/school/masters/Scripts/ANPDB/anpdb_plants.csv')

classdf = pd.read_csv('/home/school/masters/Scripts/NpClassifier_ClassyFire/NpClassifierClassesDB.csv')
classdict = dict(zip(classdf['class'], classdf['class_id']))
entry =[]

url = 'https://npclassifier.gnps2.org/classify?smiles=<smiles string>'


for coconut_id, classname in compoundsdf[['identifier', 'np_classifier_class']].values:
    if classname == 'nan':
        r = requests.get(url.replace('<smiles string>', coconut_id), timeout=10)
        r.raise_for_status()
        data = r.json()
        try:
            class_id = classdict[data['class']]
            entry.append((coconut_id, class_id, data['class']))
        except KeyError:
            entry.append((coconut_id, None, None))
junction1 = pd.DataFrame(entry, columns=['compound_id', 'class_id', 'class'])

print(junction1.head())

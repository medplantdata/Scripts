import pandas as pd
import pdfplumber


#////////////extracts the NPClassifier classes from the pdf and saves them as a csv file.////////////
"""
pdf = '/home/school/masters/Scripts/NpClassifier_ClassyFire/listOfAllNPClassifierClasses.pdf'
out = []

with pdfplumber.open(pdf) as pdf:
    for i in range(15,44):
        page = pdf.pages[i]
        table = page.extract_table()
        if table:
            df = pd.DataFrame(table)
            out.append(df)

final = pd.concat(out, ignore_index=True)
final.to_csv('/home/school/masters/Scripts/NpClassifier_ClassyFire/listOfAllNPClassifierClasses.csv', index=False)
"""
#//////cleaning up csv
"""
df = pd.read_csv('/home/school/masters/Scripts/NpClassifier_ClassyFire/listOfAllNPClassifierClasses.csv')
dropDF = df.iloc[2:, :-4]
cleanDF = pd.DataFrame(dropDF.values, columns=['pathway', 'superclass','class'])
cleanDF.to_csv('/home/school/masters/Scripts/NpClassifier_ClassyFire/cleaned_listOfAllNPClassifierClasses.csv', index=False)
"""
#//////making data in DB format apparently this wont work
"""df = pd.read_csv('/home/school/masters/Scripts/NpClassifier_ClassyFire/cleaned_listOfAllNPClassifierClasses.csv')

pathwayDf = pd.DataFrame(df['pathway'].tolist(index = True).drop_duplicates(), columns=['pathway_id','pathway'])
spcList = []
superclass_counter = 0

superclasWorkingdf = df.drop_duplicates(subset=['superclass'])
for pathway, superclass in superclasWorkingdf[['pathway', 'superclass']].values:
    superclass_counter += 1
    pathway_id = pathwayDf[pathwayDf['pathway'] == pathway].index[0]
    spcList.append((superclass_counter, superclass, pathway_id))

superclassDf = pd.DataFrame(spcList, columns=['superclass_id','superclass','pathway_id'])

classList = []
class_counter = 0
for superclass, class_ in df[['superclass', 'class']].values:
    class_counter += 1
    superclass_id = superclassDf[superclassDf['superclass'] == superclass].index[0]
    classList.append((class_counter, class_, superclass_id))

classDf = pd.DataFrame(classList, columns=['class_id','class','superclass_id'])


pathwayDf.to_csv('/home/school/masters/Scripts/NpClassifier_ClassyFire/NpClassifierPathwaysDB.csv', index=False)
superclassDf.to_csv('/home/school/masters/Scripts/NpClassifier_ClassyFire/NpClassifierSuperclassesDB.csv', index=False)
classDf.to_csv('/home/school/masters/Scripts/NpClassifier_ClassyFire/NpClassifierClassesDB.csv', index=False)
"""

# ai assisted version of the above -> this still lead to some duplicates
"""
df = pd.read_csv(
    "/home/school/masters/Scripts/NpClassifier_ClassyFire/cleaned_listOfAllNPClassifierClasses.csv"
)

# Ensure pathway is treated as categorical dim table
# 1) get unique pathways
pathway_unique = df["pathway"].drop_duplicates().reset_index(drop=True)

# 2) build pathwayDf with explicit IDs
pathwayDf = pd.DataFrame(
    {
        "pathway_id": range(1, len(pathway_unique) + 1),
        "pathway": pathway_unique
    }
)

# ---------- SUPERCLASS ----------
spcList = []
superclass_counter = 0

# unique (pathway, superclass) pairs so you don't duplicate superclasses per pathway
superclasWorkingdf = df.drop_duplicates(subset=["pathway", "superclass"])

for pathway, superclass in superclasWorkingdf[["pathway", "superclass"]].values:
    superclass_counter += 1
    # find pathway_id by value, not relying on the current index
    pathway_id = pathwayDf.loc[pathwayDf["pathway"] == pathway, "pathway_id"].iloc[0]
    spcList.append((superclass_counter, superclass, pathway_id))

superclassDf = pd.DataFrame(
    spcList,
    columns=["superclass_id", "superclass", "pathway_id"]
)

# ---------- CLASS ----------
classList = []
class_counter = 0

# unique (superclass, class) pairs
classWorkingdf = df.drop_duplicates(subset=["superclass", "class"])

for superclass, class_ in classWorkingdf[["superclass", "class"]].values:
    class_counter += 1
    # look up superclass_id by value
    superclass_id = superclassDf.loc[
        superclassDf["superclass"] == superclass, "superclass_id"
    ].iloc[0]
    classList.append((class_counter, class_, superclass_id))

classDf = pd.DataFrame(
    classList,
    columns=["class_id", "class", "superclass_id"]
)

# ---------- WRITE OUT ----------
pathwayDf.to_csv(
    "/home/school/masters/Scripts/NpClassifier_ClassyFire/NpClassifierPathwaysDB.csv",
    index=False,
)
superclassDf.to_csv(
    "/home/school/masters/Scripts/NpClassifier_ClassyFire/NpClassifierSuperclassesDB.csv",
    index=False,
)
classDf.to_csv(
    "/home/school/masters/Scripts/NpClassifier_ClassyFire/NpClassifierClassesDB.csv",
    index=False,
)
"""

# checking for duplicates
""""
classDf = pd.read_csv('/home/school/masters/Scripts/NpClassifier_ClassyFire/NpClassifierClassesDB.csv')
duplicates = classDf[classDf.duplicated(subset=['class'], keep=False)]
print(duplicates)
"""

# redoing to try to remove duplicates but not assign the foreign key just yet
"""
df = pd.read_csv("/home/school/masters/Scripts/NpClassifier_ClassyFire/cleaned_listOfAllNPClassifierClasses.csv")

pathwayDF = pd.DataFrame(df['pathway'].drop_duplicates().reset_index(drop=True)).reset_index()
pathwayDF.columns = ['pathway_id', 'pathway']
pathwayDF['pathway_id'] += 1
pathwayDF.to_csv('/home/school/masters/Scripts/NpClassifier_ClassyFire/NpClassifierPathwaysDB.csv', index=False)

superclassDF = pd.DataFrame(df['superclass'].drop_duplicates().reset_index(drop=True)).reset_index()
superclassDF.columns = ['superclass_id', 'superclass']
superclassDF['superclass_id'] += 1
superclassDF.to_csv('/home/school/masters/Scripts/NpClassifier_ClassyFire/NpClassifierSuperclassesDB.csv', index=False)

classDF = pd.DataFrame(df['class'].drop_duplicates().reset_index(drop=True)).reset_index()
classDF.columns = ['class_id', 'class']
classDF['class_id'] += 1
classDF.to_csv('/home/school/masters/Scripts/NpClassifier_ClassyFire/NpClassifierClassesDB.csv', index=False)
"""

# now assigning the foreign keys
"""
df = pd.read_csv("/home/school/masters/Scripts/NpClassifier_ClassyFire/cleaned_listOfAllNPClassifierClasses.csv")
pathwayDF = pd.read_csv('/home/school/masters/Scripts/NpClassifier_ClassyFire/NpClassifierPathwaysDB.csv')
superclassDF = pd.read_csv('/home/school/masters/Scripts/NpClassifier_ClassyFire/NpClassifierSuperclassesDB.csv')
classDF = pd.read_csv('/home/school/masters/Scripts/NpClassifier_ClassyFire/NpClassifierClassesDB.csv')

fkSuperClassDF = pd.DataFrame(superclassDF,columns=['superclass_id','superclass','pathway_id'])
fkclassDF = pd.DataFrame(classDF,columns=['class_id','class','superclass_id'])

fkSuperClassDF['pathway_id'] =

fkclassDF['superclass_id'] = fkclassDF['superclass'].map(
    lambda x: fkSuperClassDF.loc[fkSuperClassDF['superclass'] == x, 'superclass_id'].values[0]  
)
"""

# trying to remove duplicates and then assigning FK is difficult attempting to do it all in one go 


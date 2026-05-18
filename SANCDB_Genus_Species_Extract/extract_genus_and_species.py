# using the rest api for SANCDB I am attempting to grip all the plants genusses and their species names to cross correlate with family to go into the DB
import requests
import pandas as pd
from bs4 import BeautifulSoup
# takes the search page of source on sancdb and extracts from each div that contains the genus names and species names and makes a db and adds it to csv called genus_species_fromSANCDB.csv
url = 'https://sancdb.rubi.ru.ac.za/compounds/organisms/#ShowALL'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
names = []

for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    div = soup.find('div', id = letter)
    if div:
        names.extend([a.get_text(strip=True) for a in div.find_all('a', href=True)])

print(names)
entry = []
entries = []
for name in names:
    if ' ' in name:
        genus, species = name.split(' ', 1)
        entry = [genus, species]
        entries.append(entry)

db = pd.DataFrame(entries,columns=['genus', 'species'])
db.to_csv('/home/school/masters/Scripts/SANCDB_Genus_Species_Extract/genus_species_fromSANCDB.csv', index=False)
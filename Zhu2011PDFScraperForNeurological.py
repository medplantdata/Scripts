import pdfplumber
import pandas as pd
import re

pdfPath = '/home/school/masters/Scripts/Zhu2011Supplementary.pdf'

startpg = 13
endpg = 46

table_of_tables = []
header = None  # will store the real column names from the first table

with pdfplumber.open(pdfPath) as pdf:
    for page_num in range(startpg - 1, endpg):
        if page_num >= len(pdf.pages):
            break

        page = pdf.pages[page_num]
        tables = page.extract_tables()

        for t in tables:
            if not t:
                continue

            if header is None:
                # First table we see: take first row as header, rest as data
                header = t[0]
                rows = t[1:]
            else:
                # Later tables: all rows are data, reuse header
                rows = t

            # Build DataFrame with fixed header
            df = pd.DataFrame(rows, columns=header)

            df["source_page"] = page_num + 1

            # Optional: drop duplicate columns and clean index
            df = df.loc[:, ~df.columns.duplicated()].reset_index(drop=True)

            table_of_tables.append(df)

# Concatenate everything
fullDF = pd.concat(table_of_tables, ignore_index=True) if table_of_tables else pd.DataFrame()

print(fullDF.head())


neuroList = ["Neurological disease	","neuro", "Parkinson", "Alzheimer", "epilepsy","degeneration","nootropic",
             "ADHD","stim","depress","narcolepsy","relax","spas","analgesic","pain","arthritic","tussive",
             "epileptic","sclerosis","dementia","insecticide","oxytocic","convulsant","cerebral","emetic",
             "neuroleptic", "narcolepsy", "CNS","Anxiolytic", "depressive","photosensitizergi"]

col = "Therapeutic class or\ntargeted disease"


pattern = "|".join(map(re.escape, neuroList))  # build "neuro|Parkinson|Alzheimer|epilepsy"

mask = (
    fullDF[col]
    .astype(str)
    .str.contains(pattern, case=False, na=False)
)

newDF = fullDF[mask].copy()

fullDF.to_csv('output.csv')
newDF.to_csv('ExtractedNeurologicals.csv')

import pandas as pd

# Import des données individuelles
url_individu = "https://object.data.gouv.fr/ministere-culture/FREQ_MUSEES/ENTREES_ET_CATEGORIES_DE_PUBLIC.csv"

# Séparateur : ;
df_individu = pd.read_csv(url_individu, sep=';')

print(df_individu.head())

# Import des données totales
url = "https://static.data.gouv.fr/resources/frequentation-des-musees-de-france-1/20250827-121955/frequentation-totale-mdf-2001-a-2016-data-def9.xlsx"


all_sheets = pd.read_excel(url, sheet_name=None)

# Pour voir les noms des feuilles disponibles
print(all_sheets.keys())

# Pour accéder à une table précise
df_musees = all_sheets['FREQUENTATION TOTALE']
import pandas as pd
import numpy as np
import requests
import zipfile


class Get_Data:
    def __init__(self, file_path, url):
        self.file_path = file_path
        self.url = url


    def Raw_ZIPPED_Data(self):
        response = requests.get(self.url, stream=True)
        if response.status_code == 200:
            try:
                with open(self.file_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=10000):
                        file.write(chunk)
            except Exception as e:
                print(e)

    def unzip_file(self, unziped_file_path):
        with zipfile.ZipFile(self.file_path) as z:
            z.extractall(unziped_file_path)
            self.unziped_file_path = unziped_file_path

    def create_parquet(self, csv_file_path, encoding, sep, cols, parquet_file_name):
        # 3 = Dépendance
        # 1 = Maison
        # 2 = Appartement
        # 4 = Local industriel. commercial ou assimilé
        try:
            print('ok!!!!')
            df = pd.read_csv(csv_file_path, encoding=encoding, sep=sep, usecols=cols)
            print('ok!!!!')
            df = df[(df['Valeur fonciere'].notna())& (df['Code postal'].notna()) & (df['Code type local'].notna()) & (df['Surface reelle bati'].notna())] 
            print('ok!!!!')

            df['Valeur fonciere'] = (df['Valeur fonciere'].astype(str).str.replace(r'\s+', '', regex=True).str.replace(',', '.', regex=False).astype(float))
            df = self.remove_outlayers(df, 'Valeur fonciere')
            df.to_parquet(parquet_file_name, engine='fastparquet' , compression='snappy')
            print('ok!!!!')
            self.parquet_file_name = parquet_file_name
        except Exception as e:
            print(e)

    def remove_outlayers(self, df, col):
        Q1 = np.percentile(df[col], 25)
        Q3 = np.percentile(df[col], 75)
        df = df[(df[col] >= Q1)&(df[col] <= Q3)]
        return df



        





# --- Reccupération et Transformation des données de valeurs foncières. ---
valeurs_fonciere_pipe = Get_Data(
    file_path = "raw_VF.txt.zip",
    url = "https://static.data.gouv.fr/resources/demandes-de-valeurs-foncieres/20260405-002321/valeursfoncieres-2025.txt.zip"
    )

valeurs_fonciere_pipe.Raw_ZIPPED_Data()
valeurs_fonciere_pipe.unzip_file('raw_VF.txt')


csv_file_name = 'raw_VF.txt/ValeursFoncieres-2025.txt'
parquet_file_name = 'ValeursFoncieres-2025.parquet'
sample_size = 100
encoding = 'latin-1'
sep = '|'
cols = ['Valeur fonciere','Code postal', 'Code type local', 'Surface reelle bati']

valeurs_fonciere_pipe.create_parquet(csv_file_name, encoding, sep, cols, parquet_file_name)




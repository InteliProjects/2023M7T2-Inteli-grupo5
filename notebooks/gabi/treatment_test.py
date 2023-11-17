
import pandas as pd
import numpy as np
from datetime import datetime

df = pd.read_parquet('C:/Users/Inteli/Documents/Facul/M7/Data/06120077/TCRF_ARCHIVE_06120077_20221011185503.parquet')


class Treatment:
    
    def __init__(self, df):
        self.df = df
        # print(self.df.columns)

    def aplica_moda(self):
        colunas_mode = ['bleedPrecoolDiffPress-1b']
        for i in colunas_mode:
                self.df[i + '-mode'] = np.nan
                self.df[i + '-mode'] = self.df[i].mode().iloc[0]
        return self

    def aplica_media(self):
        colunas_mean = ['bleedPrecoolDiffPress-1b', 'bleedPrecoolDiffPress-1a', 'bleedPrsovFbk-1a', 'bleedPrsovClPosStatus-1a', 'bleedFavTmFbk-2b']
        for i in colunas_mean:
                self.df[i + '-mean'] = np.nan
                self.df[i + '-mean'] = self.df[i].mean()
        return self

    def aplica_max(self):
        colunas_max = ['correctedN1Speed-1a', 'bleedPrecoolDiffPress-2a', 'bleedPrsovFbk-2b', 'bleedOutTemp-1b', 'bleedPrecoolDiffPress-1a', 'bleedPrecoolDiffPress-1b']
        for i in colunas_max:
                self.df[i + '-max'] = np.nan
                self.df[i + '-max'] = self.df[i].max()
        return self

    def aplica_min(self):
        colunas_min = ['bleedSwPress-1b',  'bleedSwPress-1a', 'bleedSwPress-2b']
        for i in colunas_min:
                self.df[i + '-min'] = np.nan
                self.df[i + '-min'] = self.df[i].min()
        return self


    def failed(self):

        self.df["answer1"] = np.nan
        self.df["answer2"] = np.nan
        
        self.df["answer1"].iloc[0] = 1.0 if self.df["message0418DAA-1"].max()>0.0 else 0.0
        self.df["answer2"].iloc[0] = 1.0 if self.df["message0422DAA-1"].max()>0.0 else 0.0

        self.df["hasfailed"] = np.nan

        self.df["hasfailed"].iloc[0] = 1 if (self.df["answer1"].iloc[0] == 1.0) | (self.df["answer2"].iloc[0] == 1.0) else 0.0
        self.df.drop(["answer1", "answer2", "message0418DAA-1", "message0422DAA-1"], axis=1, inplace=True)

        return self

    def data(self):
        # Create a new DataFrame with columns of interest
        df = self.df[["timeSeconds-1","timeMinutes-1","timeHours-1","dateMonth-1","dateDay-1","dateYear-1"]].dropna().astype(int)
        date_lambda = lambda x: datetime(x["dateYear-1"], x["dateMonth-1"], x["dateDay-1"], x["timeHours-1"], x["timeMinutes-1"], x["timeSeconds-1"])
        self.df["date"] = df.apply(date_lambda, axis=1)
        
        min_ = self.df["date"].min()
        max_ = self.df["date"].max()
        self.df["start_date"] = min_
        self.df["end_date"] = max_
        self.df["duration"] = max_ - min_
        self.df["duration"] = self.df["duration"].dt.total_seconds()

        print('Duração: %f', self.df["duration"].iloc[0])

        self.df.drop(["timeSeconds-1", "timeMinutes-1", "timeHours-1", "dateMonth-1", "dateDay-1", "dateYear-1"], axis=1, inplace=True)

        return self

    def cumulative(self):
        # Needs to fetch the last cumulative_duration from the database using aircraftSerNum-1
        cumulative_duration = 200
        self.df["cumulative_duration"] = cumulative_duration + self.df["duration"].iloc[0]

        return self

    def rename_columns(self):
        self.df.columns = self.df.columns.str.replace('-', '_')
        return self

    def final(self):
        colunas_selecionadas = ['aircraftSerNum-1', 'start_date', 'end_date', 'duration', 'cumulative_duration', 'bleedSwPress_1b_min', 'bleedSwPress_1a_min', 'bleedSwPress_2b_min', 'correctedN1Speed_1a_max', 'bleedPrecoolDiffPress_2a_max', 'bleedPrecoolDiffPress_1b_mean', 'bleedPrsovFbk_2b_max', 'bleedPrecoolDiffPress_1a_mean', 'bleedPrsovFbk_1a_mean', 'bleedOutTemp_1b_max', 'bleedPrecoolDiffPress_1a_max', 'bleedPrecoolDiffPress_1b_mode', 'bleedPrecoolDiffPress_1b_max', 'bleedPrsovClPosStatus_1a_mean', 'bleedFavTmFbk_2b_mean']
        self.df = self.df[colunas_selecionadas]
        self.df = self.df.iloc[[0]]
        return self.df


df_final = Treatment(df)

df_final = df_final.aplica_moda()
print(type(df_final))  # Verifique o tipo aqui

df_final = df_final.aplica_media()
print(type(df_final))  # Verifique o tipo aqui

df_final = df_final.aplica_max()
print(type(df_final))  # Verifique o tipo aqui

df_final = df_final.aplica_min()
print(type(df_final))  # Verifique o tipo aqui

df_final = df_final.failed()
print(type(df_final))  # Verifique o tipo aqui

df_final = df_final.data()
print(type(df_final))  # Verifique o tipo aqui

df_final = df_final.cumulative()
print(type(df_final))  # Verifique o tipo aqui

df_final = df_final.rename_columns()
print(type(df_final))  # Verifique o tipo aqui

df_final = df_final.final() # Verifique o tipo aqui
print(type(df_final)) 

df_final.to_parquet('C:/Users/Inteli/Documents/Facul/M7/Data/TCRF_ARCHIVE_06120077_20221011185503_final.parquet')





    
"""Pega os dados aggregated_data e adciona a coluna resposta e bota em final_data """
import pandas as pd
import numpy as np
import os

def process_parquet(df):
    df.sort_values(by=["aircraftSerNum-1","start_date"], inplace=True)
    df["hasfailed"] = np.where((df["answer1"] == 1.0) | (df["answer2"] == 1.0), 1.0, 0.0)
    df.drop(["answer1","answer2"], axis=1, inplace=True)
    df["cumulative_duration"] = df.groupby("aircraftSerNum-1")["duration"].cumsum()
    df["cumulative_hasfailed"] = df.groupby("aircraftSerNum-1")["hasfailed"].cumsum()
    df.reset_index(inplace=True)
    df.drop("index", axis=1, inplace=True)
    df[df["hasfailed"]==1].index.sort_values()
    df["soma_betinho"] = df["cumulative_duration"]
    index_list = df[df["hasfailed"]==1].index.sort_values()

    cumulative_numpy = df["cumulative_duration"].to_numpy().copy()

    for v, i in enumerate(index_list):
        break_index = v + 1
        initial_chunck_cursor = 0 if v == 0 else index_list[v-1] + 1
        final_chunck_cursor = i

        cumulative_numpy[initial_chunck_cursor:] = cumulative_numpy[final_chunck_cursor] - cumulative_numpy[initial_chunck_cursor:]


    df["time_to_failure"] = cumulative_numpy

    return df

final_df = pd.DataFrame()

for file in os.listdir("./plane_data"):
    df = pd.read_parquet(f"./plane_data/{file}")
    df = process_parquet(df)

    try:
        final_df = pd.concat([final_df, df], ignore_index=True)
    except:
        final_df = df
    
final_df.to_parquet(f"final_data/min/final_data.parquet")

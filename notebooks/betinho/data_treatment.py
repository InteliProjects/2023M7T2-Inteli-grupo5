""""""

import pandas as pd
import os
import numpy as np


pd.set_option('display.max_columns', 93)
folder_name = os.listdir("./reduced_data2/")



name = "std"
count = 0
error_count = 0
data_list = []
plane_count = {}
size = len(os.listdir(f'./reduced_data2/'))
for file_name in os.listdir(f'./reduced_data2/'):

    try:
       
        count += 1
        print(100*((count)/size))
        if count/size>1.0:
            break
        
        df =  pd.read_parquet(f'./reduced_data2/'+file_name)
     
        try:
            plane_count[df["aircraftSerNum-1"].values[0]] += 1
        except Exception as e:
            plane_count[df["aircraftSerNum-1"].values[0]] = 1
            print(e)
        
        
        lista = list(df.columns)
        
        lista.remove("recording_time")
        line = df[lista].std()
       
       
        year = int(file_name.split("_")[3][:4])
        month = int(file_name.split("_")[3][4:6])
        day = int(file_name.split("_")[3][6:8])
        hour = int(file_name.split("_")[3][8:10])
        minute = int(file_name.split("_")[3][10:12])
        line["date"]  =  pd.Timestamp(year=year, month=month, day=day, hour=hour, minute=minute)
        line["duration"] = df["recording_time"].max()/1000
        
        line["answer1"] = 1.0 if df["message0418DAA-1"].max()>0.0 else 0.0
        line["answer2"] = 1.0 if df["message0422DAA-1"].max()>0.0 else 0.0
        line["aircraftSerNum-1"] = df.loc(df["aircraftSerNum-1"].first_valid_index())["aircraftSerNum-1"].values[0]
        
        line.drop(["timeSeconds-1","timeMinutes-1","timeHours-1","dateMonth-1","dateDay-1","dateYear-1","message0418DAA-1","message0422DAA-1"], inplace=True)
        del df
        # #matrix transpose

        
        line = line.to_frame().T
        data_list.append(line)
            
        
    
    except Exception as e:
        error_count += 1
        print(e)
        continue


df = pd.concat(data_list, ignore_index=True)
df.to_parquet(f'./agregated_data/{name}.parquet')
del df
df = pd.read_parquet(f'./agregated_data/{name}.parquet')
try:
    os.mkdir(f"./plane_data/{name}")
except:
    pass

for value in df["aircraftSerNum-1"].unique():
    df[df["aircraftSerNum-1"] == value].to_parquet(f'./plane_data/{name}/{value}.parquet')
del df

def process_parquet(df):
    
    df.sort_values(by=["aircraftSerNum-1","date"], inplace=True)

    df["hasfailed"] = np.where((df["answer1"] == 1.0) | (df["answer2"] == 1.0), 1.0, 0.0)
    df.drop(["answer1","answer2"], axis=1, inplace=True)
    df["cumulative_duration"] = df.groupby("aircraftSerNum-1")["duration"].cumsum()
    df["cumulative_hasfailed"] = df.groupby("aircraftSerNum-1")["hasfailed"].cumsum()
    df.reset_index(inplace=True)
    df.drop("index", axis=1, inplace=True)
    df[df["hasfailed"]==1].index.sort_values()
    df["soma_betinho"] = df["cumulative_duration"]
    index_list = df[df["hasfailed"]==1].index.sort_values().to_list()
    


    cumulative_numpy = df["cumulative_duration"].to_numpy().copy()

    for v, i in enumerate(index_list):
        if len(index_list) ==0:
            pass
        else: 
            break_index = v + 1
            initial_chunck_cursor = 0 if v == 0 else index_list[v-1] + 1
            final_chunck_cursor = i

            cumulative_numpy[initial_chunck_cursor:] = cumulative_numpy[final_chunck_cursor] - cumulative_numpy[initial_chunck_cursor:]
            cumulative_numpy[final_chunck_cursor:] =  - cumulative_numpy[final_chunck_cursor:]

        df["time_to_failure"] = cumulative_numpy
        
        df.drop("soma_betinho", axis=1, inplace=True)
        df.columns = df.columns.str.replace("-","_")
        df.columns = df.columns.str.lower()

        return df

final_df = pd.DataFrame()
lista = []

for file in os.listdir(f"./plane_data/{name}"):
    df = pd.read_parquet(f"./plane_data/{name}/{file}")
    df = process_parquet(df)

  
    lista.append(df)
    

final_df = pd.concat(lista, ignore_index=True)
    
try:
    os.mkdir(f"./final_data/{name}")
except:
    pass
final_df.to_parquet(f"final_data/{name}/final_data.parquet")
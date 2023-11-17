"""Nesse arquivo reduizimos o tamanho dos dados de raw_data, e tratamos os dados faltantes e salvamos na pasta reduced_data2"""

#import files
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', 93)
pd.set_option('display.max_rows', 93)
folder_name = os.listdir("./raw_data/voos(19-21)/Apache_parquet_files")    
repeated_files = os.listdir("./reduced_data2/")    
col_desc = pd.read_csv('./description.csv', sep=',')
size =len(folder_name)
count =0
for file in folder_name:

    try:
        if not file in repeated_files:
            
            print(100*((count)/size))
            count +=1
        
            df =  pd.read_parquet(f'./raw_data/voos(19-21)/Apache_parquet_files/'+file)
            columns = col_desc[["Mnemonic","Enum_count"]].values
            df =df[list(col_desc["Mnemonic"])]
            df = df.ffill()
            df = df[1:]
            df["aircraftSerNum-1"] = df["aircraftSerNum-1"].mode()[0]
            for name,values in columns:


                if pd.isna(values):
                    df[name] = df[name].astype(np.float32)
                if values == 2:

                    df[name] = df[name].astype(np.byte)

            df.to_parquet(f"./reduced_data2/{file}")
            del df

    except Exception as e:
        print(e)
        print(file)
        continue
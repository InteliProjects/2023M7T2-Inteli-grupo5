import pandas as pd
import pyarrow.parquet as pq
import os

# Caminho para a pasta onde os arquivos Parquet estão armazenados
path = 'C:/Users/gabig/OneDrive/Área de Trabalho/ETL/Final Unidos'

# Lista para armazenar os DataFrames
dataframes = []

# Iterar através de todos os arquivos na pasta especificada
for filename in os.listdir(path):
    if filename.endswith('.parquet'):
        # Caminho completo para o arquivo
        file_path = os.path.join(path, filename)
        
        # Ler o arquivo Parquet
        df = pd.read_parquet(file_path, engine='pyarrow')
        
        # Adicionar o DataFrame à lista
        dataframes.append(df)

# Concatenar todos os DataFrames
final_df = pd.concat(dataframes, ignore_index=True)

# Caminho para o arquivo Parquet final
output_path = 'C:/Users/gabig/OneDrive/Área de Trabalho/ETL/Final/061200_unido.parquet'

# Salvar o DataFrame final como um arquivo Parquet
final_df.to_parquet(output_path, engine='pyarrow')

print(f'Todos os {len(dataframes)} arquivos Parquet foram unidos e salvos em {output_path}')

import os
import pandas as pd
import numpy as np
import pyarrow.parquet as pq
from sklearn.preprocessing import MinMaxScaler

import warnings
warnings.filterwarnings('ignore')

def reduz_dimensao (df):  
    df.fillna(method='ffill', inplace=True)

    df.fillna(method='bfill', inplace=True)

    n = len(df)
    indices = np.linspace(0, n-1, 10).astype(int)
    df = df.iloc[indices]

    return df

def reorganizar_predicao(df):   
    # Função para transformar qualquer valor diferente de 0 em 1
    def transform_value(value):
        if value == 0 or pd.isna(value):
            return 0
        return 1

    # Aplicando a função às colunas 'A' e 'B'
    df[['message0418DAA-1', 'message0422DAA-1']] = df[['message0418DAA-1', 'message0422DAA-1']].applymap(transform_value)

    df['bleed_fail'] = (df[ 'message0418DAA-1'] | df['message0422DAA-1']).astype(int)

    if df['bleed_fail'].any() == 1:
        df['bleed_fail'] = 1

    df.drop(['message0418DAA-1', 'message0422DAA-1'], axis=1, inplace=True)

    return df

def data(df):
    # Criar um novo DataFrame com as colunas de interesse
    df_hora = df[['dateDay-1', 'dateMonth-1', 'dateYear-1', 'timeHours-1', 'timeMinutes-1', 'timeSeconds-1']].copy()
    # Acessar os valores pelo índice
    # Remover as linhas onde todas as colunas de hora, minuto e segundo são NaN
    df_hora.dropna(how='all', inplace=True)

    ano = int(df_hora["dateYear-1"].iloc[0])
    mes = int(df_hora["dateMonth-1"].iloc[0])
    dia = int(df_hora["dateDay-1"].iloc[0])

    ano_f = int(df_hora["dateYear-1"].iloc[-1])
    dia_f = int(df_hora["dateDay-1"].iloc[-1])
    mes_f = int(df_hora["dateMonth-1"].iloc[-1])

    # Combinar os valores para criar uma string representando a data
    data_str_i = str(ano) + '-' + str(mes).zfill(2) + '-' + str(dia).zfill(2) + ' ' + str(int(df_hora['timeHours-1'].iloc[0])) + ':' + str(int(df_hora['timeMinutes-1'].iloc[0])) + ':' + str(int(df_hora['timeSeconds-1'].iloc[0]))
    data_str_f = str(ano_f) + '-' + str(mes_f).zfill(2) + '-' + str(dia_f).zfill(2) + ' ' + str(int(df_hora['timeHours-1'].iloc[-1])) + ':' + str(int(df_hora['timeMinutes-1'].iloc[-1])) + ':' + str(int(df_hora['timeSeconds-1'].iloc[-1]))
    
    # Converta a string 'data_str' para o tipo de data
    data_i = pd.to_datetime(data_str_i)
    data_f = pd.to_datetime(data_str_f)

    # Criar uma coluna 'data' e preencher com o valor de 'data'
    df['data_inicio'] = data_i
    df['data_final'] = data_f

    #  Calcula o tempo de voo
    flight_time = abs((data_f - data_i).total_seconds()) / 3600  # tempo em horas
    flight_time_rounded = round(flight_time, 2)  # arredonda para duas casas decimais

    df['flight_time'] = flight_time_rounded

    df['flight_time'] = df['flight_time'].round(2) 

    return df

def selecao_colunas(df):
    colunas_importantes = [
    'recording_time', 'aircraftSerNum-1',
    'correctedCoreSpeed-1a', 'bleedMonPress-1a', 'bleedMonPress-1b', 'bleedMonPress-2a', 'bleedMonPress-2b',
    'bleedPrecoolDiffPress-1a', 'bleedPrecoolDiffPress-1b', 'bleedPrecoolDiffPress-2a', 'bleedPrecoolDiffPress-2b', 'bleedPrsovFbk-1b', 
    'bleedOutTemp-1a', 'bleedOutTemp-1b', 'bleedOutTemp-2a', 'bleedOutTemp-2b',
    'data_inicio', 'data_final', 'bleed_fail', 'flight_time'
]

    df = df[colunas_importantes]

    return df


def normalizar(df):

    # Identificar colunas categóricas com base no número de valores únicos
    colunas_categoricas = [col for col in df.columns if df[col].nunique() < 2]

    # Identificar colunas numéricas (excluindo as colunas categóricas transformadas)
    colunas_numericas = [col for col in df.columns if col not in colunas_categoricas]

    # Aplicar MinMaxScaler para dimensionar as colunas numéricas
    scaler = MinMaxScaler()
    df[colunas_numericas] = scaler.fit_transform(df[colunas_numericas])

    df[colunas_numericas] = df[colunas_numericas].astype('float32')
    df[colunas_numericas] = df[colunas_numericas].round(4)

    return df

def cumulativo(df):
    df['cumulative_time'] = df['flight_time'].where(df['recording_time'] == 0, 0).cumsum().round(2)

    df['cumulative_time'] = df['cumulative_time'].round(2) 

    return df

def time_to_failure(df):

    fail_indices = df[(df['bleed_fail'] == 1) & (df['recording_time'] == 0)].index
    

    if len(fail_indices) == 0:
        print("Não falhou nenhuma vez")
        return df
    else:
        end_index = fail_indices[-1] + 9 # 9
        df = df.loc[0:end_index]

    cumulative_times = df[(df['bleed_fail'] == 1) & (df['recording_time'] == 0)]['cumulative_time'].values
    indices = df[(df['recording_time'] == 0)].index
    
    cumulative_times_right = [cumulative_times[0]]

    # print(indices)

    for i in range(1, len(cumulative_times)):  # começa do segundo item (índice 1)
        aux = 0
        aux = cumulative_times[i - 1]
        cumulative_times_right.append(cumulative_times[i] - aux)

    df['time_to_failure'] = np.nan

    k = 0
    n = len(cumulative_times_right)

    for i in indices:
        if i not in fail_indices:
            if k < n:
                df.at[i, 'time_to_failure'] = cumulative_times_right[k] - df.at[i, 'flight_time']
                cumulative_times_right[k] -= df.at[i, 'flight_time']
        else:
            # print("Falhou")
            df.at[i, 'time_to_failure'] = 0
            k += 1

    df = df.ffill()

    return df

# Função de tratamento de dados (substitua por suas próprias funções)
def tratar_dados(df):
    
    df = reorganizar_predicao(df)
    df = reduz_dimensao(df) 
    df = data(df)
    df = selecao_colunas(df)
    df = normalizar(df)
    
    # print('Dados tratados com sucesso!')
    return df

aeronaves = [91, 92]

# aeronaves = [18, 20, 21, 25, 28, 32, 33, 34, 35, 77,79, 81, 83, 88, 89, 91, 92]

# Diretório onde os arquivos Parquet estão armazenados
for nave in aeronaves:
    diretorio = f'C:/Users/gabig/OneDrive/Área de Trabalho/ETL/Datasets/061200{nave}' 

    # Lista para armazenar DataFrames após o tratamento
    lista_dfs = []

    # Iterar através de cada arquivo no diretório
    for arquivo in os.listdir(diretorio):
        if arquivo.endswith('.parquet'):
            caminho_arquivo = os.path.join(diretorio, arquivo)

            # print(f'Lendo {caminho_arquivo}...')
            
            # Ler o arquivo Parquet
            df = pd.read_parquet(caminho_arquivo, engine='pyarrow')
            
            # Aplicar a função de tratamento de dados
            df_tratado = tratar_dados(df)
            
            # Adicionar o DataFrame tratado à lista
            lista_dfs.append(df_tratado)

    # Concatenar todos os DataFrames tratados
    df_final = pd.concat(lista_dfs, ignore_index=True)
   
    df_final.sort_values(by='data_inicio', inplace=True)

    df_final = cumulativo(df_final)

    df_final = time_to_failure(df_final)

    df_final = df_final.round(4)

    # Caminho para salvar o arquivo Parquet unido
    caminho_final = f'C:/Users/gabig/OneDrive/Área de Trabalho/ETL/Final Unidos/061200{nave}_unido.parquet'

    # Salvar o DataFrame final como um arquivo Parquet
    df_final.to_parquet(caminho_final, engine='pyarrow')

    print(f'Arquivo final salvo em {caminho_final}')

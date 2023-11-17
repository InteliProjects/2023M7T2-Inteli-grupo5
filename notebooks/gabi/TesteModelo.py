from joblib import load
import pandas as pd

colunas_ignoradas = ['data_inicio', 'data_final', 'bleedFail']

# 1. Carregar o modelo treinado
modelo_carregado = load('modelo_random_forest.joblib')

# 2. Preparar os novos dados (exemplo com um DataFrame Pandas)
novo_dados = pd.read_parquet('C:/Users/gabig/OneDrive/Área de Trabalho/ETL/Final Unidos/06120081_unido.parquet')

# Certifique-se de que os novos dados são processados da mesma forma que os dados de treinamento
# Isso pode incluir a remoção de colunas ignoradas, preenchimento de valores ausentes, etc.
novo_dados = novo_dados.drop(columns=colunas_ignoradas)

# 3. Fazer previsões
previsoes = modelo_carregado.predict(novo_dados)

# 4. Interpretar ou salvar os resultados
# Você pode adicionar as previsões ao DataFrame e salvá-lo, por exemplo
novo_dados['previsoes'] = previsoes
novo_dados.to_parquet('resultados.parquet', index=False)
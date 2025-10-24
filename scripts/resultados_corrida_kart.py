import pandas as pd

# Carregar o arquivo csv contendo os dados da corrida de kart
df_kart_logs = pd.read_csv("data\log_kart.csv", delimiter=";") # Utilizar ; como delimitador

print(df_kart_logs.head())
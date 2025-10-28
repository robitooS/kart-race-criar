import pandas as pd
import sys

# Carregar o arquivo csv contendo os dados da corrida de kart
try:
    df_race_kart_logs = pd.read_csv("data/log_kart.csv", delimiter=";")
except Exception as e:
    print(f"Não foi possível abrir o arquivo de log: {e}")
    sys.exit()

print(f"\n************** KART LOG INICIAL **************\n{df_race_kart_logs}\n")

# === Instanciando df resultante com as respectivas colunas ===
df_results_columns = [
    "Posição de chegada",
    "Código do piloto",
    "Nome do piloto",
    "Quantidade de voltas completadas",
    "Tempo total de prova"
]
df_results_race_kart = pd.DataFrame(columns=df_results_columns)

# === 1. Extrair código e nome do piloto ===
cod_pilotos = {}
for piloto in df_race_kart_logs["Piloto"]:
    partes = piloto.split("-")
    cod = partes[0].strip()
    nome = partes[-1].strip()
    cod_pilotos[cod] = nome

# === Criar coluna auxiliar no DF original com apenas o código do piloto ===
df_race_kart_logs["Cod_Piloto"] = df_race_kart_logs["Piloto"].apply(
    lambda p: p.split("-")[0].strip()
)

# === Coluna auxiliar com o nome do piloto ===
df_race_kart_logs["Nom_Piloto"] = df_race_kart_logs["Piloto"].apply(
    lambda p: p.split("-")[-1].strip()
)

# === Inserir no df resultante o código e nome do piloto ===
df_results_race_kart["Código do piloto"] = list(cod_pilotos.keys())
df_results_race_kart["Nome do piloto"] = list(cod_pilotos.values())

# print(f"\n************** DF RESULTANTE APÓS NOME E CÓDIGO DO PILOTO **************\n{df_results_race_kart}\n")
print(f"\n************** DF INICIAL **************\n{df_race_kart_logs}\n")

# === 2. Contar voltas por piloto ===
qtd_voltas_series = df_race_kart_logs["Piloto"].value_counts()
qtd_voltas_dict = {
    piloto_str.split("-")[0].strip(): qtd
    for piloto_str, qtd in qtd_voltas_series.items()
}

# === Inserir quantidade de voltas no DF de resultados ===
df_results_race_kart["Quantidade de voltas completadas"] = (
    df_results_race_kart["Código do piloto"].map(qtd_voltas_dict)
)

# print(f"\n************** DF RESULTANTE APÓS QTD DE VOLTAS **************\n{df_results_race_kart}\n")

# === 3. Tempo total de prova ===
df_race_kart_logs['Tempo_Volta_td'] = pd.to_timedelta(
    '00:' + df_race_kart_logs['Tempo_Volta']
) # Transformar em timedelta p calcular as durações, vem como object no df

# === Retorna uma serie com o valor somado por cada cod. de piloto ===
tempo_por_piloto_series = df_race_kart_logs.groupby("Cod_Piloto")["Tempo_Volta_td"].sum()
df_results_race_kart["Tempo total de prova"] = df_results_race_kart["Código do piloto"].map(tempo_por_piloto_series)
# print(f"\n************** DF RESULTANTE APÓS TEMPO TOTAL DE PROVA **************\n{df_results_race_kart}\n")

# === Formatar a coluna para tornar mais legível ===
df_results_race_kart["Tempo total de prova"] = df_results_race_kart["Tempo total de prova"].astype(str).apply(lambda x: x.split(" ")[2])

# print(f"\n************** DF RESULTANTE APÓS FORMATAÇÃO DA DURAÇÃO **************\n{df_results_race_kart}\n")

# === 3. Posição de chegada dos pilotos ===
df_results_race_kart = df_results_race_kart.sort_values(by=["Quantidade de voltas completadas", "Tempo total de prova"], ascending=[False, True]).reset_index(drop=True)

# === Como resetamos o index, a posição vai ser o index + 1 ===
df_results_race_kart["Posição de chegada"] = df_results_race_kart.index + 1

print(f"\n************** DF FINAL **************\n{df_results_race_kart}\n")

try:
    df_results_race_kart.to_excel("data/results_race_kart.xlsx")
except Exception as e:
    print(f"Não foi possível salvar o dataframe resultante: {e}")
    sys.exit()

# === BÔNUS ===
print("""
     **********************************************************************
                                SEÇÃO DE BONUS
     **********************************************************************
      """)

# === Melhor volta de cada piloto ===
idx_melhores_voltas = df_race_kart_logs.groupby("Cod_Piloto")["Tempo_Volta_td"].idxmin()

df_melhores_voltas = df_race_kart_logs.loc[idx_melhores_voltas, ["Cod_Piloto", "Tempo_Volta_td", "N_Volta", "Nom_Piloto"]]
df_melhores_voltas["Tempo_Volta_td"] = df_melhores_voltas["Tempo_Volta_td"].astype(str).apply(lambda x: x.split(" ")[2])
df_melhores_voltas = df_melhores_voltas.reset_index(drop=True)

try:
    df_melhores_voltas.to_excel("data/melhores_voltas_por_piloto.xlsx")
except Exception as e:
    print(f"Não foi possível salvar o dataframe resultante: {e}")
    sys.exit()

print(f"\n************** DF COM AS MELHORES VOLTAS DA CORRIDA POR PILOTO **************\n{df_melhores_voltas}\n")

# === Melhor volta da corrida ===
idx_melhor_volta_corrida = df_race_kart_logs["Tempo_Volta_td"].idxmin()
df_melhor_volta_corrida = df_race_kart_logs.loc[[idx_melhor_volta_corrida], ["Cod_Piloto", "Nom_Piloto", "Tempo_Volta", "N_Volta"]]
df_melhor_volta_corrida = df_melhor_volta_corrida.reset_index(drop=True)

try:
    df_melhor_volta_corrida.to_excel("data/melhor_volta_corrida.xlsx")
except Exception as e:
    print(f"Não foi possível salvar o dataframe resultante: {e}")
    sys.exit()

print(f"\n************** MELHOR VOLTA DA CORRIDA NO GERAL **************\n{df_melhor_volta_corrida}\n")

# === Velocidade média por piloto ===
df_race_kart_logs["Velocidade_Media_da_Volta"] = (df_race_kart_logs["Velocidade_Media_da_Volta"].str.replace(",", ".", regex=False).astype(float))
velocidades_medias = df_race_kart_logs.groupby("Cod_Piloto")["Velocidade_Media_da_Volta"].mean().round(2)
df_velocidades_medias = velocidades_medias.reset_index()

df_velocidades_medias["Piloto"] = df_velocidades_medias["Cod_Piloto"].map(cod_pilotos)
df_velocidades_medias.rename(columns={"Velocidade_Media_da_Volta": "Velocidade média (km/h)", "Cod_Piloto": "Código do Piloto"}, inplace=True)

try:
    df_velocidades_medias.to_excel("data/velocidades_medias_por_piloto.xlsx")
except Exception as e:
    print(f"Não foi possível salvar o dataframe resultante: {e}")
    sys.exit()

print(f"\n************** DF COM AS VELOCIDADES MÉDIAS DOS PILOTOS **************\n{df_velocidades_medias}\n")

# === Tempo de diferença para o vencedor === 
df_results_race_kart["Tempo_total_td"] = pd.to_timedelta(df_results_race_kart["Tempo total de prova"])
tempo_vencedor = df_results_race_kart.loc[0, "Tempo_total_td"]

df_results_race_kart["Diferença para o vencedor"] = df_results_race_kart["Tempo_total_td"] - tempo_vencedor
df_results_race_kart["Diferença para o vencedor"] = df_results_race_kart["Diferença para o vencedor"].astype(str).apply(lambda d: d.split(" ")[2])

try:
    df_velocidades_medias.to_excel("data/diff_tempo_para_o_vencedor.xlsx")
except Exception as e:
    print(f"Não foi possível salvar o dataframe resultante: {e}")
    sys.exit()

print(f"\n************** DF COM AS DIFERENÇAS DE TEMPO EM RELAÇÃO AO VENCEDOR **************\n{df_velocidades_medias}\n")

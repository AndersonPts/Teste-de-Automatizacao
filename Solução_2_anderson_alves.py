#==========================================================================================================================
#   Solução 2 - Anderson Alves.py
#   Desenvolvedor: Anderson Alves
#   Data: 24/05/2024
#   Teste para comexport
#   Script em Python que recebe um arquivo csv e para cada linha desse arquivo, pesquise o status de CE e BL no endpoint do agricultura.gov
#==========================================================================================================================

import csv
import requests
import pandas as pd
import datetime
import pytz

br_timezone = pytz.timezone("America/Sao_Paulo")
br_datetime = datetime.datetime.now(br_timezone)
hora_Data = br_datetime.strftime("%d/%m/%Y %H:%M")


# Arquivos para processamento. Para teste, substituir os caminhos abaixo
arq_entrada = '/content/Solução 2 - Entrada.csv'
arq_saida = '/content/Solução 2 - Saída.csv'

# Função para fazer a requisição a API
def consultarAPI(cod_conhecimento, num_conhecimento):
    url = f"https://api-shiva.rhmg.agricultura.gov.br/api/publico/madeira/datem/status?codConhecimento={num_conhecimento}&numConhecimento={cod_conhecimento}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        resposta_api = response.json()
        resultado = resposta_api['data']
        return {
            'codConhecimento': resultado['codConhecimento'],
            'numConhecimento': resultado['numConhecimento'],
            'datemTipoDescricao': resultado['datemTipo']['descricao'],
            'viaTransporte': resultado['viaTransporte'],
            'canalParametrizacaoDescricao': resultado['canalParametrizacao']['descricao'],
            'datemSituacaoDescricao': resultado['datemSituacao']['descricao'],
            'datemParecerDescricao': resultado['datemParecer']['descricao'],
            'dataConsulta': hora_Data
        }
    except requests.RequestException as e:
      # Caso tenha alguma falha na requisição
        return {"Falha": str(e)}

# Função para processar o arquivo CSV e chamar a função consultarAPI
def gerar_saida_csv(arq_entrada, arq_saida):
    # Ler o arquivo CSV
    data = pd.read_csv(arq_entrada, sep=';')

    # Verificar se as colunas existem
    if 'AWB BL' not in data.columns or 'CE Mercante' not in data.columns:
        raise ValueError("O arquivo CSV deve conter as colunas 'AWB BL' e 'CE Mercante'")

    resultado_final = []

    # Iterar sobre cada linha do CSV
    for index, row in data.iterrows():
        cod_conhecimento = row['AWB BL']
        num_conhecimento = row['CE Mercante']
        result_api = consultarAPI(cod_conhecimento, num_conhecimento)
        #print(result_api)
        resultado_final.append(result_api)

    # Salvar os resultados em um novo arquivo CSV
    results_df = pd.DataFrame(resultado_final)
    results_df.to_csv(arq_saida, index=False, header=False)

# Buscar arquivos e realizar consulta na API
gerar_saida_csv(arq_entrada, arq_saida)
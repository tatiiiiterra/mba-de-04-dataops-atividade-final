import logging
import os
import uuid
from datetime import datetime

import requests
import pandas as pd
from dotenv import load_dotenv

from config import configs
import utils

config_file = configs
load_dotenv()
logging.basicConfig(level=logging.INFO)

def ingestion():
    """
    Função de ingestão dos dados
    Outputs: Salva base raw em local específico e retorna o nome do arquivo
    """

    logging.info("Iniciando a ingestão")
    api_url = os.getenv('URL')

    try:
        logging.info("Iniciando a coleta dos dados no endpoint %s", api_url)
        response = requests.get(api_url, timeout=10).json()
        data = response['results']
        df = pd.json_normalize(data)
        df['load_date'] = datetime.now().strftime("%H:%M:%S")
        file = f"{config_file['raw_path']}{str(uuid.uuid4())}.csv"
        logging.info("Dados coletados, salvando no arquivo raw %s", file)
        df.to_csv(file, sep=";", index=False)
        return file
    except Exception as exception_error:
        logging.error("Erro na ingestão: %s",exception_error)
        utils.error_handler(exception_error, 'read_api')
        return None


def preparation(file):
    """
    Função de preparação dos dados: renomeia, tipagem, normaliza strings
    Arguments: file -> nome do arquivo raw
    Outputs: Salva base limpa em local específico
    """
    try:
        logging.info("Iniciando a preparação")
        logging.info("Lendo arquivo %s", file)
        df = pd.read_csv(file, sep=";")
        clean_data = utils.Sanitation(df, config_file)
        clean_data.select_rename()
        logging.info("Dados renomeados e selecionados")
        clean_data.typing()
        logging.info("Dados tipados")
        clean_data.save_work()
        logging.info("Dados salvos")
    except Exception as exception_error:
        logging.error("Erro na preparação: %s", exception_error)
        utils.error_handler(exception_error, 'preparation')

if __name__ == '__main__':
    file_name = ingestion()
    preparation(file_name)

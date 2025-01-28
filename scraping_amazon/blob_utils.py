from azure.storage.blob import BlobClient
from os import getenv
from dotenv import load_dotenv
import logging
from datetime import date

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
def upload_file_to_blob(local_file_path):

    try:
        connection_string = getenv("AZURE_BLOB_CONNECTION_STRING")
        container_name = getenv("AZURE_BLOB_CONTAINER_NAME")
        blob_name = getenv("AZURE_BLOB_NAME") + "_" + str(date.today()).replace("-", "") + ".json"

        if not all([connection_string, container_name, blob_name, local_file_path]):
            raise ValueError("Uma ou mais variáveis de ambiente necessárias não foram configuradas.")

        blob = BlobClient.from_connection_string(
            conn_str=connection_string,
            container_name=container_name,
            blob_name=blob_name
        )

        with open(local_file_path, "rb") as data:
            blob.upload_blob(data, overwrite=True)

        logging.info(
            f"Arquivo '{local_file_path}' enviado com sucesso para o blob '{blob_name}' no container '{container_name}'.")

    except Exception as e:
        logging.error(f"Erro ao fazer upload do arquivo: {e}")


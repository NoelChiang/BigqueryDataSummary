from google.cloud import bigquery
import os

class SqlCommander:
    def __init__(self):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './<# Google Service Account Auth#>.json'
    
    def send(self, command):
        client = bigquery.Client()
        query = client.query(command)
        return query.result()    
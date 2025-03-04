import psycopg2
import boto3
import os
from datetime import datetime

# Získať údaje zo secrets
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')

# Pripojenie k databáze
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
cursor = conn.cursor()

# Vytvorenie zálohy databázy
backup_filename = f"backup_{datetime.now().strftime('%Y%m%d%H%M%S')}.sql"
with open(backup_filename, 'w') as f:
    cursor.copy_expert(f"COPY {DB_NAME} TO STDOUT WITH CSV HEADER", f)

# Uloženie zálohy na MEGA (tu je len ukážka pre použitie s boto3 alebo iným nástrojom na ukladanie)
# Budeš musieť implementovať kód na pripojenie a upload na MEGA

# Uzatvorenie pripojenia
cursor.close()
conn.close()

print(f"Backup completed and saved as {backup_filename}")

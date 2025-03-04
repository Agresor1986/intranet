#!/bin/bash

# Premenné
DB_NAME="$DB_NAME"
DB_USER="$DB_USER"
DB_PASSWORD="$DB_PASSWORD"
DB_HOST="dpg-cv1glnl2ng1s738d0h4g-a"  # Použite váš hostname
BACKUP_DIR="/tmp"
FILENAME="backup_$(date +\%Y-\%m-\%d_\%H-\%M-\%S).sql"

# Kontrola, či sú všetky premenné nastavené
if [ -z "$DB_NAME" ] || [ -z "$DB_USER" ] || [ -z "$DB_PASSWORD" ] || [ -z "$DB_HOST" ]; then
  echo "Chýbajúce premenné! Skontrolujte GitHub Secrets."
  exit 1
fi

# Inštalácia Rclone, ak chýba
if ! command -v rclone &> /dev/null
then
    echo "Inštalácia Rclone..."
    curl https://rclone.org/install.sh | sudo bash
fi

# Vytvorenie adresára pre konfiguráciu Rclone, ak neexistuje
mkdir -p ~/.config/rclone

# Konfigurácia Rclone
MEGA_PASS_ENCODED=$(echo -n "$MEGA_PASS" | base64)  # Zakódovanie hesla
echo "[mega_backup]
type = mega
user = $MEGA_USER
pass = $MEGA_PASS_ENCODED" > ~/.config/rclone/rclone.conf

# Kontrola pripojenia k databáze
echo "Kontrola pripojenia k databáze..."
export PGPASSWORD="$DB_PASSWORD"
if ! psql "postgresql://$DB_USER@$DB_HOST/$DB_NAME" -c "\q"; then
  echo "Chyba pri pripájaní k databáze!"
  exit 1
fi

# Export databázy
echo "Export databázy..."
pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME > $BACKUP_DIR/$FILENAME

# Kontrola, či sa export podaril
if [ $? -eq 0 ]; then
    echo "Databáza bola úspešne exportovaná do $BACKUP_DIR/$FILENAME"
else
    echo "Chyba pri exporte databázy!"
    exit 1
fi

# Odoslanie zálohy na MEGA
echo "Odosielanie zálohy na MEGA..."
rclone copy $BACKUP_DIR/$FILENAME mega_backup:/backups/

# Kontrola, či sa odoslanie podarilo
if [ $? -eq 0 ]; then
    echo "Záloha bola úspešne odoslaná na MEGA."
else
    echo "Chyba pri odosielaní zálohy na MEGA!"
    exit 1
fi

# Vymazanie starých záloh (ponechá len posledných 7 dní)
echo "Vymazávanie starých záloh..."
rclone delete mega_backup:/backups --min-age 7d

# Kontrola, či sa vymazanie podarilo
if [ $? -eq 0 ]; then
    echo "Staré zálohy boli úspešne vymazané."
else
    echo "Chyba pri vymazávaní starých záloh!"
    exit 1
fi

echo "Backup hotový: $FILENAME"

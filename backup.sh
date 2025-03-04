#!/bin/bash

# Premenné zo Secrets
DB_NAME="intranet-databaza"
DB_USER="intranet_databaza_r0nq_user"
DB_HOST="dpg-cv1glnl2ng1s738d0h4g-a"  # Použite váš hostname
DB_PASSWORD="$DB_PASSWORD"  # Heslo z GitHub Secrets
BACKUP_DIR="/tmp"
FILENAME="backup_$(date +\%Y-\%m-\%d_\%H-\%M-\%S).sql"

# Inštalácia Rclone, ak chýba
if ! command -v rclone &> /dev/null
then
    curl https://rclone.org/install.sh | sudo bash
fi

# Vytvorenie adresára pre konfiguráciu Rclone
mkdir -p ~/.config/rclone

# Konfigurácia Rclone (stačí raz, potom ju uložíš ako secret v GitHub Actions)
echo "[mega_backup]
type = mega
user = $MEGA_USER
pass = $MEGA_PASS" > ~/.config/rclone/rclone.conf

# Export databázy
echo "Export databázy..."
export PGPASSWORD="$DB_PASSWORD"  # Nastavenie hesla pre pg_dump
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

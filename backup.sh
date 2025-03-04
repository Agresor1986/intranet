#!/bin/bash

# Premenné
DB_NAME="intranet_databaza_r0nq"
DB_USER="intranet_databaza_r0nq_user"
DB_PASSWORD="f5QYUoydyFf1lFaiIH8oMwGsQTVOmDMa"
DB_HOST="dpg-cv1glnl2ng1s738d0h4g-a.frankfurt-postgres.render.com"
BACKUP_DIR="/tmp"
FILENAME="backup_$(date +\%Y-\%m-\%d_\%H-\%M-\%S).sql"
# Inštalácia Rclone, ak chýba
if ! command -v rclone &> /dev/null
then
    curl https://rclone.org/install.sh | sudo bash
fi

# Konfigurácia Rclone (stačí raz, potom ju uložíš ako secret v GitHub Actions)
echo "[mega_backup]
type = mega
user = $MEGA_USER
pass = $MEGA_PASS" > ~/.config/rclone/rclone.conf

# Export databázy
pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME > $BACKUP_DIR/$FILENAME

# Odoslanie na MEGA
rclone copy $BACKUP_DIR/$FILENAME mega_backup:/backups/

# Vymazanie starých záloh (ponechá len posledných 7)
rclone delete mega_backup:/backups --min-age 7d

echo "Backup hotový: $FILENAME"  

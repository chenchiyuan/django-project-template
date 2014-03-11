#!/bin/bash

DBBackupDir=/home/chiyuan/projects/hertz/data/db_backup
DBDailyBackupFile="$DBBackupDir/db.$(date +%Y%m%d).sql"

mysqldump --password=900303 --user=root hertz > $DBDailyBackupFile
tar czvf db.$(date +%Y%m%d).sql.tar.gz db.$(date +%Y%m%d).sql
rm db.$(date +%Y%m%d).sql

echo "DB daily backup done!"
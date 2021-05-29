#!/bin/bash
# MongoDB Database Backup Script 

CURRENT_DATE=`date +"%d%b%Y"`

 
BACKUP_PATH='mongodb'
MONGO_HOST='localhost'
MONGO_PORT='27017'
 
DATABASE_NAME='YWCA_reports'
COLLECTION='reports'
 

# make new file record
mkdir -p ${BACKUP_PATH}/${TODAY}

#export as Json 
mongodump --db ${DATABASE_NAME} --collection ${COLLECTION} --out ${BACKUP_PATH}/${CURRENT_DATE}


# Only keep 3 days of back up record

## Number of days to keep local backup copy
BACKUP_RETAIN_DAYS=3 

 
RMDATE=`date +"%d%b%Y" --date="${BACKUP_RETAIN_DAYS} days ago"`
 
if [ ! -z ${BACKUP_PATH} ]; then
      cd ${BACKUP_PATH}
      # if RMDATE exists then remove
      if [ ! -z ${RMDATE} ] && [ -d ${RMDATE} ]; then
            rm -rf ${RMDATE}
      fi
fi
 
######################### End of script ##############################
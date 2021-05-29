#!/bin/bash
# MongoDB Database Restore Script 

 
BACKUP_PATH='mongodb'
MONGO_HOST='localhost'
MONGO_PORT='27017'
 
DATABASE_NAME='YWCA_reports'
COLLECTION='reports'

#restore to local instance at the same database
#There are three copies will be keeping on the local back up file  
#Default set to restore the most recent copy which is yesterday.
#There should be three copies, so the maximum days can be set to RESTORE_DAYS is 3.
RESTORE_DAYS=-1
RSDATE=`date +"%d%b%Y" --date="${RESTORE_DAYS} days ago"`

mongorestore --nsInclude=${DATABASE_NAME}.${COLLECTION} ${BACKUP_PATH}/${RSDATE}
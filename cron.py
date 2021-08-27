from apscheduler.schedulers.blocking import BlockingScheduler
import os, time

import blueprints.cronBackup.functions as func


sched = BlockingScheduler()
@sched.scheduled_job('interval', days=1, misfire_grace_time=1000)
def backup():
    '''
    DAILY BACKUP
    ============

    "BACKUP_DAILY_COUNT" set the number of daily backup that should be kept. By default BACKUP_DAILY_COUNT=7
    To change the default count, integer or integer 'like' shall be entered in environment.
    If no limits shall be entered (unlimited backup creation), then one should use the following:
       BACKUP_DAILY_COUNT: "UNLIMITED"


    WEEKLY BACKUP
    ============

    "BACKUP_WEEKLY_COUNT" sets the number of weekly backup that should be kept. By default BACKUP_WEEKLY_COUNT=4
    To change the default count, integer or integer 'like' shall be entered in environment.
    If no limits shall be entered (unlimited backup creation), then one should use the following:
       BACKUP_WEEKLY_COUNT: "UNLIMITED"

    "BACKUP_WEEKLY_DAY" sets the week day you wish the weekly backup to be performed.
    To change the default count, integer or integer 'like' shall be entered in environment:
        0: Monday
        1: Tuesday
        2: Wednesday
        3: Thursday
        4: Friday
        5: Saturday
        6: Sunday

    By default BACKUP_WEEKLY_DAY = 5


    MONTHLY BACKUP
    ============

    "BACKUP_MONTHLY_COUNT" sets the number of monthly backup that should be kept. By default BACKUP_MONTHLY_COUNT=12
    To change the default count, integer or integer 'like' shall be entered in environment.
    If no limits shall be entered (unlimited backup creation), then one should use the following:
       BACKUP_MONTHLY_COUNT: "UNLIMITED"

    "BACKUP_MONTHLY_DAY" sets the day you wish the monthly backup to be performed.
    To change the default count, integer or integer 'like' shall be entered in environment:
        1: First of the month
        2: Second of the month ...

    By default BACKUP_MONTHLY_DAY = 1


    YEARLY BACKUP
    ============

    "BACKUP_YEARLY_COUNT" sets the number of annual backup that should be kept. By default BACKUP_YEARLY_COUNT="UNLIMITED"
    To change the default count, integer or integer 'like' shall be entered in environment.
    If no limits shall be entered (unlimited backup creation), then one should use the following:
       BACKUP_DAILY_COUNT: "UNLIMITED"

    "BACKUP_YEARLY_DAY" sets the day you wish the annual backup to be performed.
    To change the default count, integer or integer 'like' shall be entered in environment:
        1: First of the month
        2: Second of the month ...

    "BACKUP_YEARLY_MONTH" sets the month you wish the annual backup to be performed.
    To change the default count, integer or integer 'like' shall be entered in environment:
        1: January
        2: February ...

    By default BACKUP_YEARLY_DAY = 31
    By default BACKUP_YEARLY_MONTH = 12

    
    =============================================================

    Note: Backups are saved as tar.gz files. In order to extract them, keeping directory trees, the following can be used using python3:

    > import tarfile, os
    > from cryptography.fernet import Fernet
    >
    > # extract file
    > date_to_extract = '2021-06-18'  # to be changed if other backup to extract
    > DIRECTION_BACKUP_DAILY = "C:/Users/renau/Desktop/mongo/backuptest/backup/data/DAILY" # to be changed if other backup to extract
    > tar = tarfile.open(os.path.join(DIRECTION_BACKUP_DAILY, date_to_extract, "w:gz")
    > tar.add(DIRECTION, arcname=BACKUPNAME)
    > tar.close()
    >
    > # decrypt file
    > with open(os.path.join(DIRECTION, BACKUPNAME), "rb") as file:
    >     encrypted_data = file.read()
    > cipher_suite = Fernet(str.encode(KEY))
    > decrypted_data = cipher_suite.decrypt(encrypted_data)
    > with open(os.path.join(DIRECTION, BACKUPNAME), "wb") as file:
    >     file.write(decrypted_data)
    '''

    backup_sources = [s.strip() for s in os.environ.get('SOURCES').split(",")]
    for bs in backup_sources:
      
      # Create backup repositories
      directions = func.create_backup_directions(bs)
    
      bs = "/" + bs

      time.sleep(1)
      
      # Daily backup
      func.create_daily_backup(bs, directions['DAILY'])
      
      # Weekly backup
      func.create_weekly_backup(bs, directions['WEEKLY'])
      
      # Monthly backup
      func.create_monthly_backup(bs, directions['MONTHLY'])
      
      # Yearly backup
      func.create_yearly_backup(bs, directions['YEARLY'])


sched.start()
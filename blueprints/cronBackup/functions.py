import shutil, os, tarfile
from pathlib import Path
from datetime import datetime
from cryptography.fernet import Fernet

import blueprints.cronBackup.config as cg


def create_backup_directions(source):
    try:
        os.mkdir(cg.DIRECTION_BACKUP)
    except FileExistsError:
        pass
    try:
        os.mkdir(os.path.join(cg.DIRECTION_BACKUP, source))
    except FileExistsError:
        pass
    frequencies = ['DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY']
    directions = dict()
    for f in frequencies:
        try:
            directions[f] = os.mkdir(os.path.join(cg.DIRECTION_BACKUP, source, f))
        except FileExistsError:
            directions[f] = os.path.join(cg.DIRECTION_BACKUP, source, f)
    return directions


def encrypt_file(source, today_date):
    with open(os.path.join(source, today_date), "rb") as file:
        decrypted_data = file.read()
    cipher_suite = Fernet(str.encode(os.environ.get('ENCRYPT_K')))
    encrypted_data = cipher_suite.encrypt(decrypted_data)
    with open(os.path.join(source, today_date), "wb") as file:
        file.write(encrypted_data)

def create_daily_backup(source, destination):
    if os.environ.get('BACKUP_DAILY_COUNT').lower() != "unlimited":
        daily_backup_list = sorted(Path(destination).iterdir(), key=lambda f: f.stat().st_ctime)
        if len(daily_backup_list) == int(os.environ.get('BACKUP_DAILY_COUNT')):
            os.remove(daily_backup_list[0])
    
    today_date = str(datetime.now().date())
    tar = tarfile.open(os.path.join(destination, today_date), "w:gz")
    tar.add(source, arcname=today_date)
    tar.close()

    encrypt_file(destination, today_date)


def create_weekly_backup(source, destination):
    if datetime.now().weekday() == int(os.environ.get('BACKUP_WEEKLY_DAY')):
        if os.environ.get('BACKUP_WEEKLY_COUNT').lower() != "unlimited":
            weekly_backup_list = sorted(Path(destination).iterdir(), key=lambda f: f.stat().st_ctime)
            if len(weekly_backup_list) == int(os.environ.get('BACKUP_WEEKLY_COUNT')):
                os.remove(weekly_backup_list[0])
        
        today_date = str(datetime.now().date())
        tar = tarfile.open(os.path.join(destination, today_date), "w:gz")
        tar.add(source, arcname=today_date)
        tar.close()

        encrypt_file(destination, today_date)


def create_monthly_backup(source, destination):
    if datetime.now().day == int(os.environ.get('BACKUP_MONTHLY_DAY')):
        if os.environ.get('BACKUP_MONTHLY_COUNT').lower() != "unlimited":
            monthly_backup_list = sorted(Path(destination).iterdir(), key=lambda f: f.stat().st_ctime)
            if len(monthly_backup_list) == int(os.environ.get('BACKUP_MONTHLY_COUNT')):
                os.remove(monthly_backup_list[0])
        
        today_date = str(datetime.now().date())
        tar = tarfile.open(os.path.join(destination, today_date), "w:gz")
        tar.add(source, arcname=today_date)
        tar.close()

        encrypt_file(destination, today_date)


def create_yearly_backup(source, destination):
    if datetime.now().day == int(os.environ.get('BACKUP_YEARLY_DAY')) and datetime.now().month == int(os.environ.get('BACKUP_YEARLY_MONTH')):
        if os.environ.get('BACKUP_YEARLY_COUNT').lower() != "unlimited":
            yearly_backup_list = sorted(Path(destination).iterdir(), key=lambda f: f.stat().st_ctime)
            if len(yearly_backup_list) == int(os.environ.get('BACKUP_YEARLY_COUNT')):
                os.remove(yearly_backup_list[0])
        
        today_date = str(datetime.now().date())
        tar = tarfile.open(os.path.join(destination, today_date), "w:gz")
        tar.add(source, arcname=today_date)
        tar.close()

        encrypt_file(destination, today_date)
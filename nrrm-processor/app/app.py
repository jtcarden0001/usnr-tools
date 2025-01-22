import os
import time
from .store import import_sailors  # Replace 'some_module' with the actual module name
from .models import Sailor
import pandas as pd
import openpyxl
import shutil

def start():
    while True:
        dir_to_watch = '/watch'
        file_name = os.getenv('REPORT_FILE_NAME')
        file_path = os.path.join(dir_to_watch, file_name)
        # if file does not exist, sleep for 1 minute
        if not os.path.exists(file_path):
            if os.getenv('IS_TEST') == 'true':
                raise FileNotFoundError(f"The file {file_path} does not exist.")
            time.sleep(60)

        # if file exists, process the excel file to get the sailors from the excel rows
        sailors = process_report(file_path)

        # import the sailors into the database
        import_sailors(sailors)

        # move the file to the archive directory
        archive_dir = '/archive'

        # if the archive directory does not exist, create it
        archive_dir_exists = os.path.exists(archive_dir)
        if not archive_dir_exists:
            os.mkdir(archive_dir)
        
        # archive the file
        timestamp = time.strftime('%Y%m%d%H%M%S')
        archive_file_name = f'{timestamp}_{file_name}'
        archive_file_path = os.path.join(archive_dir, archive_file_name)
        shutil.copy2(file_path, archive_file_path)
        os.remove(file_path)
        
        # if this is a test run, undo the file move and break the loop
        if os.getenv('IS_TEST') == 'true':
            shutil.copy2(archive_file_path, file_path)
            os.remove(archive_file_path)
            if not archive_dir_exists:
                os.rmdir(archive_dir)

            break

def process_report(file_path: str) -> list[Sailor]:
    df = pd.read_excel(file_path)
    sailors = []
    for _, row in df.iterrows():
        sailor = Sailor(
            dodid=row['DoDID'],
            last_name=row['LastName'],
            first_name=row['FirstName'],
            rank=row['RateRank'],
            truic=row['Truic'],
            umuic=row['Umuic'],
            deployability=row['Deployability'],
            medical_readiness=convert_medical_readiness(row['Imr Status']), 
            prd=row['ProjectedRotationDate'] 
        )
        sailors.append(sailor)
    return sailors

def convert_medical_readiness(nrrm_value: str) -> str:
    if nrrm_value == 'Fully Medically Ready':
        return 'FQ'
    elif nrrm_value == 'Partially Medically Ready':
        return 'PQ'
    elif nrrm_value == 'Not Medically Ready':
        return 'NQ'
    else:
        return 'Unknown'


        

    

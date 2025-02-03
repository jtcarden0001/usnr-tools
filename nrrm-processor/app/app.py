import os
import time
from .store import import_sailors  # Replace 'some_module' with the actual module name
from .models import Sailor
from .reporter import generate_pdf_report
import pandas as pd
import openpyxl
import shutil

def start():
    while True:
        dir_to_watch = '/watch'
        file_name = os.getenv('EXCEL_FILE_NAME')
        file_path = os.path.join(dir_to_watch, file_name)
        # if file does not exist, sleep for 1 minute
        if not os.path.exists(file_path):
            if os.getenv('IS_TEST') == 'true':
                raise FileNotFoundError(f"The file {file_path} does not exist.")
            time.sleep(60)
            continue

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

        generate_pdf_report()
        
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
            last_name=row['LastName'].strip(),
            first_name=row['FirstName'].strip(),
            rank=row['RateRank'].strip(),
            truic=row['Truic'],
            umuic=row['Umuic'],
            deployability=row['Deployability'].strip(),
            medical_readiness=convert_medical_readiness(row['Imr Status'].strip()), 
            prd=row['ProjectedRotationDate'].strip(), 
            phone_number=convert_phone_number(row['HomePhone'].strip()),
            admin_mas=convert_admin_mas(row['Admin MAS Code'].strip()),
            medical_mas=convert_medical_mas(row['Medical MAS Code'].strip()),
            training_mas=convert_training_mas(row['Training MAS Code'].strip())
        )
        sailors.append(sailor)
    return sailors

#region: converters
def convert_medical_readiness(nrrm_value: str) -> str:
    if nrrm_value == 'Fully Medically Ready':
        return 'FQ'
    elif nrrm_value == 'Partially Medically Ready':
        return 'PQ'
    elif nrrm_value == 'Not Medically Ready':
        return 'NQ'
    else:
        return 'Unknown'

def convert_phone_number(phone_number: str) -> str:
    if phone_number == '--':
        return None
    return phone_number

def convert_admin_mas(admin_mas: str) -> str:
    if admin_mas == '--':
        return None
    return admin_mas

def convert_medical_mas(medical_mas: str) -> str:
    if medical_mas == '--':
        return None
    return medical_mas

def convert_training_mas(training_mas: str) -> str:
    if training_mas == '--':
        return None
    return training_mas
#endregion: converters

        

    

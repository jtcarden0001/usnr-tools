import psycopg
import os
import models
from psycopg.rows import class_row

# connect to the database using env args
env_database=os.getenv('DB_NAME')
env_user=os.getenv('DB_USER')
env_password=os.getenv('DB_PASSWORD')
env_host=os.getenv('DB_HOST')
env_port=os.getenv('DB_PORT')

# I am using this monolithic function to import a report and do all operations in a single transaction
# I will refactor it as needed
def import_sailors(sailors: list[models.Sailor]):
    with psycopg.connect(dbname=env_database,
                        user=env_user,
                        password=env_password,
                        host=env_host,
                        port=env_port) as conn:
        with conn.cursor() as cur:
            process_lost_sailors(cur, sailors)
            process_gained_sailors(cur, sailors)
            insert_sailors(cur, sailors)
            snapshot_unit_metrics(cur)

# identify sailors who are in the current db table but not in the report
# add entries for them in the sailor_loss table
# remove them from the current db table
def process_lost_sailors(cur: psycopg.cursor, sailors: list[models.Sailor]):
    sailorMap = {}
    for sailor in sailors:
        sailorMap[sailor.dodid] = True
    cur.execute('SELECT dodid FROM sailor_current')
    dodids = cur.fetchall()
    for dodid in dodids:
        if dodid not in sailorMap:
            cur.execute('INSERT INTO sailor_loss (dodid, action_pending, action_notes) VALUES (%s, %s, %s)', (dodid, True, ''))
            cur.execute('DELETE FROM sailor_current WHERE dodid = %s', (dodid))


# identify sailors who are in the report but not in the current db table
# add entries for them in the sailor_gain table
def process_gained_sailors(cur: psycopg.cursor, sailors: list[models.Sailor]):
    cur.execute('SELECT dodid FROM sailor_current')
    dodids = cur.fetchall()
    for sailor in sailors:
        if sailor.dodid not in dodids:
            cur.execute(
                'INSERT INTO sailor_gain (dodid, action_pending, action_notes) '
                'VALUES (%s, %s, %s)',
                (sailor.dodid, True, '')
            )
        

# take snapshots of all the records in the sailor_current table and insert them into sailor_historical
# update or insert the records in the sailor_current table
def insert_sailors(cur: psycopg.cursor, sailors: list[models.Sailor]):
    cur.row_factory = class_row(models.Sailor)
    cur.execute('SELECT * FROM sailor_current')
    sailors_current = cur.fetchall()
    sailors_current_map = {}
    for sailor in sailors_current:
        sailors_current_map[sailor.dodid] = sailor
        cur.execute(
            'INSERT INTO sailor_historical (dodid, last_name, first_name, rank, deployability, medical_readiness, prd) '
            'VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (sailor.dodid, sailor.last_name, sailor.first_name, sailor.rank, sailor.deployability, sailor.medical_readiness, sailor.prd)
        )
    
    for sailor in sailors:
        if sailor.dodid in sailors_current_map:
            cur.execute(
                'UPDATE sailor_current SET last_name = %s, first_name = %s, rank = %s, deployability = %s, medical_readiness = %s, prd = %s WHERE dodid = %s',
                (sailor.last_name, sailor.first_name, sailor.rank, sailor.deployability, sailor.medical_readiness, sailor.prd, sailor.dodid)
            )
        else:
            cur.execute(
                'INSERT INTO sailor_current (dodid, last_name, first_name, rank, deployability, medical_readiness, prd) '
                'VALUES (%s, %s, %s, %s, %s, %s, %s)',
                (sailor.dodid, sailor.last_name, sailor.first_name, sailor.rank, sailor.deployability, sailor.medical_readiness, sailor.prd)
            )
    
    # reset the row factory
    cur.row_factory = psycopg.rows.tuple_row

# process the sailor_current table and insert a snapshot of the unit metrics into the unit_metric_snapshot table
# TODO: this should be in the application layer, business logic abound, moving quick.  Will refactor
def snapshot_unit_metrics(cur: psycopg.cursor):
    cur.row_factory = class_row(models.Sailor)
    cur.execute('SELECT * FROM sailor_current')
    sailors_current = cur.fetchall()
    cai_count = 0
    local_count = 0
    cai_deployability_fd_count = 0
    cai_deployability_pd_count = 0
    cai_deployability_nd_count = 0
    local_deployability_fd_count = 0
    local_deployability_pd_count = 0
    local_deployability_nd_count = 0
    cai_medical_fq_count = 0
    cai_medical_pq_count = 0
    cai_medical_nq_count = 0
    local_medical_fq_count = 0
    local_medical_pq_count = 0
    local_medical_nq_count = 0
    for sailor in sailors_current:
        if sailor.truic != sailor.umuic:
            cai_count += 1
            if sailor.deployability == 'FD':
                cai_deployability_fd_count += 1
            elif sailor.deployability == 'PD':
                cai_deployability_pd_count += 1
            elif sailor.deployability == 'ND':
                cai_deployability_nd_count += 1
            if sailor.medical_readiness == 'FQ':
                cai_medical_fq_count += 1
            elif sailor.medical_readiness == 'PQ':
                cai_medical_pq_count += 1
            elif sailor.medical_readiness == 'NQ':
                cai_medical_nq_count += 1
        else:
            local_count += 1
            if sailor.deployability == 'FD':
                local_deployability_fd_count += 1
            elif sailor.deployability == 'PD':
                local_deployability_pd_count += 1
            elif sailor.deployability == 'ND':
                local_deployability_nd_count += 1
            if sailor.medical_readiness == 'FQ':
                local_medical_fq_count += 1
            elif sailor.medical_readiness == 'PQ':
                local_medical_pq_count += 1
            elif sailor.medical_readiness == 'NQ':
                local_medical_nq_count += 1
    cur.execute("""
        INSERT INTO unit_metric_snapshot 
            (cai_count, local_count, cai_deployability_fd_count, cai_deployability_pd_count, cai_deployability_nd_count, local_deployability_fd_count, local_deployability_pd_count, local_deployability_nd_count, cai_medical_fq_count, cai_medical_pq_count, cai_medical_nq_count, local_medical_fq_count, local_medical_pq_count, local_medical_nq_count) '
        VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s),
        """,
        (cai_count, local_count, cai_deployability_fd_count, cai_deployability_pd_count, cai_deployability_nd_count, local_deployability_fd_count, local_deployability_pd_count, local_deployability_nd_count, cai_medical_fq_count, cai_medical_pq_count, cai_medical_nq_count, local_medical_fq_count, local_medical_pq_count, local_medical_nq_count)
        )


    







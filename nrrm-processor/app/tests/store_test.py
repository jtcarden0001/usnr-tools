
import pytest
from ..app import import_sailors
from ..store import get_latest_unit_metrics, get_all_sailor_gains, get_all_sailor_losses
from ..models import Sailor
import random
import os

def test_hello_store():
    assert 1 == 1

def test_import_sailors():
    medical_readiness = ['FQ', 'PQ', 'NQ']
    deployability = ['FD', 'PD', 'ND']

    sailors = []
    # create local sailors
    for i in range(3):
        dodidrand = random.randint(1000000000, 9999999999)
        sailors.append(Sailor(
            dodid=dodidrand,
            last_name='Doe',
            first_name='John',
            rank='PO1',
            truic='123',
            umuic='123',
            deployability=deployability[i],
            medical_readiness=medical_readiness[i],
            prd='2021-01-01'
        ))
    
    # create cai sailors
    for i in range(3):
        dodidrand = random.randint(1000000000, 9999999999)
        sailors.append(Sailor(
            dodid=dodidrand,
            last_name='Doe',
            first_name='Jane',
            rank='PO1',
            truic='123',
            umuic='456',
            deployability=deployability[i],
            medical_readiness=medical_readiness[i],
            prd='2021-01-01'
        ))

    # import sailors
    import_sailors(sailors)
    assert True

    # ensure metrics are correct 
    unit_metrics = get_latest_unit_metrics()
    assert unit_metrics.cai_count == 3
    assert unit_metrics.local_count == 3
    assert unit_metrics.cai_deployability_fd_count == 1
    assert unit_metrics.cai_deployability_pd_count == 1
    assert unit_metrics.cai_deployability_nd_count == 1
    assert unit_metrics.local_deployability_fd_count == 1
    assert unit_metrics.local_deployability_pd_count == 1
    assert unit_metrics.local_deployability_nd_count == 1
    assert unit_metrics.cai_medical_fq_count == 1
    assert unit_metrics.cai_medical_pq_count == 1
    assert unit_metrics.cai_medical_nq_count == 1
    assert unit_metrics.local_medical_fq_count == 1
    assert unit_metrics.local_medical_pq_count == 1
    assert unit_metrics.local_medical_nq_count == 1

    # ensure all sailors added are new gains
    sailor_gains = get_all_sailor_gains()
    assert len(sailor_gains) == 6

    # replace the first 3 sailors with ND local sailors
    for i in range(3):
        dodidrand = random.randint(1000000000, 9999999999)
        sailors[i] = Sailor(
            dodid=dodidrand,
            last_name='Doe',
            first_name='John',
            rank='PO1',
            truic='123',
            umuic='123',
            deployability='ND',
            medical_readiness='NQ',
            prd='2021-01-01'
        )
    
    # import sailors
    import_sailors(sailors)

    # we should have 9 new sailors now
    sailor_gains = get_all_sailor_gains()
    assert len(sailor_gains) == 9

    # and 3 lost sailors
    sailor_losses = get_all_sailor_losses()
    assert len(sailor_losses) == 3





    
    
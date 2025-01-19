from dataclasses import dataclass
from datetime import datetime, date

@dataclass
class Sailor:
    dodid: int
    last_name: str
    first_name: str
    rank: str
    truic: str
    umuic: str
    deployability: str
    medical_readiness: str
    prd: str

@dataclass
class SailorHistorical:
    dodid: int
    snapshot_datetime: datetime
    last_name: str
    first_name: str
    rank: str
    truic: str
    umuic: str
    deployability: str
    medical_readiness: str
    prd: str

@dataclass
class SailorLoss:
    dodid: int
    nrrm_loss_date: date
    action_pending: bool
    action_notes: str

@dataclass
class SailorGain:
    dodid: int
    nrrm_gain_date: date
    action_pending: bool
    action_notes: str

@dataclass
class UnitMetricSnapshot:
    snapshot_datetime: datetime
    cai_count: int
    local_count: int
    cai_deployability_fd_count: int
    cai_deployability_pd_count: int
    cai_deployability_nd_count: int
    cai_deployability_mob_count: int
    local_deployability_fd_count: int
    local_deployability_pd_count: int
    local_deployability_nd_count: int
    local_deployability_mob_count: int
    cai_medical_fq_count: int
    cai_medical_pq_count: int
    cai_medical_nq_count: int
    local_medical_fq_count: int
    local_medical_pq_count: int
    local_medical_nq_count: int

    

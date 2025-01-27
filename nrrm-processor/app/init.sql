-- lots of things not normalized, given the good enough stamp for now

-- only holds sailors in last loaded report
CREATE TABLE sailor_current (
  dodid bigint,
  last_name varchar NOT NULL,
  first_name varchar NOT NULL,
  rank varchar NOT NULL, -- not normalized
  truic varchar NOT NULL, -- not normalized
  umuic varchar NOT NULL, -- not normalized
  deployability varchar NOT NULL, -- not normalized
  medical_readiness varchar NOT NULL, -- not normalized
  prd date NOT NULL,
  phone_number varchar,
  admin_mas varchar,
  medical_mas varchar,
  training_mas varchar,
  PRIMARY KEY (dodid)
);

-- holds all sailors ever reported with snapshots to capture changes
CREATE TABLE sailor_historical (
  dodid bigint,
  snapshot_datetime timestamptz NOT NULL DEFAULT now(),
  last_name varchar NOT NULL,
  first_name varchar NOT NULL,
  rank varchar NOT NULL, -- not normalized
  truic varchar NOT NULL, -- not normalized
  umuic varchar NOT NULL, -- not normalized
  deployability varchar NOT NULL, -- not normalized
  medical_readiness varchar NOT NULL, -- not normalized
  prd date NOT NULL,
  phone_number varchar,
  admin_mas varchar,
  medical_mas varchar,
  training_mas varchar,
  PRIMARY KEY (dodid, snapshot_datetime)
);

CREATE TABLE sailor_loss (
    dodid bigint,
    nrrm_loss_date date NOT NULL DEFAULT now(),
    action_pending boolean NOT NULL,
    action_notes varchar,
    PRIMARY KEY (dodid, nrrm_loss_date)
);

CREATE TABLE sailor_gain (
    dodid bigint,
    nrrm_gain_date date NOT NULL DEFAULT now(),
    action_pending boolean NOT NULL,
    action_notes varchar,
    PRIMARY KEY (dodid, nrrm_gain_date)
);

CREATE TABLE unit_metric_snapshot (
    snapshot_datetime timestamptz DEFAULT now(),
    cai_count int NOT NULL,
    local_count int NOT NULL,
    cai_deployability_fd_count int NOT NULL,
    cai_deployability_pd_count int NOT NULL,
    cai_deployability_nd_count int NOT NULL,
    cai_deployability_mob_count int NOT NULL,
    local_deployability_fd_count int NOT NULL,
    local_deployability_pd_count int NOT NULL,
    local_deployability_nd_count int NOT NULL,
    local_deployability_mob_count int NOT NULL,
    cai_medical_fq_count int NOT NULL,
    cai_medical_pq_count int NOT NULL,
    cai_medical_nq_count int NOT NULL,
    local_medical_fq_count int NOT NULL,
    local_medical_pq_count int NOT NULL,
    local_medical_nq_count int NOT NULL,
    PRIMARY KEY (snapshot_datetime)
)
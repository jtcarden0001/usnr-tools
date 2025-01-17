CREATE TABLE sailor (
  dodid bigint,
  last_name varchar NOT NULL,
  first_name varchar NOT NULL,
  rank varchar NOT NULL,
  deployability varchar NOT NULL, -- this is not normalized, that is fine for now
  medical_readiness varchar NOT NULL, -- this is not normalized, that is fine for now
  prd date NOT NULL,
  PRIMARY KEY (dodid)
);

CREATE TABLE sailor_historical (
  dodid bigint,
  snapshot_datetime timestampz NOT NULL DEFAULT now(),
  last_name varchar NOT NULL,
  first_name varchar NOT NULL,
  rank varchar NOT NULL,
  deployability varchar NOT NULL, -- this is not normalized, that is fine for now
  medical_readiness varchar NOT NULL, -- this is not normalized, that is fine for now
  prd date NOT NULL,
  PRIMARY KEY (dodid, snapshot_datetime)
);

CREATE TABLE sailor_loss (
    dodid bigint,
    nrrm_loss_date date NOT NULL,
    action_pending boolean NOT NULL,
    action_notes varchar,
    PRIMARY KEY (dodid)
);

CREATE TABLE sailor_gain (
    dodid bigint,
    nrrm_gain_date date NOT NULL,
    action_pending boolean NOT NULL,
    action_notes varchar,
    PRIMARY KEY (dodid)
);

CREATE TABLE unit_metric_snapshot (
    snapshot_datetime timestampz DEFAULT now(),
    cai_count int NOT NULL,
    local_count int NOT NULL,
    cai_deployability_fd_count int NOT NULL,
    cai_deployability_pd_count int NOT NULL,
    cai_deployability_nd_count int NOT NULL,
    local_deployability_fd_count int NOT NULL,
    local_deployability_pd_count int NOT NULL,
    local_deployability_nd_count int NOT NULL,
    cai_medical_fd_count int NOT NULL,
    cai_medical_pd_count int NOT NULL,
    cai_medical_nd_count int NOT NULL,
    local_medical_fd_count int NOT NULL,
    local_medical_pd_count int NOT NULL,
    local_medical_nd_count int NOT NULL,
    PRIMARY KEY (snapshot_datetime)
)
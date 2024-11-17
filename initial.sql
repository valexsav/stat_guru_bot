CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE metric (
    uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4() NOT NULL,
    tg_id BIGINT NOT NULL,
    name VARCHAR(50) NOT NULL,
    CONSTRAINT unique_tg_id_name UNIQUE (tg_id, name),
);

CREATE TABLE stat (
    uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4() NOT NULL,
    metric_uuid UUID NOT NULL REFERENCES metrics(uuid) ON DELETE CASCADE,
    value NUMERIC(9, 2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
);

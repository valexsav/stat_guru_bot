CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE metric (
    uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4() NOT NULL,
    name BYTEA NOT NULL,
    chat_id BIGINT NOT NULL
);

CREATE TABLE stat (
    uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4() NOT NULL,
    metric_uuid UUID NOT NULL REFERENCES metric(uuid) ON DELETE CASCADE,
    value BYTEA NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_metric_user_uuid ON metric(chat_id);
CREATE INDEX idx_stat_metric_uuid ON stat(metric_uuid);

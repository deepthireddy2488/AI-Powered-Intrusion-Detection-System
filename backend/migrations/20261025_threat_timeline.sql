-- Safe, additive migration for the threat investigation timeline.
-- Run this in the same PostgreSQL database configured by backend/.env.
-- It does not delete existing users, predictions, attack logs, or sessions.

CREATE TABLE IF NOT EXISTS analysis_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    session_id VARCHAR(100) UNIQUE NOT NULL,
    source_type VARCHAR(30) NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_analysis_sessions_user_id
    ON analysis_sessions(user_id);
CREATE INDEX IF NOT EXISTS ix_analysis_sessions_session_id
    ON analysis_sessions(session_id);
CREATE INDEX IF NOT EXISTS ix_analysis_sessions_created_at
    ON analysis_sessions(created_at);

ALTER TABLE predictions ADD COLUMN IF NOT EXISTS user_id INTEGER;
ALTER TABLE predictions ADD COLUMN IF NOT EXISTS session_id VARCHAR(100);
ALTER TABLE predictions ADD COLUMN IF NOT EXISTS row_number INTEGER;
CREATE INDEX IF NOT EXISTS ix_predictions_user_id ON predictions(user_id);
CREATE INDEX IF NOT EXISTS ix_predictions_session_id ON predictions(session_id);
CREATE INDEX IF NOT EXISTS ix_predictions_created_at ON predictions(created_at);

ALTER TABLE attack_logs ADD COLUMN IF NOT EXISTS user_id INTEGER;
ALTER TABLE attack_logs ADD COLUMN IF NOT EXISTS session_id VARCHAR(100);
ALTER TABLE attack_logs ADD COLUMN IF NOT EXISTS source_port INTEGER;
ALTER TABLE attack_logs ADD COLUMN IF NOT EXISTS destination_port INTEGER;
ALTER TABLE attack_logs ADD COLUMN IF NOT EXISTS protocol VARCHAR(10);
ALTER TABLE attack_logs ADD COLUMN IF NOT EXISTS packet_count INTEGER;
ALTER TABLE attack_logs ADD COLUMN IF NOT EXISTS confidence DOUBLE PRECISION;
ALTER TABLE attack_logs ADD COLUMN IF NOT EXISTS recommendation TEXT;
CREATE INDEX IF NOT EXISTS ix_attack_logs_user_id ON attack_logs(user_id);
CREATE INDEX IF NOT EXISTS ix_attack_logs_session_id ON attack_logs(session_id);
CREATE INDEX IF NOT EXISTS ix_attack_logs_created_at ON attack_logs(created_at);


-- Composite indexes support the session-scoped timeline queries.
CREATE INDEX IF NOT EXISTS ix_predictions_user_session_row
    ON predictions(user_id, session_id, row_number, id);
CREATE INDEX IF NOT EXISTS ix_attack_logs_user_session_time
    ON attack_logs(user_id, session_id, created_at DESC, id DESC);
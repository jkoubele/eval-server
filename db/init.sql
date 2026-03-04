CREATE TABLE submissions (
  id BIGSERIAL PRIMARY KEY,
  submission_time TIMESTAMPTZ NOT NULL DEFAULT now(),

  challenge_id TEXT NOT NULL,
  name TEXT NOT NULL,

  language TEXT NOT NULL
         CHECK (language IN ('Python', 'R')),

  status TEXT NOT NULL DEFAULT 'uploading'
         CHECK (status IN ('uploading', 'waiting', 'evaluated')),

  timed_out BOOLEAN,
  produced_output BOOLEAN,
  correct BOOLEAN,
  cpu_time DOUBLE PRECISION,

  metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);
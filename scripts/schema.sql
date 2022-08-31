CREATE TABLE data(
    time TIMESTAMPTZ NOT NULL, -- timestamp of the measurement
    uuid  TEXT  NOT NULL,      -- unique identifier for the variable (pointer between brick schema and database)
    value FLOAT NOT NULL,      -- actual value related to the variable
    PRIMARY KEY (time, uuid)
);

-- creates an index to have quicker queries on db
CREATE INDEX ON data (uuid, time DESC);

-- command to create timeseries table in timeseries db
SELECT * FROM create_hypertable('data', 'time');

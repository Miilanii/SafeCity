CREATE TABLE IF NOT EXISTS incidents_raw (
  id SERIAL PRIMARY KEY,
  incident_date DATE,
  incident_time TIME,
  latitude DOUBLE PRECISION,
  longitude DOUBLE PRECISION,
  province TEXT,
  district TEXT,
  crime_category TEXT,
  victim_gender TEXT,
  victim_age INT,
  reported_to_police BOOLEAN
);

CREATE TABLE IF NOT EXISTS daily_hotspots (
  agg_date DATE,
  district TEXT,
  lat DOUBLE PRECISION,
  lon DOUBLE PRECISION,
  incident_count INT,
  rolling_7d_avg REAL,
  alert BOOLEAN,
  PRIMARY KEY (agg_date, district)
);

CREATE TABLE IF NOT EXISTS resources (
  id SERIAL PRIMARY KEY,
  name TEXT,
  district TEXT,
  phone TEXT,
  type TEXT,
  address TEXT
);

-- Expanded schema for Avinox List
-- bikes + prices + images tables

DROP TABLE IF EXISTS images;
DROP TABLE IF EXISTS prices;
DROP TABLE IF EXISTS bikes;

CREATE TABLE bikes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  slug TEXT NOT NULL UNIQUE,
  brand TEXT NOT NULL,
  model TEXT NOT NULL,
  build TEXT NOT NULL,
  country TEXT,
  status TEXT NOT NULL DEFAULT 'NEW',
  motor TEXT,
  peak_w INTEGER,
  peak_nm INTEGER,
  battery_wh INTEGER,
  battery_type TEXT,
  removable TEXT NOT NULL DEFAULT 'No',
  front_travel_mm INTEGER,
  rear_travel_mm INTEGER,
  frame TEXT,
  wheels TEXT,
  weight_kg REAL,
  weight_source TEXT,
  fork TEXT,
  shock TEXT,
  drivetrain TEXT,
  brakes TEXT,
  wheelset TEXT,
  dropper TEXT,
  instagram TEXT,
  notes TEXT,
  source_url TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE UNIQUE INDEX idx_bikes_brand_model_build ON bikes (brand, model, build);

CREATE TABLE prices (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  bike_id INTEGER NOT NULL REFERENCES bikes(id) ON DELETE CASCADE,
  currency TEXT NOT NULL,
  amount INTEGER NOT NULL,
  source_url TEXT,
  verified_at TEXT,
  UNIQUE(bike_id, currency)
);

CREATE INDEX idx_prices_bike ON prices (bike_id);

CREATE TABLE images (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  bike_id INTEGER NOT NULL REFERENCES bikes(id) ON DELETE CASCADE,
  url TEXT NOT NULL,
  sort_order INTEGER NOT NULL DEFAULT 0,
  is_primary INTEGER NOT NULL DEFAULT 0,
  alt_text TEXT
);

CREATE INDEX idx_images_bike ON images (bike_id);

CREATE TABLE IF NOT EXISTS subscribers (
  email TEXT PRIMARY KEY,
  source TEXT NOT NULL DEFAULT 'avinoxlist',
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bikes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  brand TEXT NOT NULL,
  model TEXT NOT NULL,
  build TEXT NOT NULL,
  country TEXT,
  motor TEXT,
  peak_w INTEGER,
  peak_nm INTEGER,
  battery_wh INTEGER,
  frame TEXT,
  weight REAL,
  removable TEXT,
  source_url TEXT
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_bikes_unique_trim
  ON bikes (brand, model, build);

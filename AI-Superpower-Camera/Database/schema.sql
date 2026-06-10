CREATE TABLE IF NOT EXISTS custom_powers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    primary_color TEXT NOT NULL,
    secondary_color TEXT NOT NULL,
    particle_profile TEXT NOT NULL,
    sound_profile TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

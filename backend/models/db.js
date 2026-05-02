const sqlite3 = require("sqlite3").verbose();

const db = new sqlite3.Database("./database.sqlite", (err) => {
  if (err) console.error(err);
  else console.log("📦 DB Connected");
});

db.serialize(() => {
  db.run(`
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT UNIQUE,
      password TEXT,
      role TEXT
    )
  `);

  db.run(`
    CREATE TABLE IF NOT EXISTS products (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT,
      price REAL,
      stock INTEGER,
      barcode TEXT UNIQUE
    )
  `);

  db.run(`
    INSERT OR IGNORE INTO users (username,password,role)
    VALUES ('admin','1234','admin')
  `);
});

module.exports = db;

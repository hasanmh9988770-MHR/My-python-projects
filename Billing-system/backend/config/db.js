const sqlite3 = require("sqlite3").verbose();

const db = new sqlite3.Database("./database.sqlite");

function initDB() {
  return new Promise((resolve, reject) => {
    db.serialize(() => {
      console.log("📦 Initializing DB...");

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

      db.run(`
        INSERT OR IGNORE INTO users (username,password,role)
        VALUES ('cashier','1234','cashier')
      `);

      console.log("✅ DB READY");
      resolve();
    });
  });
}

module.exports = { db, initDB };
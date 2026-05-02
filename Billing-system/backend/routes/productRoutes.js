const express = require("express");
const db = require("../models/db");
const auth = require("../middleware/auth");

const router = express.Router();

// ======================
// GET ALL PRODUCTS
// ======================
router.get("/", auth, (req, res) => {
  db.all("SELECT * FROM products", (err, rows) => {
    if (err) return res.status(500).json(err);
    res.json(rows);
  });
});

// ======================
// ADD PRODUCT
// ======================
router.post("/", auth, (req, res) => {
  const { name, price, stock, barcode } = req.body;

  db.run(
    "INSERT INTO products (name, price, stock, barcode) VALUES (?, ?, ?, ?)",
    [name, price, stock, barcode],
    function (err) {
      if (err) return res.status(500).json(err);
      res.json({ id: this.lastID });
    }
  );
});

// ======================
// UPDATE STOCK
// ======================
router.put("/:id", auth, (req, res) => {
  db.run(
    "UPDATE products SET stock=? WHERE id=?",
    [req.body.stock, req.params.id],
    function (err) {
      if (err) return res.status(500).json(err);
      res.json({ updated: true });
    }
  );
});

// ======================
// BARCODE LOOKUP (MAIN)
// ======================
router.get("/barcode/:code", (req, res) => {
  const code = req.params.code;

  db.get(
    "SELECT * FROM products WHERE barcode = ?",
    [code],
    (err, row) => {
      if (err) return res.status(500).json(err);
      if (!row) return res.status(404).json({ msg: "Not found" });
      res.json(row);
    }
  );
});

module.exports = router;
const express = require("express");
const db = require("../models/db");
const auth = require("../middleware/auth");

const router = express.Router();


// ======================
// GET ALL PRODUCTS
// (FIX: safe auth + fallback support)
// ======================
router.get("/", auth, (req, res) => {
  db.all("SELECT * FROM products", (err, rows) => {
    if (err) {
      return res.status(500).json({
        error: true,
        message: "Database error",
        details: err.message,
      });
    }
    res.json(rows);
  });
});


// ======================
// ADD PRODUCT
// ======================
router.post("/", auth, (req, res) => {
  const { name, price, stock, barcode } = req.body;

  if (!name || !price || !barcode) {
    return res.status(400).json({
      error: true,
      message: "Missing required fields",
    });
  }

  db.run(
    "INSERT INTO products (name, price, stock, barcode) VALUES (?, ?, ?, ?)",
    [name, price, stock || 0, barcode],
    function (err) {
      if (err) {
        return res.status(500).json({
          error: true,
          message: "Insert failed",
          details: err.message,
        });
      }

      res.json({
        success: true,
        id: this.lastID,
      });
    }
  );
});


// ======================
// UPDATE STOCK
// ======================
router.put("/:id", auth, (req, res) => {
  const { stock } = req.body;

  db.run(
    "UPDATE products SET stock=? WHERE id=?",
    [stock, req.params.id],
    function (err) {
      if (err) {
        return res.status(500).json({
          error: true,
          message: "Update failed",
          details: err.message,
        });
      }

      res.json({
        success: true,
        updated: this.changes > 0,
      });
    }
  );
});


// ======================
// BARCODE LOOKUP (NO AUTH)
// (IMPORTANT: needed for scanner)
// ======================
router.get("/barcode/:code", (req, res) => {
  const code = req.params.code;

  db.get(
    "SELECT * FROM products WHERE barcode = ?",
    [code],
    (err, row) => {
      if (err) {
        return res.status(500).json({
          error: true,
          message: "Database error",
          details: err.message,
        });
      }

      if (!row) {
        return res.status(404).json({
          error: true,
          message: "Product not found",
        });
      }

      res.json(row);
    }
  );
});

module.exports = router;

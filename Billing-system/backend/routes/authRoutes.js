const express = require("express");
const jwt = require("jsonwebtoken");
const db = require("../models/db");

const router = express.Router();

router.post("/login", (req, res) => {
  const { username, password } = req.body;

  db.get(
    "SELECT * FROM users WHERE username=? AND password=?",
    [username, password],
    (err, user) => {
      if (!user) return res.status(401).json({ msg: "Invalid login" });

      const token = jwt.sign(
        { id: user.id, role: user.role },
        "SECRET",
        { expiresIn: "1d" }
      );

      res.json({ token, role: user.role });
    }
  );
});

module.exports = router;

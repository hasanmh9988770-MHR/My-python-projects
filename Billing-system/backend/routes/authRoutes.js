const express = require("express");
const jwt = require("jsonwebtoken");
const SECRET = require("../config/secret");

const router = express.Router();

router.post("/login", (req, res) => {
  const { username, password } = req.body;

  // FIXED LOGIN
  if (username === "Admin" && password === "9090") {
    const token = jwt.sign(
      { id: 1, role: "admin" },
      SECRET,
      { expiresIn: "1d" }
    );

    return res.json({ token });
  }

  return res.status(401).json({ message: "Invalid Login" });
});

module.exports = router;

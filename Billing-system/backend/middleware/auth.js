const jwt = require("jsonwebtoken");

const SECRET = process.env.JWT_SECRET || "SECRET";

module.exports = (req, res, next) => {
  try {
    const authHeader = req.headers.authorization;

    if (!authHeader) {
      return res.status(401).json({
        success: false,
        message: "No token provided",
      });
    }

    // Expect: Bearer TOKEN
    const parts = authHeader.split(" ");

    if (parts.length !== 2) {
      return res.status(401).json({
        success: false,
        message: "Invalid token format",
      });
    }

    const token = parts[1];

    const decoded = jwt.verify(token, SECRET);

    req.user = decoded;
    next();
  } catch (err) {
    return res.status(401).json({
      success: false,
      message: "Invalid or expired token",
    });
  }
};

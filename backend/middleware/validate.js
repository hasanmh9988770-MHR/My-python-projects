module.exports = (req, res, next) => {
  if (!req.body.customer_name) {
    return res.status(400).json({ error: "Name required" });
  }
  next();
};

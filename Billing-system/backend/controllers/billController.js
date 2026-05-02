const { createBillService } = require("../services/billService");

exports.createBill = (req, res) => {
  createBillService(req.body, (err, result) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(result);
  });
};

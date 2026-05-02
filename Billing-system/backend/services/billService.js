const db = require("../config/db");
const calculateProfit = require("../utils/profitCalculator");

const createBillService = (data, callback) => {
  const { customer_name, phone, items } = data;

  const { total, cost, profit } = calculateProfit(items);

  db.run(
    `INSERT INTO bills (customer_name, phone, items, total, cost, profit)
     VALUES (?, ?, ?, ?, ?, ?)`,
    [customer_name, phone, JSON.stringify(items), total, cost, profit],
    function (err) {
      if (err) return callback(err);
      callback(null, { id: this.lastID, total, profit });
    }
  );
};

module.exports = { createBillService };

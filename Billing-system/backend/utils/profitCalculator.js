const calculateProfit = (items) => {
  let total = 0;
  let cost = 0;

  items.forEach(i => {
    total += i.price * i.qty;
    cost += i.cost * i.qty;
  });

  return {
    total,
    cost,
    profit: total - cost
  };
};

module.exports = calculateProfit;

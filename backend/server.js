const express = require("express");
const cors = require("cors");
require("dotenv").config();

require("./models/db");

const app = express();

app.use(cors());
app.use(express.json());

app.use("/api/auth", require("./routes/authRoutes"));
app.use("/api/products", require("./routes/productRoutes"));

app.get("/", (req, res) => {
  res.send("🚀 POS Backend Running");
});

const PORT = process.env.PORT || 5050;

app.listen(PORT, () => {
  console.log(`✅ POS Server running on ${PORT}`);
});

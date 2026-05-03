export const login = (req, res) => {
  const { username, password } = req.body;

  if (username === "Admin" && password === "9090") {
    return res.json({
      token: "demo-token",
      user: { role: "admin" }
    });
  }

  return res.status(401).json({ message: "Invalid Login" });
};

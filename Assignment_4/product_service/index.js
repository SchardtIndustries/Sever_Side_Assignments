const express = require("express");
const app = express();
const port = 3001;

// Mock product data
const products = {
  "1": { id: "1", name: "Laptop", description: "Powerful laptop for work and play" },
  "2": { id: "2", name: "Keyboard", description: "Ergonomic keyboard for comfortable typing" },
  "3": { id: "3", name: "Mouse", description: "Wireless mouse with adjustable DPI" },
};

app.get("/products/:id", (req, res) => {
  const product = products[req.params.id];
  if (!product) return res.status(404).json({ message: "Product not found" });
  res.json(product);
});

app.listen(port, () => {
  console.log(`Product service running on port ${port}`);
});

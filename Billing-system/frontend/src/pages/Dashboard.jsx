import { useEffect, useState } from "react";
import API from "../services/api";
import BarcodeScanner from "../components/BarcodeScanner";
import { generateInvoice } from "../utils/pdf";

export default function Dashboard() {
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState([]);

  useEffect(() => {
    API.get("/products").then(res => setProducts(res.data));
  }, []);

  const addToCart = (p) => {
    setCart(prev => {
      const found = prev.find(i => i.id === p.id);
      if (found) {
        return prev.map(i =>
          i.id === p.id ? { ...i, qty: i.qty + 1 } : i
        );
      }
      return [...prev, { ...p, qty: 1 }];
    });
  };

  const total = cart.reduce((sum, i) => sum + i.price * i.qty, 0);

  return (
    <div style={{ padding: 20 }}>
      <h2>📦 POS DASHBOARD</h2>

      <h3>Products</h3>
      {products.map(p => (
        <div key={p.id}>
          {p.name} - ${p.price} - Stock:{p.stock}
          <button onClick={() => addToCart(p)}>Add</button>
        </div>
      ))}

      <h3>🛒 Cart</h3>
      {cart.map(c => (
        <div key={c.id}>
          {c.name} x {c.qty}
        </div>
      ))}

      <h3>Total: ${total}</h3>

      <button onClick={() => generateInvoice(cart, total)}>
        🧾 Generate Invoice
      </button>

      <h3>📷 Barcode Scanner</h3>
      <BarcodeScanner onScan={(code)=>console.log("Scanned:", code)} />
    </div>
  );
}

import { useState, useEffect } from "react";
import API from "../services/api";
import jsPDF from "jspdf";

export default function Billing() {
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState([]);
  const [search, setSearch] = useState("");

  // 📦 LOAD PRODUCTS
  useEffect(() => {
    API.get("/products")
      .then((res) => setProducts(res.data))
      .catch((err) => console.error(err));
  }, []);

  // 🛒 ADD TO CART
  const add = (product) => {
    setCart((prev) => {
      const exists = prev.find((p) => p.id === product.id);

      if (exists) {
        return prev.map((p) =>
          p.id === product.id
            ? { ...p, qty: p.qty + 1 }
            : p
        );
      }

      return [...prev, { ...product, qty: 1 }];
    });
  };

  // 📷 BARCODE INFO ONLY (NO CART ADD)
  const scan = async (e) => {
    if (e.key !== "Enter") return;

    const code = e.target.value.trim();
    if (!code) return;

    try {
      const res = await API.get(`/products/barcode/${code}`);

      if (res.data?.id) {
        alert(
          `PRODUCT INFO\n\n` +
          `Name: ${res.data.name}\n` +
          `Price: $${res.data.price}\n` +
          `Stock: ${res.data.stock}\n` +
          `Barcode: ${res.data.barcode}`
        );
      } else {
        alert("Product not found");
      }
    } catch (err) {
      console.error(err);
      alert("Error fetching product");
    }

    e.target.value = "";
  };

  // 🧾 PDF INVOICE (FIXED 100%)
  const invoice = () => {
    if (cart.length === 0) {
      alert("Cart is empty");
      return;
    }

    const doc = new jsPDF();

    let y = 10;

    // HEADER (SAFE TEXT ONLY)
    doc.setFont("helvetica", "bold");
    doc.setFontSize(16);
    doc.text("MH SUPERMARKET INVOICE", 10, y);

    y += 10;

    doc.setFont("helvetica", "normal");
    doc.setFontSize(12);

    doc.text("----------------------------", 10, y);
    y += 10;

    cart.forEach((item) => {
      doc.text(
        `${item.name} x${item.qty} = $${(
          item.price * item.qty
        ).toFixed(2)}`,
        10,
        y
      );
      y += 8;
    });

    const total = cart.reduce(
      (sum, item) => sum + item.price * item.qty,
      0
    );

    y += 5;

    doc.text("----------------------------", 10, y);
    y += 10;

    doc.setFont("helvetica", "bold");
    doc.setFontSize(14);
    doc.text(`TOTAL: $${total.toFixed(2)}`, 10, y);

    y += 10;

    doc.setFont("helvetica", "normal");
    doc.setFontSize(10);
    doc.text("Thank you for shopping with MH Supermarket", 10, y);

    doc.save("invoice.pdf");
  };

  // 💰 TOTAL
  const total = cart.reduce(
    (sum, item) => sum + item.price * item.qty,
    0
  );

  // 🔍 FILTER PRODUCTS
  const filtered = products.filter((p) =>
    p.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "Arial" }}>

      {/* LEFT SIDE */}
      <div style={{ flex: 2, padding: 20, borderRight: "1px solid #ddd" }}>
        <h2>📦 PRODUCTS</h2>

        {/* SEARCH */}
        <input
          placeholder="Search products..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{
            padding: 10,
            width: "100%",
            marginBottom: 10
          }}
        />

        {/* BARCODE INPUT (INFO MODE) */}
        <input
          placeholder="Type barcode + Enter (info only)"
          onKeyDown={scan}
          style={{
            padding: 10,
            width: "100%",
            marginBottom: 15
          }}
        />

        {/* PRODUCTS */}
        {filtered.map((p) => (
          <div
            key={p.id}
            style={{
              display: "flex",
              justifyContent: "space-between",
              padding: 10,
              borderBottom: "1px solid #eee"
            }}
          >
            <div>
              {p.name} - ${p.price}
            </div>

            <button onClick={() => add(p)}>
              Add
            </button>
          </div>
        ))}
      </div>

      {/* RIGHT SIDE */}
      <div style={{ flex: 1, padding: 20 }}>
        <h2>🛒 CART</h2>

        {cart.length === 0 ? (
          <p>No items</p>
        ) : (
          cart.map((i) => (
            <div key={i.id}>
              {i.name} x{i.qty} = ${i.qty * i.price}
            </div>
          ))
        )}

        <hr />

        <h3>💰 Total: ${total.toFixed(2)}</h3>

        {/* INVOICE BUTTON */}
        <button
          onClick={invoice}
          style={{
            width: "100%",
            padding: 12,
            marginTop: 10,
            background: "black",
            color: "white",
            borderRadius: 8,
            border: "none",
            cursor: "pointer"
          }}
        >
          🧾 Generate PDF Invoice
        </button>
      </div>
    </div>
  );
}
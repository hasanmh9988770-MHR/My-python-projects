import { useState, useEffect } from "react";
import API from "../services/api";
import jsPDF from "jspdf";
import { Howl } from "howler";

const beep = new Howl({
  src: ["https://actions.google.com/sounds/v1/cartoon/wood_plank_flicks.ogg"]
});

export default function Billing() {
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    API.get("/products")
      .then((res) => setProducts(res.data))
      .catch((err) => console.log(err));
  }, []);

  const addToCart = (item) => {
    beep.play();
    setCart((prev) => {
      const exists = prev.find((p) => p.id === item.id);
      if (exists) {
        return prev.map((p) =>
          p.id === item.id ? { ...p, qty: p.qty + 1 } : p
        );
      }
      return [...prev, { ...item, qty: 1 }];
    });
  };

  const scanBarcode = async (e) => {
    if (e.key !== "Enter") return;
    const code = e.target.value;

    const res = await API.get(`/products/barcode/${code}`);
    if (res.data?.id) addToCart(res.data);

    e.target.value = "";
  };

  const total = cart.reduce((sum, i) => sum + i.price * i.qty, 0);

  const invoice = () => {
    const doc = new jsPDF();
    doc.text("POS INVOICE", 10, 10);

    let y = 20;
    cart.forEach((i) => {
      doc.text(`${i.name} x${i.qty} = ${i.price * i.qty}`, 10, y);
      y += 10;
    });

    doc.text("TOTAL: " + total, 10, y + 10);
    doc.save("invoice.pdf");
  };

  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "Arial" }}>

      {/* PRODUCTS */}
      <div style={{ flex: 2, padding: 20 }}>
        <h2>📦 PRODUCTS</h2>

        <input
          placeholder="Search..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

        <input
          placeholder="Scan barcode here"
          onKeyDown={scanBarcode}
          style={{ display: "block", marginTop: 10 }}
        />

        {products
          .filter((p) =>
            p.name.toLowerCase().includes(search.toLowerCase())
          )
          .map((p) => (
            <div key={p.id}>
              {p.name} - ${p.price}
              <button onClick={() => addToCart(p)}>Add</button>
            </div>
          ))}
      </div>

      {/* CART */}
      <div style={{ flex: 1, padding: 20 }}>
        <h2>🛒 CART</h2>

        {cart.map((i) => (
          <div key={i.id}>
            {i.name} x{i.qty} = ${i.qty * i.price}
          </div>
        ))}

        <hr />
        <h3>Total: ${total}</h3>

        <button onClick={invoice}>
          🧾 Generate Invoice
        </button>
      </div>
    </div>
  );
}

import { useRef, useState } from "react";
import API from "../services/api";

export default function BarcodeScanner({ onScan }) {
  const fileRef = useRef(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setLoading(true);

    const formData = new FormData();
    formData.append("image", file);

    try {
      const res = await API.post("/products/scan-barcode", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      if (res.data?.product) {
        onScan(res.data.product);
      } else {
        alert("❌ Barcode not found");
      }
    } catch (err) {
      console.error(err);
      alert("❌ Scan failed (backend error)");
    }

    setLoading(false);
    e.target.value = "";
  };

  return (
    <div style={{ marginTop: 15 }}>
      <button
        onClick={() => fileRef.current.click()}
        disabled={loading}
        style={{
          width: "100%",
          padding: 14,
          background: loading ? "#444" : "#111",
          color: "white",
          border: "none",
          borderRadius: 10,
          fontWeight: "600",
          cursor: "pointer",
        }}
      >
        {loading ? "⌛ Decoding..." : "📷 Scan Barcode (Pro Mode)"}
      </button>

      <input
        type="file"
        accept="image/*"
        ref={fileRef}
        onChange={handleUpload}
        style={{ display: "none" }}
      />
    </div>
  );
}
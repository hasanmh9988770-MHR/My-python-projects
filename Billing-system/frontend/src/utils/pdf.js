import jsPDF from "jspdf";

export const generateInvoice = (cart, total) => {
  const doc = new jsPDF();

  doc.setFont("helvetica", "normal");
  doc.setFontSize(12);

  doc.text("POS INVOICE", 10, 10);

  let y = 20;

  cart.forEach((item) => {
    doc.text(
      `${item.name} x${item.qty} = ${item.price * item.qty}`,
      10,
      y
    );
    y += 10;
  });

  doc.text(`TOTAL: ${total}`, 10, y + 10);

  doc.save("invoice.pdf");
};

import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Billing from "./pages/Billing";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/billing" element={<Billing />} />
      </Routes>
    </BrowserRouter>
  );
}

import { Routes, Route } from "react-router-dom";
import Home from "../pages/Home";
import Products from "../pages/Products";
import Cart from "../pages/Cart";
import Login from "../pages/Login";

const AppRoutes = () => (
  <Routes>
    <Route path="/" element={<Home />} />
    <Route path="/products" element={<Products />} />
    <Route path="/cart" element={<Cart />} />
    <Route path="/login" element={<Login />} />
  </Routes>
);

export default AppRoutes;

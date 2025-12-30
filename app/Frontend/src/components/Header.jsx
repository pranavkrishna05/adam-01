import { Link } from "react-router-dom";
import { useCart } from "../context/CartContext";

const Header = () => {
  const { cart } = useCart();

  return (
    <header className="header">
      <div className="header-container">

        {/* Left: Brand */}
        <div className="header-left">
          <h1 className="logo">ShopSphere</h1>
        </div>

        {/* Center: Search */}
        <div className="header-center">
          <input
            type="text"
            placeholder="Search for products, brands and more"
            className="search-input"
          />
        </div>

        {/* Right: Navigation */}
        <nav className="header-right">
          <Link to="/">Home</Link>
          <Link to="/products">Products</Link>
          <Link to="/cart">Cart ({cart.length})</Link>
          <Link to="/login">Login</Link>
        </nav>

      </div>
    </header>
  );
};

export default Header;

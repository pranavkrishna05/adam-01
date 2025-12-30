import { Link } from "react-router-dom";
import { useCart } from "../context/CartContext";

const ProductCard = ({ product }) => {
  const { addToCart } = useCart();

  return (
    <div className="product-card">
      <div className="product-image-wrapper">
        <img src={product.image} alt={product.title} />
      </div>

      <div className="product-info">
        <h4 className="product-title">{product.title}</h4>
        <p className="product-price">₹ {product.price}</p>

        <div className="product-actions">
          <button onClick={() => addToCart(product)}>Add to Cart</button>
          <Link to={`/products/${product.id}`}>View</Link>
        </div>
      </div>
    </div>
  );
};

export default ProductCard;

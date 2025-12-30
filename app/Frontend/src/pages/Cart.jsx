import { useCart } from "../context/CartContext";

const Cart = () => {
  const {
    cart,
    removeFromCart,
    increaseQty,
    decreaseQty
  } = useCart();

  const total = cart
    .reduce((sum, item) => sum + item.price * item.quantity, 0)
    .toFixed(2);

  return (
    <section className="page cart-page">
      <h2>Your Shopping Cart</h2>

      {cart.length === 0 && <p>Your cart is empty.</p>}

      {cart.map(item => (
        <div key={item.id} className="cart-item">
          {/* Product Image */}
          <img src={item.image} alt={item.title} />

          {/* Product Details */}
          <div className="cart-details">
            <h4>{item.title}</h4>
            <p className="cart-price">$ {item.price}</p>

            {/* Quantity Control */}
            <div className="cart-qty">
              <button onClick={() => decreaseQty(item.id)}>-</button>
              <span>{item.quantity}</span>
              <button onClick={() => increaseQty(item.id)}>+</button>
            </div>
          </div>

          {/* Actions */}
          <div className="cart-actions">
            <p className="cart-subtotal">
              $ {(item.price * item.quantity).toFixed(2)}
            </p>
            <button
              className="remove-btn"
              onClick={() => removeFromCart(item.id)}
            >
              Remove
            </button>
          </div>
        </div>
      ))}

      {cart.length > 0 && (
        <div className="cart-summary">
          <h3>Total: $ {total}</h3>
          <button className="primary-btn">Proceed to Pay</button>
        </div>
      )}
    </section>
  );
};

export default Cart;

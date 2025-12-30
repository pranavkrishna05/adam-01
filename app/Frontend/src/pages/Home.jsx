import { Link } from "react-router-dom";

const Home = () => {
  return (
    <section className="page">
      <h1>Welcome to ShopSphere</h1>
      <p className="subtitle">
        Your one-stop destination for quality products at unbeatable prices.
      </p>

      <div className="home-features">
        <div className="feature-card">
          <h3>Wide Selection</h3>
          <p>Thousands of products across electronics, fashion & more.</p>
        </div>

        <div className="feature-card">
          <h3>Fast Delivery</h3>
          <p>Quick and reliable delivery, right to your doorstep.</p>
        </div>

        <div className="feature-card">
          <h3>Secure Payments</h3>
          <p>100% secure payments with easy returns.</p>
        </div>
      </div>

      <Link to="/products" className="primary-btn">
        Start Shopping
      </Link>
    </section>
  );
};

export default Home;

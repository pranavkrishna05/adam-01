const Login = () => {
  return (
    <section className="page login-page">
      <h2>Login to ShopSphere</h2>
      <p className="subtitle">
        Access your orders, wishlist and personalized recommendations.
      </p>

      <input type="email" placeholder="Email address" />
      <input type="password" placeholder="Password" />

      <button className="primary-btn">Login</button>

      <p className="small-text">
        New to ShopSphere? Create an account to start shopping.
      </p>
    </section>
  );
};

export default Login;

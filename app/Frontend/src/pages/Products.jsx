import { useEffect, useState } from "react";
import api from "../api/axios";
import ProductCard from "../components/ProductCard";

const Products = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get("/products")
      .then(res => {
        if (Array.isArray(res.data)) {
          setProducts(res.data);
        } else {
          setError("Failed to load products");
        }
      })
      .catch(() => {
        setError("Something went wrong while fetching products");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <p>Loading products...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <section className="page">
      <h2>Explore Products</h2>
      <p className="subtitle">
        Discover top-rated products curated just for you.
      </p>

      <div className="grid">
        {products.map(product => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
    </section>
  );
};

export default Products;

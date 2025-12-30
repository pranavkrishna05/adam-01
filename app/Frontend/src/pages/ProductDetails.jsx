import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import api from "../api/axios";
import { useCart } from "../context/CartContext";

const ProductDetails = () => {
  const { id } = useParams();
  const { addToCart } = useCart();
  const [product, setProduct] = useState(null);

  useEffect(() => {
    api.get(`/products/${id}`).then(res => setProduct(res.data));
  }, [id]);

  if (!product) return <p>Loading...</p>;

  return (
    <section className="page">
      <h2>{product.title}</h2>
      <img src={product.image} width="200" />
      <p>{product.description}</p>
      <p><strong>${product.price}</strong></p>
      <button onClick={() => addToCart(product)}>Add to Cart</button>
    </section>
  );
};

export default ProductDetails;

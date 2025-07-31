import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

export default function ProductDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [product, setProduct] = useState(null);
  useEffect(() => {
    fetch(`http://localhost:5000/api/products/${id}`)
      .then(res => res.ok ? res.json() : Promise.reject("Not found"))
      .then(data => setProduct(data))
      .catch(() => setProduct(null));
  }, [id]);
  if (!product) return <div>Product not found.<br/><button onClick={()=>navigate(-1)}>Back</button></div>;
  return (
    <div>
      <button onClick={()=>navigate(-1)}>← Back</button>
      <h2>{product.name}</h2>
      <div>Category: {product.category}</div>
      <div>Brand: {product.brand}</div>
      <div>Department: {product.department}</div>
      <div>SKU: {product.sku}</div>
      <div>Retail Price: ₹{product.retail_price}</div>
    </div>
  );
}

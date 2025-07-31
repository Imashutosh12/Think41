import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

export default function ProductList() {
  const [products, setProducts] = useState([]);
  useEffect(() => {
    fetch("http://localhost:5000/api/products")
      .then(res => res.json())
      .then(data => setProducts(Array.isArray(data) ? data : data.products || []));
  }, []);

  if (!products.length) return <div>No products found.</div>;

  return (
    <div>
      <h2>Product List</h2>
      <ul>
        {products.map(product => (
          <li key={product.id}>
            <Link to={`/products/${product.id}`}>{product.name}</Link>
            <span> | Department: {product.department}</span>
          </li>
        ))}
      </ul>
      <Link to="/">Back to Departments</Link>
    </div>
  );
}

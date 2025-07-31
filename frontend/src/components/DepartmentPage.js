import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";

export default function DepartmentPage() {
  const { id } = useParams();
  const [depName, setDepName] = useState("");
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetch(`http://localhost:5000/api/departments/${id}/products`)
      .then(res => res.json())
      .then(data => {
        setDepName(data.department || "");
        setProducts(data.products || []);
        setLoading(false);
      });
  }, [id]);

  if (loading) return <div>Loading department...</div>;
  if (!depName) return <div>Department not found</div>;

  return (
    <div>
      <h2>{depName} ({products.length} products)</h2>
      <Link to="/">← Back to Departments</Link>
      <ul>
        {products.map(p => (
          <li key={p.id}>
            <Link to={`/products/${p.id}`}>{p.name}</Link>
            {" "}₹{p.retail_price}
          </li>
        ))}
      </ul>
      {!products.length && <p>No products in this department.</p>}
    </div>
  );
}

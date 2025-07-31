import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

export default function DepartmentList() {
  const [departments, setDepartments] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/api/departments")
      .then(res => res.json())
      .then(data => setDepartments(data.departments || []));
  }, []);

  return (
    <div>
      <h2>Departments</h2>
      <ul>
        {departments.map(dep => (
          <li key={dep.id}>
            <Link to={`/departments/${dep.id}`}>
              {dep.name} ({dep.product_count})
            </Link>
          </li>
        ))}
      </ul>
      <Link to="/products">Browse All Products</Link>
    </div>
  );
}

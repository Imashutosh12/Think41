import { Routes, Route } from 'react-router-dom';
import DepartmentList from './components/DepartmentList';
import DepartmentPage from './components/DepartmentPage';
import ProductList from './components/ProductList';
import ProductDetail from './components/ProductDetail';

function App() {
  return (
    <Routes>
      <Route path="/" element={<DepartmentList />} />
      <Route path="/departments/:id" element={<DepartmentPage />} />
      <Route path="/products" element={<ProductList />} />
      <Route path="/products/:id" element={<ProductDetail />} />
    </Routes>
  );
}

export default App;

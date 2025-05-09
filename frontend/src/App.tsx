import React from "react";
import { ProductList } from "./components/ProductList";
import "./styles/ProductList.css";
import "./styles/products.css";
function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Product Catalog</h1>
      </header>
      <main>
        <ProductList />
      </main>
    </div>
  );
}

export default App;

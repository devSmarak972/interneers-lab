import React, { useState, useEffect } from "react";
import { Product as ProductType, Category } from "../types/Product";
import { Product } from "./Product";

export const ProductList: React.FC = () => {
  const [products, setProducts] = useState<ProductType[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>("");
  const [searchTerm, setSearchTerm] = useState<string>("");
  const [isAddingNew, setIsAddingNew] = useState(false);
  const [isAddingCategory, setIsAddingCategory] = useState(false);
  const [newCategory, setNewCategory] = useState({
    name: "",
    title: "",
    description: "",
  });

  // Fetch categories on mount
  useEffect(() => {
    fetchCategories();
  }, []);

  // Fetch products when filters change
  useEffect(() => {
    fetchProducts();
  }, [selectedCategory, searchTerm]);

  const handleAddCategory = async () => {
    if (!newCategory.title.trim()) return;
    try {
      const response = await fetch("http://localhost:8000/product/cat/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken") || "",
        },
        body: JSON.stringify(newCategory),
      });

      if (!response.ok) throw new Error("Failed to add category");
      setNewCategory({ name: "", title: "", description: "" });
      setIsAddingCategory(false);
      fetchCategories();
    } catch (error) {
      console.error(error);
    }
  };
  const fetchCategories = async () => {
    try {
      const response = await fetch("http://localhost:8000/product/cat/");
      if (!response.ok) throw new Error("Failed to fetch categories");
      const data = await response.json();
      setCategories(data);
      console.log(data);
    } catch (error) {
      console.error(error);
    }
  };

  const fetchProducts = async () => {
    try {
      const filters: any = {};
      if (selectedCategory) filters.category = selectedCategory;
      if (searchTerm) filters.search = searchTerm;
      const queryParams = new URLSearchParams(filters).toString();
      const response = await fetch(
        `http://localhost:8000/product/filter/?${queryParams}`,
      );
      if (!response.ok) throw new Error("Failed to fetch products");
      const data = await response.json();
      setProducts(data);
    } catch (error) {
      console.error(error);
    }
  };

  const handleCategoryChange = (
    event: React.ChangeEvent<HTMLSelectElement>,
  ) => {
    setSelectedCategory(event.target.value);
  };

  const handleSearch = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
  };

  const handleAddNew = () => {
    setIsAddingNew(true);
  };

  const handleEdit = (id: number) => {
    // Handle edit mode
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm("Are you sure you want to delete this product?"))
      return;
    try {
      const response = await fetch(`http://localhost:8000/product/d/${id}/`, {
        method: "DELETE",
        headers: {
          "X-CSRFToken": getCookie("csrftoken") || "",
        },
      });
      if (!response.ok) throw new Error("Failed to delete product");
      fetchProducts();
    } catch (error) {
      console.error(error);
    }
  };

  const handleSave = async (id: number, data: Partial<ProductType>) => {
    try {
      const url = id === -1 ? "/product/list/" : `/product/d/${id}/`;
      const method = id === -1 ? "POST" : "PUT";
      const productData = id === -1 ? { ...data, id: undefined } : data;

      const response = await fetch(`http://localhost:8000${url}`, {
        method,
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken") || "",
        },
        body: JSON.stringify(productData),
      });

      if (!response.ok) throw new Error("Failed to save product");
      fetchProducts();
      setIsAddingNew(false);
    } catch (error) {
      console.error(error);
    }
  };

  const handleCancel = (id: number) => {
    if (id === -1) {
      setIsAddingNew(false);
    }
  };

  const filteredProducts = products.filter((product) => {
    const matchesCategory =
      !selectedCategory || product.category?.id.toString() === selectedCategory;
    const matchesSearch =
      !searchTerm ||
      product.name.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  return (
    <div className="container">
      <h1>Our Products</h1>

      <div className="add-product-section">
        <button className="add-btn" onClick={handleAddNew}>
          Add New Product
        </button>
      </div>

      <div className="filters">
        <select
          value={selectedCategory}
          onChange={handleCategoryChange}
          className="category-filter"
        >
          <option value="">All Categories</option>
          {categories.map((category) => (
            <option key={category.id} value={category.id}>
              {category.title}
            </option>
          ))}
        </select>

        <input
          type="text"
          placeholder="Search products..."
          value={searchTerm}
          onChange={handleSearch}
          className="search-input"
        />
      </div>
      {/* Categories Section */}
      <div className="categories-section">
        <div className="categories-header">
          <h2>Categories</h2>
          <button
            className="add-category-btn"
            onClick={() => setIsAddingCategory(!isAddingCategory)}
          >
            {isAddingCategory ? "Cancel" : "Add Category"}
          </button>
        </div>

        {isAddingCategory && (
          <div className="add-category-form">
            <div className="form-group">
              <input
                type="text"
                value={newCategory.title}
                onChange={(e) =>
                  setNewCategory((prev) => ({
                    ...prev,
                    title: e.target.value,
                  }))
                }
                placeholder="Category Title"
                className="category-input"
                required
              />
            </div>
            <div className="form-group">
              <textarea
                value={newCategory.description}
                onChange={(e) =>
                  setNewCategory((prev) => ({
                    ...prev,
                    description: e.target.value,
                  }))
                }
                placeholder="Category Description"
                className="category-textarea"
              />
            </div>
            <button className="save-category-btn" onClick={handleAddCategory}>
              Save Category
            </button>
          </div>
        )}

        <div className="categories-list">
          {categories.map((category) => (
            <div key={category.id} className="category-card">
              <h3 className="category-title">{category.title}</h3>
              {category.description && (
                <p className="category-description">{category.description}</p>
              )}
            </div>
          ))}
        </div>
      </div>
      <div className="products-grid">
        {isAddingNew && (
          <Product
            product={{
              id: -1,
              name: "",
              price: 0,
              quantity: 0,
            }}
            categories={categories}
            onEdit={handleEdit}
            onDelete={handleDelete}
            onSave={handleSave}
            onCancel={handleCancel}
          />
        )}
        {filteredProducts.map((product) => (
          <Product
            key={product.id}
            product={product}
            categories={categories}
            onEdit={handleEdit}
            onDelete={handleDelete}
            onSave={handleSave}
            onCancel={handleCancel}
          />
        ))}
      </div>
    </div>
  );
};

function getCookie(name: string) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

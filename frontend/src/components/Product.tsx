import React, { useState } from "react";
import { Product as ProductType, Category } from "../types/Product";

interface ProductProps {
  product: ProductType;
  categories: Category[];
  onEdit: (id: number) => void;
  onDelete: (id: number) => void;
  onSave: (id: number, data: Partial<ProductType>) => void;
  onCancel: (id: number) => void;
}

export const Product: React.FC<ProductProps> = ({
  product,
  categories,
  onEdit,
  onDelete,
  onSave,
  onCancel,
}) => {
  const [isEditing, setIsEditing] = useState(product.id === -1);
  const [editedProduct, setEditedProduct] = useState(product);
  const handleCategoryChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const categoryId = e.target.value;
    console.log(categoryId);
    const selectedCategory = categories.find((cat) => cat.id === categoryId);
    console.log(selectedCategory);
    console.log(categories);
    setEditedProduct((prev) => ({
      ...prev,
      category: selectedCategory || undefined,
    }));
  };

  const handleEdit = () => {
    setIsEditing(true);
    onEdit(product.id);
  };

  const handleDelete = () => {
    if (window.confirm("Are you sure you want to delete this product?")) {
      onDelete(product.id);
    }
  };

  const handleSave = () => {
    if (!editedProduct.name || !editedProduct.price) {
      alert("Please fill in all required fields (Name, Price, and Category)");
      return;
    }
    onSave(product.id, editedProduct);
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditedProduct(product);
    setIsEditing(false);
    onCancel(product.id);
  };

  const handleInputChange = (
    field: keyof ProductType,
    value: string | number,
  ) => {
    setEditedProduct((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  // const handleCategoryChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
  //   const categoryId = parseInt(e.target.value);
  //   const categoryName = e.target.options[e.target.selectedIndex].text;
  //   setEditedProduct((prev) => ({
  //     ...prev,
  //     category: categoryId ? { id: categoryId, name: categoryName } : undefined,
  //   }));
  // };

  const formattedPrice = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(product.price);

  const quantityMessage =
    product.quantity > 0 ? `In Stock: ${product.quantity}` : "Out of Stock";

  return (
    <div className={`product-card ${isEditing ? "editing" : ""}`}>
      <div className="product-content">
        {isEditing ? (
          <>
            <input
              type="text"
              value={editedProduct.name}
              onChange={(e) => handleInputChange("name", e.target.value)}
              placeholder="Product Name"
              required
            />
            <input
              type="number"
              value={editedProduct.price}
              onChange={(e) =>
                handleInputChange("price", parseFloat(e.target.value))
              }
              step="0.01"
              min="0"
              required
            />
            <select
              value={editedProduct.category?.id || ""}
              onChange={handleCategoryChange}
              required
              className="category-select"
              style={{ color: "#333", backgroundColor: "white" }}
            >
              <option value="">Select Category</option>
              {categories.map((cat) => (
                <option key={cat.id} value={cat.id}>
                  {cat.title}
                </option>
              ))}
            </select>
            <input
              type="text"
              value={editedProduct.description || ""}
              onChange={(e) => handleInputChange("description", e.target.value)}
              placeholder="Description"
            />
            <input
              type="text"
              value={editedProduct.brand || ""}
              onChange={(e) => handleInputChange("brand", e.target.value)}
              placeholder="Brand"
            />
            <input
              type="number"
              value={editedProduct.quantity || 0}
              onChange={(e) =>
                handleInputChange("quantity", parseInt(e.target.value))
              }
              min="0"
              required
            />
          </>
        ) : (
          <>
            <div className="product-name">{product.name}</div>
            <div className="product-price">{formattedPrice}</div>
            <div className="product-category">
              {product.category?.title || "Uncategorized"}
            </div>
            {product.description && (
              <div className="product-description">{product.description}</div>
            )}
            {product.brand && (
              <div className="product-brand">{product.brand}</div>
            )}
            <div className="product-quantity">{quantityMessage}</div>
          </>
        )}
      </div>
      <div className="product-actions">
        {isEditing ? (
          <>
            <button className="save-btn" onClick={handleSave}>
              Save
            </button>
            <button className="cancel-btn" onClick={handleCancel}>
              Cancel
            </button>
          </>
        ) : (
          <>
            <button className="edit-btn" onClick={handleEdit}>
              Edit
            </button>
            <button className="delete-btn" onClick={handleDelete}>
              Delete
            </button>
          </>
        )}
      </div>
    </div>
  );
};

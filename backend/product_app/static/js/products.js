document.addEventListener('DOMContentLoaded', function() {
    // Initial load of products
    fetchProducts();
    // Load categories for filter
    fetchCategories();
    
    // Add event listeners
    document.getElementById('categoryFilter').addEventListener('change', handleCategoryFilter);
    document.getElementById('searchInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            handleSearch();
        }
    });
    
    // Add new product button handler
    document.getElementById('addNewProductBtn').addEventListener('click', showAddProductForm);
});

// Debounce function to limit API calls
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

async function fetchProducts(filters = {}) {
    try {
        const queryParams = new URLSearchParams(filters).toString();
        const response = await fetch(`/product/filter/?${queryParams}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const products = await response.json();
        console.log('Fetched products:', products);
        renderProducts(products);
    } catch (error) {
        console.error('Error fetching products:', error);
        const productsGrid = document.getElementById('products-grid');
        productsGrid.innerHTML = '<p class="error">Error loading products. Please try again later.</p>';
    }
}

async function fetchCategories() {
    try {
        const response = await fetch('/product/cat/');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const categories = await response.json();
        console.log('Fetched categories:', categories);
        populateCategoryFilter(categories);
        populateCategorySelect(categories); // Populate the add product form category select
    } catch (error) {
        console.error('Error fetching categories:', error);
    }
}

function populateCategoryFilter(categories) {
    const select = document.getElementById('categoryFilter');
    select.innerHTML = '<option value="">All Categories</option>';
    
    categories.forEach(category => {
        const option = document.createElement('option');
        option.value = category.id;
        option.textContent = category.name;
        select.appendChild(option);
    });
}

function populateCategorySelect(categories) {
    const select = document.getElementById('productCategory');
    select.innerHTML = '<option value="">Select Category</option>';
    
    categories.forEach(category => {
        const option = document.createElement('option');
        option.value = category.id;
        option.textContent = category.name;
        select.appendChild(option);
    });
}

function renderProducts(products) {
    const productsGrid = document.getElementById('products-grid');
    productsGrid.innerHTML = ''; // Clear existing content

    if (!products || products.length === 0) {
        productsGrid.innerHTML = '<p class="no-products">No products found</p>';
        return;
    }

    products.forEach(product => {
        const productCard = createProductCard(product);
        productsGrid.appendChild(productCard);
    });
}

function createProductCard(product) {
    const card = document.createElement('div');
    card.className = 'product-card';
    card.dataset.productId = product.id;
    
    // Format price with commas for thousands
    const formattedPrice = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(product.price);
    
    // Format quantity with appropriate message
    const quantityMessage = product.quantity > 0 
        ? `In Stock: ${product.quantity}`
        : 'Out of Stock';
    
    // Format category name
    const categoryName = product.category?.name || 'Uncategorized';
    
    card.innerHTML = `
        <div class="product-content">
            <div class="product-name" data-field="name">${product.name}</div>
            <div class="product-price" data-field="price">${formattedPrice}</div>
            <div class="product-category" data-field="category">${categoryName}</div>
            ${product.description ? `<div class="product-description" data-field="description">${product.description}</div>` : ''}
            ${product.brand ? `<div class="product-brand" data-field="brand">${product.brand}</div>` : ''}
            <div class="product-quantity" data-field="quantity">${quantityMessage}</div>
        </div>
        <div class="product-actions">
            <button class="edit-btn" onclick="toggleEditMode('${product.id}')">Edit</button>
            <button class="delete-btn" onclick="deleteProduct('${product.id}')">Delete</button>
            <button class="save-btn" onclick="saveProductChanges('${product.id}')" style="display: none;">Save</button>
            <button class="cancel-btn" onclick="cancelEdit('${product.id}')" style="display: none;">Cancel</button>
        </div>
    `;
    
    return card;
}

function showAddProductForm() {
    const productsGrid = document.getElementById('products-grid');
    const newProductCard = createEmptyProductCard();
    productsGrid.insertBefore(newProductCard, productsGrid.firstChild);
    toggleEditMode('new');
}

function createEmptyProductCard() {
    const card = document.createElement('div');
    card.className = 'product-card';
    card.dataset.productId = 'new';
    
    card.innerHTML = `
        <div class="product-content">
            <div class="product-name" data-field="name">New Product</div>
            <div class="product-price" data-field="price">0.00</div>
            <div class="product-category" data-field="category">Select Category</div>
            <div class="product-description" data-field="description"></div>
            <div class="product-brand" data-field="brand"></div>
            <div class="product-quantity" data-field="quantity">0</div>
        </div>
        <div class="product-actions">
            <button class="save-btn" onclick="saveProductChanges('new')">Save</button>
            <button class="cancel-btn" onclick="cancelEdit('new')">Cancel</button>
        </div>
    `;
    
    return card;
}

function toggleEditMode(productId) {
    const card = document.querySelector(`.product-card[data-product-id="${productId}"]`);
    if (!card) return;

    const content = card.querySelector('.product-content');
    const editBtn = card.querySelector('.edit-btn');
    const deleteBtn = card.querySelector('.delete-btn');
    const saveBtn = card.querySelector('.save-btn');
    const cancelBtn = card.querySelector('.cancel-btn');
    
    // Toggle button visibility
    if (editBtn) editBtn.style.display = 'none';
    if (deleteBtn) deleteBtn.style.display = 'none';
    if (saveBtn) saveBtn.style.display = 'block';
    if (cancelBtn) cancelBtn.style.display = 'block';
    
    // Add editing class to card
    card.classList.add('editing');
    
    // Make all fields editable
    content.querySelectorAll('[data-field]').forEach(field => {
        const currentValue = field.textContent;
        const fieldName = field.dataset.field;
        
        if (fieldName === 'price') {
            const numericValue = currentValue.replace(/[^0-9.-]+/g, '');
            field.innerHTML = `<input type="number" value="${numericValue}" step="0.01" min="0" required>`;
        } else if (fieldName === 'quantity') {
            const numericValue = currentValue.match(/\d+/)?.[0] || '0';
            field.innerHTML = `<input type="number" value="${numericValue}" min="0" required>`;
        } else if (fieldName === 'category') {
            const select = document.createElement('select');
            select.required = true;
            select.innerHTML = '<option value="">Select Category</option>';
            const categoryFilter = document.getElementById('categoryFilter');
            Array.from(categoryFilter.options).forEach(option => {
                if (option.value) {
                    const newOption = document.createElement('option');
                    newOption.value = option.value;
                    newOption.textContent = option.textContent;
                    if (option.textContent === currentValue) {
                        newOption.selected = true;
                    }
                    select.appendChild(newOption);
                }
            });
            field.innerHTML = '';
            field.appendChild(select);
        } else {
            // For text fields, preserve empty values for optional fields
            const isRequired = fieldName === 'name';
            const value = currentValue.trim();
            field.innerHTML = `<input type="text" value="${value}" ${isRequired ? 'required' : ''}>`;
        }
    });
}

function cancelEdit(productId) {
    if (productId === 'new') {
        // If it's a new product card, just remove it
        const card = document.querySelector(`.product-card[data-product-id="new"]`);
        if (card) {
            card.remove();
        }
        return;
    }

    const card = document.querySelector(`.product-card[data-product-id="${productId}"]`);
    if (!card) return;

    // Show edit and delete buttons, hide save and cancel
    const editBtn = card.querySelector('.edit-btn');
    const deleteBtn = card.querySelector('.delete-btn');
    const saveBtn = card.querySelector('.save-btn');
    const cancelBtn = card.querySelector('.cancel-btn');
    
    if (editBtn) editBtn.style.display = 'block';
    if (deleteBtn) deleteBtn.style.display = 'block';
    if (saveBtn) saveBtn.style.display = 'none';
    if (cancelBtn) cancelBtn.style.display = 'none';
    
    // Reset the card content to its original state
    fetch(`/product/d/${productId}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(product => {
            const newCard = createProductCard(product);
            card.replaceWith(newCard);
        })
        .catch(error => {
            console.error('Error refreshing product:', error);
            alert('Error refreshing product. Please try again.');
        });
}

async function saveProductChanges(productId) {
    const card = document.querySelector(`.product-card[data-product-id="${productId}"]`);
    if (!card) return;

    // Get all input and select elements
    const inputs = card.querySelectorAll('input, select');
    
    // Create product data object with existing values as fallback
    const productData = {
        name: card.querySelector('[data-field="name"] input')?.value || '',
        price: parseFloat(card.querySelector('[data-field="price"] input')?.value || '0'),
        category: card.querySelector('[data-field="category"] select')?.value || '',
        description: card.querySelector('[data-field="description"] input')?.value || '',
        brand: card.querySelector('[data-field="brand"] input')?.value || '',
        quantity: parseInt(card.querySelector('[data-field="quantity"] input')?.value || '0')
    };

    // Validate required fields
    if (!productData.name || !productData.price || !productData.category) {
        alert('Please fill in all required fields (Name, Price, and Category)');
        return;
    }

    try {
        const url = productId === 'new' ? '/product/list/' : `/product/d/${productId}/`;
        const method = productId === 'new' ? 'POST' : 'PUT';
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(productData)
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
        }

        // Refresh the products list
        await fetchProducts();
        alert(productId === 'new' ? 'Product added successfully!' : 'Product updated successfully!');
    } catch (error) {
        console.error('Error saving product:', error);
        alert(error.message || 'Error saving product. Please try again.');
    }
}

function handleCategoryFilter(event) {
    const categoryId = event.target.value;
    if (categoryId) {
        fetch(`/product/cat/${categoryId}`)
            .then(response => response.json())
            .then(products => renderProducts(products))
            .catch(error => {
                console.error('Error fetching products by category:', error);
                const productsGrid = document.getElementById('products-grid');
                productsGrid.innerHTML = '<p class="error">Error loading products. Please try again later.</p>';
            });
    } else {
        fetchProducts();
    }
}

function handleSearch() {
    const searchTerm = document.getElementById('searchInput').value;
    const filters = searchTerm ? { search: searchTerm } : {};
    fetchProducts(filters);
}

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function deleteProduct(productId) {
    if (!confirm('Are you sure you want to delete this product?')) {
        return;
    }

    try {
        const response = await fetch(`/product/d/${productId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Remove the card from the DOM
        const card = document.querySelector(`.product-card[data-product-id="${productId}"]`);
        if (card) {
            card.remove();
        }

        // Show success message
        alert('Product deleted successfully!');
    } catch (error) {
        console.error('Error deleting product:', error);
        alert('Error deleting product. Please try again.');
    }
} 
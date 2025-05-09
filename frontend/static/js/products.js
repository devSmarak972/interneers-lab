document.addEventListener('DOMContentLoaded', function() {
    // Initial load of products
    fetchProducts();
    // Load categories for filter
    fetchCategories();
    
    // Add event listeners for filters
    document.getElementById('categoryFilter').addEventListener('change', handleCategoryFilter);
    document.getElementById('searchInput').addEventListener('input', debounce(handleSearch, 300));
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
        const response = await fetch(`/api/products/?${queryParams}`);
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
        const response = await fetch('/api/categories/');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const categories = await response.json();
        console.log('Fetched categories:', categories);
        populateCategoryFilter(categories);
    } catch (error) {
        console.error('Error fetching categories:', error);
    }
}

function populateCategoryFilter(categories) {
    const select = document.getElementById('categoryFilter');
    select.innerHTML = '<option value="">All Categories</option>'; // Reset options
    
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
    
    card.innerHTML = `
        <div class="product-name">${product.name}</div>
        <div class="product-price">$${product.price.toFixed(2)}</div>
        <div class="product-category">${product.category?.name || 'Uncategorized'}</div>
        <div class="product-description">${product.description || ''}</div>
    `;
    
    return card;
}

function handleCategoryFilter(event) {
    const categoryId = event.target.value;
    const filters = categoryId ? { category: categoryId } : {};
    fetchProducts(filters);
}

function handleSearch(event) {
    const searchTerm = event.target.value;
    const filters = searchTerm ? { search: searchTerm } : {};
    fetchProducts(filters);
} 
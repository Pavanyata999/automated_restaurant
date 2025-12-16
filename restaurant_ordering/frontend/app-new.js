const API_BASE = 'http://localhost:8001/api/v1';
let selectedTable = null;
let cart = [];
let menuItems = [];
let tables = [];

function formatCurrency(amount) {
    return `₹${amount.toFixed(0)}`;
}

async function fetchMenu() {
    const response = await fetch(`${API_BASE}/menu`);
    menuItems = await response.json();
    renderMenu();
}

async function fetchTables() {
    const response = await fetch(`${API_BASE}/tables`);
    tables = await response.json();
    renderTables();
}

function renderTables() {
    const container = document.getElementById('tables-container');
    container.innerHTML = tables.map(table => `
        <div class="table-card bg-white p-4 rounded-lg shadow-md cursor-pointer ${selectedTable === table.id ? 'ring-2 ring-orange-500' : ''}" onclick="selectTable(${table.id})">
            <div class="text-center"><h3 class="font-bold text-lg">${table.number}</h3></div>
        </div>
    `).join('');
}

function renderMenu() {
    const container = document.getElementById('menu-container');
    container.innerHTML = menuItems.map(item => `
        <div class="menu-item-card bg-white rounded-lg shadow-md overflow-hidden">
            <img src="${item.image}" alt="${item.name}" class="w-full h-48 object-cover">
            <div class="p-6">
                <h3 class="text-xl font-bold mb-2">${item.name}</h3>
                <p class="text-gray-600 mb-4 text-sm">${item.description}</p>
                <div class="flex justify-between items-center">
                    <span class="text-2xl font-bold text-orange-600">${formatCurrency(item.price)}</span>
                    <button onclick="addToCart(${item.id})" class="bg-orange-500 text-white px-4 py-2 rounded-lg hover:bg-orange-600">Add</button>
                </div>
            </div>
        </div>
    `).join('');
}

function selectTable(tableId) {
    selectedTable = tableId;
    renderTables();
}

function addToCart(itemId) {
    const menuItem = menuItems.find(item => item.id === itemId);
    if (!menuItem) return;
    
    const existingItem = cart.find(item => item.id === itemId);
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({id: menuItem.id, name: menuItem.name, price: menuItem.price, quantity: 1});
    }
    updateCart();
    updateHeader();
}

function updateHeader() {
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    const totalPrice = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    
    document.getElementById('cart-count').textContent = `${totalItems} items`;
    document.getElementById('cart-total').textContent = formatCurrency(totalPrice);
}

function updateCart() {
    const cartItems = document.getElementById('cart-items');
    const cartSummary = document.getElementById('cart-summary');
    
    if (cart.length === 0) {
        cartItems.innerHTML = '<p class="text-gray-500 text-center py-8">Your cart is empty</p>';
        cartSummary.classList.add('hidden');
    } else {
        const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        cartItems.innerHTML = cart.map(item => `
            <div class="flex justify-between py-2 border-b">
                <span>${item.name} x ${item.quantity}</span>
                <span>${formatCurrency(item.price * item.quantity)}</span>
            </div>
        `).join('');
        
        document.getElementById('cart-summary-total').textContent = formatCurrency(total);
        cartSummary.classList.remove('hidden');
    }
}

async function placeOrder() {
    if (!selectedTable) {
        alert('Please select a table');
        return;
    }
    if (cart.length === 0) {
        alert('Cart is empty');
        return;
    }
    
    const response = await fetch(`${API_BASE}/orders`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            table_id: selectedTable, 
            items: cart.map(item => ({menu_item_id: item.id, quantity: item.quantity}))
        })
    });
    
    if (response.ok) {
        alert('Order placed!');
        cart = [];
        updateCart();
        updateHeader();
    }
}

document.addEventListener('DOMContentLoaded', function() {
    fetchMenu();
    fetchTables();
    const btn = document.getElementById('place-order-btn');
    if (btn) btn.addEventListener('click', placeOrder);
});

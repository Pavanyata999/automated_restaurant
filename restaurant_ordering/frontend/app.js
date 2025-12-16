// Global state
let selectedTable = null;
let cart = [];
let menuItems = [];
let tables = [];
let orders = [];

// API base URL
const API_BASE = 'http://localhost:8001/api/v1';

// Utility functions
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toast-message');
    
    toastMessage.textContent = message;
    toast.className = `fixed bottom-4 right-4 px-6 py-3 rounded-lg shadow-lg transform transition-transform duration-300 ${
        type === 'success' ? 'bg-green-500' : 'bg-red-500'
    } text-white`;
    
    setTimeout(() => {
        toast.classList.remove('translate-y-full');
    }, 100);
    
    setTimeout(() => {
        toast.classList.add('translate-y-full');
    }, 3000);
}

function formatCurrency(amount) {
    return `$${amount.toFixed(2)}`;
}

// API functions
async function fetchMenu() {
    try {
        const response = await fetch(`${API_BASE}/menu`);
        menuItems = await response.json();
        renderMenu();
    } catch (error) {
        console.error('Error fetching menu:', error);
        showToast('Failed to load menu', 'error');
    }
}

async function fetchTables() {
    try {
        const response = await fetch(`${API_BASE}/tables`);
        tables = await response.json();
        renderTables();
    } catch (error) {
        console.error('Error fetching tables:', error);
        showToast('Failed to load tables', 'error');
    }
}

async function fetchOrders() {
    try {
        const response = await fetch(`${API_BASE}/orders`);
        orders = await response.json();
        renderOrders();
    } catch (error) {
        console.error('Error fetching orders:', error);
    }
}

async function placeOrder() {
    if (!selectedTable) {
        showToast('Please select a table first', 'error');
        return;
    }
    
    if (cart.length === 0) {
        showToast('Your cart is empty', 'error');
        return;
    }

    try {
        const orderData = {
            table_id: selectedTable,
            items: cart.map(item => ({
                menu_item_id: item.id,
                quantity: item.quantity
            }))
        };
        
        const response = await fetch(`${API_BASE}/orders`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(orderData)
        });

        if (response.ok) {
            const order = await response.json();
            showToast('Order placed successfully!');
            cart = [];
            updateCart();
            fetchOrders();
        } else {
            showToast('Failed to place order', 'error');
        }
    } catch (error) {
        console.error('Error placing order:', error);
        showToast('Failed to place order', 'error');
    }
}

// Rendering functions
function renderTables() {
    const container = document.getElementById('tables-container');
    container.innerHTML = tables.map(table => `
        <div class="table-card bg-white p-4 rounded-lg shadow-md cursor-pointer transition hover:shadow-lg ${
            selectedTable === table.id ? 'ring-2 ring-orange-500' : ''
        }" onclick="selectTable(${table.id})">
            <div class="text-center">
                <i class="fas fa-chair text-2xl mb-2 text-gray-600"></i>
                <h3 class="font-bold text-lg">${table.number}</h3>
                <p class="text-sm text-gray-500">Capacity: ${table.capacity}</p>
                <span class="inline-block mt-2 px-2 py-1 text-xs rounded-full ${
                    table.status === 'available' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                }">
                    ${table.status}
                </span>
            </div>
        </div>
    `).join('');
}

function renderMenu() {
    const container = document.getElementById('menu-container');
    container.innerHTML = menuItems.map(item => `
        <div class="menu-item-card bg-white rounded-lg shadow-md overflow-hidden">
            <div class="p-6">
                <div class="flex justify-between items-start mb-4">
                    <h3 class="text-xl font-bold text-gray-800">${item.name}</h3>
                    <span class="text-2xl font-bold text-orange-600">${formatCurrency(item.price)}</span>
                </div>
                <p class="text-gray-600 mb-4">${item.description || 'Delicious item'}</p>
                <div class="flex justify-between items-center">
                    <span class="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm">${item.category}</span>
                    <button onclick="addToCart(${item.id})" class="bg-orange-500 text-white px-4 py-2 rounded-lg hover:bg-orange-600 transition">
                        <i class="fas fa-plus mr-2"></i>Add to Cart
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

function updateCart() {
    const cartItems = document.getElementById('cart-items');
    const cartSummary = document.getElementById('cart-summary');
    const cartCount = document.getElementById('cart-count');
    const cartTotal = document.getElementById('cart-total');
    const cartSummaryTotal = document.getElementById('cart-summary-total');

    if (cart.length === 0) {
        cartItems.innerHTML = '<p class="text-gray-500 text-center py-8">Your cart is empty. Add items from the menu above.</p>';
        cartSummary.classList.add('hidden');
        cartCount.textContent = '0 items';
        cartTotal.textContent = '$0.00';
    } else {
        cartItems.innerHTML = cart.map(item => `
            <div class="flex justify-between items-center py-2 border-b">
                <div>
                    <h4 class="font-semibold">${item.name}</h4>
                    <p class="text-sm text-gray-500">${formatCurrency(item.price)} x ${item.quantity}</p>
                </div>
                <div class="flex items-center space-x-2">
                    <button onclick="updateQuantity(${item.id}, -1)" class="text-red-500 hover:text-red-700">
                        <i class="fas fa-minus-circle"></i>
                    </button>
                    <span class="font-semibold">${item.quantity}</span>
                    <button onclick="updateQuantity(${item.id}, 1)" class="text-green-500 hover:text-green-700">
                        <i class="fas fa-plus-circle"></i>
                    </button>
                    <span class="font-bold ml-4">${formatCurrency(item.price * item.quantity)}</span>
                </div>
            </div>
        `).join('');

        const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        cartSummary.classList.remove('hidden');
        cartCount.textContent = `${cart.reduce((sum, item) => sum + item.quantity, 0)} items`;
        cartTotal.textContent = formatCurrency(total);
        cartSummaryTotal.textContent = formatCurrency(total);
    }
}

function renderOrders() {
    const container = document.getElementById('orders-container');
    
    if (orders.length === 0) {
        container.innerHTML = '<p class="text-gray-500 text-center py-8">No orders yet.</p>';
    } else {
        container.innerHTML = orders.map(order => {
            const table = tables.find(t => t.id === order.table_id);
            return `
                <div class="bg-white rounded-lg shadow-md p-6">
                    <div class="flex justify-between items-start mb-4">
                        <div>
                            <h3 class="text-lg font-bold">Order #${order.id}</h3>
                            <p class="text-gray-600">Table: ${table ? table.number : 'Unknown'}</p>
                        </div>
                        <span class="px-3 py-1 rounded-full text-sm font-semibold ${
                            order.status === 'completed' ? 'bg-green-100 text-green-800' :
                            order.status === 'preparing' ? 'bg-yellow-100 text-yellow-800' :
                            order.status === 'cancelled' ? 'bg-red-100 text-red-800' :
                            'bg-blue-100 text-blue-800'
                        }">
                            ${order.status}
                        </span>
                    </div>
                    <div class="mb-4">
                        <h4 class="font-semibold mb-2">Items:</h4>
                        ${order.items.map(item => {
                            const menuItem = menuItems.find(m => m.id === item.menu_item_id);
                            return `
                                <div class="flex justify-between py-1">
                                    <span>${menuItem ? menuItem.name : 'Unknown item'} x ${item.quantity}</span>
                                    <span>${formatCurrency((menuItem ? menuItem.price : 0) * item.quantity)}</span>
                                </div>
                            `;
                        }).join('')}
                    </div>
                    <div class="flex justify-between items-center pt-4 border-t">
                        <span class="text-lg font-bold">Total: ${formatCurrency(order.total)}</span>
                    </div>
                </div>
            `;
        }).join('');
    }
}

// Event handlers
function selectTable(tableId) {
    selectedTable = tableId;
    renderTables();
    showToast(`Table ${tables.find(t => t.id === tableId)?.number} selected`);
}

function addToCart(itemId) {
    const menuItem = menuItems.find(item => item.id === itemId);
    if (!menuItem) return;

    const existingItem = cart.find(item => item.id === itemId);
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: menuItem.id,
            name: menuItem.name,
            price: menuItem.price,
            quantity: 1
        });
    }

    updateCart();
    showToast(`${menuItem.name} added to cart`);
}

function updateQuantity(itemId, change) {
    const item = cart.find(item => item.id === itemId);
    if (!item) return;

    item.quantity += change;
    if (item.quantity <= 0) {
        cart = cart.filter(item => item.id !== itemId);
    }

    updateCart();
}

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    fetchMenu();
    fetchTables();
    fetchOrders();

    // Set up event listeners
    document.getElementById('place-order-btn').addEventListener('click', placeOrder);

    // Auto-refresh orders every 5 seconds
    setInterval(fetchOrders, 5000);
});

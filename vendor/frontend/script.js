const API_URL = 'http://127.0.0.1:8000/vendors';

// State management
let vendorsData = [];

// DOM Elements
const locationInput = document.getElementById('locationInput');
const serviceSelect = document.getElementById('serviceSelect');
const searchBtn = document.getElementById('searchBtn');

const searchInput = document.getElementById('searchInput');
const ratingFilter = document.getElementById('ratingFilter');
const sortSelect = document.getElementById('sortSelect');
const vendorGrid = document.getElementById('vendorGrid');
const loadingState = document.getElementById('loadingState');
const errorState = document.getElementById('errorState');
const emptyState = document.getElementById('emptyState');
const initialState = document.getElementById('initialState'); // new

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    // Optionally default to "Madurai"
    locationInput.value = "Madurai";
    showState('initial');
    setupEventListeners();
});

// Setup event listeners for filtering and sorting
function setupEventListeners() {
    searchBtn.addEventListener('click', fetchVendors);

    // Live frontend filtering
    searchInput.addEventListener('input', updateUI);
    ratingFilter.addEventListener('change', updateUI);
    sortSelect.addEventListener('change', updateUI);
}

// Fetch data from API
async function fetchVendors() {
    showState('loading');

    const locationVal = encodeURIComponent(locationInput.value.trim() || "Madurai");
    const serviceVal = encodeURIComponent(serviceSelect.value);

    try {
        const urlArgs = `${API_URL}?location=${locationVal}&service=${serviceVal}`;
        const response = await fetch(urlArgs);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        vendorsData = await response.json();
        updateUI();
    } catch (error) {
        console.error('Error fetching vendors:', error);
        showState('error');
    }
}

// Update UI based on current state and filters
function updateUI() {
    let filteredData = filterVendors(vendorsData);
    filteredData = sortVendors(filteredData);

    if (filteredData.length === 0) {
        showState('empty');
    } else {
        renderVendors(filteredData);
        showState('content');
    }
}

// Filter logic
function filterVendors(data) {
    const searchTerm = searchInput.value.toLowerCase().trim();
    const minRating = parseFloat(ratingFilter.value);

    return data.filter(vendor => {
        const matchesSearch = vendor.name.toLowerCase().includes(searchTerm) ||
            (vendor.address && vendor.address.toLowerCase().includes(searchTerm));
        const vendorRating = vendor.rating || 0;
        const matchesRating = vendorRating >= minRating;

        return matchesSearch && matchesRating;
    });
}

// Sort logic
function sortVendors(data) {
    const sortBy = sortSelect.value;

    return [...data].sort((a, b) => {
        const valA = a[sortBy] || 0;
        const valB = b[sortBy] || 0;
        // All sorts are High to Low descending
        return valB - valA;
    });
}

// Render vendor cards to the grid
function renderVendors(vendors) {
    vendorGrid.innerHTML = '';

    vendors.forEach(vendor => {
        const card = document.createElement('div');
        card.className = 'vendor-card';

        // Handle optional missing data cleanly
        const score = vendor.score !== undefined ? vendor.score.toFixed(1) : 'N/A';
        const rating = vendor.rating !== undefined ? vendor.rating.toFixed(1) : 'N/A';
        const reviews = vendor.reviews !== undefined ? vendor.reviews.toLocaleString() : '0';
        const address = vendor.address || 'Address not provided';

        card.innerHTML = `
            <div class="vendor-header">
                <h2 class="vendor-name">${escapeHTML(vendor.name)}</h2>
                <p class="vendor-address">${escapeHTML(address)}</p>
            </div>
            <div class="vendor-stats">
                <div class="stat-group">
                    <span class="stat-value">⭐ ${rating}</span>
                    <span class="stat-label">Rating</span>
                </div>
                <div class="stat-group">
                    <span class="stat-value">${reviews}</span>
                    <span class="stat-label">Reviews</span>
                </div>
                <div class="stat-group">
                    <span class="badge-score">${score} pts</span>
                </div>
            </div>
        `;

        vendorGrid.appendChild(card);
    });
}

// Manage UI states (initial, loading, error, empty, content)
function showState(state) {
    if (initialState) initialState.classList.add('hidden');
    loadingState.classList.add('hidden');
    errorState.classList.add('hidden');
    emptyState.classList.add('hidden');
    vendorGrid.classList.add('hidden');

    if (state === 'initial') {
        if (initialState) initialState.classList.remove('hidden');
    } else if (state === 'loading') {
        loadingState.classList.remove('hidden');
    } else if (state === 'error') {
        errorState.classList.remove('hidden');
    } else if (state === 'empty') {
        emptyState.classList.remove('hidden');
    } else if (state === 'content') {
        vendorGrid.classList.remove('hidden');
    }
}

// Utility to prevent XSS
function escapeHTML(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

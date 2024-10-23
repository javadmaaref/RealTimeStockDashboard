// app/static/js/main.js
document.addEventListener('DOMContentLoaded', () => {
    // DOM
    const ui = {
        loginBtn: document.getElementById('loginBtn'),
        registerBtn: document.getElementById('registerBtn'),
        logoutBtn: document.getElementById('logoutBtn'),
        authForms: document.getElementById('authForms'),
        loginForm: document.getElementById('loginForm'),
        registerForm: document.getElementById('registerForm'),
        getStockBtn: document.getElementById('getStockBtn'),
        watchlist: document.getElementById('watchlist'),
        addToWatchlistForm: document.getElementById('addToWatchlistForm')
    };

    let stockChart = null;

    // Event listeners
    ui.loginBtn.onclick = () => {
        ui.authForms.classList.remove('hidden');
        ui.loginForm.classList.remove('hidden');
        ui.registerForm.classList.add('hidden');
    };

    ui.registerBtn.onclick = () => {
        ui.authForms.classList.remove('hidden');
        ui.registerForm.classList.remove('hidden');
        ui.loginForm.classList.add('hidden');
    };

    // Form submissions
    ui.loginForm.onsubmit = async (e) => {
        e.preventDefault();
        const formData = {
            username: document.getElementById('loginUsername').value,
            password: document.getElementById('loginPassword').value
        };

        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: new URLSearchParams(formData)
            });

            const data = await response.json();
            alert(response.ok ? data.message : data.error);
            if (response.ok) updateUIAfterLogin();
        } catch (err) {
            alert('Login failed. Please try again.');
        }
    };

    ui.registerForm.onsubmit = async (e) => {
        e.preventDefault();
        const formData = {
            username: document.getElementById('registerUsername').value,
            password: document.getElementById('registerPassword').value,
            phone: document.getElementById('registerPhone').value,
            email: document.getElementById('registerEmail').value
        };

        try {
            const response = await fetch('/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: new URLSearchParams(formData)
            });

            const data = await response.json();
            alert(response.ok ? data.message : data.error);
            if (response.ok) updateUIAfterLogin();
        } catch (err) {
            alert('Registration failed. Please try again.');
        }
    };

    ui.logoutBtn.onclick = async () => {
        try {
            const response = await fetch('/logout');
            const data = await response.json();
            if (response.ok) {
                alert(data.message);
                updateUIAfterLogout();
            }
        } catch (err) {
            alert('Logout failed. Please try again.');
        }
    };

    // Stock functionality
    ui.getStockBtn.onclick = () => {
        const symbol = document.getElementById('stockSymbol').value;
        fetchStockData(symbol);
    };

    ui.addToWatchlistForm.onsubmit = async (e) => {
        e.preventDefault();
        const formData = {
            symbol: document.getElementById('watchlistSymbol').value,
            alert_price: document.getElementById('alertPrice').value
        };

        try {
            const response = await fetch('/watchlist', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: new URLSearchParams(formData)
            });

            const data = await response.json();
            alert(response.ok ? data.message : data.error);
            if (response.ok) fetchWatchlist();
        } catch (err) {
            alert('Failed to add to watchlist. Please try again.');
        }
    };

    // Helper functions
    async function fetchStockData(symbol) {
        try {
            const response = await fetch(`/api/stock/${symbol}`);
            const data = await response.json();

            if (response.ok) {
                displayStockInfo(data);
                fetchHistoricalData(symbol);
            } else {
                alert(data.error);
            }
        } catch (err) {
            alert('Failed to fetch stock data. Please try again.');
        }
    }

    function displayStockInfo(data) {
        document.getElementById('stockInfo').innerHTML = `
            <h3>${data.symbol}</h3>
            <p>Price: $${data.price}</p>
            <p>Last Updated: ${data.datetime}</p>
        `;
    }

    async function fetchHistoricalData(symbol) {
        try {
            const response = await fetch(`/api/historical/${symbol}`);
            const data = await response.json();

            if (data?.length) {
                displayChart(data);
            } else {
                alert('No historical data available for this stock.');
            }
        } catch (err) {
            alert('Failed to fetch historical data. Please try again.');
        }
    }

    function displayChart(data) {
        const ctx = document.getElementById('stockChart');
        if (stockChart) stockChart.destroy();

        stockChart = new Chart(ctx, {
            type: 'line',
            data: {
                datasets: [{
                    label: 'Stock Price',
                    data: data.map(item => ({
                        x: new Date(item.datetime),
                        y: item.price
                    })),
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.1)',
                    tension: 0.1,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        type: 'time',
                        time: { unit: 'day' },
                        title: { display: true, text: 'Date' }
                    },
                    y: {
                        title: { display: true, text: 'Price' }
                    }
                }
            }
        });
    }

    async function fetchWatchlist() {
        try {
            const response = await fetch('/watchlist');
            const data = await response.json();

            if (response.ok) {
                displayWatchlist(data);
            } else {
                alert(data.error);
            }
        } catch (err) {
            alert('Failed to fetch watchlist. Please try again.');
        }
    }

    function displayWatchlist(data) {
        const list = document.getElementById('watchlistItems');
        list.innerHTML = data.map(stock =>
            `<li>${stock.symbol} - Alert Price: $${stock.alert_price}</li>`
        ).join('');
    }

    function updateUIAfterLogin() {
        [ui.loginBtn, ui.registerBtn, ui.authForms].forEach(el => el.classList.add('hidden'));
        [ui.logoutBtn, ui.watchlist].forEach(el => el.classList.remove('hidden'));
        fetchWatchlist();
    }

    function updateUIAfterLogout() {
        [ui.loginBtn, ui.registerBtn].forEach(el => el.classList.remove('hidden'));
        [ui.logoutBtn, ui.watchlist, ui.authForms].forEach(el => el.classList.add('hidden'));
    }
});
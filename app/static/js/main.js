// app/static/js/main.js
document.addEventListener('DOMContentLoaded', () => {
    const loginBtn = document.getElementById('loginBtn');
    const registerBtn = document.getElementById('registerBtn');
    const logoutBtn = document.getElementById('logoutBtn');
    const authForms = document.getElementById('authForms');
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const getStockBtn = document.getElementById('getStockBtn');
    const watchlist = document.getElementById('watchlist');
    const addToWatchlistForm = document.getElementById('addToWatchlistForm');
    
    let stockChart;

    loginBtn.addEventListener('click', () => {
        authForms.classList.remove('hidden');
        loginForm.classList.remove('hidden');
        registerForm.classList.add('hidden');
    });

    registerBtn.addEventListener('click', () => {
        authForms.classList.remove('hidden');
        registerForm.classList.remove('hidden');
        loginForm.classList.add('hidden');
    });

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('loginUsername').value;
        const password = document.getElementById('loginPassword').value;

        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`,
        });

        const data = await response.json();
        if (response.ok) {
            alert(data.message);
            updateUIAfterLogin();
        } else {
            alert(data.error);
        }
    });

    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('registerUsername').value;
        const password = document.getElementById('registerPassword').value;
        const phone = document.getElementById('registerPhone').value;
        const email = document.getElementById('registerEmail').value;

        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}&phone=${encodeURIComponent(phone)}&email=${encodeURIComponent(email)}`,
        });

        const data = await response.json();
        if (response.ok) {
            alert(data.message);
            updateUIAfterLogin();
        } else {
            alert(data.error);
        }
    });

    logoutBtn.addEventListener('click', async () => {
        const response = await fetch('/logout');
        const data = await response.json();
        if (response.ok) {
            alert(data.message);
            updateUIAfterLogout();
        }
    });

    getStockBtn.addEventListener('click', async () => {
        const symbol = document.getElementById('stockSymbol').value;
        await fetchStockData(symbol);
    });

    addToWatchlistForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const symbol = document.getElementById('watchlistSymbol').value;
        const alertPrice = document.getElementById('alertPrice').value;

        const response = await fetch('/watchlist', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `symbol=${encodeURIComponent(symbol)}&alert_price=${encodeURIComponent(alertPrice)}`,
        });

        const data = await response.json();
        if (response.ok) {
            alert(data.message);
            fetchWatchlist();
        } else {
            alert(data.error);
        }
    });

    async function fetchStockData(symbol) {
        const response = await fetch(`/api/stock/${symbol}`);
        const data = await response.json();

        if (response.ok) {
            displayStockInfo(data);
            await fetchHistoricalData(symbol);
        } else {
            alert(data.error);
        }
    }

    function displayStockInfo(data) {
        const stockInfo = document.getElementById('stockInfo');
        stockInfo.innerHTML = `
            <h2>${data.symbol}</h2>
            <p>Price: $${data.price}</p>
            <p>Last Updated: ${data.datetime}</p>
        `;
    }

async function fetchHistoricalData(symbol) {
    try {
        const response = await fetch(`/api/historical/${symbol}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Historical data received:', data);

        if (data && data.length > 0) {
            displayChart(data);
        } else {
            console.error('No data received from API');
            alert('No historical data available for this stock.');
        }
    } catch (error) {
        console.error('Error fetching historical data:', error);
        alert('Error fetching historical data. Please try again.');
    }
}

    function displayChart(data) {
        console.log('Displaying chart with data:', data);

        const ctx = document.getElementById('stockChart');

        if (!ctx) {
            console.error('Canvas element not found');
            return;
        }

        if (stockChart) {
            stockChart.destroy();
        }

        const chartData = data.map(item => ({
            x: new Date(item.datetime),
            y: item.price
        }));

        console.log('Chart data:', chartData);

        try {
            stockChart = new Chart(ctx, {
                type: 'line',
                data: {
                    datasets: [{
                        label: 'Stock Price',
                        data: chartData,
                        borderColor: 'rgb(75, 192, 192)',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        x: {
                            type: 'time',
                            time: {
                                unit: 'day'
                            },
                            title: {
                                display: true,
                                text: 'Date'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Price'
                            }
                        }
                    }
                }
            });
            console.log('Chart created successfully');
        } catch (error) {
            console.error('Error creating chart:', error);
        }
    }

    async function fetchWatchlist() {
        const response = await fetch('/watchlist');
        const data = await response.json();

        if (response.ok) {
            displayWatchlist(data);
        } else {
            alert(data.error);
        }
    }

    function displayWatchlist(data) {
        const watchlistItems = document.getElementById('watchlistItems');
        watchlistItems.innerHTML = '';

        data.forEach(stock => {
            const li = document.createElement('li');
            li.textContent = `${stock.symbol} - Alert Price: $${stock.alert_price}`;
            watchlistItems.appendChild(li);
        });
    }

    function updateUIAfterLogin() {
        loginBtn.classList.add('hidden');
        registerBtn.classList.add('hidden');
        logoutBtn.classList.remove('hidden');
        authForms.classList.add('hidden');
        watchlist.classList.remove('hidden');
        fetchWatchlist();
    }

    function updateUIAfterLogout() {
        loginBtn.classList.remove('hidden');
        registerBtn.classList.remove('hidden');
        logoutBtn.classList.add('hidden');
        authForms.classList.add('hidden');
        watchlist.classList.add('hidden');
    }
});
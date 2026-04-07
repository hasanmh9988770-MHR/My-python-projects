// Global variables
let allQuotes = [];
let index = 0;
let batchSize = 5;
let myChart; // Tracks the chart instance to prevent "Canvas already in use" errors

/**
 * 1. LOAD QUOTES FEED
 * Fetches the full list of quotes and triggers the first batch display
 */
async function loadQuotes() {
    try {
        let res = await fetch("/api/live");
        allQuotes = await res.json();
        loadMore();
    } catch (err) {
        console.error("Feed error:", err);
    }
}

/**
 * 2. INFINITE SCROLL LOGIC
 * Slices the next batch of quotes from the global array and appends to the DOM
 */
function loadMore() {
    let feed = document.getElementById("feed");
    if (!feed) return;

    let next = allQuotes.slice(index, index + batchSize);

    next.forEach(q => {
        let card = document.createElement("div");
        card.className = "card";
        card.innerHTML = `
            <div class="quote">“${q.text}”</div>
            <div class="author">- ${q.author}</div>
            <div class="actions">
                <div class="like" onclick="like(this)">❤️ Like</div>
            </div>
        `;
        feed.appendChild(card);
    });

    index += batchSize;
}

/**
 * 3. STATS & ANALYTICS
 * Fetches aggregation data from the backend and updates the UI/Chart
 */
async function loadStats() {
    try {
        const res = await fetch("/api/stats");
        const data = await res.json();

        // Update Text Stats
        document.getElementById("total").innerText = data.total_quotes;
        document.getElementById("today").innerText = data.today_quotes;

        // Update Authors List
        let list = document.getElementById("authors-list");
        if (list) {
            list.innerHTML = "";
            data.top_authors.forEach(a => {
                let li = document.createElement("li");
                li.style.padding = "3px 0";
                li.innerText = `${a[0]} (${a[1]} quotes)`;
                list.appendChild(li);
            });
        }

        renderChart(data.top_authors);
    } catch (err) {
        console.error("Stats error:", err);
    }
}

/**
 * 4. CHART RENDERING
 * Uses Chart.js to draw the bar graph
 */
function renderChart(authors) {
    const ctx = document.getElementById("chart");
    if (!ctx) return;

    // Destroy the old chart instance before creating a new one
    if (myChart) {
        myChart.destroy();
    }

    myChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: authors.map(a => a[0]),
            datasets: [{
                label: "Quotes by Author",
                data: authors.map(a => a[1]),
                backgroundColor: 'rgba(255, 59, 92, 0.5)',
                borderColor: 'rgba(255, 59, 92, 1)',
                borderWidth: 1,
                borderRadius: 5
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: '#222' },
                    ticks: { color: '#888' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#888' }
                }
            }
        }
    });
}

/**
 * 5. UI INTERACTIONS
 */
function like(el) {
    el.innerText = el.innerText.includes("Like") ? "❤️ Liked" : "❤️ Like";
}

// Infinite Scroll Trigger
window.onscroll = () => {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 10) {
        loadMore();
    }
};

// INITIALIZE
loadQuotes();
loadStats();

// Auto-refresh stats every 3 seconds to reflect new database entries
setInterval(loadStats, 3000);
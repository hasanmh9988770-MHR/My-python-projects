// Weather Alert System - Frontend JS

document.addEventListener("DOMContentLoaded", function () {
    console.log("🌦 Weather Alert System Loaded");

    const form = document.querySelector("form");
    const input = document.querySelector("input[name='city']");

    if (form) {
        form.addEventListener("submit", function () {
            if (input.value.trim() === "") {
                alert("Please enter a city name!");
            }
        });
    }

    // Future upgrade hook: auto-refresh weather every 60 seconds
    function autoRefresh() {
        console.log("Auto-refresh placeholder (future feature)");
    }

    // Example: run every 60 seconds (disabled for now)
    // setInterval(autoRefresh, 60000);
});
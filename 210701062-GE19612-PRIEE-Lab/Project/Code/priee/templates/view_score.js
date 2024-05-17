document.addEventListener("DOMContentLoaded", function () {
    // Make AJAX request to retrieve score
    fetch("/view_score")
        .then(response => response.json())
        .then(data => {
            const scoreDisplay = document.getElementById("score-display");
            scoreDisplay.innerHTML = `<p>Your score: ${data.score}</p>`;
        })
        .catch(error => {
            console.error("Error fetching score:", error);
            // Display error message
            const scoreDisplay = document.getElementById("score-display");
            scoreDisplay.innerHTML = `<p>Error fetching score. Please try again later.</p>`;
        });
});

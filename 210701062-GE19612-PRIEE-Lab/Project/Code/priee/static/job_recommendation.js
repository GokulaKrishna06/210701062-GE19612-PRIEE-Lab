document.addEventListener("DOMContentLoaded", function () {
    // Make AJAX request to retrieve job recommendations
    fetch("/recommend_job")
        .then(response => response.json())
        .then(data => {
            const recommendationsContainer = document.getElementById("recommendations-container");
            recommendationsContainer.innerHTML = `<p>Recommended job: ${data.recommendation}</p>`;
        })
        .catch(error => {
            console.error("Error fetching job recommendation:", error);
            // Display error message
            const recommendationsContainer = document.getElementById("recommendations-container");
            recommendationsContainer.innerHTML = `<p>Error fetching job recommendation. Please try again later.</p>`;
        });
});

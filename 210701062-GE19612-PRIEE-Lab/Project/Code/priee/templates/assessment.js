document.addEventListener("DOMContentLoaded", function () {
    const questionsContainer = document.getElementById("questions");
    const paginationContainer = document.getElementById("pagination");

    // Function to fetch and display assessment questions
    function fetchAssessmentQuestions(pageNumber = 1) {
        fetch(`/fetch_assessment?page=${pageNumber}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Clear previous questions
                questionsContainer.innerHTML = "";
                // Display new questions
                data.questions.forEach(question => {
                    const questionElement = document.createElement("div");
                    questionElement.textContent = question;
                    questionsContainer.appendChild(questionElement);
                });
                // Generate pagination
                generatePagination(data.totalPages, pageNumber);
            })
            .catch(error => {
                console.error('Error fetching assessment questions:', error);
                questionsContainer.innerHTML = "<p>Error fetching assessment questions. Please try again later.</p>";
            });
    }

    // Function to generate pagination
    function generatePagination(totalPages, currentPage) {
        paginationContainer.innerHTML = "";
        for (let i = 1; i <= totalPages; i++) {
            const pageLink = document.createElement("li");
            pageLink.classList.add("page-item");
            if (i === currentPage) {
                pageLink.classList.add("active");
            }
            pageLink.innerHTML = `<a class="page-link" href="#" data-page="${i}">${i}</a>`;
            paginationContainer.appendChild(pageLink);
        }
    }

    // Event listener for pagination links
    paginationContainer.addEventListener("click", function (event) {
        event.preventDefault();
        if (event.target.tagName === "A") {
            const pageNumber = parseInt(event.target.dataset.page);
            fetchAssessmentQuestions(pageNumber);
        }
    });

    // Initial fetch for assessment questions on page load
    fetchAssessmentQuestions();
});

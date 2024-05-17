document.addEventListener("DOMContentLoaded", function () {
    const generateButton = document.getElementById("generate-button");
    const questionsContainer = document.getElementById("questions");

    generateButton.addEventListener("click", function () {
        fetch("/generate_assessment")
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
            })
            .catch(error => {
                console.error('Error generating assessment:', error);
                questionsContainer.innerHTML = "<p>Error generating assessment. Please try again later.</p>";
            });
    });
});

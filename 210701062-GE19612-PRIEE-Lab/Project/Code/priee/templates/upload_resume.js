document.getElementById("upload-form").addEventListener("submit", function(event) {
    event.preventDefault();
    var formData = new FormData(this);
    fetch("/upload_resume", {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            document.getElementById("message").innerHTML = "Resume uploaded successfully";
        } else {
            document.getElementById("message").innerHTML = "Error uploading resume";
        }
    })
    .catch(error => {
        console.error('Error uploading resume:', error);
        document.getElementById("message").innerHTML = "Error uploading resume";
    });
});

const majorLabel = document.getElementById("majorLabel");
const majorOptions = document.getElementById("majorOptions");

document.addEventListener("DOMContentLoaded", function () {
    const button = document.getElementById("create-account1");

    // Add event click listener to button
    button.addEventListener("click", function () {
        button.textContent = "Enter";

        // Show the label and select elements
        majorLabel.style.display = "inline-block";
        majorOptions.style.display = "inline-block";
    });
});
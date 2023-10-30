document.getElementById("passwordCheckForm").onsubmit = function(event) {
    event.preventDefault();

    var password = document.getElementById("password").value;
    var username = document.getElementById("hiddenUsername").value; // Getting username from a hidden input field

    // Sending POST request to verify password
    fetch('/verify_password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    }).then(response => response.json()).then(data => {
        if (data.status == "success") {
            window.location.href = '/change_account_info'; // Redirect to change account info page
        } else {
            alert("Wrong password. Please try again.");
        }
    });
};

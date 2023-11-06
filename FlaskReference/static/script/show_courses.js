// Function to get and display taken courses
function getAndDisplayTakenCourses() {
    var username = document.getElementById("hiddenUsername").value; // Assumes you have a hidden input with the username
    fetch(`/get_taken_course/${username}`)
      .then(response => response.json())
      .then(courses => {
        var coursesBox = document.getElementById('takenCoursesBox');
        coursesBox.innerHTML = ''; // Clear the container before adding new content
        courses.forEach(course => {
          coursesBox.innerHTML += `<p>${course.sid} ${course.cid}, </p>`; // Display each course in a new paragraph
        });
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }

  // Call the function to get and display courses when the page loads
  window.onload = function() {
    getAndDisplayTakenCourses();
  };

function searchCourse() {
    let searchTerm = document.getElementById('searchInput').value;
    fetch('/search_course', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `query=${searchTerm}`,
    })
    .then(response => response.json())
    .then(data => {
        let resultsBox = document.getElementById('resultsBox');
        resultsBox.innerHTML = '';  // Clear previous results
        data.forEach(course => {
            let courseElem = document.createElement('div');
            courseElem.innerHTML = `<br><strong>${course.title} (${course.sid} ${course.cid})</strong>: ${course.description}`;
            resultsBox.appendChild(courseElem);
            course.sections.forEach(section => {
                let sectionElem = document.createElement('a');
                sectionElem.href = '#';
                sectionElem.innerHTML = `Section: ${section.snum}, ${section.starttime}-${section.endtime} <br>`;
                sectionElem.addEventListener('click', function() {
                    // Perform action for the welcome page
                    alert(`Clicked on section ${section.snum} of ${course.title} from welcome.html`); 
                });
                resultsBox.appendChild(sectionElem);
            });
        });
    });
}

function searchTakenCourse() {
    let searchTerm = document.getElementById('searchInput').value;
    fetch('/search_course', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `query=${searchTerm}`,
    })
    .then(response => response.json())
    .then(data => {
        let resultsBox = document.getElementById('resultsBox');
        resultsBox.innerHTML = '';  // Clear previous results
        data.forEach(course => {
            let courseElem = document.createElement('div');
            let takenElem = document.createElement('a');
            takenElem.href = '#';
            courseElem.innerHTML = `<br><strong>${course.title} (${course.sid} ${course.cid})</strong>: ${course.description}`;
            takenElem.innerHTML = `I've already taken this`;
            resultsBox.appendChild(courseElem);
            resultsBox.appendChild(takenElem);
            takenElem.addEventListener('click', function() {
                var username = document.getElementById('hiddenUsername').value;
                alert(`Page 2 action for ${course.title} from profile.html`);
                fetch('/add_taken_course', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        username: username,
                        sid : course.sid,
                        cid : course.cid
                    })
                }).then(response => response.json()).then(data => {
                    if (data.status == "success") {
                        //window.location.href = '/change_account_info'; // Redirect to change account info page
                    } else {
                        alert("Something wrong happened. F.");
                    }
                }); 
                getAndDisplayTakenCourses();
            });
        });
    });
}

function submitForm() {
    document.getElementById('profileForm').submit();
}

// Function to get and display taken courses
function getAndDisplayTakenCourses() {
    var username = document.getElementById("hiddenUsername").value; // Assumes you have a hidden input with the username
    fetch(`/get_taken_course/${username}`)
      .then(response => response.json())
      .then(courses => {
        var coursesBox = document.getElementById('takenCoursesBox');
        coursesBox.innerHTML = ''; // Clear the container before adding new content
        courses.forEach(course => {
          coursesBox.innerHTML += `<p>${course.sid} ${course.cid}, </p>`; // Display each course in a new paragraph
        });
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }

  // Call the function to get and display courses when the page loads
  window.onload = function() {
    getAndDisplayTakenCourses();
  };
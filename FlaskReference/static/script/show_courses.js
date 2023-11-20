// Function to get and display taken courses
function getAndDisplayTakenCourses() {
    var username = document.getElementById("hiddenUsername").value; // Assumes you have a hidden input with the username
    fetch(`/get_taken_course/${username}`)
        .then(response => response.json())
        .then(courses => {
            var coursesBox = document.getElementById('takenCoursesBox');
            coursesBox.innerHTML = ''; // Clear the container before adding new content
            courses.sort((a, b) => a.sid.localeCompare(b.sid));
            let lastSID = ''; // Keep track of the last 'sid' we've seen
            courses.forEach(course => {
                //alert(`${lastSID} and ${course.sid}`);
                if (lastSID !== course.sid) {
                    // Check if 'sid' has changed since the last course
                    if (lastSID !== '') {
                        // New line if this is not the first course added
                        
                        coursesBox.innerHTML += `<p></p>`;
                    }
                    // Start a new paragraph and update 'lastSID'
                    coursesBox.innerHTML += `| <a class="course-link" href="#" data-sid="${course.sid}" data-cid="${course.cid}">${course.sid} ${course.cid}</a> | `;
                    
                } else {
                    coursesBox.innerHTML += ` | <a class="course-link" href="#" data-sid="${course.sid}" data-cid="${course.cid}">${course.sid} ${course.cid}</a> |  `;
                }
                lastSID = course.sid;
                
            });

            if (courses.length > 0) {
                // Close the last paragraph if any courses were added
                coursesBox.innerHTML += `</p>`;
            }

            coursesBox.addEventListener('click', function (del) {
                if (del.target.classList.contains('course-link')) {
                    sid = del.target.dataset.sid;
                    cid = del.target.dataset.cid;

                    fetch('/del_taken_course', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            username: username,
                            sid: sid,
                            cid: cid
                        })
                    }).then(response => response.json()).then(data => {
                        if (data.status == "success") {
                            getAndDisplayTakenCourses(); // Refresh the displayed courses after deletion
                        }
                    });
                }
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

//JavaScript Debugging to find out why the height of box changes
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
                var shortDesc = course.description.substring(0, course.description.indexOf(". ") + 1);
                courseElem.innerHTML = `<br><strong>${course.title} (${course.sid} ${course.cid})</strong>: ${shortDesc}`;
                resultsBox.appendChild(courseElem);
                course.sections.forEach(section => {
                    let sectionElem = document.createElement('a');
                    sectionElem.href = '#';
                    sectionElem.innerHTML = `Section: ${section.snum}, ${section.days} from ${section.starttime}-${section.endtime} <br>`;
                    sectionElem.addEventListener('click', function () {
                        // Array of colors for courses
                        colors = ['#f5ad1d', '#e37730', '#3ad6aa', '#10bce3', '#9e3ccf', '#cbd932', '#d93237']

                        // Convert days from MTWRF to numbers
                        let days = []
                        for (const day of section.days) {
                            days.push('MTWRF'.indexOf(day)+1);
                        }

                        // Check if the class exists
                        if(calendar.getEventById(section.crn) == null)
                        {
                            // Add course to calendar
                            calendar.addEvent({
                                id: section.crn,
                                title: `${course.sid} ${course.cid}`, // The text to display
                                startTime: section.starttime, // start time
                                endTime: section.endtime, // end time
                                daysOfWeek: days, // The days of the class
                                color: colors[calendar.getEvents().length%colors.length], // Cycle through colors
                            });

                            // Update class list
                            updateClassList();

                        }

                        var username = document.getElementById('name').value;
                        fetch('/add_to_schedule', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                username: username,
                                crn: section.crn,
                                sindex: '1'
                            })
                        }).then(response => response.json()).then(data => {
                            if (data.status == "success") {
                                //window.location.href = '/change_account_info'; // Redirect to change account info page
                            } else {
                                alert("Something wrong happened. F.");
                            }
                        });
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
                takenElem.addEventListener('click', function () {
                    // Perform action for the profile page
                    var username = document.getElementById('hiddenUsername').value;
                    fetch('/add_taken_course', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            username: username,
                            sid: course.sid,
                            cid: course.cid
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

function getAndDisplayRemainingCourses(username) {
    fetch(`/get_remaining_courses/${username}`)
        .then(response => response.json())
        .then(remainingCourses => {
            return fetch(`/get_remaining_hours/${username}`)
                .then(response => response.json())
                .then(remainingHours => ({ remainingCourses, remainingHours }));
        })
        .then(data => {
            const { remainingCourses, remainingHours } = data;
            const remainingCoursesBox = document.getElementById('remainingCoursesBox');
            remainingCoursesBox.innerHTML = ''; // Clear previous content

            for (let requirement in remainingCourses) {
                if (requirement.toLowerCase().includes('elective')) {
                    // If the requirement contains the word 'elective', display the requirement and hours needed
                    const hours = remainingHours[requirement];
                    remainingCoursesBox.innerHTML += `<p><strong>${requirement}:</strong> ${hours} credit hours needed</p>`;
                } else {
                    // Otherwise, display the list of courses for that requirement
                    const coursesList = remainingCourses[requirement].join(', ');
                    remainingCoursesBox.innerHTML += `<p><strong>${requirement}:</strong> ${coursesList}</p>`;
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function getAndDisplayRecommendedCourses(username) {
    // Make a GET request to the server
    fetch(`/get_recommended_courses/${username}`)
      .then(response => {
        // Check if the response is ok (status code 200-299)
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json(); // Parse JSON response into native JavaScript objects
      })
      .then(recommendedCourses => {
        // Get the element with id="recommendedClasses"
        const recommendedClassesBox = document.getElementById('recommendedClasses');
        recommendedClassesBox.innerHTML = ''; // Clear any previous content
  
        // Create a list of recommended courses
        recommendedCourses.forEach(course => {
          // course is expected to be a tuple-like array, for example: [10172, 'ECE211', 3]
          const courseId = course[0];  // Assuming the first element is the course ID
          const courseCode = course[1]; // Assuming the second element is the course code
          const courseCredit = course[2]; // Assuming the third element is the course credit
  
          // Create a new div element for this course and add it to the box
          const courseDiv = document.createElement('div');
          courseDiv.className = 'recommended-course';
          courseDiv.innerHTML = `${courseCode}`;
          recommendedClassesBox.appendChild(courseDiv);
        });
      })
      .catch(error => {
        console.error('Error fetching recommended courses:', error);
      });
  }
  

function submitForm() {
    document.getElementById('profileForm').submit();
}

function deleteCourse(id) {
    calendar.getEventById(id).remove()
}
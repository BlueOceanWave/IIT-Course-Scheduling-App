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
                    // Handle the click event for the section here
                    // For instance:
                    let pageName = document.getElementById('pageIdentifier').dataset.pageName;
                    if (pageName === 'welcome') {
                        // Perform action for the welcome page
                        alert(`Clicked on section ${section.snum} of ${course.title} from welcome.html`);
                        
                    } else if (pageName === 'profile') {
                        // Perform action for the profile page
                        var username = document.getElementById('hiddenUsername').value;
                        alert(`Page 2 action for section ${section.snum} of ${course.title} from profile.html`);
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
                    }
                });
                resultsBox.appendChild(sectionElem);
            });
        });
    });
}

function submitForm() {
    document.getElementById('profileForm').submit();
}
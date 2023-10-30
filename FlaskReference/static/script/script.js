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
            courseElem.innerHTML = `<strong>${course.title}</strong>: ${course.description}`;
            resultsBox.appendChild(courseElem);
            course.sections.forEach(section => {
                let sectionElem = document.createElement('a');
                sectionElem.href = '#';
                sectionElem.innerHTML = `Section: ${section.snum}, ${section.starttime}-${section.endtime} <br>`;
                sectionElem.addEventListener('click', function() {
                    // Handle the click event for the section here
                    // For instance:
                    alert(`Clicked on section ${section.snum} of ${course.title}`);
                });
                resultsBox.appendChild(sectionElem);
            });
        });
    });
}

function submitForm() {
    document.getElementById('profileForm').submit();
}
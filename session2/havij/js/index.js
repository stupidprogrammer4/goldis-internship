function showExperienceForm() {
    document.getElementById('experience-list').style.display = 'none';
    document.getElementById('add-experience-button').style.display = 'none';
    document.getElementById('experience-form').style.display = 'block';
}

function hideExperienceForm() {
    document.getElementById('experience-list').style.display = 'block';
    document.getElementById('add-experience-button').style.display = 'block';
    document.getElementById('experience-form').style.display = 'none';
}

function showEducationForm() {
    document.getElementById('education-list').style.display = 'none';
    document.getElementById('add-education-button').style.display = 'none';
    document.getElementById('education-form').style.display = 'block';
}

function hideEducationForm() {
    document.getElementById('education-list').style.display = 'block';
    document.getElementById('add-education-button').style.display = 'block';
    document.getElementById('education-form').style.display = 'none';
}

function showSkillForm() {
    document.getElementById('skills-list').style.display = 'none';
    document.getElementById('add-skill-button').style.display = 'none';
    document.getElementById('skill-form').style.display = 'block';
}

function hideSkillForm() {
    document.getElementById('skills-list').style.display = 'block';
    document.getElementById('add-skill-button').style.display = 'block';
    document.getElementById('skill-form').style.display = 'none';
}

function setNewSkillRating(rating) {
    const stars = document.getElementById('new-skill-stars').children;
    for (let i = 0; i < stars.length; i++) {
        stars[i].innerHTML = i < rating ? '&#9733;' : '&#9734;';
    }
    newSkillRating = rating;
}


function sendDataToServer(endpoint, data) {
    fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function addExperience() {
    const jobTitle = document.getElementById('job-title').value
    const companyName = document.getElementById('company-name').value;
    const jobDescription = document.getElementById('job-description').value;
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
    const emptyExp = document.getElementById('empty-exp')

    const experienceData = {
        job_title: jobTitle,
        company_name: companyName,
        desc: jobDescription,
        start_date: startDate,
        end_date: endDate,
    };




    sendDataToServer('/add-experience', experienceData);

    const experienceList = document.getElementById('experience-list');
    const newJob = document.createElement('div');
    newJob.className = 'job';
    newJob.innerHTML = `
        <h3>${companyName}</h3>
        <p>${startDate} - ${endDate}</p>
        <p>${jobDescription}</p>
    `;
    experienceList.appendChild(newJob);

    if (emptyExp !== null) {
        experienceList.removeChild(emptyExp)
    }
    hideExperienceForm();
}

function addEducation() {
    const degreeName = document.getElementById('degree-name').value;
    const institutionName = document.getElementById('institution-name').value;
    const startDate = document.getElementById('start-date-ed').value;
    const endDate = document.getElementById('end-date-ed').value;
    const emptyEdu = document.getElementById('empty-edu')

    const educationData = {
        degree_name: degreeName,
        institution: institutionName,
        start_date: startDate,
        end_date: endDate
    };

    sendDataToServer('/add-education', educationData);

    const educationList = document.getElementById('education-list');
    const newEducation = document.createElement('div');
    newEducation.className = 'education-item';
    newEducation.innerHTML = `
        <h3>${degreeName}</h3>
        <p>${institutionName}</p>
        <p>${startDate} - ${endDate}</p>
    `;

    if (emptyEdu !== null) {
        educationList.removeChild(emptyEdu)
    }
    educationList.appendChild(newEducation);
    hideEducationForm();
}

function addSkill() {
    const skillName = document.getElementById('skill-name').value;
    const emptySkill = document.getElementById('empty-skill')

    if (skillName === '' || newSkillRating === 0) {
        alert('Please provide a skill name and rating.');
        return;
    }

    const skillData = {
        name: skillName,
        rate: newSkillRating,
    };

    sendDataToServer('/add-skill', skillData);

    const skillList = document.getElementById('skills-list');
    const newSkill = document.createElement('div');
    newSkill.className = 'skill';
    newSkill.innerHTML = `
        <span>${skillName}</span>
        <div class="stars" data-skill="${skillName.toLowerCase()}">
            ${Array.from({ length: 5 }, (_, i) =>
                `<span class="star" onclick="setRating(this, ${i + 1}, '${skillName.toLowerCase()}')">
                ${i < newSkillRating ? '&#9733;' : '&#9734;'}</span>`
            ).join('')}
        </div>
    `;
    skillList.appendChild(newSkill);

    if (emptySkill !== null) {
        skillList.removeChild(emptySkill)
    }
    hideSkillForm();
}

const mobileScreen = window.matchMedia("(max-width: 990px )");
$(document).ready(function () {
    $(".dashboard-nav-dropdown-toggle").click(function () {
        $(this).closest(".dashboard-nav-dropdown")
            .toggleClass("show")
            .find(".dashboard-nav-dropdown")
            .removeClass("show");
        $(this).parent()
            .siblings()
            .removeClass("show");
    });
    $(".menu-toggle").click(function () {
        if (mobileScreen.matches) {
            $(".dashboard-nav").toggleClass("mobile-show");
        } else {
            $(".dashboard").toggleClass("dashboard-compact");
        }
    });
});

function printResume() {
    window.print();
}
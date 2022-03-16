let loginButton = document.getElementById('login')
let logoutButton = document.getElementById('logout')

if (localStorage.getItem('token')) {
    loginButton.style.display = "none"
    logoutButton.style.display = "block"
} else {
    loginButton.style.display = "block"
    logoutButton.style.display = "none"
}

logoutButton.addEventListener('click', (e) => {
    e.preventDefault()
    localStorage.removeItem('token')

    let basePath = window.location.href.substring(0, window.location.href.lastIndexOf("/") + 1)
    window.location = basePath + 'login.html'
})

let projectsUrl = 'http://localhost:8000/api/projects/'

let getProjects = () => {
    fetch(projectsUrl)
    .then(response => response.json())
    .then(data => {
        buildProjects(data)
    })
}

let buildProjects = (projects) => {
    let projectsWrapper = document.getElementById('projects-wrapper')
    projectsWrapper.innerHTML = ''

    for(let i = 0; i < projects.length; ++i) {
        let project = projects[i]
        projectsWrapper.innerHTML += `
            <div class="project--card">
                <div class="card--image">
                    <img src="http://localhost:8000${project.featured_image}" alt="">
                </div>
                <div>
                    <div class="card--header">
                        <h3>${project.title}</h3>
                        
                        <div class="header--buttons">
                            <div>${project.vote_ratio}% positive feedbacks</div>
                            <div class="buttons">
                                <button class="vote--option" data-vote="up" data-project="${project.id}">&#8593;</button>
                                <button class="vote--option" data-vote="down" data-project="${project.id}">&#8595;</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `
    }

    addVoteEvents()
}

let addVoteEvents = () => {
    let voteButtons = document.getElementsByClassName('vote--option')
    for(let i = 0; i < voteButtons.length; ++i) {
        voteButtons[i].addEventListener('click', (e) => {
            let token = localStorage.getItem('token')
            let vote = e.target.dataset.vote
            let project = e.target.dataset.project

            fetch(`http://localhost:8000/api/projects/${project}/vote/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({'value': vote}),
            })
            .then(response => response.json())
            .then(data => {
                getProjects()
            })
        })
    }
}

getProjects()
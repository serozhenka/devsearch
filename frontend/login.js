let form = document.getElementById('login-form')

form.addEventListener('submit', (e) => {
    e.preventDefault()

    let link = 'http://localhost:8000/api/users/token/'
    let formData = {
        'username': form.username.value,
        'password': form.password.value,
    }

    fetch(`${link}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        let token = data.access
        if (data.access) {
            localStorage.setItem('token', token)
            let basePath = window.location.href.substring(0, window.location.href.lastIndexOf("/") + 1)
            window.location = basePath + 'projects-list.html'
        } else {
            alert('Username or password is incorrect')
        }
    })
})
var procDiv;
var selDiv;
var loader;

document.addEventListener("DOMContentLoaded", init, false);

function init() {
    document.querySelector('form').addEventListener('submit', handleFormSubmit, false);
    procDiv = document.querySelector("#processedfiles");
    loader = document.querySelector("#loading");
    selDiv = document.querySelector("#selectedfiles");
}

async function handleFormSubmit(e) {
    e.preventDefault();
    const formData = new FormData(document.querySelector('form'))
    // console.log(formData)
    var files = document.querySelector('#file').files;
    if (files.length <= 0) return;
    displayLoading();
    // console.log(files);
    const response = await fetch('/upload', {
        method: 'POST',
        body: formData,
    });
    hideLoading();
    selDiv.innerHTML = "";
    console.log(response);
    var images = await response.json()
    console.log(images)
    for (var i in images) {
        // console.log(i)
        const f = await fetch(images[i], {
            method: 'GET',
        });
        var file = await f.blob()
        console.log(file)
        procDiv.innerHTML += `<li class="list-group-item d-flex align-items-center">
								<img class="img-reponsive img-rounded preview-image" src=${URL.createObjectURL(file)} />
								${images[i].substring(images[i].lastIndexOf('/')+1)}
							<li/>`
    }
    
}

async function displayLoading() {
    loader.classList.add("display");
}

async function hideLoading() {
    loader.classList.remove("display");
}

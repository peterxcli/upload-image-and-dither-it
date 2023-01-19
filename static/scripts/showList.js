var selDiv = "";
var procDiv;
	
document.addEventListener("DOMContentLoaded", init, false);

function init() {
	document.querySelector('#file').addEventListener('change', handleFileSelect, false);
	selDiv = document.querySelector("#selectedfiles");
	procDiv = document.querySelector("#processedfiles");
}
	
function handleFileSelect(e) {
	
	if(!e.target.files) return;
	
	selDiv.innerHTML = "";
	procDiv.innerHTML = "";
	
	var files = e.target.files;
	for(var i=0; i<files.length; i++) {
		var f = files[i];

		var fileType = f.type.split('/')[0];
        if (fileType !== 'image') {
            alert("Invalid file type. Please select an image file.");
            return;
        }
		
		selDiv.innerHTML += `<li class="list-group-item d-flex align-items-center">
								<img class="img-reponsive img-rounded preview-image" src=${URL.createObjectURL(f)} />
								${f.name}
								<span class="close" onclick="removeItem($(this))">x</span>
							<li/>`
	}
}

function removeItem(item) {
	item.parent().remove();

	selDiv.innerHTML = "";

	var files = e.target.files;
	for(var i=0; i<files.length; i++) {
		var f = files[i];
		console.log(f)
		console.log(item)
		if (f != item) {
			selDiv.innerHTML += `<li class="list-group-item d-flex align-items-center">
									<img class="img-reponsive img-rounded preview-image" src=${URL.createObjectURL(f)} />
									${f.name}
									<span class="close" onclick="removeItem($(this))">x</span>
								<li/>`
		}
	}
  }

$( document ).ready(function(){
	if($("#alert").length){
		$('#alert').fadeIn('slow', function(){
			$('#alert').delay(5000).fadeOut(); 
		});
	}
});
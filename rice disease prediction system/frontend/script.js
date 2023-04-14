const form = document.querySelector("#upload-form");
const resultDiv = document.querySelector(".result");
const fileInput = document.querySelector("#image-upload");
const imgUpload = document.querySelector("#img-upload");
const dp = document.querySelector("#dp");
const submitButton = document.querySelector("#img-submit");

fileInput.addEventListener('change', function(){ //img change
	dp.src = URL.createObjectURL(fileInput.files[0]);
});

imgUpload.addEventListener("click", function() { //upload btn click function
	fileInput.click();
  });

form.addEventListener("submit", (event) => {
	event.preventDefault();
	// const fileInput = document.getElementById("image-upload");
	const file = fileInput.files[0];
	if (!file) return;
	
	const formData = new FormData();
	formData.append("file", file);
	
	fetch("http://localhost:8000/predict", {
		method: "POST",
		body: formData,
	})
	.then(response => response.json())
	.then(data => {
		resultDiv.innerHTML = `
			<p>Predicted Class: ${data.class_name}</p>
			<p>Confidence: ${data.confidence}</p>
		`;
	})
	.catch(error => {
		console.error(error);
		resultDiv.innerHTML = "An error occurred while processing the image.";
	});
});
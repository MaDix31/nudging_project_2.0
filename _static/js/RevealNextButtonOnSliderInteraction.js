document.getElementById("wtp").addEventListener("mousedown", showNextButton);

function showNextButton() {
	try {
    document.getElementById("nextButton").classList.remove("initiallyHidden");
	}
	catch(err) {
	}
}

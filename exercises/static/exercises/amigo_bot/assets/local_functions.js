// Load code part

const realFileBtn = document.getElementById("real-file");
const customBtn = document.getElementById("load");

// Load button acts as a fake interface
// Adding event listener to it
customBtn.addEventListener("click", function(){
	realFileBtn.click();
});

// The actual work that is done behind
// The load button acctually activates the element real-file
// which loads the file
realFileBtn.addEventListener("change", function() {
	if (realFileBtn.value) {
		var fr = new FileReader();
		fr.onload = function(){
			editor.setValue(fr.result, 1);
		}
		fr.readAsText(this.files[0]);
	
	} 
});

// Function to save the code locally
function saveCodeLocally(){
	var python_code = editor.getValue();
	var blob = new Blob([python_code], {type: "text/plain; charset=utf-8"});
	if (window.navigator.msSaveOROpenBlob)
		window.navigator.msSaveOrOpenBlob(blob, "academy.py");
	else{
		var a = document.createElement("a"),
		url = URL.createObjectURL(blob);
		a.href = url;
		a.download = "academy.py";
		document.body.appendChild(a);
		a.click()
		setTimeout(function(){
			document.body.removeChild(a);
			window.URL.revokeObjectURL(url);
		}, 0);
	}
}
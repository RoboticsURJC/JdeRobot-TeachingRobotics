//Editor Part
var editor = ace.edit("editor");
editor.setTheme("ace/theme/monokai");
editor.session.setMode("ace/mode/python");

var stop_button = document.getElementById("stop");
stop_button.disabled = true;
stop_button.style.opacity = "0.4";
stop_button.style.cursor = "not-allowed";

// running variable for psuedo decoupling 
// Play/Pause from Reset
var frequency = "0",
	running = false;

//WebSocket for Code
var websocket_code;
function declare_code(websocket_address){
	websocket_code = new WebSocket("ws://" + websocket_address + ":1905/");

	websocket_code.onopen = function(event){
		radiConect.contentWindow.postMessage({command: 'launch_level', level: '5'}, '*');
		if (websocket_gui.readyState == 1) {
			alert("[open] Connection established!");
			radiConect.contentWindow.postMessage('up', '*');
		}
	}
	websocket_code.onclose = function(event){
		if(event.wasClean){
			alert(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
		}
		else{
			alert("[close] Connection closed!");
		}
	}

	websocket_code.onmessage = function(event){
		var source_code = event.data;
		operation = source_code.substring(0, 5);
		
		if(operation == "#load"){
			editor.setValue(source_code.substring(5,));
		}
		else if(operation == "#freq"){
			var frequency_message = JSON.parse(source_code.substring(5,));
			// Parse GUI and Brain frequencies
			document.querySelector("#ideal_gui_frequency").value = frequency_message.gui;
			document.querySelector('#ideal_code_frequency').value = frequency_message.brain;
			// Parse real time factor
			document.querySelector('#real_time_factor').value = frequency_message.rtf;
		}
		
		// The acknowledgement messages invoke the python server to send further
		// messages to this client (inside the server's handle function)
		// Send the acknowledgment message along with frequency
		code_frequency = document.querySelector('#code_freq').value;
		gui_frequency = document.querySelector('#gui_freq').value;
		real_time_factor = document.querySelector('#real_time_factor').value;
    
		frequency_message = {"brain": code_frequency, "gui": gui_frequency, "rtf": real_time_factor};
		websocket_code.send("#freq" + JSON.stringify(frequency_message));
	};
}

// Function that sends/submits the code!
function submitCode(){
	try {
		// Get the code from editor and add headers
		var python_code = editor.getValue();
		python_code = "#code\n" + python_code
		
		websocket_code.send(python_code);
		console.log("Code Sent! Check terminal for more information!");
		unpause_lap();

		stop_button.disabled = false;
		stop_button.style.opacity = "1.0";
		stop_button.style.cursor = "default";

		running = true;
	}
	catch {
		alert("Connection must be established before sending the code.")
	}
}

// Function that send/submits an empty string
function stopCode(){
    var stop_code = "#code\n";
    console.log("Message sent!");
	websocket_code.send(stop_code);
	pause_lap();
	
	running = false;
}

// Function to command the simulation to reset
function resetSim(){
	// Send message to initiate reset
	var message = "#rest"
	websocket_code.send(message)
	reset_gui();

	if(running == true){
		stopCode();
		submitCode();
	}
}

// Function for range slider
function codefrequencyUpdate(vol) {
	document.querySelector('#code_frequency').value = vol;
}

// Function for range slider
function guifrequencyUpdate(vol) {
	document.querySelector('#gui_frequency').value = vol;
}

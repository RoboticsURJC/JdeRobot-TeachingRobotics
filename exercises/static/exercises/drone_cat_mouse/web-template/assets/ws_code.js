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

// variables for the evaluator
var draw = undefined,
    dist = 0,
    relayout_flag = false;

// Measure each point at an interval of 500 ms
var interval = 500;
// Evaluate for maximum of time 2 mins that is 120 secs
// 120 secs = 240 measuring points
var max_points = 240;
// Evaluate for minimum of 30 secs
// 30 secs = 60 measuring points
var min_points = 60;
// Each time the evaluate button is pressed, reduce time by 15 secs
// 15 secs = 30 measuring points
var reduce_points = 30;
// set reduce_points_flag to True after the first press of Evaluate button
var reduce_points_flag = false;


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
			// Parse score
			document.querySelector('#score').value = frequency_message.score;
		}

		// Send the acknowledgment message along with frequency
		code_frequency = document.querySelector('#code_freq').value;
		gui_frequency = document.querySelector('#gui_freq').value;
		real_time_factor = document.querySelector('#real_time_factor').value;
		score = document.querySelector('#score').value;
        dist = frequency_message.dist;
		frequency_message = {"brain": code_frequency, "gui": gui_frequency, "rtf": real_time_factor, "score": score, "dist": dist};
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

		stop_button.disabled = false;
		stop_button.style.opacity = "1.0";
		stop_button.style.cursor = "default";

		running = true;
        // reset evaluator graph
        clearInterval(draw)
        reduce_points_flag = false;
        max_points = 240;
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

	running = false;
    // stop evaluator graph
    clearInterval(draw)
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

// Function for graph
function evaluator() {
    // stop existing plot if any
    clearInterval(draw);

    // start reducing points from the second press of Evaluate button
    if (max_points > min_points && reduce_points_flag == true) {
        max_points = max_points - reduce_points;
    }

    var xtickvals = [];
    var xticktext = [];
    for (let i = 0; i <= max_points; i+=reduce_points) {
        console.log(i*interval/1000)
        xtickvals.push(i);
        xticktext.push(i*interval/1000)
    }

    // https://plotly.com/javascript/reference/layout/
    data = {
        data : [{ y: [dist] }],
        layout : {
            title : "Drone Cat Mouse",
            width : 800, 
            height : 300, 
            plot_bgcolor : "#cfffcf",
            xaxis : {
                range : [0, max_points], 
                title : "Time (in seconds)", 
                tickvals : xtickvals,
                ticktext : xticktext
            }, 
            yaxis : {
                range : [0, 6], 
                title : "Distance", 
                tickvals : [1,2,3,4,5,6]
            }
        }
    };

    Plotly.newPlot("eval", data)
    var cnt = 0;
    
    draw = setInterval(function() {
        Plotly.extendTraces("eval", { y:[[dist]]}, [0]);
        cnt++;
        if (cnt >= max_points) {
            clearInterval(draw);
        }
        // change background color of the plot to red when distance > 4
        if(dist > 4) {
            Plotly.relayout("eval", {plot_bgcolor: "#ffcccb"});
            relayout_flag = true;
        } else if (dist <= 4 && relayout_flag == true ) {
            Plotly.relayout("eval", {plot_bgcolor: "#cfffcf"});
            relayout_flag = false;
        }
    },interval);

    reduce_points_flag = true;
}
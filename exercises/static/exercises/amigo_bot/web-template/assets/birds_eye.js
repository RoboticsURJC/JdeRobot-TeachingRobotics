// Retreive the canvas elements and context
var mapCanvas = document.getElementById("birds-eye"),
	ctx = mapCanvas.getContext("2d");
	
	
var trail = [],
	coords = [-1, -1];;

// Complete draw function
function draw(pos, contorno, laser_data, sonar_sensor_point, pos_vertices, laser_global){
	mapCanvas.width = 769;
	mapCanvas.height = 729;
	
	// clearMap();
	// drawTrail(coords[0], coords[1]);
	drawLaser(laser_data, laser_global);
	drawAmigobot(pos, contorno);
	drawSonar(sonar_sensor_point, pos_vertices);
}

// Function to draw triangle
// Given the coordinates of center, and
// the angle towards which it points
function drawCircle(x, y){
	cursor_x = x;
	cursor_y = y;
	
	ctx.beginPath();
	ctx.arc(x, y, 1.5, 0, 2 * Math.PI);
	ctx.closePath();
	
	ctx.lineWidth = 1.5;
	ctx.strokeStyle = "#0000FF";
	ctx.stroke();
	
	ctx.fillStyle = "#0000FF";
	ctx.fill();
}

// Testing to be carried out with Python interface
function drawTriangle(posx, posy, angx, angy){
	/*Crea un nuevo trazo. Una vez creado, los comandos
	de dibujo futuros son aplicados dentro del trazo y 
	usados para construir el nuevo trazo hacia arriba*/
	ctx.beginPath();
	
	px = posx;
	py = posy;
	
	// The main line
	ctx.strokeStyle = '#FF0000';
	
	// Sides
	side = 1.5 * Math.hypot(2, 2);
	
	if(angx != 0){
		ang = Math.atan2(angy, angx);
	}
	else{
		ang = Math.PI / 2;
	}
	
	px1 = posx + side * Math.cos(2 * Math.PI / 3 + ang);
	py1 = posy - side * Math.sin(2 * Math.PI / 3 + ang);
	px2 = posx + side * Math.cos(2 * Math.PI / 3 - ang);
	py2 = posy + side * Math.sin(2 * Math.PI / 3 - ang);
	px3 = posx + side * Math.cos(ang);
	py3 = posy - side * Math.sin(ang);
	
	ctx.moveTo(px3, py3);
	ctx.lineTo(px1, py1);
	ctx.lineTo(px2, py2);
	ctx.lineTo(px3, py3);
	
	rx = px;
	ry = py;
	
	ctx.stroke();
	ctx.closePath();
	
	ctx.fillStyle = "#FF0000";
	ctx.fill();
	
	return [rx, ry];
}

function drawTrail(px, py){
	trail.push({x: px, y: py});

	for(i = 0; i < trail.length; i = i + 1){
		drawCircle(trail[i].x, trail[i].y);
	}
}

function clearMap(){
	ctx.clearRect(0, 0, mapCanvas.width, mapCanvas.height);
	trail = [];
}

function drawAmigobot(pos, contorno){
	ctx.beginPath();
	ctx.strokeStyle = "#000000";
	// First: draw the circle
	ctx.arc(pos[0], pos[1], 5, 0, 2 * Math.PI);
	ctx.stroke();
	ctx.fillStyle = "#000000";
	ctx.fill();
	ctx.closePath();
	   
	// Second: draw the triangle
	ctx.beginPath();
	ctx.strokeStyle = "#FFFB00";
	ctx.moveTo(contorno[0][0], contorno[0][1]);
	ctx.lineTo(contorno[1][0], contorno[1][1]);
	ctx.lineTo(contorno[2][0], contorno[2][1]);
	ctx.lineTo(contorno[0][0], contorno[0][1]);
	ctx.stroke();
	ctx.fillStyle = "#FFFB00";
	ctx.fill();
	ctx.closePath();
}
function drawLaser(dataLaser, laser_global){
	for(let d of dataLaser){
		ctx.beginPath();
		ctx.strokeStyle = "#FF2D00";
		ctx.moveTo(laser_global[0], laser_global[1]);
		ctx.lineTo(d[0], d[1]);
		ctx.stroke();
		ctx.closePath();
	}
}
function drawSonar(sonar_sensor_point, pos_vertices){
	let px_sensor = [];
	let py_sensor = [];
	let j = 0;
	let z = 0;

	for(let k of sonar_sensor_point){
		px_sensor[j] = k[0];
		py_sensor[j] = k[1];
		j++;	
	}
	px_v = pos_vertices[0]
	for(let d of pos_vertices){

		ctx.beginPath();
		ctx.strokeStyle = "#4AA434";
		ctx.fillStyle = "#4AA434";
		ctx.moveTo(px_sensor[z], py_sensor[z]);
		ctx.lineTo(d[0],d[1]);
		ctx.lineTo(d[2],d[3]);
		ctx.lineTo(px_sensor[z], py_sensor[z]);
		ctx.stroke();
		ctx.fill();
		ctx.closePath();
		z++;
	}
}

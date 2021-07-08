var mapping = document.getElementById("mapping"),
    ctx_map = mapping.getContext("2d");

var trail = [],
	coords = [-1, -1];;

var aux_map = 0;
var points = new Array();
var mapCoord = new Map();

function drawMapping(laser_data, robot_coord){
    mapping.width = 769;
    mapping.height = 729;
    drawMap(laser_data, robot_coord);
}
function clearMap(){
	ctx_map.clearRect(0, 0, mapping.width, mapping.height);
	trail = [];
}
function drawMap(dataLaser, robot_coord){
    var distance = 0;
    var n = 0;
    var px = 0, py = 0;

    /* In the first iteration there is nothing to restore */
    if(aux_map != 0){
        restoreDrawingSurface();
    }
    else{
        aux_map = 1;
    }
    
    for(let d of dataLaser){
        // alert(`code=${d[0]} reason=${d[1]}`);
        px = Math.round(d[0]);
        py = Math.round(d[1]);
        n = Math.pow((d[0]-robot_coord[0]),2) + Math.pow((d[1]-robot_coord[1]),2);
        distance = Math.sqrt(n);
        points = [px, py];
        if(mapCoord.has(points) == false){
            mapCoord.set(points, 255);
        }
        else{
            number = mapCoord.get(points);
            number = number - 1;
            mapCoord.set(points, number);
        }
        color = '#' + (mapCoord.get(points)).toString(16);
        ctx_map.fillStyle = color;
        ctx_map.strokeStyle = "#FFFFFF";
        ctx_map.beginPath();
        ctx_map.moveTo(robot_coord[0], robot_coord[1]);
        ctx_map.lineTo(px,py);
        ctx_map.stroke();
        if(distance < 260){
            ctx_map.fillRect(px,py,1,1);
        }
        ctx_map.closePath();
    }    
    saveDrawingSurface();
}

function saveDrawingSurface(){
    drawingSurfaceImageData = ctx_map.getImageData(0, 0, mapping.width, mapping.height);
}
function restoreDrawingSurface(){
    ctx_map.putImageData(drawingSurfaceImageData, 0, 0);
}
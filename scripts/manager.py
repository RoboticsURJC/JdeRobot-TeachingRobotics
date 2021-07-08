#!/usr/bin/env python3
import sys
import subprocess
import asyncio
import websockets
import os
import threading
import time
import json
import stat

# Function to check if a device exists
def check_device(device_path):
    try:
        return stat.S_ISCHR(os.lstat(device_path)[stat.ST_MODE])
    except:
        return False

DRI_PATH = "/dev/dri/card0"
ACCELERATION_ENABLED = check_device(DRI_PATH)

# Docker Thread class for running commands on threads
class DockerThread(threading.Thread):
    def __init__(self, cmd):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.out = None

    def run(self):
        stream = os.popen(self.cmd)
        output = stream.read()
        self.out = output
     
    def print_output(self):
        return self.out

# Class to store the commands
class Commands:
    # Initialization function
    def __init__(self):
        # Constants
        self.GAZEBO_RESOURCE_PATH = "export GAZEBO_RESOURCE_PATH=/usr/share/gazebo-9:$GAZEBO_RESOURCE_PATH:"
        self.DISPLAY = ":0"

        self.read_json_instructions("instructions.json")

    # Function to read the instructions to run an exercise
    def read_json_instructions(self, path):
        with open(path) as f:
            self.instructions = json.load(f)

    # Function to get the Gazebo Path Variables
    def get_gazebo_path(self, exercise):
        gazebo_path = self.GAZEBO_RESOURCE_PATH + self.instructions[exercise]["gazebo_path"] + ";"
        return gazebo_path

    # Function to get the instructions to run ROS
    def get_ros_instructions(self, exercise):
        if ACCELERATION_ENABLED:
            roslaunch_cmd = '/bin/sh -c "export PWD="/";chmod +rwx /;export DISPLAY=:0;export VGL_DISPLAY=/dev/dri/card0;export OLDPWD=/etc/ros/rosdep;cd /;export LD_LIBRARY_PATH=/opt/ros/melodic/lib:/usr/lib/x86_64-linux-gnu/gazebo-9/plugins;export GAZEBO_MODEL_PATH=/usr/share/gazebo-9/models:$GAZEBO_MODEL_PATH;export GAZEBO_MODEL_DATABASE_URI=http://gazebosim.org/models;export ROS_DISTRO=melodic;export PKG_CONFIG_PATH=/opt/ros/melodic/lib/pkgconfig;export OGRE_RESOURCE_PATH=/usr/lib/x86_64-linux-gnu/OGRE-1.9.0;export SHLVL=1;export GAZEBO_PLUGIN_PATH=/usr/lib/x86_64-linux-gnu/gazebo-9/plugins:${GAZEBO_PLUGIN_PATH};export TERM=xterm;export ROS_VERSION=1;export GAZEBO_MASTER_URI=http://localhost:11345;ROS_ETC_DIR=/opt/ros/melodic/etc/ros;export CMAKE_PREFIX_PATH=/opt/ros/melodic;export ROS_PACKAGE_PATH=/opt/ros/melodic/share; chmod +x /opt/ros/melodic/bin/rosmaster;export ' \
                        'PYTHONPATH=/opt/ros/melodic/lib/python2.7/dist-packages; chmod +x /opt/ros/melodic/bin/roslaunch ; cd ' \
                        '/; export ROS_ROOT=/opt/ros/melodic/share/ros;export GAZEBO_RESOURCE_PATH=/usr/share/gazebo-9:$GAZEBO_RESOURCE_PATH; export ' \
                        'ROS_MASTER_URI=http://localhost:11311; export PATH=/opt/ros/melodic/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin;' \
                        'export ROS_PACKAGE_PATH=/opt/ros/melodic/share:/Firmware:/Firmware/Tools/sitl_gazebo;'
        elif ("amigo_bot" in exercise): 
            roslaunch_cmd = ""
        else:
            roslaunch_cmd = '/bin/sh -c "export PWD="/";chmod +rwx /;export DISPLAY=:0;export OLDPWD=/etc/ros/rosdep;cd /;export LD_LIBRARY_PATH=/opt/ros/melodic/lib:/usr/lib/x86_64-linux-gnu/gazebo-9/plugins;export GAZEBO_MODEL_PATH=/usr/share/gazebo-9/models:$GAZEBO_MODEL_PATH;export GAZEBO_MODEL_DATABASE_URI=http://gazebosim.org/models;export ROS_DISTRO=melodic;export PKG_CONFIG_PATH=/opt/ros/melodic/lib/pkgconfig;export OGRE_RESOURCE_PATH=/usr/lib/x86_64-linux-gnu/OGRE-1.9.0;export SHLVL=1;export GAZEBO_PLUGIN_PATH=/usr/lib/x86_64-linux-gnu/gazebo-9/plugins:${GAZEBO_PLUGIN_PATH};export TERM=xterm;export ROS_VERSION=1;export GAZEBO_MASTER_URI=http://localhost:11345;ROS_ETC_DIR=/opt/ros/melodic/etc/ros;export CMAKE_PREFIX_PATH=/opt/ros/melodic;export ROS_PACKAGE_PATH=/opt/ros/melodic/share; chmod +x /opt/ros/melodic/bin/rosmaster;export ' \
                        'PYTHONPATH=/opt/ros/melodic/lib/python2.7/dist-packages; chmod +x /opt/ros/melodic/bin/roslaunch ; cd ' \
                        '/; export ROS_ROOT=/opt/ros/melodic/share/ros;export GAZEBO_RESOURCE_PATH=/usr/share/gazebo-9:$GAZEBO_RESOURCE_PATH; export ' \
                        'ROS_MASTER_URI=http://localhost:11311; export PATH=/opt/ros/melodic/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin;' \
                        'export ROS_PACKAGE_PATH=/opt/ros/melodic/share:/Firmware:/Firmware/Tools/sitl_gazebo;'
        gz_cmd = roslaunch_cmd
        roslaunch_cmd = roslaunch_cmd + self.get_gazebo_path(exercise)
        for instruction in self.instructions[exercise]["instructions_ros"]:
            if not (ACCELERATION_ENABLED):
                roslaunch_cmd = roslaunch_cmd + instruction + ";"
            else:
                roslaunch_cmd = roslaunch_cmd + "vglrun " + instruction + ";"
        roslaunch_cmd = roslaunch_cmd + '"'
        return roslaunch_cmd, gz_cmd

    # Function to start gzclient
    def start_gzclient(self, exercise, width, height):
        # Configure browser screen width and height for gzclient
        gzclient_config_cmds = ["echo [geometry] > ~/.gazebo/gui.ini;",
                                "echo x=0 >> ~/.gazebo/gui.ini;",
                                "echo y=0 >> ~/.gazebo/gui.ini;",
                                f"echo width={width} >> ~/.gazebo/gui.ini;",
                                f"echo height={height} >> ~/.gazebo/gui.ini;"]

        if not (ACCELERATION_ENABLED):
	    # Write display config and start gzclient
            gzclient_cmd = (f"export DISPLAY={self.DISPLAY};" + self.get_gazebo_path(exercise) + "".join(gzclient_config_cmds) + "gzclient --verbose")
        else:
            gzclient_cmd = (f"export DISPLAY={self.DISPLAY};" +
		    self.get_gazebo_path(exercise) +
		    "".join(gzclient_config_cmds) +
		    "export VGL_DISPLAY=/dev/dri/card0; vglrun gzclient --verbose")
        gzclient_thread = DockerThread(gzclient_cmd)
        gzclient_thread.start()

    # Function to stop gzclient
    def stop_gzclient(self):
        cmd_stop = "pkill -f gzclient"
        os.popen(cmd_stop)

    # Function to start the console
    def start_console(self, width, height):
        # Write display config and start the console
        width = int(width) / 10; height = int(height) / 18
        console_cmd = f"export DISPLAY=:1;"
        if ACCELERATION_ENABLED:
            console_cmd += f"vglrun xterm -fullscreen -sb -fa 'Monospace' -fs 10 -bg black -fg white"
        else:
            console_cmd += f"xterm -geometry {int(width)}x{int(height)} -fa 'Monospace' -fs 10 -bg black -fg white"

        console_thread = DockerThread(console_cmd)
        console_thread.start()

    # Function to start VNC server
    def start_vnc(self, display, internal_port, external_port):
        if not (ACCELERATION_ENABLED):
            # Start VNC server without password, forever running in background
            x11vnc_cmd = f"x11vnc -display {display} -nopw -forever -xkb -bg -rfbport {internal_port}"
            x11vnc_thread = DockerThread(x11vnc_cmd)
            x11vnc_thread.start()

            # Start noVNC with default port 6080 listening to VNC server on 5900
            novnc_cmd = f"/noVNC/utils/launch.sh --listen {external_port} --vnc localhost:{internal_port}"
            novnc_thread = DockerThread(novnc_cmd)
            novnc_thread.start()
        else:
            # Start VNC server without password, forever running in background
            turbovnc_cmd = f"export VGL_DISPLAY=/dev/dri/card0; export TVNC_WM=startlxde; /opt/TurboVNC/bin/vncserver {display} -geometry '1920x1080' -vgl -noreset -SecurityTypes None -rfbport {internal_port}"
            turbovnc_thread = DockerThread(turbovnc_cmd)
            turbovnc_thread.start()

            # Start noVNC with default port 6080 listening to VNC server on 5900
            novnc_cmd = f"noVNC/utils/launch.sh  --listen {external_port} --vnc localhost:{internal_port}"
            novnc_thread = DockerThread(novnc_cmd)
            novnc_thread.start()

    # Function to start an exercise
    def start_exercise(self, exercise):
        host_cmd = self.instructions[exercise]["instructions_host"]
        host_thread = DockerThread(host_cmd)
        host_thread.start()

        try:
            gui_cmd = self.instructions[exercise]["instructions_gui"]
            gui_thread = DockerThread(gui_cmd)
            gui_thread.start()
        except KeyError:
            pass

    # Function to start the Xserver
    def start_xserver(self, display):
        xserver_cmd = f"/usr/bin/Xorg -noreset +extension GLX +extension RANDR +extension RENDER -logfile ./xdummy.log -config ./xorg.conf {display}"
        xserver_thread = DockerThread(xserver_cmd)
        xserver_thread.start() 

    # Function to roslaunch Gazebo Server
    def start_gzserver(self, exercise):
        roslaunch_cmd,gz_cmd = self.get_ros_instructions(exercise)
        if exercise in ("drone_cat_mouse", "follow_turtlebot", "follow_road", "position_control", "labyrinth_escape"):
            os.popen(roslaunch_cmd)
        else:
            roslaunch_thread = DockerThread(roslaunch_cmd)
            roslaunch_thread.start()
        args=["gz", "stats", "-p"]
        repeat = True
        while repeat:
            process = subprocess.Popen(args, stdout=subprocess.PIPE, bufsize=1)
            with process.stdout:
                for line in iter(process.stdout.readline, b''):
                    if not ("is not running" in line.decode()):
                        repeat = False
                        break
                    else:
                        repeat = True



    # Function to pause Gazebo physics
    def pause_physics(self):
        cmd = "/opt/ros/melodic/bin/rosservice call gazebo/pause_physics"
        rosservice_thread = DockerThread(cmd)
        rosservice_thread.start()

    # Function to unpause Gazebo physics
    def unpause_physics(self):
        cmd = "/opt/ros/melodic/bin/rosservice call gazebo/unpause_physics"
        rosservice_thread = DockerThread(cmd)
        rosservice_thread.start()

    # Function to reset Gazebo physics
    def reset_physics(self):
        cmd = "/opt/ros/melodic/bin/rosservice call gazebo/reset_simulation"
        rosservice_thread = DockerThread(cmd)
        rosservice_thread.start()

    # Function to kill every program
    async def kill_all(self):
        cmd_py = 'pkill -9 -f "python "'
        os.popen(cmd_py)
        cmd_gz = "pkill -9 -f gz"
        os.popen(cmd_gz)
        cmd_launch = "pkill -9 -f launch.py"
        os.popen(cmd_launch)
        cmd_exercise = "pkill -9 -f exercise.py"
        os.popen(cmd_exercise)
        cmd_gui = "pkill -9 -f gui.py"
        os.popen(cmd_gui)
        cmd_host = "pkill -9 -f node"
        os.popen(cmd_host)
        cmd_host = "pkill -9 -f gzserver"
        os.popen(cmd_host)
        cmd_client = "pkill -9 -f gzclient"
        os.popen(cmd_client)
        cmd_ros = "pkill -9 -f roslaunch"
        os.popen(cmd_ros)
        cmd_rosout = "pkill -9 -f rosout"
        os.popen(cmd_rosout)
        cmd_mel = "pkill -9 -f melodroot"
        os.popen(cmd_mel)
        cmd_rosout = "pkill -9 -f rosout"
        os.popen(cmd_rosout)
        cmd_websocki = "pkill -9 -f websockify"
        os.popen(cmd_websocki)
        cmd_x11vnc = "pkill -9 -f x11vnc"
        os.popen(cmd_x11vnc)
        cmd_novnc = "pkill -9 -f launch.sh"
        os.popen(cmd_novnc)
        os.popen(cmd_novnc)
        cmd_console = "pkill -9 -f xterm"
        os.popen(cmd_console)


# Main Manager class
class Manager:
    # Initialization function
    def __init__(self):
        self.server = None
        self.client = None
        self.host = "0.0.0.0"
        self.commands = Commands()
        self.launch_level = 0

        self.exercise = None
        self.height = None
        self.width = None

    # Function to handle all the requests
    async def handle(self, websocket, path):
        self.client = websocket
        
        async for message in websocket:
            data = json.loads(message)
            command = data["command"]
            if command == "open":
                self.width = data.get("width", 1920)
                self.height = data.get("height", 1080)
                self.exercise = data["exercise"]

                if not (ACCELERATION_ENABLED):
                    self.open_simulation(self.exercise, self.width, self.height)
                else:
                    self.open_accelerated_simulation(self.exercise, self.width, self.height)
            elif command == "resume":
                self.resume_simulation()
            elif command == "stop":
                self.stop_simulation()
            elif command == "start":
                self.start_simulation()
            elif command == "reset":
                self.reset_simulation()
            elif command == "stopgz":
                self.stop_gz()
                await websocket.send("Ping{}".format(self.launch_level))
            elif command == "startgz":
                self.start_gz()
                await websocket.send("Ping{}".format(self.launch_level))
            elif "Pong" in command:
                await websocket.send("Ping{}".format(self.launch_level))
            else:
                await self.kill_simulation()

    
    # Function to open non-accelerated simulation
    def open_simulation(self, exercise, width, height):
        print("> Starting simulation")

        # X Server for Console and Gazebo
        self.commands.start_xserver(":0")
        self.commands.start_xserver(":1")

        # Start the exercise

        if not ("color_filter" in exercise):
            self.commands.start_gzserver(exercise)
            self.commands.start_exercise(exercise)
            time.sleep(5)
            self.launch_level = 3

            # Start x11vnc servers
            self.commands.start_vnc(":0", 5900, 6080)
            self.commands.start_vnc(":1", 5901, 1108)

            # Start gazebo client
            time.sleep(2)
            self.commands.start_console(width, height)
        else:
            self.commands.start_exercise(exercise)
            time.sleep(2)
            self.launch_level = 3
            self.commands.start_vnc(":1", 5900, 1108)
            self.commands.start_console(1920, 1080)

    # Function to open accelerated simulation
    def open_accelerated_simulation(self, exercise, width, height):
        print("> Starting accelerated simulation")

        # Start VNC and accelerated displays
        self.commands.start_vnc(":0", 5900, 6080)

        # Start the exercise
        
        if not ("color_filter" in exercise):
            self.commands.start_gzserver(exercise)
            self.commands.start_exercise(exercise)
            time.sleep(5)
            self.launch_level = 3

            self.commands.start_vnc(":1", 5901, 1108)

            # Start gazebo client
            time.sleep(2)
            self.commands.start_console(width, height)
        else:
            self.commands.start_exercise(exercise)
            time.sleep(2)
            self.launch_level = 3
            self.commands.start_vnc(":1", 5900, 1108)
            self.commands.start_console(1920, 1080)

    # Function to resume simulation
    def resume_simulation(self):
        print("Resume Simulation")
        self.commands.unpause_physics()

    # Function to stop simulation
    def stop_simulation(self):
        print("Stop Simulation")
        self.commands.pause_physics()

    # Function to start simulation
    def start_simulation(self):
        print("Starting Simulation")
        self.commands.unpause_physics()

    # Function to reset simulation
    def reset_simulation(self):
        print("Reset Simulation")
        self.commands.reset_physics()

    # Function to start gz client
    def start_gz(self):
        print("Starting Gzclient")
        self.commands.start_gzclient(self.exercise, self.width, self.height)

    # Function to stop gz client
    def stop_gz(self):
        print("Closing Gzclient")
        self.commands.stop_gzclient()

    # Function to kill simulation
    async def kill_simulation(self):
        print("Kill simulation")
        await self.commands.kill_all()
                
    # Function to start the websocket server
    def run_server(self):

        self.server = websockets.serve(self.handle, self.host, 8765)
        asyncio.get_event_loop().run_until_complete(self.server)
        asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    server = Manager()
    server.run_server()

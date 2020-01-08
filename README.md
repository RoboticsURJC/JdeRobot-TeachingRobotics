# JdeRobot-Academy: Learn Robotics and Computer Vision 

## Status

Available exercises and its status:

|      Category       |        Exercise         |     Status     |      Robot       | Infrastructure | Solution |  Theory  | Language |
| :-----------------: | :---------------------: | :------------: | :--------------: | :------------: | :------: | :------: | :------: |
|                     | 3D Reconstruction       | **Production** |      Camera      |    **DONE**    | **DONE** | **DONE** |  Python  |
|       Vision        | Color Filter            | **Production** |      Camera      |    **DONE**    | **DONE** | **DONE** |  Python  |
|                     | FollowFace              | **Production** |  Sony Evi d100p  |    **DONE**    | **DONE** | **DONE** |  Python  |
| :-----------------: | :---------------------: | :------------: | :--------------: | :------------: | :------: | :------: | :------: |
|                     | Bump&Go                 | **Production** | TurtleBot        | **DONE**       | **DONE** | **DONE** |  Python  |
|                     | Amazon Warehouse        | Prototype      | AmazonBot        | **DONE**       | WIP      |  Review  |  Python  |
|   Mobile Robots     | Follow Line Turtlebot   | **Production** | TurtleBot        | **DONE**       | ?        | **DONE** |  Python  |
|                     | Laser Loc               | **Production** | Roomba           | **DONE**       | **DONE** | **DONE** |  Python  |
|                     | Vacuum Cleaner          | **Production** | Roomba           | **DONE**       | **DONE** | **DONE** |  Python  |
|                     | Vacuum SLAM             | **Production** | Roomba           | **DONE**       | **DONE** | **DONE** |  Python  |
| :-----------------: | :---------------------: | :------------: | :--------------: | :------------: | :------: | :------: | :------: |
|                     | Autopark                | **Production** | TaxiHolo         | **DONE**       | **DONE** | **DONE** |  Python  |
|                     | Cross Roads with Stop   | **Production** | Opel             | **DONE**       | **DONE** | **DONE** |  Python  |
|   Autonomous Cars   | Qualifying F1           | WIP            | F1               | WIP            | WIP      | Review   |  Python  |
|                     | Global Navigation (GPP) | **Production** | TaxiHolo         | **DONE**       | **DONE** | **DONE** |  Python  |
|                     | Obstacle Avoidance (VFF)| **Production** | F1               | **DONE**       | **DONE** | **DONE** |  Python  |
|                     | Follow Line             | **Production** | F1               | **DONE**       | **DONE** | **DONE** |  Python  |
| :-----------------: | :---------------------: | :------------: | :--------------: | :------------: | :------: | :------: | :------: |
|                     | Drone Hangar            | Prototype      | Drone            | WIP            | WIP      | **DONE** |  Python  |
|                     | Follow Road             | **Production** | Drone            | **DONE**       | ?        | **DONE** |  Python  |
|                     | Follow Turtlebot        | **Production** | Drone            | **DONE**       | ?        | **DONE** |  Python  |
|                     | Drone Cat Mouse         | **Production** | Drone            | **DONE**       | **DONE** | **DONE** |  Python  |
|       Drones        | Labyrinth Escape        | **Production** | Drone            | **DONE**       | ?        | **DONE** |  Python  |
|                     | Position Control        | **Production** | Drone            | **DONE**       | **DONE** | **DONE** |  Python  |
|                     | Rescue People           | **Production** | Drone            | **DONE**       | Review   | **DONE** |  Python  |
|                     | Visual Lander           | ?              | Drone            | **DONE**       | ?        | Review   |  Python  |
|                     | Path Planning and Navigation in 3D | **Prototype** | Drone  | **DONE**       | ?        | ?        |  Python  |
| :-----------------: | :---------------------: | :------------: | :--------------: | :------------: | :------: | :------: | :------: |
|  Industrial Robots  | Look and Push           | ?              | Robotic Arm      | ?              | ?        | ?        |  Python  |











## Introduction

JdeRobot-Academy is an **open source** collection of exercises to learn robotics in a practical way. Gazebo simulator is the main tool required, as ROS. The students program their solutions in **Python language**. Each exercise is composed of :

1. Gazebo configuration files,
2. A ROS node that hosts the student's code, 
3. A file with instructions, hints, etc.. 
4. The student solution itself. 

1, 2, and 3 are already provided, the student has to develop her code on a separate file which already has a **template**. The student may use there an existing simple *Python* *API* to access to sensor readings and actuator commands_ (**HAL API**) and she may use an existing simple *Python* API for Graphical User Interface and debugging_ (**GUI API**). To develop her solution the student has to edit that template file and add her
code, using her favorite text editor.

For execution the student launches Gazebo with certain configuration file (specifying the robot and the simulated scenario for that exercise) and launches the ROS node hosting her code. On that code lies the intelligence of the robot to solve the exercise. For instance, check the recent solution of one degree student here for the local navigation exercise:

[![http://jderobot.org/store/jmplaza/uploads/jderobot-academy/vff-f1.png](http://img.youtube.com/vi/ID7qaEcIu4k/0.jpg)](http://www.youtube.com/watch?v=ID7qaEcIu4k "Obstacle Avoidance exercise in JdeRobot-Academy")

There are exercises about drone programming, about computer vision, about mobile robots, about autonomous cars, etc..  In the JdeRobotFoundation we are improving the quality of the existing exercises and creating a few exercises more. We are also working in a webserver to code and [run the exercises from the web browser](https://www.youtube.com/watch?v=bTwt6W8vCGQ) but that is a ongoing project yet.

## Installation Guide

### Software Infraestructure: Ubuntu/Debian

The programming environment is composed of the (a) Gazebo simulator, (b) ROS middleware and (c) the Academy package. All this software is open source so there are alternative ways to install all of them directly from the source code. Currently we use Gazebo-7.4.0, ROS Medloci and JdeRobot-Academy with (2018-06-06) releases Ubuntu 18.04.3 . Follow the next steps to have the environment up and running, ready to use.

### Installation                             

##### Step One: Install ROS framework

Add the lastest ROS sources:

```Bash
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
```

```bash
sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116
```

##### Step Two: Add the lastest Gazebo sources:

 Add the lastest Gazebo sources:

```bash
sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable lsb_release -cs main" > /etc/apt/sources.list.d/gazebo-stable.list'
```

```bash
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key 67170598AF249743
```

##### Step Three: Add JdeRobot sources

Add the JdeRobot sources. For Ubuntu Xenial(16.04):

```bash
sudo sh -c 'cat<<EOF>/etc/apt/sources.list.d/jderobot.list
# for ubuntu 16.04 LTS (64 bit)

deb [arch=amd64] http://wiki.jderobot.org/apt bionic main
EOF'
```

```bash
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 24E521A4
```

##### Step Four: Update repositories and Install the packages

Update the repositories
```bash
sudo apt update
```

Install the packages

```bash
sudo apt-get install ros-melodic-desktop-full
sudo apt-get install gazebo7
sudo apt install jderobot-gazebo-assets
```

### Install the JdeRobot-Academy software

  Once you have JdeRobot installed in your system, you can download and install the Academy software. To do so, you must:

```bash
 git clone https://github.com/JdeRobot/Academy.git
```

On the directory of each exercise you will find particular directions to launch the simulated scenario and the academic node where you should write your code.


## Software Infraestructure: Windows(x64)

The programming environment is composed of the (a) *Docker* with *Gazebo* simulator, (b) *JdeRobot* *middleware* for *Python* and (c) the *TeachingRobotics* package. All this software is open source so there are alternative ways to install all of them directly from the source code. Currently we use *Gazebo-7.4.0*, *JdeRobot-5.4.1* and TeachingRobotics-0.1.0 releases. *JdeRobot* Docker includes the Gazebo plugins, models and configuration files to simulate the robot used in the exercises. Follow the next four steps to have the environment up and running, ready to use.        

#### Installation

* Install checked `env` variables (Is possible that you need restart to run the PATH). You can <a href="https://www.python.org/ftp/python/3.5.2/python-3.5.2-amd64.exe">download here</a>.
* Download qt 5.7. <a href="http://download.qt.io/official_releases/qt/5.7/5.7.0/qt-opensource-windows-x86-msvc2015_64-5.7.0.exe">Here</a>.
* Download github Desktop from <a href="https://desktop.github.com/">here</a>.
* Download Docker:
    * <a href="https://download.docker.com/win/stable/InstallDocker.msi">Windows 10 x64 proffesional or enterprise</a>
    * <a href="http://www.docker.com/products/docker-toolbox">Other Windows x64</a>

##### Open `CMD` or powershell and upgrade pip

```bash
python -m pip install --upgrade pip
```

##### Install depencencies:

```bash
pip3 install numpy zeroc-ice
pip3 install pyqt5
pip3 install opencv-python
```

##### Install JdeRobot Python:

```bash
pip3 install http://jderobot.org/store/aitormf/uploads/windows/JdeRobot-0.1.0-py3-none-any.whl
```

##### Download the Academy software

With git Shell clone the repository as in Linux and run the exercices with CMD o powershell

```
git clone https://github.com/jderobot/academy.git
```

*Note: Github repositories are located in Documents\GitHub*


## Run Exercises

Open Kinematics of Docker and push "Docker cli".

Run the docker passing the world to use (the first time docker image is downloaded):

```bash
docker run -tiP --rm -p 7681:7681 jderobot/jderobot world [world_name]
```

With CMD or PowerShell go to practice directory in Academy and run it:

```bash
python [practice_file][config_file]
```

You can watch a [video demonstration](https://www.youtube.com/embed/v00TCr-aSWM).


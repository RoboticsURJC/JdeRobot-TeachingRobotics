---
permalink: /installation/
title: "INSTALLATION INSTRUCTIONS"

sidebar:
  nav: "docs"

toc: true
toc_label: "TOC installation"
toc_icon: "cog"
---


Robotics-Academy currently supports **Linux** operating system. These installation instructions have been prepared for Ubuntu Linux 18.04 (LTS). Don't install everything listed here, just follow the directions on the Academy exercise you want to perform. For instance, not all the specific infrastructure packages are required for every exercise, and they can be large packages.

1. *Generic infrastucture*
    - Required
    - ROS middleware, Gazebo simulator, JdeRobot-base, JdeRobot-assets

2. *Specific infrastructure*
    - Optional, depends on the exercise
    - Some exercises require also additional software pieces such as OpenCV, MoveIt!, MavROS, PX4, VisualStates, OpenMotionPlanningLibrary, etc.

3. *JdeRobot Academy source code*
    - Required
    - Academy includes templates for the exercises

# Generic infrastructure

## ROS Middleware

Supported release is ROS-Melodic. It can be easily installed from official Debian packages, maintained by OpenRobotics organization.

1. Add the lastest ROS source:

    ```bash
    sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
    ```

    ```bash
 sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
    ```
<!-- sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116 -->


2. Update the repositories

    ```bash
    sudo apt update
    ```

3. Install the official ROS Melodic Debian package

    ```bash
    sudo apt install ros-melodic-desktop-full
    ```

## Gazebo simulator

Supported release is Gazebo-9. It can be easily installed from official Debian packages, maintained by OpenRobotics organization. You can safely ignore this step as Gazebo-9 will be automatically installed with ROS Melodic package (described in the [previous step](/RoboticsAcademy/installation/#ros-middleware)).

<!--
1. Add the lastest Gazebo source:

    ```bash
    sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable lsb_release -cs main" > /etc/apt/sources.list.d/gazebo-stable.list'
    ```

    ```bash
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key 67170598AF249743
    ```

2. Install the official Gazebo package:

    ```bash
    sudo apt install gazebo9
    ```
-->

## JdeRobot-base

Supported release is 6.0.0.
It contains ROS drivers not included in the official ROS packages.

1. Add the latest JdeRobot-base source

    ```bash
    sudo sh -c 'echo "deb [arch=amd64] http://wiki.jderobot.org/apt `lsb_release -cs` main" > /etc/apt/sources.list.d/jderobot.list'
    ```

2. Get and add the public key from the JdeRobot repository

    ```bash
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 24E521A4
    ```

3. Update the repositories

    ```bash
    sudo apt update
    ```

4. Install JdeRobot-base

    ```bash
    sudo apt install jderobot
    ```

## JdeRobot-assets

Supported release is 6.0.2
It contains Gazebo world files and configuration files required for the Academy exercises.

1. Install jderobot-assets debian package

    ```bash
    sudo apt install jderobot-assets
    ```

2. Install jderobot-assets ROS package

    ```bash
    sudo apt install ros-melodic-jderobot-assets
    ```

3. Install jderobot-gazebo-assets ROS package

    ```bash
    sudo apt install jderobot-gazebo-assets
    ```

# Specific infrastructure

## OpenCV

You can install OpenCV in several ways:

- Installing from the [PyPi repository](https://pypi.org/project/opencv-python/).
- Compiling it from its [source code](https://docs.opencv.org/3.4.1/d2/de6/tutorial_py_setup_in_ubuntu.html).

For more information, visit the [official repository](https://github.com/opencv/opencv).

## MavROS

1. Install ROS Melodic, MAVROS and extras

    ```bash
    sudo apt install ros-melodic-mavros ros-melodic-mavros-extras
    ```


## PX4

Install previous dependencies:

1. Download and install GeographicLib

    ```bash
    wget https://raw.githubusercontent.com/mavlink/mavros/master/mavros/scripts/install_geographiclib_datasets.sh
    ./install_geographiclib_datasets.sh
    ```

2. Remove modemmanager

    ```bash
    sudo apt remove modemmanager
    ```

3. Install common dependencies

    ```bash
    sudo apt update -y
    sudo apt install git zip qtcreator cmake \
        build-essential genromfs ninja-build exiftool -y
    ```

4. Install xxd

    ```bash
    which xxd || sudo apt install xxd -y || sudo apt install vim-common --no-install-recommends -y
    ```

5. Install required python packages

    ```bash
    sudo apt install python-argparse \
        python-empy python-toml python-numpy python-yaml \
        python-dev python-pip -y
    sudo -H pip install --upgrade pip
    sudo -H pip install pandas jinja2 pyserial cerberus
    sudo -H pip install pyulog
    ```

6. Install ninja

    ```bash
    sudo apt install ninja-build -y
    ```

7. Get FastRTPS and FastCDR

    ```bash
    wget https://www.eprosima.com/index.php/component/ars/repository/eprosima-fast-rtps/eprosima-fast-rtps-1-7-1/eprosima_fastrtps-1-7-1-linux-tar-gz -O eprosima_fastrtps-1-7-1-linux.tar.gz
    tar -xzf eprosima_fastrtps-1-7-1-linux.tar.gz eProsima_FastRTPS-1.7.1-Linux/
    tar -xzf eprosima_fastrtps-1-7-1-linux.tar.gz requiredcomponents
    tar -xzf requiredcomponents/eProsima_FastCDR-1.0.8-Linux.tar.gz
    ```

8. Build FastRTPS and FastCDR

    ```bash
    (cd eProsima_FastCDR-1.0.8-Linux && ./configure --libdir=/usr/lib && make -j2 && sudo make install)
    (cd eProsima_FastRTPS-1.7.1-Linux && ./configure --libdir=/usr/lib && make -j2 && sudo make install)
    rm -rf requiredcomponents eprosima_fastrtps-1-7-1-linux.tar.gz
    ```

9. Install catkin tools

    ```bash
    sudo apt install python-catkin-tools
    ```

10. Set up catkin workspace

    ```bash
    mkdir -p catkin_ws/src
    cd catkin_ws/src
    git clone https://github.com/PX4/Firmware.git
    cd Firmware
    git submodule update --init --recursive
    cd ..
    ln -s Firmware/Tools/sitl_gazebo mavlink_sitl_gazebo
    cd ..
    ```

11. Update ROS dependencies

    ```bash
    rosdep update
    rosdep check --from-paths . --ignore-src --rosdistro melodic
    rosdep install --from-paths . --ignore-src --rosdistro melodic -y
    ```

12. Build catkin (make sure to be at /catkin_ws)

    ```bash
    catkin build
    ```

13. Export environment variables

    ```bash
    echo 'source '$PWD'/devel/setup.bash' >> ~/.bashrc
    echo 'export GAZEBO_RESOURCE_PATH=${GAZEBO_RESOURCE_PATH}:/usr/share/gazebo-9' >> ~/.bashrc
    echo 'export GAZEBO_MODEL_PATH=${GAZEBO_MODEL_PATH}:/opt/ros/melodic/share/jderobot_assets/models' >> ~/.bashrc

    source ~/.bashrc
    ```

## MoveIt!

# Academy source code

Once you have generic and specific infrastructure installed in your system, you can download and install the JdeRobot Academy software.

1. Clone the Academy software repository

    ```bash
    git clone https://github.com/JdeRobot/Academy.git
    ```

<!---

# Installation on Windows(x64)  DEPRECATED

The programming environment is composed of the (a) Docker with Gazebo simulator, (b) JdeRobot middleware for Python and (c) the TeachingRobotics package. All this software is open source so there are alternative ways to install all of them directly from the source code. Currently we use Gazebo-7.4.0, JdeRobot-5.4.1 and TeachingRobotics-0.1.0 releases. JdeRobot Docker includes the Gazebo plugins, models and configuration files to simulate the robot used in the exercises.

### Prerequisites

First check that you have the following dependencies installed. If not, you can install them in the links provided.

- Install checked `env` variables (Is possible that you need restart to run the PATH). You can <a href="https://www.python.org/ftp/python/3.5.2/python-3.5.2-amd64.exe" target="_blank">download here</a>.

- Download qt 5.7 <a href="http://download.qt.io/official_releases/qt/5.7/5.7.0/qt-opensource-windows-x86-msvc2015_64-5.7.0.exe" target="_blank">here</a>.
- Download github Desktop <a href="https://desktop.github.com" target="_blank">from here</a>.
- Download Docker:
  - <a href="https://download.docker.com/win/stable/InstallDocker.msi" target="_blank">Windows 10 x64 proffesional or enterprise</a>
  - <a href="http://www.docker.com/products/docker-toolbox" target="_blank"> Other Windows x64</a>



### Installation

Follow the next four steps to have the environment up and running, ready to use.

1. Upgrade pip.

    Open `CMD` or powershell and upgrade pip typing:

    ```bash
    python -m pip install --upgrade pip
    ```

2. Install dependencies.

    Install the following depencencies

    ```bash
    pip3 install numpy zeroc-ice
    pip3 install pyqt5
    pip3 install opencv-python
    ```

3. Install JdeRobot Python.

    Install JdeRobot Python typing:

    ```bash
    pip3 install http://jderobot.org/store/aitormf/uploads/windows/JdeRobot-0.1.0-py3-none-any.whl
    ```

4. Clone Robotics-Academy repository.

    Download the Academy software. With git Shell clone the repository as in Linux and run the exercices with `CMD` o powershell

    ```bash
    git clone https://github.com/jderobot/academy.git
    ```

_Note: Github repositories are located in `Documents\GitHub`_




### Run Exercises

Open Kinematics of Docker and push "Docker cli".

Run the docker passing the world to use (the first time docker image is downloaded):

```bash
docker run -tiP --rm -p 7681:7681 jderobot/jderobot world [world_name]
```

With `CMD` or PowerShell go to practice directory in Academy and run it:

```bash
python [practice_file][config_file]
```

You can watch a video demonstration.


--->

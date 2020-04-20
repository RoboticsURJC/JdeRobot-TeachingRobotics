---
permalink: /exercises/AutonomousCars/car_junction/
title: "Car Junction exercise"

sidebar:
  nav: "docs"

toc: true
toc_label: "TOC Car Junction"
toc_icon: "cog"

<!--- layout: archive --->

<!--- classes: wide --->

gallery:
  - url: /assets/images/exercises/car_junction/car_junction.png
    image_path: /assets/images/exercises/car_junction/car_junction.png
    alt: "Top View."
    title: "Top View."
  - url: /assets/images/exercises/car_junction/car_junction_teaser.png
    image_path: /assets/images/exercises/car_junction/car_junction_teaser.png
    alt: "Cars at the junction."
    title: "Cars at the junction."
  - url: /assets/images/exercises/car_junction/car_junction_2.png
    image_path: /assets/images/exercises/car_junction/car_junction_2.png
    alt: "GUI."
    title: "GUI."

youtubeId1: hF2i0rdlIqE

---

## Goal

The goal of this practice is to implement the logic of a navigation algorithm for an automated vehicle. The vehicle must Stop at the T joint, where there is a stop sign, wait until there are no cars and pass once the road is clear.

## Installation 

To launch the infrastructure of this practice, first set up the gazebo sources, then launch the simulator with the appropriate scenario:

```bash
source /opt/jderobot/share/jderobot/gazebo/assets-setup.sh
```

or add them directly to your bashrc to run automatically whenever you open a terminal:

```bash
echo 'source /opt/jderobot/share/jderobot/gazebo/gazebo-setup.sh' >> ~/.bashrc
```

```bash
echo 'source /opt/jderobot/share/jderobot/gazebo/assets-setup.sh' >> ~/.bashrc
```

```bash
source ~/.bashrc
```

## How to run your solution

Navigate to the car_junction directory

```bash
cd exercises/car_junction
```

Launch Gazebo with the tele_taxi world through the command 

```bash
roslaunch /opt/jderobot/share/jderobot/gazebo/launch/car_1_junction.launch
```

Execute the practice and user interface
```bash
python2 ./stop.py stop_conf.yml
```

To simplify the closure of the environment, just close the Stop Component window(s). *Ctrl + C will give problems*.

## How to do the practice
To carry out the practice, you must edit the file MyAlgorithm.py and insert all the functionality in it.

### Where to insert the code

- The code that will allow the car to move and stop at the junction will be placed in the execute function, which is executed periodically. 
MyAlgorithm.py

```python
def execute(self):
        
    # Add your code here
    print "Running"
    # Getting the images
    input_image = self.cameraC.getImage().data      
```

### API
* `self.cameraC.getImage().data` - to get image from center camera
* `self.cameraL.getImage().data` - to get image from left camera
* `self.cameraR.getImage().data` - to get image from right camera

* `self.pose3d.getPose3d().x` - to obtain the position of the robot
* `self.pose3d.getPose3d().y` - to obtain the position of the robot
* `self.pose3d.getPose3d().yaw` - to obtain the position of the robot

* `self.motors.sendW()` - to set the angular velocity
* `self.motors.sendV()` - to set the linear velocity

## Demonstrative Video

Stop practice:

{% include youtubePlayer.html id=page.youtubeId1 %}

## Contributers

- Contributors: [Eduardo Perdices](https://github.com/eperdices), [Aitor Martinez Fernandez](https://github.com/aitormf), [Shyngyskhan Abilkassov](https://github.com/kurshakuz/)



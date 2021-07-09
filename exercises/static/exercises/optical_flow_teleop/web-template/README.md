# Follow Line Exercise using WebTemplates

## How to launch the exercise?

For users of Robotics Academy, follow the instructions given on this [link](http://jderobot.github.io/RoboticsAcademy/exercises/AutonomousCars/follow_line/)

Note: For Windows users running the exercise through the web template, the websocket_address would be the IP address of the **vEthernet adapter(WSL)**. This can be found through the following command at the command prompt:
```
ipconfig/all
```

## Dependencies

[F1 models](https://github.com/JdeRobot/CustomRobots/tree/melodic-devel/f1) from CustomRobots repository

### Launch Files

`launch` folder contains the various launch files and world files, for running the Gazebo simulation of the exercise

### Asset Files

`assets` folder contains the Javascript code for the webpage part of the web templates

### Python Files

`exercise.py` is the main Python file to run the exercise

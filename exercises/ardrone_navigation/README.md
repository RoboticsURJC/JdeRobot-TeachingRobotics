# Navigation3DOmpl Exercise

In this practice we will learn the use of ompl to implement a local navigation algorithm in the quadricopters.
For this practice a world has been designed for the Gazebo simulator. This world has a 3D model of the AR.Drone and a indoor environment. 

You can see this [repo](https://github.com/TheRoboticsClub/colab-gsoc2018-HanqingXie) and [web](https://jderobot.org/Club-hanqingxie) for more detials.

## Dependency
This project requires the follow dependency:
* jedrobot
* python2.7
* [OMPL](http://ompl.kavrakilab.org/)

### install ompl
[Download the OMPL installation script](http://ompl.kavrakilab.org/install-ompl-ubuntu.sh). First, make the script executable:

```chmod u+x install-ompl-ubuntu.sh```

Next, there are three ways to run this script:

```./install-ompl-ubuntu.sh --python will install OMPL with Python bindings```

## How to run

1. Copy the inHouse model into jderobot gazebo models

	`$ cp -r models/inHouse /root_jderobot/share/jderobot/gazebo/models/`

2. In a terminal launch the gazebo simulator:

	`$ gazebo ardrone-inHouse.world`

3. In other terminal launch the position_control component with your algorithm:

	`$ python2 ./Navigation3dOmpl.py ardrone_conf.yml`

## How to do the practice
To carry out the practice, you must edit the MyAlgorithm.py file and insert the control logic into it.

## Where to insert the code
[MyAlgorithm.py](MyAlgorithm.py#L65)
```
    def execute(self):

        # Add your code here
        print "Runing"

        #EXAMPLE OF HOW TO SEND INFORMATION TO THE ROBOT ACTUATORS
        #self.motors.sendV(10)
        #self.motors.sendW(5)
        # TODO
        
```

## API

* self.pose.getPose3d().x - returns the position values ​​of the drone in X axis
* self.pose.getPose3d().y - returns the position values ​​of the drone in Y axis
* self.pose.getPose3d().roll, self.pose.getPose3d().pitch, self.pose.getPose3d().yaw: returns the rotation values ​​of the drone in space.
* self.camera.getImage().data: returns the image captured by the active camera of the drone (frontal or ventral).
* self.cmdvel.setVX(velx): set linear speed of the drone.
* self.cmdvel.setVY(vely): set linear speed of the drone.
* self.cmdvel.setVZ(vely): set linear speed of the drone.
* self.cmdvel.setVYaw(vely): set angular speed of the drone.
* self.cmdvel.sendVelocities(): send set velocities to the drone.
* self.cmdvel.sendCMDVel(self,vx,vy,vz,ax,ay,az): sends linear and angular speed commands to the drone.
* self.extra.toggleCam(): changes the drone's active camera (frontal or the one below).
* self.extra.takeOff(): Takeoff of the drone.
* self.extra.land(): landing of the drone.


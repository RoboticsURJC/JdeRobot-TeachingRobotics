---
layout: splash
permalink: /
header:
#  overlay_color: "#5e616c"
  overlay_color: "#FFFFFF"
  overlay_image: /assets/images/cover/test_header_shear_3.png
#  actions:
#    - label: "<i class='fas fa-download'></i> Install now"
#      url: "/installation/"
excerpt: 
  A practical and fun way of learning Robotics and Computer Vision
  
feature_row:
  - image_path: /assets/images/cover/cover_column_1.png
    alt: "Exercises"
    title: "Exercises"
    excerpt: "Learn robot programming solving the Robotics-Academy challenges"
    url: "/exercises/"
    btn_class: "btn--primary"
    btn_label: "Go!"

  - image_path: /assets/images/cover/cover_column_2.png
    alt: "fully responsive"
    title: "Installation"
    excerpt: "Instructions for installing Robotics-Academy dependencies (ROS, Gazebo, assets...)"
    url: "/installation"
    btn_class: "btn--primary"
    btn_label: "Go!"

#  - image_path: /assets/images/cover/cover_column_3.png
#    alt: "100% free"
#    title: "Web release (beta)"
#    excerpt: "Use RoboticsAcademy from your browser, no installation required"
#    url: "/webrelease"
#    btn_class: "btn--primary"
#    btn_label: "Learn more"

  - image_path: /assets/images/cover/forum1.png
    alt: "100% free"
    title: "Forum"
    excerpt: "Receive support, show your results and help others at the community forum"
    url: "https://forum.jderobot.org/c/english/roboticsacademy"
#    url: "/webrelease"
    btn_class: "btn--primary"
    btn_label: "Go!"

  - image_path: /assets/images/cover/cover_column_2.png
    alt: "fully responsive"
    title: "Do you want to contribute?"
    excerpt: "Info for Robotics-Academy *developers*: create a new exercise, improve documentation, fix bugs.... Contributors are welcome!"
    url: "/contribute"
    btn_class: "btn--primary"
    btn_label: "Go!"

youTube_id: ID7qaEcIu4k
---


Robotics-Academy is an **open source** collection of exercises and challenges to learn robotics in a practical way.
There are exercises about drone programming, about computer vision, about mobile robots, about autonomous cars, etc. 
It is mainly based on [Gazebo simulator](http://gazebosim.org) and [ROS](https://www.ros.org). The students program their solutions in **Python** language.

Each exercise is composed of (a) Gazebo configuration files, (b) a ROS node that is the template to host student's code and (c) theory contents. In which student can insert their code in the templete file and uses the provided simple API to access to _sensor readings_ and _actuator commands_ (HAL API) and the provided simple API for Graphical User Interface and debugging (GUI API).

For execution the student launches Gazebo with certain configuration file (specifying the robot and the simulated scenario for that exercise) and launches the ROS node hosting her code.

{% include feature_row %}

{% include video id="ID7qaEcIu4k" provider="youtube" %}

## Releases

* 2.3
    + Web pages for exercise templates
    + Browser for editing user code and execution monitoring
    + Dependencies are pre-installed in [RADI Docker Image](https://hub.docker.com/r/jderobot/robotics-academy/tags)
    + based in ROS-Melodic and Gazebo9
    + works on Linux, Windows and MacOS
* 2.1
    + ROS nodes for exercise templates
    + File editing for user code
    + Dependencies should be installed locally, debian and ROS packages
    + based in ROS-Melodic and Gazebo9
* 2.0

## Scientific papers

1. *Open-Source Drone Programming Course for Distance Engineering Education*. José M. Cañas, Diego Martín-Martín, Pedro Arias, Julio Vega, David Roldán-Álvarez, Lía García-Pérez, Jesús Fernández-Conde. Electronics 2020, 9(12), 2163, MDPI 2020 (Special Issue Open Source Software in Learning Environments). [DOI: https://doi.org/10.3390/electronics9122163](https://doi.org/10.3390/electronics9122163)
2. *A ROS‐Based Open Tool for Intelligent Robotics Education*. José M. Cañas, Eduardo Perdices, Lía García-Pérez, Jesús Fernández-Conde. Applied Sciences 10(21), 7419, MDPI 2020 (Special Issue Advances in Artificial Intelligence Learning Technologies). [DOI: https://doi.org/10.3390/app10217419](https://doi.org/10.3390/app10217419)
3. *Entorno docente universitario para la programación de robots*. José M.Cañas, Alberto Martín, Eduardo Perdices, Francisco Rivas, Roberto Calvo. Revista Iberoamericana de Automática e Informática Industrial, 15, 404-415, 2018 [DOI: https://doi.org/10.4995/riai.2018.8962](https://doi.org/10.4995/riai.2018.8962)

## Sponsors

<figure class="third">
    <a href="https://www.urjc.es/" target="_blank"><img src="{{ site.url }}{{ site.baseurl }}/assets/images/cover/logoURJC.jpg" style="width:400px;"></a>
    <a href="https://github.com/RoboticsLabURJC" target="_blank"><img src="{{ site.url }}{{ site.baseurl }}/assets/images/cover/peloto.png" style="width:400px;"></a>
    <a href="https://summerofcode.withgoogle.com" target="_blank"><img src="{{ site.url }}{{ site.baseurl }}/assets/images/cover/gsoc.png" style="width:200px;"></a>
</figure>

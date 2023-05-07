# Robot_StateEstimation
This is a State Estimation for Robot Rotation module created for Turtlebot3 Burger using ROS, gazebo physics simulator and python. Through sensor fusion of robot odometery and IMU readings by Linear Kalman filter we are able to determine the estimated heading of the robot moving in a circular path as illustrated in the video below. 


https://user-images.githubusercontent.com/73821958/235322117-45ab94d6-cdbf-4264-b908-e422a17d6969.mp4

State estimator architechture is composed of three modules sensors , kalman filtering and output states. In our case the sensors are odometer and IMU which provide the rotation angle and angular velocity. The Kalman filtering process starts with the prediction and update stages using the propgation and measurement model which gives us the final output. The output result of the fusion is the robot estimated state (Rotational angle and angular velocity).  

![Robot State Estimator](https://user-images.githubusercontent.com/73821958/235322829-ad215d92-6396-4d7f-9a89-b1179d269687.png)


The result of the fusion and error ellimination is shown in the graph: 

![Screenshot from 2023-01-07 20-19-02](https://user-images.githubusercontent.com/73821958/235322352-a40c7b6d-2dd7-4f5d-bc77-2a70192a263a.png)

For more information check the full documentation file: [State Estimation of Robot Rotation](https://github.com/dinaashraf20003/TurtleBot_StateEstimation/files/11360014/State.Estimation.of.Robot.Rotation.pdf)

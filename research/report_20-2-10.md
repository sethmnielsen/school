# Simulated Vision-Based Boat Landing - Seth Nielsen

This project is focused on developing a vision-based approach to the problem of autonomously landing a multirotor UAV on an arbitary ship at sea. Previous projects have relied on the placement of a fiducial marker on the boat at the desired landing location for the UAV to estimate its relative position and to execute the landing sequence. Because such an approach limits the ability of the UAV to land on any sea vessel to only those that have been specially prepared with the marker, we chose to design a method that could allow a UAV to land on an arbitrary boat of a given type without any modification beyond the basic requirement of providing a flat, cleared area of sufficient size to accommodate the UAV.

To accomplish this task, we have planned a new method consisting of three parts that will utilize a combination of vision-based techniques.
    Stage 1 will use a convolutional neural network to analyze the
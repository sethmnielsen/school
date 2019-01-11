%MDL_HW_2

clear L

%%%%%%%%%%%%% theta, d, a, alpha, revolute or prismatic, offset
L(1) = Link([ 0     0.2     0          -pi/2    0        0], 'standard');
L(2) = Link([ 0 	0.      0.2        0        0        0], 'standard');
L(3) = Link([ 0     0.      0         pi/2    0         pi/2], 'standard');
L(4) = Link([ 0     0.4     0        -pi/2    0         pi/2], 'standard');
L(5) = Link([ 0     0.0     0         pi/2    0         0   ], 'standard');
L(6) = Link([ 0     0.4     0          0      0         0], 'standard');


%% defining the robot now
robot = SerialLink(L, 'name', 'a');
robotb = SerialLink(L, 'name', 'b');
robotc = SerialLink(L, 'name', 'c');

% some useful poses
qz = [0 0 0 0 0 0]; % zero angles, L shaped pose

clear L

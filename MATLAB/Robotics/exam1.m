% clear

% Declaring robot
robot = SerialLink([0 4 0 pi/2;
                    0 0 0 pi/2;
                    0 2 0 pi/2;
                    0 0 2    0;
                    0 0 2 pi/2]);

robot.links(1).offset = pi/2;
robot.links(2).offset = pi/6;
robot.links(4).offset = pi/2;
robot.links(5).offset = -pi/3;

% Params
q_init = zeros(length(robot.links),1);
goal = [0 2 4]';
obst_location = [0 3 2]';
obst_radius = 1;

% Path planning function (potential fields method)
q_s = compute_robot_path(robot, q_init, goal, obst_location, obst_radius);

% Plotting init configuration and obstacle
robot.plot(q_init')
hold on
p = obst_location;
r = obst_radius;
[x,y,z] = sphere;
h = surf(x*r+p(1), y*r+p(2), z*r+p(3));
set(h, 'FaceAlpha', 0.4);
shading interp;
axis equal;

pause(3)

% Plotting path
for i=1:length(q_s(:,1))
    if mod(i,5) == 0
        robot.plot(q_s(i,:))
    end
end
hold off

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
q_init = zeros(1,length(robot.links));
% q_init = [-0.110912130909545,0.610746293825459,-0.211556778577238,-0.624305390034086,-1.57079632679490];
goal = [0 2 4]';
obst_location = [-1 4 3]';
obst_radius = 1;

% Main compute function
q_s = compute_robot_path(robot, q_init, goal, obst_location, obst_radius);

% Plotting init configuration and obstacle
robot.plot(q_init)
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
    if mod(i,1) == 0
        robot.plot(q_s(i,:))
%         pause(0.3)
    end
end

hold off




function f = compute_robot_path(robot, q_init, goal, obst_location, obst_radius)
    k = 0.12;
    k2 = 0.9;
    kd = 0.2;
    % k = 0.002;
    % k2 = 0.08;

    FK = robot.fkine(q_init).T;
    ksi = FK(1:3, 4);

    counter = 0;
    error = goal - ksi;
    q = q_init;

    q_s = q_init;
    epsilon = 0.3;
    delta_t = 1;
    while norm(error) >= epsilon && counter < 1000
        J = robot.jacob0(q);
        J = J(1:3, :);
        qdot = J'/(J*J' + kd^2 * eye(3)) * k*error;
        % qdot = J' * k*error;

        for i=length(robot.links):-1:1
            J = J(:, 1:i);

            A = double(robot.A(1:i, q));
            p = A(1:3, 4) - obst_location;
            p(1) = p(1) + 0.1;  % bias for x-direction
            p_n = p / norm(p);
            vel = J * qdot(1:i);
            if i == length(robot.links)
                m = 2.2;
                r = obst_radius*1;
            else
                m = 1.3;
                r = obst_radius;
            end
            vel = vel + p_n * norm(vel) * exp(-(norm(p)/m-r));

            error2 = vel*delta_t;
            qdot(1:i) = J'/(J*J' + kd^2 * eye(3)) * error2*k2;
            % qdot(1:i) = J' * error2*k2;
        end

        q = q + qdot' * delta_t;
        if q(5) < -pi/2
            q(5) = -pi/2; end
        if q(5) > 3*pi/4
            q(5) = 3*pi/4; end
        if q(4) > 3*pi/4
            q(4) = 3*pi/4; end
        if q(4) < -pi/2
            q(4) = -pi/2; end
        if q(2) < 0
            q(2) = 0;
        end
%         q(1) = q(1) - 0.005;
        q_s = [q_s; q];

        FK = robot.fkine(q).T;
        ksi = FK(1:3, 4);
        error = goal - ksi;
        counter = counter + 1;
        % k2 = k2 + 0.00009;
        norm(error)
    end
    f = q_s;
end

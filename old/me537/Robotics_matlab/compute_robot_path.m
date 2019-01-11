function f = compute_robot_path(robot, q_init, goal, obst_location, obst_radius)
    % Gains
    k = 0.12; % error gain
    kd = 0.2; % damped pseudo-inverse gain


    % Loop
    FK = robot.fkine(q_init).T;
    ksi = FK(1:3, 4);
    counter = 0;
    error = goal - ksi;
    q = q_init';
    q_s = q_init';
    r = obst_radius;
    epsilon = 0.3;
    delta_t = 1;
    while norm(error) >= epsilon && counter < 1000
        J = robot.jacob0(q);
        J = J(1:3, :);
        qdot = J'/(J*J' + kd^2 * eye(3)) * k*error;

        % For joints 5-2, measure distance to obstacle and push/repel
        % velocity vector of joint outward from center of sphere
        for i=length(robot.links):-1:2
            J = J(:, 1:i); % remove columns from Jacobian

            A = double(robot.A(1:i, q));
            p = A(1:3, 4) - obst_location; % vector from obstacle to joint
            p(1) = p(1) + 0.1; % bias for x-direction
            p_n = p / norm(p);
            vel = J * qdot(1:i); % from joint to cartesian space
            % m is the repulsion factor
            if i == length(robot.links)
                m = 2.2; % end effector gets repelled more than the other joints
            else
                m = 1.3;
            end
            vel = vel + p_n * norm(vel) * exp(-(norm(p)/m-r)); % where the repelling happens

            error2 = vel*delta_t;
            qdot(1:i) = J'/(J*J' + kd^2 * eye(3)) * error2; % calculate new qdot from repelled velocity
        end

        q = q + qdot' * delta_t;

        % Setting some joint limits
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
        q_s = [q_s; q];

        FK = robot.fkine(q).T;
        ksi = FK(1:3, 4);
        error = goal - ksi;
        counter = counter + 1;
        norm(error)
    end
    f = q_s;
end

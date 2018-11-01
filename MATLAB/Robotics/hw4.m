%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%% problem 2g)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

run robot_6dof

%number of tests
num_tests = 10;

%generating random joint angles with joint limits
jt_angles = random('unif', -pi, pi/2, 6, num_tests);

%making emtpy vector to store positions
positions = zeros(3, num_tests);

%calculating FK for each set of random joint angles
for i=1:1:num_tests
    FK = robot.fkine(jt_angles(:,i)).T;
    positions(:, i) = FK(1:3, 4);
%     i
end

qinit1 = zeros(1,6);
qinit2 = ones(1,6) * pi/2;
qf1 = zeros(10,6);
qf2 = zeros(10,6);
ksi_error1 = zeros(10,3);
ksi_error2 = zeros(10,3);
for i=1:10
    ksi_des = positions(:,i);
    qf1(i,:) = IK(qinit1, ksi_des, robot, 1);
    FK = robot.fkine(qf1(i,:)).T;
    ksi_error1(i,:) = ksi_des - FK(1:3, 4);
end


for i=1:10
    ksi_des = positions(:,i);
    qf2(i,:) = IK(qinit1, ksi_des, robot, 2);
    FK = robot.fkine(qf2(i,:)).T;
    ksi_error2(i,:) = ksi_des - FK(1:3, 4);
end

robot.plot(qinit1)
hold on
robotb.plot(qf1(1,:))
robotc.plot(qf2(1,:))
hold off

function f = IK(qinit, ksi_des, robot, j)
    k = 0.4;
    kd = 0.001;

    FK = robot.fkine(qinit).T;
    ksi = FK(1:3, 4);

    counter = 0;
    error = ksi_des - ksi;
    q = qinit';
    epsilon = 0.5;
    delta_t = 1;
    while norm(error) >= epsilon && counter < 1000
        J = robot.jacob0(q);
        J = J(1:3, :);
        if j == 1
            J_dag = J'*inv(J*J' + (kd^2)*eye(3));
            qdot = J_dag * error * k;
        else
            qdot = J' * k*error;
        end

        q = q + qdot * delta_t;

        FK = robot.fkine(q).T;
        ksi = FK(1:3, 4);
        error = ksi_des - ksi;
        counter = counter + 1;
        norm(error)
    end
    f = q';
end

clear

q = [0 pi/4; 0 pi/2; pi/4 pi/4; 0 0; 0 0];
F = [-1  0 0 0 0 0; ...
     -1  0 0 0 0 0; ...
     -1 -1 0 0 0 0; ...
      0  0 1 0 0 0; ...
      1  0 0 0 0 0];

robot = SerialLink([0 0 1 -pi/2; 0 0 1 0], 'name', 'robot');

tau = zeros(5,2);
for i=1:5
    J = double(robot.jacob0(q(i,:)));
    tau(i,:) = J' * F(i,:)';
end

tau

F = F * -1;
for i=1:5
    J = double(robot.jacob0(q(i,:)));
    tau(i,:) = J' * F(i,:)';
end

tau
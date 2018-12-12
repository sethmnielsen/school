q = [0.03763,0.85985,2.98853,2.51176e-07,2.43481,-0.03763]*0.5;
% q = [0,0,0,0,0,0];

pts = 50;
q_arr = zeros(pts*4,6);
x_arr = zeros(pts*4,1);
y_arr = zeros(pts*4,1);
x0 = 0.552;
y0 = -0.1294;
z  = -0.01435;
dt = 0.1;

l = 1.0;
x = linspace(x0,x0+l,pts);
y = linspace(y0,y0+l,pts);

for i=1:pts
    q_arr(i,:) = q;
    Tc = robot.fkine(q);         % from base to current location
    Td = transl(x(i), y(1), z);  % from base to desired location

    Tcd = double(inv(Tc)) * Td;

    v = Tcd(1:3,4);
    R = Tcd(1:3,1:3);

    theta = acos((trace(R)-1)/2);
    u = [R(3,2)-R(2,3);
         R(1,3)-R(3,1);
         R(2,1)-R(1,2)] * 1/(2*sin(theta));

    w = u * theta;

    ksi_dot = [v; w];
    q_dot = inv(robot.jacob0(q)) * ksi_dot;

    q = q + q_dot';

end

for i=1:pts
    q_arr(i+pts,:) = q;
    Tc = robot.fkine(q);           % from base to current location
    Td = transl(x(end), y(i), z);  % from base to desired location

    Tcd = double(inv(Tc)) * Td;

    v = Tcd(1:3,4);
    R = Tcd(1:3,1:3);

    theta = acos((trace(R)-1)/2);
    u = [R(3,2)-R(2,3);
         R(1,3)-R(3,1);
         R(2,1)-R(1,2)] * 1/(2*sin(theta));

    w = u * theta;

    ksi_dot = [v; w];
    q_dot = inv(robot.jacob0(q)) * ksi_dot;

    q = q + q_dot';
end

for i=pts:-1:1
    q_arr(i+pts*2,:) = q;
    Tc = robot.fkine(q);           % from base to current location
    Td = transl(x(i), y(end), z);  % from base to desired location

    Tcd = double(inv(Tc)) * Td;

    v = Tcd(1:3,4);
    R = Tcd(1:3,1:3);

    theta = acos((trace(R)-1)/2);
    u = [R(3,2)-R(2,3);
         R(1,3)-R(3,1);
         R(2,1)-R(1,2)] * 1/(2*sin(theta));

    w = u * theta;

    ksi_dot = [v; w];
    q_dot = inv(robot.jacob0(q)) * ksi_dot;

    q = q + q_dot';
end

for i=pts:-1:1
    i
    q_arr(i+pts*3,:) = q;
    Tc = robot.fkine(q);           % from base to current location
    Td = transl(x(1), y(i), z);  % from base to desired location

    Tcd = double(inv(Tc)) * Td;

    v = Tcd(1:3,4);
    R = Tcd(1:3,1:3);

    theta = acos((trace(R)-1)/2);
    u = [R(3,2)-R(2,3);
         R(1,3)-R(3,1);
         R(2,1)-R(1,2)] * 1/(2*sin(theta));

    w = u * theta;

    ksi_dot = [v; w];
    q_dot = inv(robot.jacob0(q)) * ksi_dot;

    q = q + q_dot';
end

for i=1:length(q_arr)
    T = double(robot.fkine(q_arr(i,:)));
    x_arr(i) = T(1,4);
    y_arr(i) = T(2,4);
end

plot(x_arr, y_arr);

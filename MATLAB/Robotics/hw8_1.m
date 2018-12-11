% q = [0.03763,0.85985,2.98853,2.51176e-07,2.43481,-0.03763];
q = [0,0,0,0,0,0];

pts = 1000;
x0 = 0.552;
y0 = -0.1294;
z  = -0.01435;
dt = 0.1;

l = 1.0;
x = linspace(x0,x0+l,pts);
y = linspace(y0,y0+l,pts);

for j=pts:-1:1
    for i=pts:-1:1
        for j=1:pts

        end
    end
end

for i=1:pts
    Tc = robot.fkine(q);         % from base to current location
    Td = transl(x(i), y(1), z);  % from base to desired location

    Tcd = double(inv(Tc) * Td;)

    v = Tcd(1:3,4)/dt;

    R = Tcd(1:3,1:3);
    u = [R(3,2)-R(2,3);
         R(1,3)-(3,1);
         R(2,1)-R(1,2)];

    th = asin(norm(u)/2);
    w =

    robot.jacob0(q)
end

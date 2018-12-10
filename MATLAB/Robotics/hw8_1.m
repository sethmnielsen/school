q = [0.03763,0.85985,2.98853,2.51176e-07,2.43481,-0.03763];

pts = 1000;
x0 = 0.552;
y0 = -0.1294;
z  = -0.01435;

l = 1;
x = linspace(x0,x0+l,pts);
y = linspace(y0,y0+l,pts);

for j=pts:-1:1
    for i=pts:-1:1
        for j=1:pts
            for i=1:pts

                Td = transl(x(i), y(j), z)
                robot.jacob0(q)

            end
        end
    end
end

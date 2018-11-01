vert = [0 1 1 0 0 1 1 0; ...
        0 0 1 1 0 0 1 1; ...
        0 0 0 0 1 1 1 1];

vert = vert - 0.5;
P = [vert;
    1 1 1 1 1 1 1 1];
fac = [1 2 6 5; 2 3 7 6; 3 4 8 7; 4 1 5 8; 1 2 3 4; 5 6 7 8];
T = trotx(pi/50) * troty(pi/50) * trotz(pi/50);

for i=1:50
    T2 = T;
    for k=1:i
        T2 = T2*T;
    end
    trplot(T2);

    for i=1:8
        P(:,i) = T*P(:,i);
    end


    vert(1,:) = P(1,:);
    vert(2,:) = P(2,:);
    vert(3,:) = P(3,:);

    patch('Vertices',vert','Faces',fac,'FaceVertexCData',hsv(6),'FaceColor', ...
          'flat', 'FaceAlpha',.3)
    set(gca, 'View', [-30, 30]);
    axis equal
    axis([-1 1 -1 1 -1 1])
    pause(0.1)
end

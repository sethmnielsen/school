d1_ = 1; a2_ = 1; d3_ = 1; d4_ = 2; a5_ = d3_; d6_ = 2;

% robot6 = SerialLink([0 d1 0 -pi/2; 0 0 a2 0; pi/2 d3 0 pi/2; pi/2 d4 0 pi/2; 0 0 -a5 -pi/2; 0 d6 0 0], 'name', 'robot6');
robot6 = SerialLink([0 d1_ 0 pi/2; 0 0 a2_ 0; pi/2 d3_ 0 pi/2; pi/2 d4_ 0 pi/2; 0 0 -a5_ -pi/2; 0 d6_ 0 0], 'name', 'robot6');
robot6.links(3).offset = pi/2;
robot6.links(4).offset = pi/2;

% robot6.fkine([th1 th2 th3 th4 th5 th6])
robot6.fkine([0 0 0 0 0 0])
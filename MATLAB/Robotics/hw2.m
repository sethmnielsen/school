clear
d1_ = 1; a2_ = d1_; d3_ = d1_; d4_ = 2*d1_; a5_ = d1_; d6_ = 2*d1_;

robot6 = SerialLink([0 d1_ 0 pi/2; 0 0 a2_ 0; pi/2 d3_ 0 pi/2; pi/2 d4_ 0 pi/2; 0 0 -a5_ -pi/2; 0 d6_ 0 0], 'name', 'robot6');
robot6.links(3).offset = pi/2;
robot6.links(4).offset = pi/2;

q0 = [0 0 0 0 0 0];
fk = robot6.fkine(q0);
r = fk.t(1);

robot6.plot(q0);
hold on
[x,y,z] = sphere;
h = surf(x*r, y*r, z*r + d1_);
set(h, 'FaceAlpha', 0.4);
shading interp;
axis equal;
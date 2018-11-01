% Part a
robot4 = SerialLink([0 1 0 pi/2; 0 0 1 0; 0 0 1 0]);

d1_ = 1; a2_ = d1_; d3_ = d1_; d4_ = 2*d1_; a5_ = d1_; d6_ = 2*d1_;

robot6 = SerialLink([0 d1_ 0 pi/2; 
                     0 0 a2_ 0; 
                     pi/2 0 0 pi/2; 
                     pi/2 d4_ 0 pi/2; 
                     0 0 0 -pi/2; 
                     0 d6_ 0 0], 'name', 'robot6');
robot6.links(3).offset = pi/2;
robot6.links(4).offset = pi/2;

robot6.teach
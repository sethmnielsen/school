clear
clc

syms d1 a2 a3 q1 q2 q3 real
robot3_sym = SerialLink([0 d1 0 pi/2; 0 0 a2 0; 0 0 a3 0], 'name', 'robot3');
J_sym = robot3_sym.jacob0([q1 q2 q3])

d1_ = 0.3; a2_ = d1_; a3_ = d1_;
robot3 = SerialLink([0 d1_ 0 pi/2; 0 0 a2_ 0; 0 0 a3_ 0], 'name', 'robot3');

q0 = [0 0 0];
qa = [pi/2 pi/2 0];
qb = [-pi/4 pi/2 0];
qc = [pi/4 pi/4 -pi/4];
J0 = robot3.jacob0(q0)
Ja = robot3.jacob0(qa)
Jb = robot3.jacob0(qb)
Jc = robot3.jacob0(qc)
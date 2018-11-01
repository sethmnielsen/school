clear
clc

syms a1 ac q1 q2 real
T01 = transl(a1*cos(q1),a1*sin(q1),0) * trotz(q1);
T1C = transl(ac*cos(q2),ac*sin(q2),0) * trotz(q2);
T0C = simplify(T01 * T1C)

robot2 = SerialLink([0 0 a1 0; 0 0 ac 0], 'name', 'robot2');
J = simplify(robot2.jacob0([q1 q2]))
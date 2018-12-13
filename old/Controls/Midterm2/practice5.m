syms w

A = [0 1 0 0; 3*w^2 0 0 2*w; 0 0 0 1; 0 -2*w 0 1];
B1 = [0 0 0 1]';
B2 = [0 1 0 0]';

Cab1 = [B1 A*B1 A*A*B1 A*A*A*B1];
Cab2 = [B2 A*B2 A*A*B2 A*A*A*B2];

r1 = rank(Cab1);
r2 = rank(Cab2);

d1 = det(Cab1);
d2 = det(Cab2);
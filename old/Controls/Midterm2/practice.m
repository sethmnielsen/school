A = [1 0 1; 2 -1 0; 0 1 0];
B = [0 1 0]';
syms s

det(s*eye(3) - A)
a = [0 -1 -2];

A_A = [1 a(1) a(2); 0 1 a(1); 0 0 1]
Cab = [B A*B A^2 * B]

alpha = poly([-2 -3+3i -3-3i]);
alpha = alpha(2:4);

K = (alpha - a)/A_A/Cab
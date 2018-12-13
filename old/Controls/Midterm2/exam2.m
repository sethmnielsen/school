% syms s
% syms K
% % K = 20;
% A = [0, 1, 0; 0, -2, 1; 0, 0, -1];
% B = [0 0 K]';
% C = [1 0 0];
% 
% Cab = [B A*B A*A*B]
% % Cab = ctrb(A,B);
% 
% rank(Cab);
% 
% Oab = [C; C*A; C*A*A];
% 
% rank(Oab);
% 
% % det(s*eye(3) - A)
% a = [3 2 0];
% A_A = [1 a(1) a(2); 0 1 a(1); 0 0 1];
% 
% P = Cab * A_A;
% 
% inv(P) * A * P


J = 0.096852;
b = 0.105231;
k = 822;
R = 120000;
L = 0.0825;

A = [0 0 1; 0 -R/L -k/L; 0 k/J -b/J];
B = [0 1/L 0]';
syms s

det(s*eye(3) - A)
a = [3601527993742321955/2476048646144 1876167501468604086812261806655789/21779554218994803725565952 0];

A_A = [1 a(1) a(2); 0 1 a(1); 0 0 1];
% Cab = [B A*B A^2 * B]
Cab = ctrb(A, B);

z = 0.707;
wn = 2.2/0.015;
poles1 = roots([1, 2*z*wn, wn^2]);
poles = [poles1(1), poles1(2), -207.39];
alpha = poly(poles);
alpha = alpha(2:4);

K = (alpha - a)/A_A/Cab
clear

%% Problem 1
% %% Part a
% syms a11 a12 a13 a21 a22 a23 a31 a32 a33
% syms b11 b12 b13 b21 b22 b23 b31 b32 b33
% syms c11 c12 c13 c21 c22 c23 c31 c32 c33
% 
% % A = [a11 a12 a13; a21 a22 a23; a31 a32 a33];
% % B = [b11 b12 b13; b21 b22 b23; b31 b32 b33];
% % C = [c11 c12 c13; c21 c22 c23; c31 c32 c33];
% 
% % C = trace(B' * A)
% % D = conj(trace(A' * B))
% 
% 
% %% Part b
% 
% syms c1 c2 c3
% 
M1 = [1 1i 0;
      0 1 1i;
      0 1i 0];

M2 = [1+1i 1+1i 1+1i;
        2   2   2;
        0   0   0];

M3 = [1-1i    4  5;
      1-2*1i  6  7;
      1-3*1i  8  9];
% 
% B = c1*M1 + c2*M2 + c3*M3;
% 
% A = [B 0];
% 
% rref(A)

%% Part c

q1 = M1 / norm(M1, 'fro');

e2 = M2 - trace(q1' * M2) * q1;
q2 = e2 / norm(e2, 'fro');

e3 = M3 - trace(q1' * M3) * q1 - trace(q2' * M3) * q2;
q3 = e3 / norm(e3, 'fro');

N1 = q1
N2 = q2
N3 = q3

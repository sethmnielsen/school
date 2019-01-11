clear

A = [1 2 0; 0 3 1];
B = [1 0; 0 1];

r = rref(A);
N = null(A, 'r');

P = N/(N'*N)*N'
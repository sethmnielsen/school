%% 2-6
A = [1 2 3; 4 5 6; 7 8 9]*0.1;

m = eye(3);
for i=1:37
   m = m + (A^i)/factorial(i);
end

expm(A)
m
%% 2-9

v = [2 3 4];
th = 0.5;

S = v / norm(v);
s = [0    -S(3) S(2); 
     S(3)    0 -S(1); 
    -S(2)  S(1)   0];

R  = expm( s * th)                         % matrix exponential
R2 = trexp(S, th)                          % trexp function
R3 = eye(3) + sin(th)*s + (1-cos(th))*s^2  % Rodrigues' formula
T  = angvec2tr(th, S)                      % angvec2tr
q  = [cos(th/2), S*sin(th/2)]              % unit quaternion [s, v1, v2, v3]

%% 2-11

R_AB = rotx(0.5) * roty(0.2) * rotz(0.6)
R_BA = R_AB'

[th1, v1] = tr2angvec(R_AB)
[th2, v2] = tr2angvec(R_BA)

tw1 = Twist('R', v1, [0 0 0])
tw2 = Twist('R', v2, [0 0 0])




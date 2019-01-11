syms m a b c real
r = [a/2 b/2 c/2];

Ixx = (m/12) * (b^2 + c^2);
Iyy = (m/12) * (a^2 + c^2);
Izz = (m/12) * (a^2 + b^2);

Icom = [Ixx 0 0; 0 Iyy 0; 0 0 Izz];

I0 = Icom - m*skew(r)^2;

simplify(I0)

%% 1(c)(i)

l = 1;
w = 0.25;
m = 1;

I1 = [(m/12) * (l^2 + w^2) 0 0; ...
      0 (m/12) * (l^2 + w^2) 0; ...
      0 0 (m/12) * (2*w^2)];

I2 = [(m/12) * (l^2 + w^2) 0 0; ...
      0 (m/12) * (l^2 + w^2) 0; ...
      0 0 (m/12) * (2*w^2)];

I3 = [(m/12) * (l^2 + w^2) 0 0; ...
      0 (m/12) * (l^2 + w^2) 0; ...
      0 0 (m/12) * (2*w^2)];

% (ii)
Jv1 = [0 0 0;
       0 0 0;
       1 0 0];
Jv2 = [0 0 0;
       0 1 0;
       1 0 0];
Jv3 = [0 0 1;
       0 1 0;
       1 0 0];

M = m*(Jv1'*Jv1 + Jv2'*Jv2 + Jv3'*Jv3);

% (iv)

syms q1 q2 q3 real

rc1 = [0; 0; l/2+q1];
rc2 = [0; l/2+q2; l+q1];
rc3 = [l/2+q3; l+q2; l+q1];
g = [0 0 9.81];

P = m*g*(rc1 + rc2 + rc3);
g1 = 3*9.81;

M + [g1; 0; 0];

%% d.
syms m1 m2 m3 Ixx Iyy Izz q1 q2 q3 qd1 qd2 qd3 qdd1 qdd2 qdd3 g real

m = [m1; m2; m3];
q = [q1; q2; q3];
qd = [qd1; qd2; qd3];
qdd = [qdd1; qdd2; qdd3];
gv = [0;  g;  0];
l = 0.4;
c = 0.2;
q0 = [0 0 0];

robot3 = SerialLink([0 0 l 0; 0 0 l 0; 0 0 l 0],'gravity',[0 -9.81 0]);
for i=1:3
    robot3.links(i).I = [Ixx Iyy Izz];
end

z_00 = [0; 0; 1];
z_01 = [0; 0; 1];
z_02 = [0; 0; 1];

O_00 = [0; 0; 0];
O_01 = l*[cos(q1); sin(q1); 0];
O_02 = l*[cos(q1)+cos(q1+q2); sin(q1)+sin(q1+q2); 0];

O_0c1 = c*[cos(q1); sin(q1); 0];
O_0c2 = [l*cos(q1)+c*cos(q1+q2); l*sin(q1)+c*sin(q1+q2); 0];
O_0c3 = [l*(cos(q1)+cos(q1+q2))+c*cos(q1+q2+q3); l*(sin(q1)+sin(q1+q2))+c*sin(q1+q2+q3); 0];

Jv = sym(zeros(3,3,3));
Jw = sym(zeros(3,3,3));
R = sym(zeros(3,3,3));

Jv(:,:,1) = [cross(z_00, O_0c1 - O_00) [0; 0; 0] [0; 0; 0]];
Jw(:,:,1) = [z_00                      [0; 0; 0] [0; 0; 0]];

Jv(:,:,2) = [cross(z_00, O_0c2 - O_00) cross(z_01, O_0c2 - O_01) [0; 0; 0]];
Jw(:,:,2) = [z_00                      z_01                      [0; 0; 0]];

Jv(:,:,3) = [cross(z_00, O_0c3 - O_00) cross(z_01, O_0c3 - O_01) cross(z_02, O_0c3 - O_02)];
Jw(:,:,3) = [z_00                      z_01                      z_02];

R(:,:,1) = rotz(q1);
R(:,:,2) = rotz(q1)*rotz(q2);
R(:,:,3) = rotz(q1)*rotz(q2)*rotz(q3);

% Mass matrix
M = sym(zeros(3,3));
for i=1:3
    M = M + m(i)*Jv(:,:,i)'*Jv(:,:,i) + ...
        Jw(:,:,i)'*Jw(:,:,i)*R(:,:,i)*robot3.links(i).I*R(:,:,i)'*Jw(:,:,i);
end

% Coriolis matrix
C = sym(zeros(3,3));
for k=1:3
    for j=1:3
        for i=1:3
            C(k,j) = C(k,j) + 0.5*(diff(M(k,j),q(i)) + diff(M(k,i),q(j)) - diff(M(i,j),q(k)))*qd(i);
        end
    end
end

% Gravity vector
P = m(1)*gv'*O_0c1;
P = P + m(2)*gv'*O_0c2;
P = P + m(3)*gv'*O_0c3;

G = [diff(P,q1); diff(P,q2); diff(P,q3)];

tau = simplify(M*qdd + C*qd + G)

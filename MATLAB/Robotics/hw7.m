clear

q = [pi/4 pi/4 pi/4];
qd = [pi/6 -pi/4 pi/3];
qdd = [-pi/6 pi/3 pi/6];

n = 3;
l = 0.4;
c = 0.2;
m = 1.0;
g = [0; -9.81; 0];
Izz = 0.01;
Ic = [0 0 0; 0 0 0; 0 0 Izz];

rob = SerialLink([0 0 l 0; 0 0 l 0; 0 0 l 0],'gravity',-g');
for i=1:3
    rob.links(i).I = [0 0 Izz];
    rob.links(i).m = m;
    rob.links(i).r = [-c; 0; 0];
    rob.links(i).Jm = 0;
end

tau = calc_tau(q, qd, qdd, rob)
tau_rne = rob.rne(q,qd,qdd)

%% part c-d

% q = q*0;
qd = qd*0;
qdd = qdd*0;

G = calc_tau(q, qd, qdd, rob);
% G = G(3,:)'

qdd1 = [1 0 0];
qdd2 = [0 1 0];
qdd3 = [0 0 1];
M(:,1) = calc_tau(q, qd, qdd1, rob) - G;
M(:,2) = calc_tau(q, qd, qdd2, rob) - G;
M(:,3) = calc_tau(q, qd, qdd3, rob) - G;

M
M_inertia = rob.inertia(q)

qd = [pi/6 -pi/4 pi/3];
qdd = [-pi/6 pi/3 pi/6];

Cqd = calc_tau(q, qd, qdd, rob) - G - M*qdd'
Cqd_coriolis = rob.coriolis(q, qd) * qd'

function Torques = calc_tau(q, qd, qdd, rob)
    n = 3;
    l = 0.4;
    c = 0.2;
    m = 1.0;
    g = [0; -9.81; 0];
    Izz = 0.01;
    Ic = [0 0 0; 0 0 0; 0 0 Izz];

    % Forward Kinematic Pass

    w_p = zeros(3,1);
    alph_p = zeros(3,1);
    ac_p = zeros(3,1);
    ae_p = zeros(3,1);

    z = [0; 0; 1];
    r_pc = [c; 0; 0];
    r_p = [l; 0; 0];

    wi = zeros(3);
    alphi = zeros(3);
    aci = zeros(3);
    aei = zeros(3);
    for i=1:n
        R_p = rotz(q(i))';
        T_0 = double(rob.A([1:i], q(1:i)));
        R_0 = T_0(1:3,1:3)';

        w = R_p * w_p  +  R_0 * z * qd(i);
        alph = R_p * alph_p  +  R_0 * z * qdd(i) + cross(w, R_0 * z * qd(i));

        ac = R_p * ae_p  +  cross(alph, r_pc)  +  cross(w, cross(w, r_pc));
        ae = R_p * ae_p  +  cross(alph, r_p )  +  cross(w, cross(w, r_p ));

        w_p = w;
        alph_p = alph;
        ac_p = ac;
        ae_p = ae;

        wi(:,i) = w;
        alphi(:,i) = alph;
        aci(:,i) = ac;
        aei(:,i) = ae;
    end

    % Backward Force/Torque Pass

    tau_n = zeros(3,1);
    f_n = zeros(3,1);

    r_pc = [c; 0; 0];
    r_c = [-c; 0; 0];

    taui = zeros(3);
    fi = zeros(3);
    for i=n:-1:1
        T_0 = double(rob.A([1:i], q(1:i)));
        R_0 = T_0(1:3,1:3)';
        R_n = rotz(q(i));

        f = R_n * f_n  -  m * R_0 * g  + m * aci(:,i);
        tau = R_n * tau_n  -  cross(f, r_pc)  +  cross(R_n * f_n, r_c)  +  ...
              Ic * alphi(:,i)  +  cross(wi(:,i), Ic * wi(:,i));

        tau_n = tau;
        f_n = f;

        taui(:,i) = tau;
        fi(:,i) = f;
    end

    Torques = taui(3,:)';
end

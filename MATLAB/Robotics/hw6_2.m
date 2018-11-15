[left, right] = mdl_baxter('sim');

%defining an initial joint configuration
q0 = zeros(7,1);

%defining an initial joint velocity
qd0 = zeros(7,1);

%defining a test joint torque
tau = 10*ones(7,1);

%calculating the mass, coriolis and gravity terms
M = left.inertia(q0');
C = left.coriolis(q0', qd0');
G = left.gravload(q0');

%calculating the joint accleration given initital conditions and a torque
q_dd = left.accel(q0', qd0', tau');

dt = t(2)-t(1);
qx = [q0'; q];
qy = [q; q0'];
qd = zeros(length(q)+1,7);
qdd = zeros(length(q)+1,7);
for i=1:7
    qd(:,i) = (qy(:,i) - qx(:,i))/dt;
end

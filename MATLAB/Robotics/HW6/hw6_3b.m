mdl_puma560;
p560 = p560.nofriction;
robot = p560;
load puma560_torque_profile.mat

dt = 0.01;
t = time(1:end-1);
qdd_o = zeros(length(torque)-1,6);
qd_o = zeros(length(torque)-1,6);
q_o = zeros(length(torque)-1,6);
for i=2:length(torque)-1
    qdd_o(i,:) = p560.accel(q_o(i-1,:), qd_o(i-1,:), torque(i-1,:));
    qd_o(i,:) = qd_o(i-1,:) + qdd_o(i,:)*dt;
    q_o(i,:) = q_o(i-1,:) + qd_o(i,:)*dt;
end

figure(1)
plot(t,q_o)
xlabel('t')
ylabel('q')
title('q from integration')
figure(2)
plot(t,qd_o)
xlabel('t')
ylabel('qd')
title('qdot from integration')
figure(3)
plot(t,qdd_o)
xlabel('t')
ylabel('qdd')
title('qddot from integration')

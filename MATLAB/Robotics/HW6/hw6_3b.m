mdl_puma560;
p560 = p560.nofriction;
robot = p560;
load puma560_torque_profile.mat

dt = 0.01;
qdd_o = zeros(length(torque)-1,6);
for i=2:length(torque)-1
    qdd_o(i,:) = qdd_o(i-1,:) + (torque(i-1,:) + torque(i,:))/2 * dt;
end

qd_o = zeros(length(torque)-1,6);
for i=2:length(torque)-1
    qd_o(i,:) = qd_o(i-1,:) + (qdd(i-1,:) + qdd(i,:))/2 * dt;
end

q_o = zeros(length(torque)-1,6);
for i=2:length(torque)-1
    q_o(i,:) = q_o(i-1,:) + (qd(i-1,:) + qd(i,:))/2 * dt;
end

subplot(2,2,1)
plot(t,q_o)
xlabel('t')
ylabel('q')
title('q from integration')
subplot(2,2,2)
plot(t,qd_o)
xlabel('t')
ylabel('qd')
title('qdot from integration')
subplot(2,2,3)
plot(t,qdd_o)
xlabel('t')
ylabel('qdd')
title('qddot from integration')

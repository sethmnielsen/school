[left, right] = mdl_baxter('sim');

q0 = zeros(7,1);

dt = t(2);
qx = [q0'; q];
qy = [q; q0'];
qd = zeros(length(q)+1,7);
qdd = zeros(length(q)+1,7);

for i=1:7
    qd(:,i) = (qy(:,i) - qx(:,i))/dt;
end
qd = qd(1:end-1,:);
qdx = [q0'; qd];
qdy = [qd; q0'];

for i=1:7
    qdd(:,i) = (qdy(:,i) - qdx(:,i))/dt;
end
qdd = qdd(1:end-1,:);


%calculating the mass, coriolis and gravity terms
tau = zeros(length(q), 7);
for i=1:length(q)
    M = left.inertia(q(i,:));
    C = left.coriolis(q(i,:), qd(i,:));
    G = left.gravload(q(i,:));

    tau(i,:) = M * qdd(i,:)' + C * qd(i,:)' + G';
end

plot(t,tau(:,2))
xlabel('t');
ylabel('\tau');

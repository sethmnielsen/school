clear
clc

mdl_puma560;
r = rand([100 6]) * 2*pi - pi;


% % Part a
A = zeros(4,4,100);
B = zeros(4,4,100);
for i=1:100
    A(:,:,i) = double(p560.fkine(r(i,:)));
end

p560.links(4).d = p560.links(4).d + 0.0005;

for i=1:100
    B(:,:,i) = double(p560.fkine(r(i,:)));
end

E = A - B;
E_avg_a = mean(E,3)
E_max_a = max(abs(E),[],3)


% % Part b
for i=1:100
    r_e = r(i,:) + [0, 0.1 * pi/180, 0, 0, 0, 0]; 
    B(:,:,i) = double(p560.fkine(r_e));
end

E = A - B;
E_avg_b = mean(E,3)
E_max_b = max(abs(E),[],3)

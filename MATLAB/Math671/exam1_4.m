% P = zeros(1001,4);
% 
% for i=1:1001
%     P(i,:) = [sin(10*t(i)) t(i)^2 t(i) 1];
% end
% 
% c = (P'*P)\ P' * x'

u_num = zeros(12,1);
u_num(1) = u(1);
for i=2:12
    u_num(i) = u_num(i-1) + u(i); 
end
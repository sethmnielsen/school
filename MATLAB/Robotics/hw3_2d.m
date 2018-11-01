clear

mdl_stanford;

q = [-pi/2 pi/2 0 pi/2 0 0];

J = zeros(6,6);
Ae = double(stanf.A(1:6, q));
Oe = Ae(1:3, 4);
for i=1:6
    Ai = double(stanf.A(1:i-1, q));
   zi = Ai(1:3, 3);
   Oi = Ai(1:3, 4);
   O = Oe - Oi;
   
   if i==3
      J(:,i) = [ zi; cross(zi, O) ];
   else
      J(:,i) = [ cross(zi, O); zi ]; 
   end
end

J

stanf.jacob0(q)
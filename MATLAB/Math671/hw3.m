clc;
clear;

% ================== Part a ==================

dt = 0.0002;
tspan = -1 : dt : 1;
tspan(1) = tspan(2);
tspan(end) = tspan(end-1);
tspan = tspan';

numTpts = size( tspan, 1 );

p_vec = zeros( numTpts, 5 );
e_mat = p_vec;

for kk = 1 : 5
    p_vec(:,kk) = tspan .^ ( kk - 1 );
end

q1_pre_sq_int = trap_integral(p_vec(:,1) .^ 2);
e1 = p_vec(:,1) / sqrt( q1_pre_sq_int );
e_mat(:,1) = e1;

for kk = 2 : 5
    e_i = grammy(p_vec(:,kk), e_mat(:,1:kk-1));
    e_mat(:,kk) = e_i;
end

f1 = figure(1);
clf( f1 );
ax1 = axes;
pl1 = plot(tspan, e_mat);
leg = legend('e1','e2','e3','e4','e5');
title('Legendre Polynomials')


% ================== Part b ==================
A = e_mat(:,1:2);
f = exp(-tspan);
x = (A' * A) \ A' * f;
f_est = A * x;

error_v = f - f_est;
error_norm = sqrt( trap_integral( error_v .^ 2) );

figure(2)
plot(tspan, [f f_est])
legend('f','f_est');
title('Legendre Approximation')

% ================== Part c ==================

c = 1 ./ (sqrt(1-tspan.^2));
q1_pre_sq_int = trap_integral(c .* p_vec(:,1) .^ 2);
e1 = p_vec(:,1) / sqrt( q1_pre_sq_int );
e_mat_cheb(:,1) = e1;

for kk = 2 : 5
    e_i = chebby(p_vec(:,kk), e_mat_cheb(:,1:kk-1), c);
    e_mat_cheb(:,kk) = e_i;
end

figure(3);
plot(tspan, e_mat_cheb);
legend('e1','e2','e3','e4','e5');
title('Chebyshev Polynomials')

% ================== Part d ==================
A = e_mat_cheb(:,1:2);
x = (A' * A) \ A' * f;
f_est = A * x;

error_v_cheb = f - f_est;
error_norm_cheb = sqrt( trap_integral( error_v_cheb .^ 2) );

figure(4)
plot(tspan, [f f_est])
legend('f','f_est');
title('Chebyshev Approximation')

% ================== Part e ==================
%
% Both norms of the error vectors (error_norm and error_norm_cheb)
% have the same value. This makes sense because the Chebyshev 
% polynomials are linear combinations of the Legendre polynomials,
% so their span is the same.


% ================ Functions ==================

function p_vec_e = grammy( p_vec, e_mat )
    in_prod = trap_integral( p_vec .* e_mat );
    proj_ei = in_prod .* e_mat;
    p_vec_q = p_vec - sum( proj_ei, 2);
    p_vec_q_norm = sqrt( trap_integral( p_vec_q .^ 2 ) );
    p_vec_e = p_vec_q / p_vec_q_norm;
end

function p_vec_e = chebby( p_vec, e_mat, c )
    in_prod = trap_integral( c .* p_vec .* e_mat );
    proj_ei = in_prod .* e_mat;
    p_vec_q = p_vec - sum( proj_ei, 2);
    p_vec_q_norm = sqrt( trap_integral( c .* p_vec_q .^ 2 ) );
    p_vec_e = p_vec_q / p_vec_q_norm;
end

function integ = trap_integral( vec )
    dt = 0.0002;
    integ = sum( vec(1:end-1,:) + vec( 2 : end, : ),1 ) * 0.5 * dt;
end

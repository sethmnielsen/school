clc;
clear;

dt = 0.0001;
tspan = -1 : dt : 1;
tspan = tspan';

numTpts = size( tspan, 1 );

p_vec = zeros( numTpts, 5 );
e_mat = p_vec;

for kk = 1 : 5
    p_vec(:,kk) = tspan .^ ( kk - 1 );
end

% ========================

q1_pre_sq = p_vec(:,1) .^ 2;
q1_pre_sq_int = sum( q1_pre_sq(1 : end - 1,1) + q1_pre_sq(2:end,1) ) * 0.5 * dt;
e1 = p_vec(:,1) / sqrt( q1_pre_sq_int );
e_mat(:,1) = e1;

% ========================
for kk = 2 : 5
    e_i = grammy(p_vec(:,kk), e_mat(:,1:kk-1));
    e_mat(:,kk) = e_i;
end
% ========================

f1 = figure(1);
clf( f1 );
ax1 = axes;
pl1 = plot(tspan, e_mat);
leg = legend('e1','e2','e3','e4','e5');

function p_vec_e = grammy( p_vec, e_mat )
    in_prod = trap_integral( p_vec .* e_mat );
    proj_ei = in_prod .* e_mat;
    p_vec_q = p_vec - sum( proj_ei, 2);
    p_vec_q_norm = sqrt( trap_integral( p_vec_q .^ 2 ) );
    p_vec_e = p_vec_q / p_vec_q_norm;
end

function integ = trap_integral( vec )
    dt = 0.0001;
    integ = sum( vec(1:end-1,:) + vec( 2 : end, : ),1 ) * 0.5 * dt;
end

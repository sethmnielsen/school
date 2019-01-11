clear all

%define the robotics toolbox Puma 560 arm
mdl_puma560;

%set the Coulomb friction terms to zero to help with numerical simulation
p560 = p560.nofriction;

robot = p560;

q0 = qz;
fps = 100;
holdplot = true;

%load the torque profile and open the simulink model
load puma560_torque_profile.mat
open sl_puma_hw6_2017

% [q, qd] = ode45(@(q,qd) myfun(q,qd,torque,robot),[time(1),time(end)], qz);
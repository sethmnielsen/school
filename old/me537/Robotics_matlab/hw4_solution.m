% Homework 4, problem 3 - ME 537
% inverse kinematics

% Some of the code below is repeated for the two different methods shown
% (things like calculating pose error).
% This is not good coding practice and instead, repeated code should be
% changed to functions that can be called from anywhere. 

%clearing workspace of variables
clear all;
close all;
clc;

%using custom defined robot from homework 2
robot_6dof;

%generating random numbers to assign to joint angles
random_joints = rand(6,10);

%forcing the random uniformly distributed numbers to be between desired
%bounds
for i=1:1:6
    %this generates 10 random joint angles that are within the joint limits
    %random_joints(i,:)= random_joints(i,:)*...
        %(robot.qlim(i,2)-robot.qlim(i,1))+robot.qlim(i,1);
        
    %in our case there are not joint limits given, so just generate them 
    %plus and minus pi. The reason for the form of this equation is that it
    %will always work for number*(max-min)+min
    random_joints(i,:) = random_joints(i,:)*(pi-(-pi))+(-pi); 
end

% required joint angles to start from
qi1 = zeros(6,1);
qi2 = pi/2*ones(6,1);

% gain for damped pseudo-inverse
K_inv = 0.3*eye(6)

%for j_transpose
K_trans = 0.5*eye(3)

%place to store solution joint angles for two different methods
q_slns_pinv = [];
status_pinv = [];
q_slns_trans = [];
status_trans = [];
num_trials = 10;

%start with pseudo-inverse method
qi = qi1 % if want to run from all joint angles being pi/2, just update this.
for i=1:1:num_trials
    
    %calculating the desired pose and the current pose
    T_des = robot.fkine(random_joints(:,i)).T;
    T_cur = robot.fkine(qi).T;
    
    %initializing q
    q = qi;

    counter = 0;
    % every time through loop, we check position error and if we have run
    % for 1000 iterations yet or not. 
    while (norm(T_des(1:3,4)- T_cur(1:3,4)) > 0.0001) & (counter < 1000)
        % update pose and jacobian for current q's
        T_cur = robot.fkine(q).T;
        J = robot.jacob0(q);

        %calculate error in pose and transform back to base frame.
        delta = tr2delta(T_cur, T_des);
        R2base = T_cur(1:3,1:3);
        delta_base = [R2base, zeros(3,3); zeros(3,3), R2base]*delta;

        %perform the pseudo-inverse method
        q = q + J'*inv(J*J'+0.1^2*eye(6))*K_inv*delta_base;
        
        counter = counter + 1
    end

    if counter >= 1000
        status_pinv = [status_pinv, 0]
    else
        status_pinv = [status_pinv, 1]
    end
    
    %storing results for reference
    q_slns_pinv = [q_slns_pinv, q];

    %reinitializing for the jacobian transpose method
    T_cur = robot.fkine(qi).T;
    q = qi;

    counter = 0;
    % every time through loop, we check position error and if we have run
    % for 1000 iterations yet or not. 
    while (norm(T_des(1:3,4)- T_cur(1:3,4)) > 0.0001) & (counter < 1000)
        % update pose and jacobian for current q's
        T_cur = robot.fkine(q).T;
        J = robot.jacob0(q);

        %calculate error in pose and transform back to base frame.
        delta = tr2delta(T_cur, T_des);
        R2base = T_cur(1:3,1:3);
        delta_base = [R2base, zeros(3,3); zeros(3,3), R2base]*delta;

        %perform the pseudo-inverse method
        q = q + J(1:3,:)'*K_trans*delta_base(1:3);
        
        counter = counter + 1
    end

    if counter >= 1000
        status_trans = [status_trans, 0]
    else
        status_trans = [status_trans, 1]
    end
    
    
    
    q_slns_trans = [q_slns_trans, q];
end


%when completed we can generate smooth joint trajectories between the start
% and end configurations for control
num_steps = 50

%this is a series of joint angle values defined by a number of steps it
%should take to reach the goal.
q_traj = mtraj(@lspb, qi', q_slns_pinv(:,1)', num_steps);
robot.plot(q_traj);

%we can do the same thing, but parameterized by time as well. 
time = 0:0.01:1;
q_traj_time = mtraj(@lspb, qi', q_slns_pinv(:,1)', time);
figure()
plot(time, q_traj_time);
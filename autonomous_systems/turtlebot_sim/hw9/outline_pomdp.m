T       % time horizon
gamma   % discount factor

Y = [0 0 0];

% dimension space of problem
N       % number of states
Nu      % number of control inputs
Nz      % number of measurements


r       % reward r(x_i, u_iu)
pt      % transition probabilities pt(x_i' | x_j, u_iu)
pz      % measurement probabilites px(z_iz | x_j)

for tau = 1:T
    Ypr = [];
    K   % number of linear constraint functions  
    for k = 1:K
        for iu = 1:Nu           % Nu = number of possible control options
            for iz = 1:Nz       % Nz = number of possible measurements 
                for j = 1:N     % N = dimension of state space = 2 
                   % Calculate v(k,iu,iz,j)
                end
            end
        end
    end    

    for iu = 1:Nu
        for k1 = 1:K        % For our problem, there are Nz = 2 nested loops from 1:K
            for k2 = 1:K
               for i = 1:N
                  % vpr(i) = ?   % Calculate end points of new set of linear functions
                                 % vpr(1) and vpr(2)
               end
               Ypr = ?           % Augment Ypr
            end
        end
    end
    
    Y = Ypr;

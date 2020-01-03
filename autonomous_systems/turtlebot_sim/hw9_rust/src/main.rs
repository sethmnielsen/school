/* 
1) Implement algorithm 15.1 with the objective of representing the value function for the illustrative example of section 15.2

2) Compute the value function for the example for a time horizon of 2 and show that you obtain the linear value function constraints of equation 15.31 (along with a few others that have not been pruned away).

3) Develop a simple pruning strategy to prune away some of the obviously superfluous constraints (replicates of initial payoff constraints, constraints dominated by (lying below) the payoff constraint for u3).

4) Modify the state transition probability for u3 as well as the measurement probabilities for states x1 and x2. Compute value functions for different probabilities. Do your results make sense? Change the payoffs associated with the control actions and compute the value function. Do the results make sense?

5) Using the probability and payoff parameters of your choice, use the associated value function to choose control actions. Assume that your true initial state is x1 and that your belief is 0.6. What outcomes do you obtain for 10 trials? Do you outcomes align with your expectations? Did your value function produce good results?
*/

mod lib;


fn main() {
    let pz: Array2<f64> = array![[0.7, 0.3], [0.3, 0.7]]; // measurement probabilities
    let pt: Array2<f64> = array![[0.2, 0.8], [0.8, 0.2]]; // transition probabilities
    let rew: Array2<i32> = array![[-100, 100, -1], [ 100, -50, -1]];
    let y0: Array2<f64> = array![[-100., 100.], [100., -50.]];
    
    let prune_rng = Array::range(0., PRUNE_RES+1., PRUNE_RES).insert_axis(Axis(0));
    // println!("prune_rng shape: {:#?}", &prune_rng.shape());
    let probs = stack![ Axis(0), prune_rng, prune_rng.slice(s![.., ..;-1]) ];
    let k = 1;
    let mut Y: Array2<f64> = Array2::<f64>::zeros((1, 2));

    for i in 0..T {
        println!("\n%%%%%%%%%%%%%%%%%%%% BEGIN LOOP {} %%%%%%%%%%%%%%%%%%%%%%", i);
        Y = sense(&Y, &pz);
        Y = prune(&Y, &probs);
        Y = predict(&Y, &pt, &y0);
        Y = prune(&Y, &probs);
        println!("\nY at {}: \n{}", i, Y);
    }

    println!("Final: \n{:.2}", Y);
}

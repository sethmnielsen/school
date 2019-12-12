/* 
1) Implement algorithm 15.1 with the objective of representing the value function for the illustrative example of section 15.2

2) Compute the value function for the example for a time horizon of 2 and show that you obtain the linear value function constraints of equation 15.31 (along with a few others that have not been pruned away).

3) Develop a simple pruning strategy to prune away some of the obviously superfluous constraints (replicates of initial payoff constraints, constraints dominated by (lying below) the payoff constraint for u3).

4) Modify the state transition probability for u3 as well as the measurement probabilities for states x1 and x2. Compute value functions for different probabilities. Do your results make sense? Change the payoffs associated with the control actions and compute the value function. Do the results make sense?

5) Using the probability and payoff parameters of your choice, use the associated value function to choose control actions. Assume that your true initial state is x1 and that your belief is 0.6. What outcomes do you obtain for 10 trials? Do you outcomes align with your expectations? Did your value function produce good results?
*/

#![allow(non_snake_case)]
extern crate ndarray;

use ndarray::prelude::*;

fn main() {
    // let T = 1;
    let gamma = 1.0;
    let N = 2;

    let reward = array![[-100, 100, -1], [ 100, -50, -1]];
    let pt = array![[0.2, 0.8], [0.8, 0.2]]; // transition probabilities
    let pz: Array2<f64> = array![[0.7, 0.3], [0.3, 0.7]]; // measurement probabilities

    let k = 1;
    let mut Y: Array2<f64> = Array2::<f64>::zeros((k, N));
    let y0: Array2<i32> = arr2(&[[-100, 100], [100, -50]]);
    let prune_res = 0.0001;

    // Y[[2, 1]] = 75;

    sense(&mut Y, pz);

    println!("Final: {:2}", Y);
}

fn sense<A>(Y: &mut Array2<f64>, pz: Array2<A>) {
    // let Ypr1 = pz.slice(s![.., 0]) * Y;
    // let Ypr2 = pz.slice(s![.., 1]) * Y;
    let Ypr1 = pz.column(0) * Y;
    let Ypr2 = pz.column(1) * Y;

    let rng = Array::range(0., Y.nrows() as f64, 1.);
    
}

fn predict(Y: &mut Array2<f64>) {

}

fn prune(Y: &mut Array2<f64>) {

}
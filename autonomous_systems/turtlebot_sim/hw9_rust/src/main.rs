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

// Params
const T: i32 = 2;
const GAMMA: f64 = 1.0;
const PRUNE_RES: f64 = 0.0001;

fn main() {
    let pz: Array2<f64> = array![[0.7, 0.3], [0.3, 0.7]]; // measurement probabilities
    let pt: Array2<f64> = array![[0.2, 0.8], [0.8, 0.2]]; // transition probabilities
    let rew: Array2<i32> = array![[-100, 100, -1], [ 100, -50, -1]];
    let y0: Array2<i32> = array![[-100, 100], [100, -50]];

    let k = 1;
    let mut Y: Array2<f64> = Array2::<f64>::zeros((1, 2));

    for i in 0..T {
        Y = sense(&Y, &pz);
        Y = predict(&Y, &pt, &)
        println!("Y at {}: {:2}", i, Y);
    }

    println!("Final: {:2}", Y);
}

fn sense(Y: &Array2<f64>, pz: &Array2<f64>) -> Array2<f64> {
    let y1 = Y * &pz.column(0);
    let y2 = Y * &pz.column(1);
    println!("y1: {}", y1);
    println!("y2: {}", y2);
    
    let rows = Y.nrows();
    let mut Y_new: Array2<f64> = Array2::<f64>::zeros((rows.pow(2), 2));
    for i in 0..rows {
        let start: usize = &i*rows;
        let end: usize = &(i+1)*rows;
        let res = &y1 + &y2.row(i);
        println!("res: {:2}", res);
        Y_new.slice_mut(s![start..end, ..]).assign(&res);
    }
    Y_new
}

fn predict(Y: &Array2<f64>, pt: &Array2<f64>) -> Array2<f64> {
    let rows = Y.nrows();
    let mut Y_new: Array2<f64> = Array2::<f64>::zeros((rows+2, 2));

    let V1 = (Y.dot(pt) - 1.)*GAMMA;
    

    Y_new
}

fn prune(Y: &mut Array2<f64>) {
  
}


fn largest(list: &[i32]) -> i32 {
    let mut largest = list[0];

    for &item in list.iter() {
        if item > largest {
            largest = item;
        }
    }

    largest
}
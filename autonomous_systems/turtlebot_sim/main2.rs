#![allow(non_snake_case)]
extern crate ndarray;

use ndarray::prelude::*;

fn main() {
    let pz = array![[0.7, 0.3], [0.3, 0.7]]; // measurement probabilities

    let mut Y = Array2::<f64>::zeros((1, 2));

    for i in 1..10 {
        do_some_maths(&mut Y, pz);
        // other functions that will modify Y
    }
    
    println!("Result: {}", Y);
}

fn do_some_maths(Y: &mut Array2<f64>, pz: Array2<f64>) {
    // let Yp = Y * pz.index_axis(Axis(1), 0);
    let Yp = Y * pz.slice(s![.., 0]);  // <-- this is the problem

    // do lots of matrix math with Yp
    // ...
    // then modify Y's data using Yp (hence Y needs to be &mut)
}
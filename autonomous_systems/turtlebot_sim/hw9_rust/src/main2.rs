#![allow(non_snake_case)]
extern crate ndarray;

use ndarray::prelude::*;

fn main() {
    let pz: Array2<f64> = array![[0.7, 0.3], [0.3, 0.7]]; // measurement probabilities

    let mut Y: Array2<f64> = Array2::<f64>::zeros((1, 2));
    let y0: Array2<i32> = arr2(&[[-100, 100], [100, -50]]);

    sense(&mut Y, pz);
}

fn sense<A>(Y: &mut Array2<f64>, pz: Array2<A>) {
    let Ypr = pz.index_axis(Axis(1), 0) * Y;

    println!("\nYpr: {}", Ypr);
}
extern crate ndarray;

use ndarray::prelude::*;
use ndarray::{stack,Zip};
use ndarray_stats::QuantileExt;

use itertools::Itertools;
use std::iter::FromIterator;

// Params
const T: i32 = 3;
const GAMMA: f64 = 1.0;
const PRUNE_RES: f64 = 0.0001;




fn sense(Y: &Array2<f64>, pz: &Array2<f64>) -> Array2<f64> {
    let y1 = Y * &pz.column(0);
    let y2 = Y * &pz.column(1);
    println!("\n y1: \n{:2}", y1);
    println!(" y2: \n{:2}", y2);
    
    let rows = Y.nrows();
    let mut Y_new: Array2<f64> = Array2::<f64>::zeros((rows.pow(2), 2));
    for i in 0..rows {
        let start: usize = &i*rows;
        let end: usize = &(i+1)*rows;
        let res = &y1 + &y2.row(i);
        // println!("res: \n{:2}", res);
        Y_new.slice_mut(s![start..end, ..]).assign(&res);
    }
    println!("\nAfter sense: \n{}", Y_new);
    Y_new
}

fn predict(Y: &Array2<f64>, pt: &Array2<f64>, y0: &Array2<f64>) -> Array2<f64> {
    let rows = Y.nrows();
    let mut Y_new: Array2<f64> = Array2::<f64>::zeros((rows+2, 2));

    let V1 = (Y.dot(pt) - 1.)*GAMMA;
    Y_new.slice_mut(s![..2, ..]).assign(&y0);
    Y_new.slice_mut(s![2.., ..]).assign(&V1);
     
    println!("\nAfter predict: \n{}", Y_new);
    Y_new
}    

fn prune(Y: &Array2<f64>, probs: &Array2<f64>) -> Array2<f64> {
    let lines = Y.dot(probs);
    let mut args: Array1<i32> = Array1::zeros(lines.ncols());
    Zip::from(&mut args)
        .and(lines.gencolumns())
        .apply( |arg, col| *arg = col.argmax().unwrap() as i32 );
    
    let indexes = Array::from_iter(args.into_iter().unique());
    let mut Y_new: Array2<f64> = Array2::<f64>::zeros((indexes.len(), 2));

    Zip::from(Y_new.genrows_mut())
         .and(&indexes)
         .apply( |mut Y_new_row, index| Y_new_row.assign(&Y.slice(s![**index, ..])) ); 
    
    println!("\nAfter prune: \n{}", Y_new);
    Y_new
}
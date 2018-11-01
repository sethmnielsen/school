%
%   ECEn 671 - Fall 2010
%   Professor Neal K. Bangerter
%   Homework #3
%
%   Problem #2
%

clear;
close all;

%   Load in the matrices needed for this problem
load('prob2.mat');

%   flatten images
x_ = reshape(x, [256^2, 1]);
A_ = zeros(256^2, 20);
e_mat = A_;

for kk=1:20
   A_(:,kk) = reshape(A(:,:,kk), [256^2, 1]); 
end

%   calculate e1
e1 = A_(:,1) / sqrt( sum(A_(:,1) .^ 2) );
e_mat(:,1) = e1;

%   calculate e_mat
for kk = 2 : 20
    e_i = grammy(A_(:,kk), e_mat(:,1:kk-1));
    e_mat(:,kk) = e_i;
end

coeff = e_mat' * x_;
temp = e_mat * coeff;
new_img_ = x_ - temp;
new_img = reshape(new_img_, [256, 256]);

figure;
imshow(new_img,[]);


%   There are two matrices, one containing 20
%   basis images, and one containing the image
%   x that we are trying to decode.

%   Display the 20 basis images in matrix A
figure;
for kk = 1:20
    subplot(4,5,kk);
    imshow(A(:,:,kk),[]);
end

%   And display the image x
figure;
imshow(x,[]);

%   The image you are trying to decode is hidden
%   in x.  In order to decode it, you need to
%   decompose x = x_hat + e, where x_hat is an
%   orthogonal projection of x onto the space
%   spanned by the 20 images in A, and e is the
%   error vector between x and its projection.
%   The hidden image will be the error vector e.

%   Some useful hints:

%   (1) To deal with images as vectors, you should
%       "flatten" each image into a column vector that
%       is 256*256 = 65,536 elements long.
%       The "reshape" command in Matlab will come
%       in handy here.
%
%   (2) Once you are done with your vector math, you
%       will probably want to reshape your result
%       back to a 256 x 256 image so you can display it.
%
%   (3) Make sure your images are either scaled from
%       0 to 1 if you are calling "imshow(image)", or
%       that you use the form "imshow(image, [])"
%       where the "[]" tells imshow to scale black
%       and white values between the minimum and
%       maximum values in the image.


function p_vec_e = grammy( vec, e_mat )
    in_prod = sum( vec .* e_mat );
    proj_ei = in_prod .* e_mat;
    p_vec_q = vec - sum( proj_ei, 2);
    p_vec_q_norm = sqrt( sum( p_vec_q .^ 2 ) );
    p_vec_e = p_vec_q / p_vec_q_norm;
end
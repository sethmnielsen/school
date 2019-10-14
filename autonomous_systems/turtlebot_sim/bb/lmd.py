"""le module
A collection of helper constants and functions.
Angle constants
Angle wrappers
Rotations: 2-D, 3-D, I2B
Rounding values to ranges
"""

from IPython.core.debugger import set_trace

import numpy as np

#

# ======================================
# ======================================

# magic numbers

r2d = 180.0 / np.pi
d2r = np.pi / 180.0
inv_360 = 1.0 / 360.0
inv_180 = 1.0 / 180.0
inv_pi = 1.0 / np.pi
inv_2pi = 0.5 / np.pi

sec2nsec = 1e9
sec2usec = 1e6
sec2msec = 1e3

msec2nsec = 1e6
msec2usec = 1e3
msec2sec  = 1e-3

usec2nsec = 1e3
usec2msec = 1e-3
usec2sec  = 1e-6

nsec2usec = 1e-3
nsec2msec = 1e-6
nsec2sec  = 1e-9

round_base = 50 # this is usec, but maybe we need to change it to nsec

i_vec_2d = np.array( [ 1, 0 ] )
j_vec_2d = np.array( [ 0, 1 ] )

i_vec = np.array( [ 1, 0, 0 ] )
j_vec = np.array( [ 0, 1, 0 ] )
k_vec = np.array( [ 0, 0, 1 ] )

enu2ned_mat = np.array( [ [0,1,0], [1,0,0], [0,0,-1] ] )

unit_2d_mat = np.array( [ [1,0], [0,1] ] )
eye2 = np.array( [ [1,0], [0,1] ] )
unit_3d_mat = np.array( [ [1,0,0], [0,1,0], [0,0,1] ] )
eye3 = np.array( [ [1,0,0], [0,1,0], [0,0,1] ] )


# ======================================
# ======================================

def deg_wrap_180( angle ):
    """wrap an angle in degrees, -180 <= theta < 180"""
    angle -= 360.0 * np.floor((angle + 180.) * inv_360)
    return angle
#
def deg_wrap_360( angle ):
    """wrap an angle in degrees, 0 <= theta < 360"""
    angle -= 360.0 * np.floor(angle * inv_360)
    return angle
#

def rad_wrap_pi( angle ):
    """wrap an angle in rads, -pi <= theta < pi"""
    angle -= 2*np.pi * np.floor((angle + np.pi) * inv_2pi)
    return angle
#
def rad_wrap_2pi( angle ):
    """wrap an angle in rads, 0 <= theta < 2*pi"""
    angle -= 2*np.pi * np.floor(angle * inv_2pi)
    return angle
#

# ======================================
# ======================================

def my_round(xx, base=round_base):
    """Round to a float"""
    # return (base * (np.array(x) / base).round()).round(prec)
    return base * np.floor(xx / base)
#
def my_round_int(xx, base=round_base):
    """Round to an integer"""
    # return (base * (np.array(x) / base).round()).round(prec)
    return (base * np.floor(xx / base)).astype(int)
#

# ======================================
# ======================================

def Rz_2d_I2B( psi ):
    """Rotation matrix about z-axis, in 2-D.
    This is the inertial_2_body rotation
    For batch processing, the Transpose of the output
    will give you a set of b2i matrices. Transpose each
    in turn to get i2b matrices."""
    cps = np.cos( psi )
    sps = np.sin( psi )

    Rz_2d_i2b = np.array([[cps,sps],[-sps,cps]])

    return Rz_2d_i2b
#

# ======================================
# ======================================

def Rx_I2B( phi ):
    """Rotation matrix about y-axis.
    This is the inertial_2_body rotation"""
    cph = np.cos( phi )
    sph = np.sin( phi )

    Rx_i2b = np.array([[1,0,0],[0,cph,sph],[0,-sph,cph]])

    return Rx_i2b
#

# ======================================

def Ry_I2B( theta ):
    """Rotation matrix about y-axis.
    This is the inertial_2_body rotation"""
    cth = np.cos( theta )
    sth = np.sin( theta )

    Ry_i2b = np.array([[cth,0,-sth],[0,1,0],[sth,0,cth]])

    return Ry_i2b
#

# ======================================

def Rz_I2B( psi ):
    """Rotation matrix about z-axis.
    This is the inertial_2_body rotation"""
    cps = np.cos( psi )
    sps = np.sin( psi )

    Rz_i2b = np.array([[cps,sps,0],[-sps,cps,0],[0,0,1]])

    return Rz_i2b
#

# ======================================

def RI2B(attitude):
    """Rotation matrix inertial frame to body frame.
    Takes an attitude represented as either:
    a 3 vector (euler), or
    a 4 vector (quaternion) --> SCALAR IS FIRST,
    and returns the specified rotation matrix"""
    # returns the transformation inertial to body frame
    # ======================================
    # first check if attitude was given in quaternion values
    # use appropriate i2b calculation

    if np.size(attitude) == 4:
        # print("size 4")
        return RI2Bq(attitude)
    elif np.size(attitude) == 3:
        # print("size 3")
        return RI2Be(attitude)
    else:
        print("Error. Size not equal to 4 or 3.\nOr possibly a shape error.")
    #
#

# ======================================

def RI2Be(attitude_Eul):
    """Sub-function RI2B.
    Takes attitude in euler representation.
    Returns Ri2b"""
    # print("RI2Be")
    # hold current phi, theta, and psi
    phi     = attitude_Eul[0]
    theta   = attitude_Eul[1]
    psi     = attitude_Eul[2]

    # ======================================

    # # trig abbreviations
    cph = np.cos(phi)
    sph = np.sin(phi)
    # tph = tan(phi)

    cth = np.cos(theta)
    sth = np.sin(theta)
    # tth = tan(theta);

    cps = np.cos(psi)
    sps = np.sin(psi)
    # tps = tan(psi);

    # rotation inertial 2 body, euler angles
    r_i2bE   = np.array([[cth*cps, cth*sps, -sth],
                        [sph*sth*cps - cph*sps, sph*sth*sps + cph*cps, sph*cth],
                        [cph*sth*cps + sph*sps, cph*sth*sps - sph*cps, cph*cth]])
    #
    return r_i2bE
    # # tb2i = rpyI2B'
#

# ======================================

def RI2Bq(attitude_Quat):
    """Requires scalar to be first!!!!
    Sub-function RI2B.
    Takes attitude in quaternion representation.
    Returns Ri2b"""
    print("Error. Size equal to 4.")
    q0 = attitude_Quat[0] # [3]
    q1 = attitude_Quat[1] # [4]
    q2 = attitude_Quat[2] # [5]
    q3 = attitude_Quat[3] # [6]

    # ======================================

    # rotation inertial 2 body, quaternion
    r_i2bQ    = [ [q0^2+q1^2-q2^2-q3^2,    2*(q1*q2+q0*q3),        2*(q1*q3-q0*q2)]
                  [2*(q1*q2-q0*q3),        q0^2-q1^2+q2^2-q3^2,    2*(q2*q3+q0*q1)]
                  [2*(q1*q3+q0*q2),        2*(q2*q3-q0*q1),        q0^2-q1^2-q2^2+q3^2] ]
    #
    return r_i2bQ
#

# ======================================
# ======================================

def calc_est_error(tbot,est):
    # set_trace()
    pos_x_error = tbot.xx_hist__np[0] - est.mu_hist[0]
    pos_y_error = tbot.xx_hist__np[1] - est.mu_hist[1]
    pos_psi_error = rad_wrap_pi(tbot.xx_hist__np[2] - est.mu_hist[2])

    est_err = [pos_x_error, pos_y_error, pos_psi_error]

    sqrt_cov_x = np.sqrt(est.sigma_hist[:,0,0])
    sqrt_cov_y = np.sqrt(est.sigma_hist[:,1,1])
    sqrt_cov_psi = np.sqrt(est.sigma_hist[:,2,2])

    sqrt_cov = [sqrt_cov_x, sqrt_cov_y, sqrt_cov_psi]

    return est_err, sqrt_cov
#

# ======================================

#

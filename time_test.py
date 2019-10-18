import timeit
import numpy as np
def wrap(angle, dim=None):
    if isinstance(angle, np.ndarray) and angle.size == 0:
        return angle
    
    if dim:
        angle[dim] -= 2*np.pi * np.floor((angle[dim] + np.pi) / (2*np.pi))
    else:
        angle -= 2*np.pi * np.floor((angle + np.pi) / (2*np.pi))
        
    return angle



def time_this():
    SETUP_CODE = '''
import numpy as np 
from __main__ import wrap
q = np.ones((3,1000));q[2] = q[2] + np.random.rand(1000)
n = np.ones((3,1000));n[2] = n[2] + np.random.rand(1000)
n[2,::148] = 4.3 + np.random.rand(7)'''

    TEST_CODE1 = '''n[2][ abs(n[2])>np.pi ] = wrap(n[2][ abs(n[2])>np.pi ])'''

    TEST_CODE2 = '''n[2] = wrap(n[2])'''

    TEST_CODE3 = '''v = abs(n[2])>np.pi;n[2][v] = wrap(n[2][v])'''

    TEST_CODE4 = '''n = wrap(n,2)'''

    TEST_CODE5 = '''inds = np.nonzero( abs(n[2])>np.pi )[0];n[2][inds] = wrap(n[2][inds])'''

    TEST_CODE6 = '''q = wrap(q,2)'''

    TEST_CODE7 = '''v = abs(q[2])>np.pi;q[2][v] = wrap(q[2][v])'''
    
    t = timeit.repeat(stmt=TEST_CODE1, setup=SETUP_CODE, repeat=1, number=1000000)
    print(f't1: {t}\n')

    t = timeit.repeat(stmt=TEST_CODE2, setup=SETUP_CODE, repeat=1, number=1000000)
    print(f't2: {t}\n')
    
    t = timeit.repeat(stmt=TEST_CODE3, setup=SETUP_CODE, repeat=1, number=1000000)
    print(f't3: {t}\n')

    t = timeit.repeat(stmt=TEST_CODE4, setup=SETUP_CODE, repeat=1, number=1000000)
    print(f't4: {t}\n')

    t = timeit.repeat(stmt=TEST_CODE5, setup=SETUP_CODE, repeat=1, number=1000000)
    print(f't5: {t}\n')

    t = timeit.repeat(stmt=TEST_CODE6, setup=SETUP_CODE, repeat=1, number=1000000)
    print(f't6: {t}\n')
    
    t = timeit.repeat(stmt=TEST_CODE7, setup=SETUP_CODE, repeat=1, number=1000000)
    print(f't7: {t}\n')


if __name__ == '__main__':
    time_this()



import numpy as np

def quaternion2euler(w, x, y, z):
    ysqr = y * y

    t0 = + 2.0 * (w * x + y * z)
    t1 = + 1.0 - 2.0 * (x * x + ysqr)
    X = np.degrees(np.arctan2(t0, t1))

    t2 = + 2.0 * (w * y - z * x)

    t2 = np.clip(t2, a_min=-1.0, a_max=1.0)
    Y = np.degrees(np.arcsin(t2))

    t3 = + 2.0 * (w * z + x * y)
    t4 = + 1.0 - 2.0 * (ysqr + z * z)
    Z = np.degrees(np.arctan2(t3, t4))

    return X, Y, Z

def addEulerAngles(data):

    if all(key in data for key in ('q[0]', 'q[1]', 'q[2]', 'q[3]')):
        print(data.keys())

    # for key, value in data.items():
    #     if key

    return data
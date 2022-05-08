import math
def trajectory(x, a, v_0):
    g = 9.82
    return x*math.tan(math.radians(a))-(g*x**2) /(2*(v_0**2)*math.cos(math.radians(a))**2)

def v_0xy(v_0, a):
    g = 9.82
    return (v_0*math.cos(math.radians(a)), v_0*math.sin(math.radians(a)))


if __name__ == '__main__':
    # for i in range(10):
    #     print(trajectory(i, 45, 10.0))
    # print(math.cos(math.radians(45)))
    print(math.asin(8/1))

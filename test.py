def f(x0, y0, Vx, Vy, ax, ay, t):
    x = x0 + Vx*t + ax*t**2/2
    y = y0 + Vy*t + ay*t**2/2
    cor = [x,y]
    return cor


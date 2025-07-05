import math
import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# 定义性别比率和资源动态的模型方程
def logistic(p):
    return 1 / (1 + math.exp(-p))


def model(y, t, params):
    rate, P, A= y
    k1, b1, k2, b2, rate_0, miu, alpha, beta = params
    r = k2 * (rate - rate_0) * (rate - rate_0) + b2
    K = (alpha * rate + beta)
    d1dt = r * logistic(k1 * A / P + b1) - (r * P / K + miu) * rate
    dP1dt = r * P * (1 - P / K) - miu * P
    if (t < 10):
        dAdt = -5
    elif ((t > 75) and (t < 100)):
        dAdt = 20
    else: dAdt = 0
    #if (t < 12.5):
        #dAdt = 20
    #elif ((t > 50) and (t < 85)):
        #dAdt = -20
    #elif ((t > 125) and (t < 150)):
        #dAdt = 20
    #else: dAdt = 0
    return [d1dt, dP1dt, dAdt]

A_1 = 500
A_2 = 50
k1 = -0.02
b1 = 1.27
k2 = -0.4
b2 = 0.1
miu = 0.05
alpha2 = 2
beta2 = 23.8
rate_0 = 0.5
y0 = [0.75, 8, 50]
#y0 = [0.6, 12, 500]
params = [k1, b1, k2, b2, rate_0, miu, alpha2, beta2]
t = np.linspace(0, 200, 10000)
solution = odeint(model, y0, t, args=(params, ))

# 绘制结果
plt.figure(figsize=(10, 5))
plt.plot(t, solution[:, 0] * 10, label='Resource $rate_t$')
plt.plot(t, solution[:, 1], label='Resource $P_t$')
plt.plot(t, solution[:, 2] / 100, label='Resource $A_t$')
plt.xlabel('Time')
plt.ylabel('Value')
plt.title('Dynamics of Sex Ratio and Resource Availability')
plt.legend()
plt.show()
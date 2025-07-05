import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# 定义性别比率和资源动态的模型方程
def logistic(p):
    return 1 / (1 + math.exp(-p))

def model(y, t, params):
    rate_1, rate_2, P1, P2= y
    A_1, A_2, k1, b1, k2, b2, rate_0, miu, alpha, beta = params
    r1 = k2 * (rate_1 - rate_0) * (rate_1 - rate_0) + b2
    r2 = k2 * (rate_2 - rate_0) * (rate_2 - rate_0) + b2
    K1 = (alpha * rate_1 + beta)
    K2 = (alpha * rate_2 + beta)
    d1dt = r1 * logistic(k1 * A_1 / P1 + b1) - (r1 * P1 / K1 + miu) * rate_1
    d2dt = r2 * logistic(k1 * A_2 / P2 + b1) - (r2 * P2 / K2 + miu) * rate_2
    dP1dt = r1 * P1 * (1 - P1 / K1) - miu * P1
    dP2dt = r2 * P2 * (1 - P2 / K2) - miu * P2
    return [d1dt, d2dt, dP1dt, dP2dt]

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
y0 = [0.5, 0.5, 10, 10]
params = [A_1, A_2, k1, b1, k2, b2, rate_0, miu, alpha2, beta2]
t = np.linspace(0, 400, 1000)
solution = odeint(model, y0, t, args=(params, ))

# 绘制结果
plt.figure(figsize=(10, 5))
plt.plot(t, solution[:, 0] * 10, label='Resource $rate1_t$')
plt.plot(t, solution[:, 1] * 10, label='Resource $rate2_t$')
plt.plot(t, solution[:, 2], label='Resource $P1_t$')
plt.plot(t, solution[:, 3], label='Resource $P2_t$')
plt.xlabel('Time')
plt.ylabel('Value')
plt.title('Dynamics of Sex Ratio and Resource Availability')
plt.legend()
plt.show()
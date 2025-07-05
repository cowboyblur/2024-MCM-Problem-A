import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# 定义性别比率和资源动态的模型方程
def logistic(p):
    return 1 / (1 + math.exp(-p))

def model(y, t, params):
    H1, H2, P1, P2, rate= y
    A, alpha1, beta1, alpha2, beta2, const_rate, delta_H = params
    K_P = (alpha2 * rate + beta2)
    drdt = r_P * logistic(k * A / P1 + b) - (r_P * P1 / K_P + (alpha1 * rate + beta1) * H1) * rate
    dP1dt = r_P * P1 * (1 - P1 / K_P) - (alpha1 * rate + beta1) * H1 * P1
    dP2dt = r_P * P2 * (1 - P2 / (alpha2 * const_rate + beta2)) - (alpha1 * const_rate + beta1) * H2 * P2
    dH1dt = delta_H * (alpha1 * rate + beta1) * H1 * P1 - miu * H1
    dH2dt = delta_H * (alpha1 * const_rate + beta1) * H2 * P2 - miu * H2
    return [dH1dt, dH2dt, dP1dt, dP2dt, drdt]

A = 100
K_P = 20
r_P = 0.4
k = -0.02
b = 1.27
P0 = 5
H0 = 2
rate = 0.65
alpha1 = -0.1
beta1 = 0.15
alpha2 = 2
beta2 = 15.7
miu = 0.2
const_rate = 0.65
delta_H = 0.35
y0 = [H0, H0, P0, P0, rate]
params = [A, alpha1, beta1, alpha2, beta2, const_rate, delta_H]
t = np.linspace(0, 200, 10000)
solution = odeint(model, y0, t, args=(params, ))

# 绘制结果
plt.figure(figsize=(10, 5))
plt.plot(t, solution[:, 0], label='Resource $H1_t$')
plt.plot(t, solution[:, 1], label='Resource $H2_t$')
plt.plot(t, solution[:, 2], label='Resource $P1_t$')
plt.plot(t, solution[:, 3], label='Resource $P2_t$')
plt.plot(t, solution[:, 4] * 10, label='Resource $rate_t$')
plt.xlabel('Time')
plt.ylabel('Value')
plt.title('Dynamics of Sex Ratio and Resource Availability')
plt.legend()
plt.show()
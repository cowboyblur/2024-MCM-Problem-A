import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# 定义性别比率和资源动态的模型方程
def logistic(p):
    return 1 / (1 + math.exp(-p))

def model(y, t, params):
    A1, A2, rate = y
    P, K_P, K_A, r_P, r_A, alpha, beta, k, b, miu, const_rate = params
    newborn_rate = logistic(k * A1 / P + b)
    drdt = r_P * newborn_rate- r_P * P / K_P * rate
    dA1dt = r_A * A1 * (1 - A1 / K_A) - miu * (alpha * rate + beta) * P * A1
    dA2dt = r_A * A2 * (1 - A2 / K_A) - miu * (alpha * const_rate + beta) * P * A2
    return [dA1dt, dA2dt, drdt]

P = 20
K_P = 20
r_P = 0.05
k = -0.02
b = 1.27
r_A = 0.05
K_A = 1000
A0 = 1000
rate = 0.56
alpha = 0.01
beta = 0.005
miu = 0.1
const_rate = 0.56
y0 = [A0, A0, rate]
params = [P, K_P, K_A, r_P, r_A, alpha, beta, k, b, miu, const_rate]
t = np.linspace(0, 100, 10000)
solution = odeint(model, y0, t, args=(params, ))

# 绘制结果
plt.figure(figsize=(10, 5))
plt.plot(t, solution[:, 0], label='Resource $A1_t$')
plt.plot(t, solution[:, 1], label='Resource $A2_t$')
plt.plot(t, solution[:, 2] * 1000, label='Resource $rate_t$')
plt.xlabel('Time')
plt.ylabel('Value')
plt.title('Dynamics of Sex Ratio and Resource Availability')
plt.legend()
plt.show()

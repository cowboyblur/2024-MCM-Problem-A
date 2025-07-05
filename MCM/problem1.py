import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# 定义性别比率和资源动态的模型方程
def logistic(p):
    return 1 / (1 + math.exp(-p))

def model(y, t, params):
    rate_1, rate_2, rate_3, rate_4 = y
    P, K, r, A_1, A_2, A_3, A_4, k, b = params
    d1dt = r * logistic(k * A_1 / P + b) - r * P / K * rate_1
    d2dt = r * logistic(k * A_2 / P + b) - r * P / K * rate_2
    d3dt = r * logistic(k * A_3 / P + b) - r * P / K * rate_3
    d4dt = r * logistic(k * A_4 / P + b) - r * P / K * rate_4
    return [d1dt, d2dt, d3dt, d4dt]

P = 20
K = 20
r = 0.1
A_1 = 1000
A_2 = 500
A_3 = 100
A_4 = 20
k = -0.02
b = 1.27
y0 = [0.5, 0.5, 0.5, 0.5]
params = [P, K, r, A_1, A_2, A_3, A_4, k, b]
t = np.linspace(0, 50, 10000)
solution = odeint(model, y0, t, args=(params, ))

# 绘制结果
plt.figure(figsize=(10, 5))
plt.plot(t, solution[:, 0], label='Resource $A1_t$')
plt.plot(t, solution[:, 1], label='Resource $A2_t$')
plt.plot(t, solution[:, 2], label='Resource $A3_t$')
plt.plot(t, solution[:, 3], label='Resource $A4_t$')
plt.xlabel('Time')
plt.ylabel('Value')
plt.title('Dynamics of Sex Ratio and Resource Availability')
plt.legend()
plt.show()
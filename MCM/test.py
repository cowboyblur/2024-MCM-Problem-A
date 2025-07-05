import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# 定义性别比率和资源动态的模型方程
def logistic(p):
    return 1 / (1 + math.exp(-p))

def model(y, t, params):
    A, B, P, rate = y
    gamma_A, gamma_B, gamma_P, K_A, theta_BA, miu, alpha_1, beta_1,\
    alpha_2, beta_2, k, b, delta_BA, delta_BP, delta_PA, m = params

    dAdt = gamma_A * A * (1 - A / K_A) - theta_BA * A * B - miu * (alpha_1 * rate + beta_1) * A * P

    dBdt = delta_BA * theta_BA * A * B + delta_BP * (alpha_2 * rate + beta_2) * B * P - gamma_B * B

    dPdt = - (alpha_2 * rate + beta_2) * B * P + delta_PA * (alpha_1 * rate + beta_1) * A * P - gamma_P * P - m * P * P

    newborn_rate = logistic(k * A / P + b)

    d_rate = delta_PA * (alpha_1 * rate + beta_1) * A * P * P * (newborn_rate - rate) # 将dPdt看作小量化简
    return [dAdt, dBdt, dPdt, d_rate]

# 初始条件
A0 = 100
B0 = 20
P0 = 2
rate = 0.56
y0 = [A0, B0, P0, rate]
gamma_A = 0.03
gamma_B = 0.04
gamma_P = 0.06
K_A = 100
theta_BA = 0.005
miu = 0.1
alpha_1 = 0.006 # 斜率
beta_1 = 0.006  # 截距
alpha_2 = -0.007
beta_2 = 0.007
k = -0.02
# 初始性别比为0.56
b = 1.3
delta_BA = 0.3
delta_BP = 0.3
delta_PA = 0.35
m = 0.001

params = [gamma_A, gamma_B, gamma_P, K_A, theta_BA, miu, alpha_1, beta_1,\
    alpha_2, beta_2, k, b, delta_BA, delta_BP, delta_PA, m]

# 时间点
t = np.linspace(0, 1000, 10000)

# 解微分方程
solution = odeint(model, y0, t, args=(params, ))

# 绘制结果
plt.figure(figsize=(10, 5))
plt.plot(t, solution[:, 0], label='Resource $A_t$')
plt.plot(t, solution[:, 1], label='Resource $B_t$')
plt.plot(t, solution[:, 2], label='Resource $P_t$')
plt.plot(t, solution[:, 3] * 100, label='Resource $rate_t$')
plt.xlabel('Time')
plt.ylabel('Value')
plt.title('Dynamics of Sex Ratio and Resource Availability')
plt.legend()
plt.show()

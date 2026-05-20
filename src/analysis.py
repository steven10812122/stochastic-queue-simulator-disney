import numpy as np
import matplotlib.pyplot as plt
from disney_simulation import run_simulation  # 確保你的模擬器檔案名稱正確

# --- 參數設定 ---
mu = 3.0
rho_values = np.linspace(0.1, 0.95, 10) # 參數掃描範圍
n_customers = 200
n_iters = 500

# 用來儲存數據
mean_wait_A = []
mean_wait_B = []
theoretical_wait = []

# --- 1 & 2. 參數研究與理論對照 ---
for rho in rho_values:
    lam = rho * mu
    theory = rho / (mu * (1 - rho)) # M/M/1 理論值
    theoretical_wait.append(theory)
    
    iters_A = []
    iters_B = []
    
    for _ in range(n_iters):
        service_times = np.random.exponential(scale=1/mu, size=n_customers)
        types = np.random.choice(['LL', 'SB'], size=n_customers, p=[0.3, 0.7])
        
        # 情境 A
        arrival_A = np.cumsum(np.random.exponential(scale=1/lam, size=n_customers))
        wait_A = run_simulation(arrival_A, service_times, types)
        iters_A.append(np.mean([wait_A[j] for j in range(n_customers) if types[j]=='SB' and j>20]))
        
        # 情境 B
        arrival_B = np.arange(1, n_customers+1) * (1/lam) + np.random.uniform(-0.1, 0.1, n_customers)
        wait_B = run_simulation(arrival_B, service_times, types)

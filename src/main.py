import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. 核心模擬器函數 (M/M/1 Priority Queue)
# ==========================================
def run_simulation(arrival_times, service_times, customer_types):
    n = len(arrival_times)
    waiting_times = np.zeros(n)
    current_time = 0.0
    served_status = np.zeros(n, dtype=bool)
    customers_served_count = 0

    while customers_served_count < n:
        # 找出已經到達且還沒被服務的顧客
        waiting_indices = np.where((arrival_times <= current_time) & (~served_status))[0]

        # 如果隊伍是空的，直接把時間快轉到下一個人的到達時間
        if len(waiting_indices) == 0:
            unserved_indices = np.where(~served_status)[0]
            current_time = np.min(arrival_times[unserved_indices])
            continue

        # 將排隊的人分為 LL (快速通關) 與 SB (一般排隊)
        ll_waiting = [idx for idx in waiting_indices if customer_types[idx] == 'LL']
        sb_waiting = [idx for idx in waiting_indices if customer_types[idx] == 'SB']

        # 優先權邏輯：有 LL 就先選 LL 最早到的，否則選 SB 最早到的
        if len(ll_waiting) > 0:
            chosen_customer = ll_waiting[0] 
        else:
            chosen_customer = sb_waiting[0]

        # 計算該顧客的實際開始服務時間與等待時間
        service_start = max(current_time, arrival_times[chosen_customer])
        waiting_times[chosen_customer] = service_start - arrival_times[chosen_customer]
        
        # 更新目前時間與服務狀態
        current_time = service_start + service_times[chosen_customer]
        served_status[chosen_customer] = True
        customers_served_count += 1

    return waiting_times

# ==========================================
# 2. 實驗環境與蒙地卡羅參數設定
# ==========================================
np.random.seed(42)   # 固定隨機種子，確保結果可重現
lambda_rate = 2      # 到達率
mu_rate = 3          # 服務率
n_customers = 100    # 每次模擬的顧客總數
p_lightning = 0.3    # LL 票的比例
warm_up = 20         # 暖機期：剔除前 20 位顧客的數據避免邊界效應
n_iters = 1000       # 蒙地卡羅模擬次數

# 用來存放每次模擬的「SB 平均等待時間」
sb_means_A = []
sb_means_B = []

print(f"開始執行蒙地卡羅模擬 (共 {n_iters} 次迭代)...")

# ==========================================
# 3. 蒙地卡羅主迴圈
# ==========================================
for i in range(n_iters):
    # (a) 生成共同的隨機變數 (Common Random Numbers)
    # 確保兩種情境下面對的服務時間與顧客身分都是一樣的，這在運籌學中稱為公平對比
    service_times = np.random.exponential(scale=1/mu_rate, size=n_customers)
    customer_types = np.random.choice(['LL', 'SB'], size=n_customers, p=[p_lightning, 1-p_lightning])
    
    # (b) 情境 A：完全隨機到達 (高變異，原始狀況)
    interarrival_A = np.random.exponential(scale=1/lambda_rate, size=n_customers)
    arrival_A = np.cumsum(interarrival_A)
    wait_A = run_simulation(arrival_A, service_times, customer_types)
    
    # 提取 SB 顧客的等待時間，並且只取 warm_up 之後的數據
    sb_wait_A = [wait_A[j] for j in range(n_customers) if customer_types[j] == 'SB' and j >= warm_up]
    if sb_wait_A: # 防呆，確保有數據
        sb_means_A.append(np.mean(sb_wait_A))
    
    # (c) 情境 B：預約分流 (低變異，加入時間視窗控制)
    # 平均每 0.5 (即 1/lambda_rate) 單位時間來 1 個人，並加入 Uniform 分配的微小擾動
    scheduled_times = np.arange(1, n_customers + 1) * (1/lambda_rate)
    noise = np.random.uniform(-0.1, 0.1, n_customers) 
    arrival_B = scheduled_times + noise
    wait_B = run_simulation(arrival_B, service_times, customer_types)
    
    # 提取 SB 顧客的等待時間，並且只取 warm_up 之後的數據
    sb_wait_B = [wait_B[j] for j in range(n_customers) if customer_types[j] == 'SB' and j >= warm_up]
    if sb_wait_B:
        sb_means_B.append(np.mean(sb_wait_B))

# ==========================================
# 4. 統計結果輸出與視覺化 (Histogram)
# ==========================================
print("-" * 50)
print(f"【情境 A (隨機到達)】 平均等待時間 (95% CI): {np.mean(sb_means_A):.3f} ± {1.96 * np.std(sb_means_A):.3f}")
print(f"【情境 B (預約分流)】 平均等待時間 (95% CI): {np.mean(sb_means_B):.3f} ± {1.96 * np.std(sb_means_B):.3f}")
print("-" * 50)

# 畫出分佈圖
plt.figure(figsize=(10, 6))

# 使用半透明直方圖來展示分佈重疊狀況
plt.hist(sb_means_A, bins=40, alpha=0.6, label='Scenario A: Random Arrivals', color='#ff6b6b', edgecolor='black')
plt.hist(sb_means_B, bins=40, alpha=0.7, label='Scenario B: Scheduled Arrivals', color='#4ecdc4', edgecolor='black')

# 加入平均值垂直線
plt.axvline(np.mean(sb_means_A), color='red', linestyle='dashed', linewidth=2)
plt.axvline(np.mean(sb_means_B), color='green', linestyle='dashed', linewidth=2)

# 圖表美化
plt.title(f"Monte Carlo Simulation: SB Waiting Time Distribution\n({n_iters} iterations, n={n_customers}, warm-up={warm_up})", fontsize=14)
plt.xlabel("Average Standby (SB) Waiting Time", fontsize=12)
plt.ylabel("Frequency", fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()

# 顯示圖表
plt.show()

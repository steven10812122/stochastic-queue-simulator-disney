# Stochastic Queueing Simulation for Service Systems  
## A Monte Carlo Study of Disney-Style Queue Management Policies

---

## 1. Overview

This project studies how different queue management strategies affect waiting times in stochastic service systems.

The system is inspired by real-world service environments such as:

- Theme parks (e.g., Disney World ride queues)
- Hospitals and emergency departments
- High-traffic service systems

We model the system as a stochastic priority queue and evaluate how scheduling and arrival control affect system performance.

---

## 2. Research Question

This project investigates:

> How do different arrival patterns and queue management policies affect waiting time in a stochastic service system?

Specifically, we compare:

- **Scenario A:** Random arrivals (Poisson process)
- **Scenario B:** Scheduled arrivals with small stochastic noise

We further study how system behavior changes under different traffic intensities.

---

## 3. System Model

We model a single-server stochastic queue with:

### Arrival process

Scenario A:
\[
T_a \sim Exp(\lambda)
\]

Scenario B:
\[
T_a = \text{deterministic schedule} + \text{uniform noise}
\]

### Service process

\[
T_s \sim Exp(\mu)
\]

### Priority rule

Customers are divided into two types:

- LL (fast pass customers, higher priority)
- SB (standard queue customers)

Service discipline:
> LL customers are served first when available.

---

## 4. Simulation Methodology

We use Monte Carlo simulation with the following structure:

- Number of customers: `n_customers = 100`
- Number of iterations: `n_iters = 1000`
- Warm-up period: first 20 customers excluded
- Common random numbers used for fair comparison

Each iteration:
1. Generate service times
2. Generate arrival process for both scenarios
3. Run discrete-event queue simulation
4. Collect SB (standard queue) waiting times
5. Compute performance metrics

---

## 5. Theoretical Benchmark

For validation, we compare simulation results with classical M/M/1 queueing theory:

:contentReference[oaicite:0]{index=0}

where:

\[
\rho = \frac{\lambda}{\mu}
\]

This allows us to validate simulation correctness and study deviations under non-Poisson arrival structures.

---

## 6. Extended Analysis: Parameter Study

Beyond A/B comparison, we perform a systematic study over traffic intensity:

\[
\rho \in [0.1, 0.95]
\]

We analyze:

- System performance under different load conditions
- Comparison between theoretical and simulated results
- Policy effectiveness under congestion regimes

---

## 7. Key Performance Metrics

We evaluate:

- Mean waiting time (SB customers)
- Variance of waiting time
- Confidence intervals (95%)
- Efficiency gain between policies

---

## 8. Key Results

### 8.1 System Performance

- Waiting time increases non-linearly as traffic intensity increases
- Scenario B (scheduled arrivals) consistently outperforms Scenario A
- Performance gap increases under high congestion (ρ → 1)

---

### 8.2 Efficiency Gain

Scheduled arrival policy achieves:

- **40%–100% reduction** in SB waiting time depending on traffic intensity
- Maximum benefit observed in high-load regimes

---

### 8.3 Theoretical Validation

Simulation results are consistent with M/M/1 theoretical trends under Poisson arrivals, validating model correctness while highlighting deviations under structured arrival processes.

---

## 9. Key Insight

This study suggests that:

> Queue congestion is driven more by arrival variability than by average arrival rate alone.

In particular, reducing variability in arrival processes can significantly improve system performance even without increasing service capacity.

---

## 10. Real-World Interpretation

This model applies to:

| Model Component | Real-world System |
|----------------|------------------|
| LL customers | Fast pass / VIP users |
| SB customers | Regular users |
| Service station | Ride / server / hospital |
| Arrival process | Customer inflow |

Applications include:

- Theme park queue optimization (e.g., Disney World)
- Hospital triage systems
- Airport boarding systems
- Service system capacity planning

---

## 11. Technologies Used

- Python
- NumPy
- Matplotlib

---

## 12. How to Run

```bash
python main.py
python analysis.py

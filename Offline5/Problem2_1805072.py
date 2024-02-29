import numpy as np
import matplotlib.pyplot as plt

ITERATION = 10000
n = 100 # sample size

success = np.zeros((4, n))

for _ in range(ITERATION):
    candidates = np.random.uniform(0, 1, n)
    sorted_candidates = np.sort(candidates)[::-1]

    for j in range(n):
        mx = 0
        for k in range(j):
            mx = max(mx, candidates[k])

        ans = candidates[n - 1]
        for k in range(j, n, 1):
            if candidates[k] >= mx:
                ans = candidates[k]
                break

        for i, s in enumerate([1, 3, 5, 10]):
            if sorted_candidates[s - 1] <= ans:
                success[i][j] += 1

success = (success / ITERATION) * 100

# Plotting
sample_sizes = np.arange(n)
success_criteria_values = [1, 3, 5, 10]

plt.figure(figsize=(10, 6))
for i, s in enumerate(success_criteria_values):
    plt.plot(sample_sizes, success[i], label=f's={s}')

plt.title("Success Rate vs. Sample Size for Different Success Criteria (s)")
plt.xlabel("Sample Size (n)")
plt.ylabel("Success Rate (%)")
plt.xlim(0, n)
plt.ylim(0, 100)
plt.legend()
plt.savefig('problem2_output.png')
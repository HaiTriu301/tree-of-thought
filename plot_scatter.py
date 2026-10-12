import json
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Larger text so labels stay readable when the figure is scaled to one column
plt.rcParams.update({'font.size': 16})

log_dir = 'logs/game24'
files = {
    'IO': 'gpt-3.5-turbo_0.7_naive_standard_sample_1_start900_end930.json',
    'CoT': 'gpt-3.5-turbo_0.7_naive_cot_sample_1_start900_end930.json',
    # ToT-1 removed: it was only run on 1 problem (start900_end901)
    'ToT-3': 'gpt-3.5-turbo_0.7_propose1_value3_greedy3_start900_end930.json',
    'ToT-5': 'gpt-3.5-turbo_0.7_propose1_value3_greedy5_start900_end930.json',
}
EXPECTED_PROBLEMS = 30


def get_accuracy_and_cost(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    solved = 0
    total_problems = 0
    cost = 0
    for item in data:
        total_problems += 1
        infos = item.get('infos', [])
        # Problem-level accuracy (cnt_any): solved if at least one output is correct
        if any(info.get('r', 0) == 1 for info in infos):
            solved += 1
        usage = item.get('usage_so_far', {})
        cost = usage.get('cost', 0)
    if total_problems != EXPECTED_PROBLEMS:
        print(f'WARNING: {file_path} has {total_problems} problems, expected {EXPECTED_PROBLEMS}')
    accuracy = solved / total_problems if total_problems > 0 else 0
    return accuracy, cost


accuracies = {}
costs = {}
for method, filename in files.items():
    file_path = os.path.join(log_dir, filename)
    if os.path.exists(file_path):
        acc, cost = get_accuracy_and_cost(file_path)
        accuracies[method] = acc
        costs[method] = cost
        print(f"{method}: accuracy={acc:.4f} ({acc*100:.2f}%), cost=${cost:.4f}")
    else:
        print(f"File not found: {file_path}")

methods = ['IO', 'CoT', 'ToT-3', 'ToT-5']
x = [costs[m] for m in methods]
y = [accuracies[m] for m in methods]
colors = ['#7f7f7f', '#3273dc', '#ff7f00', '#4daf4a']

plt.figure(figsize=(10, 7))
for i, m in enumerate(methods):
    plt.scatter(x[i], y[i], c=colors[i], s=200, label=m, zorder=5)
    plt.annotate(m, (x[i], y[i]), xytext=(8, -8),
                 textcoords='offset points', fontsize=16, fontweight='bold')

plt.xlabel('Cost ($)', fontsize=17)
plt.ylabel('Accuracy (%)', fontsize=17)
plt.ylim(0, 0.35)
plt.yticks([0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35], ['0%', '5%', '10%', '15%', '20%', '25%', '30%', '35%'])
plt.xscale('log')
plt.xlim(0.005, max(x) * 4)
plt.grid(axis='both', linestyle='--', alpha=0.4, zorder=0)
plt.tight_layout()
plt.savefig('fig_accuracy_vs_cost.png', dpi=150)
print('Saved fig_accuracy_vs_cost.png')
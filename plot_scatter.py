import json
import matplotlib.pyplot as plt
import os

log_dir = 'logs/game24'
files = {
    'IO': 'gpt-3.5-turbo_0.7_naive_standard_sample_1_start900_end930.json',
    'CoT': 'gpt-3.5-turbo_0.7_naive_cot_sample_1_start900_end930.json',
    'ToT-1': 'gpt-3.5-turbo_0.7_propose1_value3_greedy1_start900_end901.json',
    'ToT-3': 'gpt-3.5-turbo_0.7_propose1_value3_greedy3_start900_end930.json',
    'ToT-5': 'gpt-3.5-turbo_0.7_propose1_value3_greedy5_start900_end930.json',
}

def get_accuracy_and_cost(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    total_correct = 0
    total_responses = 0
    cost = 0
    for item in data:
        infos = item.get('infos', [])
        for info in infos:
            r = info.get('r', 0)
            total_responses += 1
            if r == 1:
                total_correct += 1
        usage = item.get('usage_so_far', {})
        cost = usage.get('cost', 0)
    accuracy = total_correct / total_responses if total_responses > 0 else 0
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

methods = ['IO', 'CoT', 'ToT-1', 'ToT-3', 'ToT-5']
x = [costs[m] for m in methods]
y = [accuracies[m] for m in methods]
colors = ['#7f7f7f', '#3273dc', '#984ea3', '#ff7f00', '#4daf4a']
sizes = [80, 80, 80, 80, 80]

plt.figure(figsize=(10, 7))
for i, m in enumerate(methods):
    plt.scatter(x[i], y[i], c=colors[i], s=200, label=m, zorder=5)
    plt.annotate(m, (x[i], y[i]), xytext=(8, -8),
                 textcoords='offset points', fontsize=12, fontweight='bold')

plt.xlabel('Cost ($)', fontsize=13)
plt.ylabel('Accuracy', fontsize=13)
plt.xscale('log')
plt.xlim(0.005, max(x) * 3)
plt.grid(axis='both', linestyle='--', alpha=0.4, zorder=0)
plt.tight_layout()
plt.savefig('scatter_accuracy_vs_cost.png', dpi=150)
print('Saved scatter_accuracy_vs_cost.png')
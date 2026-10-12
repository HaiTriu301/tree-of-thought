import json
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Larger text so labels stay readable when the figure is scaled to one column
plt.rcParams.update({'font.size': 16})

# Paths to log files (adjust if needed)
log_dir = 'logs/game24'
files = {
    'IO': 'gpt-3.5-turbo_0.7_naive_standard_sample_1_start900_end930.json',
    'CoT': 'gpt-3.5-turbo_0.7_naive_cot_sample_1_start900_end930.json',
    'ToT-3': 'gpt-3.5-turbo_0.7_propose1_value3_greedy3_start900_end930.json',
    'ToT-5': 'gpt-3.5-turbo_0.7_propose1_value3_greedy5_start900_end930.json',
    # ToT-1 removed: it was only run on 1 problem (start900_end901)
}
colors = ['#7f7f7f', '#3273dc', '#ff7f00', '#4daf4a']  # IO, CoT, ToT-3, ToT-5
EXPECTED_PROBLEMS = 30


def calculate_accuracy(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    total_problems = 0
    correct_problems = 0
    for item in data:
        total_problems += 1
        infos = item.get('infos', [])
        # Check if problem is solved (at least one response is correct)
        has_correct = any(info.get('r', 0) == 1 for info in infos)
        if has_correct:
            correct_problems += 1

    accuracy = correct_problems / total_problems if total_problems > 0 else 0
    return accuracy, total_problems


# Calculate accuracies
accuracies = {}
for method, filename in files.items():
    file_path = os.path.join(log_dir, filename)
    if os.path.exists(file_path):
        acc, total = calculate_accuracy(file_path)
        accuracies[method] = acc
        print(f"{method}: Accuracy = {acc:.3f} ({total} problems)")
        if total != EXPECTED_PROBLEMS:
            print(f"WARNING: {method} has {total} problems, expected {EXPECTED_PROBLEMS}")
    else:
        print(f"File not found: {file_path}")
        accuracies[method] = 0

# Plot bar chart
methods = list(accuracies.keys())
acc_values = list(accuracies.values())

max_acc = max(acc_values) if acc_values else 1
plt.figure(figsize=(10, 6))  # Larger figure
plt.bar(methods, acc_values, color=colors, width=0.6)
plt.xlabel('Methods')
plt.ylabel('Accuracy (%)')
# Title removed: the LaTeX caption names the figure
plt.ylim(0, 0.5)  # Max 50%
plt.yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5], ['0%', '10%', '20%', '30%', '40%', '50%'])
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add value labels on bars (as %)
for i, v in enumerate(acc_values):
    plt.text(i, v + max_acc*0.02, f'{v*100:.1f}%', ha='center', va='bottom')

plt.tight_layout()
plt.savefig('fig_accuracy.png', dpi=150)
print('Saved fig_accuracy.png')
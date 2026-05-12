import json
import matplotlib.pyplot as plt
import os

log_dir = 'logs/game24'
files = {
    'IO': 'gpt-3.5-turbo_0.7_naive_standard_sample_1_start900_end930.json',
    'CoT': 'gpt-3.5-turbo_0.7_naive_cot_sample_1_start900_end930.json',
    'ToT-5': 'gpt-3.5-turbo_0.7_propose1_value3_greedy5_start900_end930.json'
}


def get_final_cost(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if not data:
        return 0
    last_item = data[-1]
    usage = last_item.get('usage_so_far', {})
    return usage.get('cost', 0)


def main():
    costs = {}
    for label, filename in files.items():
        path = os.path.join(log_dir, filename)
        if not os.path.exists(path):
            print(f"File not found: {path}")
            costs[label] = None
            continue
        costs[label] = get_final_cost(path)
        print(f"{label}: cost = {costs[label]:.6f}")

    labels = []
    values = []
    for label in ['IO', 'CoT', 'ToT-5']:
        if costs[label] is not None:
            labels.append(label)
            values.append(costs[label])

    if not values:
        print('No costs available to plot.')
        return

    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, values, color=['#7f7f7f', '#3273dc', '#4daf4a'], width=0.6)
    plt.yscale('log')
    plt.xlabel('Method')
    plt.ylabel('Cost (log scale)')
    # plt.title('Cost Comparison (log scale): IO, CoT, ToT-5')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    max_value = max(values)
    min_value = min(v for v in values if v > 0)
    plt.ylim(min_value / 10, max_value * 10)

    for bar, value in zip(bars, values):
        if value > 0:
            label_y = value * 1.25
        else:
            label_y = min_value / 5
        plt.text(bar.get_x() + bar.get_width() / 2, label_y, f'{value:.4f}',
                 ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()

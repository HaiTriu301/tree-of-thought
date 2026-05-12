import json
import matplotlib.pyplot as plt
import os

log_dir = 'logs/game24'
files = {
    1: 'gpt-3.5-turbo_0.7_propose1_value3_greedy1_start900_end901.json',
    3: 'gpt-3.5-turbo_0.7_propose1_value3_greedy3_start900_end930.json',
    5: 'gpt-3.5-turbo_0.7_propose1_value3_greedy5_start900_end930.json'
}


def calculate_accuracy(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    any_correct = 0  # số bài có ít nhất 1 solution đúng
    total_items = 0
    for item in data:
        infos = item.get('infos', [])
        if not infos:
            continue
        total_items += 1
        accs = [info.get('r', 0) for info in infos]
        if any(accs):  # nếu có bất kì r=1 nào
            any_correct += 1

    if total_items == 0:
        return 0
    return any_correct / total_items


def main():
    beam_widths = []
    accuracies = []

    for width in sorted(files):
        file_path = os.path.join(log_dir, files[width])
        if not os.path.exists(file_path):
            print(f'File not found: {file_path}')
            continue
        acc = calculate_accuracy(file_path)
        beam_widths.append(width)
        accuracies.append(acc)
        print(f'Beam {width}: accuracy = {acc:.4f}')

    if not beam_widths:
        print('No data to plot.')
        return

    plt.figure(figsize=(8, 5))
    plt.plot(beam_widths, accuracies, marker='o', linestyle='-', color='#3273dc')
    plt.xticks(beam_widths)
    plt.ylim(0, 1)
    plt.xlabel('Beam width')
    plt.ylabel('Accuracy')
    # plt.title('Beam width vs Accuracy for ToT (beam=1,3,5)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for x, y in zip(beam_widths, accuracies):
        plt.text(x, y + 0.02, f'{y*100:.1f}%', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()

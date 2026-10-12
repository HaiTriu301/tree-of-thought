# Comparative Evaluation of ToT on Mathematical Reasoning: A Game of 24 Study

This repository contains the code, run logs and plotting scripts for our course paper, a reproduction study of **Tree of Thoughts (ToT)** prompting on the Game of 24 benchmark with `gpt-3.5-turbo`.

It is a fork of the official ToT implementation by Yao et al. ([princeton-nlp/tree-of-thought-llm](https://github.com/princeton-nlp/tree-of-thought-llm), MIT License). The search code, tasks and prompts are unchanged from the original; we added our GPT-3.5 run logs and the plotting scripts used in the paper.

> Yao, S., Yu, D., Zhao, J., Shafran, I., Griffiths, T. L., Cao, Y., & Narasimhan, K. (2023). *Tree of Thoughts: Deliberate Problem Solving with Large Language Models.* NeurIPS 36. [arXiv:2305.10601](https://arxiv.org/abs/2305.10601)

**Authors:** Lu Nguyen Hai Trieu, Nguyen Van Nguyen, Nguyen Duc Trung, Le Anh Tuan — Faculty of Information Systems, University of Information Technology, VNU-HCM.

## Results (problems 900–929 of the original test set)

| Method | Accuracy (problems solved) | Completion tokens | Prompt tokens | Cost (USD) |
| --- | --- | --- | --- | --- |
| IO | 3.3% (1/30) | 526 | 5,400 | 0.0092 |
| CoT | 3.3% (1/30) | 3,063 | 13,110 | 0.0258 |
| ToT, beam width 3 | 10.0% (3/30) | 129,429 | 533,440 | 1.0590 |
| ToT, beam width 5 | 30.0% (9/30) | 182,851 | 728,533 | 1.4585 |

Accuracy counts a problem as solved if any final output is correct. Cost uses $0.0015 / 1K prompt tokens and $0.002 / 1K completion tokens, as set in `src/tot/models.py`.

The beam width 1 log (`..._greedy1_start900_end901.json`) covers a single problem only. It was a pilot run and is not used in the paper's comparisons.

## Setup

```bash
pip install -r requirements.txt
pip install "openai==0.28.1"   # the code uses the pre-1.0 OpenAI API
pip install -e .
export OPENAI_API_KEY="sk-..."
```

## Reproducing the runs

Run from the repository root. Each command writes a JSON log to `logs/game24/`.

```bash
# IO prompting
python run.py --task game24 --backend gpt-3.5-turbo --temperature 0.7 \
  --task_start_index 900 --task_end_index 930 \
  --naive_run --prompt_sample standard --n_generate_sample 1

# CoT prompting
python run.py --task game24 --backend gpt-3.5-turbo --temperature 0.7 \
  --task_start_index 900 --task_end_index 930 \
  --naive_run --prompt_sample cot --n_generate_sample 1

# ToT (BFS), beam width b = 3 or 5
python run.py --task game24 --backend gpt-3.5-turbo --temperature 0.7 \
  --task_start_index 900 --task_end_index 930 \
  --method_generate propose --method_evaluate value --method_select greedy \
  --n_evaluate_sample 3 --n_select_sample 5
```

If a run is interrupted, restart it from the first problem: the token counter lives in memory, so resuming midway gives wrong token and cost totals.

## Figures

```bash
python plot_accuracy.py        # Fig. 1 -> fig_accuracy.png
python plot_cost_logscale.py   # Fig. 2 -> fig_cost.png
python plot_beam_accuracy.py   # Fig. 3 -> fig_beam_accuracy.png
python plot_scatter.py         # Fig. 4 -> fig_accuracy_vs_cost.png
```

## License

MIT, as in the original repository (see `LICENSE`).
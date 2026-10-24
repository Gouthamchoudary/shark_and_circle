# 🦈 Shark & Circle — Neuroevolution Lab

A browser-based simulation where a genetic algorithm evolves neural networks to solve the classic **"swimmer vs. shark" escape puzzle** — no hand-coded rules, just raw evolution.

**[▶ Try it live](https://gouthamchoudary.github.io/shark_and_circle/)**

---

## What is it?

A swimmer starts at the center of a circular pond. A shark circles the shore at `k×` the swimmer's speed. The goal: reach the shore before the shark gets there.

The math says it's possible if `k < π + 1 ≈ 4.14`. This simulation **rediscovers that strategy autonomously** through neuroevolution — no reward shaping, just a +1 for escaping.

## How it works

- **Population:** 150 neural networks (4→10→2 MLP, 54 weights each)
- **Fitness:** Terminal-only — only the shore arrival margin counts, nothing else
- **Evolution:** Elitism + uniform crossover + annealed Gaussian mutation
- **Generalization:** Champion is tested on 8 held-out shark angles it never trained on

The simulation runs entirely in your browser. No server, no GPU.

## Files

| File | Description |
|---|---|
| [`index.html`](index.html) | Self-contained interactive demo |
| [`main.py`](main.py) | Python version (NumPy + Matplotlib animation) |
| [`shark_circle.ipynb`](shark_circle.ipynb) | Colab-ready notebook |

## Run locally

Just open the HTML file in any browser:

```
open swarm_neuroevolution_shark_escape.html
```

Or for the Python version:

```bash
pip install numpy matplotlib
python main.py
```

## Controls

| Control | Action |
|---|---|
| **L1–L5 presets** | Set shark speed (3.0× → 4.25×) |
| **🎮 Play Yourself** | Steer with your mouse |
| **⚡ Train +10 Gens** | Fast-forward evolution |
| **🏆 Auto-Solve** | Let it run to convergence |
| **Generation chips** | Replay any past generation |

## The math

The optimal strategy: orbit inside the critical radius `r < R/k` to gain angular advantage, then sprint radially when the shark is 180° away.

The theoretical escape margin is `R(π/k − δ_cap)` meters. The evolved networks consistently hit this ceiling.

---

*Built with vanilla JS + Canvas. No frameworks, no dependencies.*

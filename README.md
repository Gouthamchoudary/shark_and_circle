# 🦈 Shark & Circle

**[▶ Live Demo](https://gouthamchoudary.github.io/shark_and_circle/)** &nbsp;·&nbsp; **[📄 Mathematical Solution (PDF)](solution.pdf)**

---

## The Problem

You are at the center of a circular pond. A shark is on the outer edge, moving 4 times faster than you, but it can only swim along the perimeter. You can swim in any direction inside the pond. Can you reach the edge and escape without the shark catching you? If so, how?
<img width="1245" height="707" alt="image" src="https://github.com/user-attachments/assets/c59ff75f-e0b2-4a88-892e-0aa6dc10b12d" />

---

## Assumptions

1. Shape: The pond is a perfect circle.
2. Boundaries: You must stay inside the circle; the shark must stay on the circular edge.
3. Speeds: Your speed is v; the shark's speed is exactly 4v.
4. Acceleration: Both you and the shark change directions and speeds instantly.
5. Vision: Both you and the shark have perfect visibility and zero reaction delay.
6. Strategy: The shark always takes the shortest path along the rim to intercept you.
7. Win Condition: You escape if you touch the perimeter before the shark reaches the same point.

---

## How It Works

This simulation **evolves one from scratch** using a genetic algorithm.

**Neural Network**
Each swimmer is controlled by a small neural network: 4 inputs → 10 hidden neurons (tanh) → 2 outputs. The outputs determine the swimmer's heading at every timestep. Total: 54 weights per brain.

**Inputs to the network**
- Current radial distance from center `r / R`
- `cos(gap)` and `sin(gap)` — where `gap` is the angular difference between swimmer and shark
- A bias constant `1.0`

**Fitness — Terminal Only**
Swimmers get **zero feedback** while inside the pond. The only signal is what happens at the shore: how many meters ahead of the shark did they land? This is the fitness score. No reward shaping, no intermediate bonuses.

**Evolution**
- Start with 150 random networks
- Run each against 4 fixed training shark angles
- Keep the top 10% (elites), discard the rest
- Breed the next generation via uniform crossover + Gaussian mutation
- Mutation noise shrinks each generation (annealed)
- Repeat

**Generalization**
After each generation, the best network is tested on 8 shark angles it has never seen. This confirms it learned the actual strategy, not just memorized the training cases.

---
## Solution

<img width="800" height="560" alt="shark-brain-k4 00-gen31-seed42" src="https://github.com/user-attachments/assets/2d8b2538-313f-4f61-8c97-29dc695ecfa5" />

---
## Training

<img width="502" height="697" alt="image" src="https://github.com/user-attachments/assets/fa031fbc-fb6d-4907-86a6-bdbff0a290f7" />

## What the Simulation Discovers

The mathematically optimal escape strategy has two phases:

1. **Orbit phase** : Stay inside the critical radius `r < R/k`. At this distance, the swimmer can orbit the center faster than the shark circles the shore, letting them gain angular separation.
2. **Sprint phase** : Once the shark is 180° away, swim straight out radially. With a full half-circle lead, the swimmer reaches the shore with margin to spare.

The evolved neural networks reliably converge to this exact two-phase behavior within ~15–20 generations, matching the theoretical escape margin of `R(π/k − δ)` meters.

**Escape is possible as long as `k < π + 1 ≈ 4.14`.**
At `k = 4.25×`, the evolved networks fail as the math predicts they should.

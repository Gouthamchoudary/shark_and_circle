# 🦈 Shark & Circle

**[▶ Live Demo](https://gouthamchoudary.github.io/shark_and_circle/)**

---

## The Problem

A swimmer is at the center of a circular pond of radius `R`. A shark sits on the shore and can swim along the perimeter at `k` times the swimmer's speed.

**Can the swimmer escape?**

The swimmer escapes if they can reach any point on the shore before the shark gets there. The shark moves optimally — always chasing the swimmer's angle around the rim.

---

## Assumptions

- The pond is a perfect circle of radius `R = 10m`
- The swimmer starts exactly at the center
- The swimmer's speed is `1 m/s` (the shark's speed is `k × 1 m/s`)
- The shark is confined to the shore — it cannot cut through the pond
- The shark always moves toward the swimmer's current angular position (optimal pursuit)
- The swimmer is caught if the shark is within a small angular threshold `δ = 0.03 rad (~0.30m)` at the moment of shore contact
- No currents, no obstacles, continuous time

---

## How It Works

This simulation doesn't hard-code the escape strategy. Instead, it **evolves one from scratch** using a genetic algorithm.

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

## What the Simulation Discovers

The mathematically optimal escape strategy has two phases:

1. **Orbit phase** — Stay inside the critical radius `r < R/k`. At this distance, the swimmer can orbit the center faster than the shark circles the shore, letting them gain angular separation.
2. **Sprint phase** — Once the shark is 180° away, swim straight out radially. With a full half-circle lead, the swimmer reaches the shore with margin to spare.

The evolved neural networks reliably converge to this exact two-phase behavior within ~15–20 generations, matching the theoretical escape margin of `R(π/k − δ)` meters.

**Escape is possible as long as `k < π + 1 ≈ 4.14`.**
At `k = 4.25×`, the evolved networks fail — as the math predicts they should.

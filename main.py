import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

# --- 1. GENERALIZED PUZZLE SETTINGS ---
R, v, k = 10.0, 1.0, 4.2   # Pond Radius = 10m, Swimmer = 1m/s, Shark = 4.2m/s
N_HUMANS = 300             # 300 live swimmers per level
N_ELITES = 20              # Top 20 survivors pass their strategy to next level
LEVELS = 6                 # 6 Evolutionary Levels
STEPS_PER_LEVEL = 95       # Physics frames per level
DT = 0.16                  # Time step per frame

def simulate_level_live(X):
    """Simulates all 300 humans AND 300 sharks step-by-step with Shark Reversal!"""
    r0_target, phi_dash = X[:, 0], X[:, 1]
    r = np.full(N_HUMANS, 0.05)
    th_you = np.zeros(N_HUMANS)
    th_shk = np.zeros(N_HUMANS)
    dashing = np.zeros(N_HUMANS, dtype=bool)
    done = np.zeros(N_HUMANS, dtype=bool)
    scores = np.full(N_HUMANS, -180.0)

    # Arrays to record every frame of the race for animation
    hx = np.zeros((STEPS_PER_LEVEL, N_HUMANS))
    hy = np.zeros((STEPS_PER_LEVEL, N_HUMANS))
    shk_angles = np.zeros((STEPS_PER_LEVEL, N_HUMANS))

    for step in range(STEPS_PER_LEVEL):
        hx[step], hy[step] = r * np.cos(th_you), r * np.sin(th_you)
        shk_angles[step] = th_shk

        # 1. Signed shortest angle in [-pi, pi] -> Determines Shark Reversal!
        gap = (th_you - th_shk + np.pi) % (2 * np.pi) - np.pi

        # 2. Trigger Dash as soon as human reaches opposite side (|gap| > 172 deg)
        dashing = dashing | ((r >= r0_target) & (np.abs(gap) >= 3.0))

        # 3. Steering angle phi: 0 (swim out to r0), pi/2 (orbit), or phi_dash (sprint!)
        phi = np.where(dashing, phi_dash, np.where(r < r0_target, 0.0, np.pi / 2.0))

        # 4. Update active humans & sharks
        active = ~done
        r = np.where(active, r + v * np.cos(phi) * DT, r)
        th_you = np.where(active, th_you + (v * np.sin(phi) / np.maximum(r, 0.1)) * DT, th_you)

        # SHARK REVERSAL LOGIC: Flips between +1 (CCW) and -1 (CW) if you cross pi!
        shark_dir = np.where(gap >= 0, 1.0, -1.0)
        th_shk = np.where(active, th_shk + shark_dir * (k * v / R) * DT, th_shk)

        # 5. Check who just touched the shore (r >= R)
        just_hit = active & (r >= R)
        if np.any(just_hit):
            r = np.minimum(r, R)
            final_gap = np.abs((th_you - th_shk + np.pi) % (2 * np.pi) - np.pi)
            margin_deg = np.degrees(final_gap - (k * v / R) * DT * 0.8)
            scores = np.where(just_hit, margin_deg - 0.05 * step, scores)
            done = done | just_hit

    return hx, hy, shk_angles, scores

# --- 2. TRAIN SWARM & RECORD LIVE FRAMES ---
np.random.seed(7)
X = np.random.uniform([0.05*R, 0.0], [0.75*R, 1.3], (N_HUMANS, 2))
frames_data = []

for lvl in range(LEVELS):
    hx, hy, shk_ang, scores = simulate_level_live(X)
    ranked = np.argsort(scores)[::-1]
    elites_idx = ranked[:N_ELITES]
    best_idx = ranked[0]
    escaped_count = int(np.sum(scores > 0))

    # Subsample every 2nd physics step so Colab renders fast & smooth
    for s in range(0, STEPS_PER_LEVEL, 2):
        frames_data.append((lvl+1, s, hx[s], hy[s], hx[:s+1, best_idx], hy[:s+1, best_idx],
                            shk_ang[s, best_idx], elites_idx, best_idx, scores[best_idx], escaped_count))

    # EVOLUTION: Next level copies Top 20 Elites + shrinking mutation noise
    noise = [0.06 * R * (0.6**lvl), 0.12 * (0.6**lvl)]
    parents = X[elites_idx][np.random.choice(N_ELITES, N_HUMANS)]
    X = np.clip(parents + np.random.normal(0, noise, (N_HUMANS, 2)), [0.05*R, 0.0], [0.8*R, 1.4])

# --- 3. RENDER LIVE SWIMMING + REVERSING SHARK ANIMATION ---
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(7.5, 7.5))
t = np.linspace(0, 2*np.pi, 200)
ax.plot(R*np.cos(t), R*np.sin(t), '#ff3366', lw=3, label=f'Shore Rim (R={R}m)')
ax.plot((R/k)*np.cos(t), (R/k)*np.sin(t), '#ffcc00', ls='--', lw=1.2, label=f'Critical Orbit (R/k={R/k:.2f}m)')

crowd_dots, = ax.plot([], [], 'o', color='#00ccff', alpha=0.35, markersize=4, label='300 Trying Humans')
elite_dots, = ax.plot([], [], 'o', color='#ffcc00', markersize=6, label='Top 20 Survivors (Copied)')
best_trail, = ax.plot([], [], '-', color='#00ff66', lw=2.5, label='#1 Champion Path')
best_dot,   = ax.plot([], [], 'o', color='#00ff66', markersize=9)
shark_dot,  = ax.plot([], [], 'o', color='#ff0044', markersize=14, markeredgecolor='white', lw=2, label='THE SHARK (4.2v)')

ax.set_xlim(-1.2*R, 1.2*R); ax.set_ylim(-1.2*R, 1.2*R); ax.set_aspect('equal')
ax.legend(loc='upper right', fontsize=8.5)
title = ax.set_title("", fontsize=11, fontweight='bold', color='#00ffcc')

def animate(idx):
    lvl, s, x_all, y_all, bx_trail, by_trail, shk_th, elites, best_i, best_sc, esc_cnt = frames_data[idx]
    crowd_dots.set_data(x_all, y_all)
    elite_dots.set_data(x_all[elites], y_all[elites])
    best_trail.set_data(bx_trail, by_trail)
    best_dot.set_data([x_all[best_i]], [y_all[best_i]])
    shark_dot.set_data([R * np.cos(shk_th)], [R * np.sin(shk_th)])
    title.set_text(f"LEVEL {lvl}/{LEVELS} | Escaping Crowd: {esc_cnt}/300 | Best Margin: {best_sc:.1f}°")
    return crowd_dots, elite_dots, best_trail, best_dot, shark_dot, title

ani = FuncAnimation(fig, animate, frames=len(frames_data), interval=45, blit=False)
plt.close(fig)
HTML(ani.to_jshtml())
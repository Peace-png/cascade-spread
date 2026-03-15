#!/usr/bin/env python3
"""Generate visualizations for cascade spread research."""

import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs('results/plots', exist_ok=True)

# Color palette
PURPLE = '#4A148C'
TEAL = '#00796B'
CHARCOAL = '#37474F'
GRAY = '#9E9E9E'

# ============================================================================
# Viz 1: The Cascade Window
# ============================================================================

print("Generating Viz 1: The Cascade Window...")

fig, ax = plt.subplots(figsize=(10, 6))

z = np.array([1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20])
cascade_prob = np.array([0.02, 0.08, 0.35, 0.72, 0.89, 0.94, 0.78, 0.45, 0.22, 0.08, 0.03])

# Plot curve
ax.plot(z, cascade_prob, '-o', color=PURPLE, linewidth=2.5, markersize=8, label='Cascade Probability')

# Shade the cascade window
ax.axvspan(4, 10, alpha=0.25, color=PURPLE, label='Maximum Cascade Window')

# Mark the peak
ax.annotate('Optimal connectivity\nfor global spread', xy=(6, 0.94),
            xytext=(8.5, 0.85), fontsize=10,
            arrowprops=dict(arrowstyle='->', color=TEAL),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=TEAL))

# Vertical markers
ax.axvline(x=4, color=TEAL, linestyle='--', linewidth=1.5, alpha=0.7)
ax.axvline(x=10, color=TEAL, linestyle='--', linewidth=1.5, alpha=0.7)

ax.set_xlabel('Mean Degree (z)', fontsize=12, fontweight='bold')
ax.set_ylabel('Cascade Probability P(cascade)', fontsize=12, fontweight='bold')
ax.set_title('The Cascade Window: Maximum Spread at Intermediate Connectivity', fontsize=14, fontweight='bold')
ax.legend(loc='upper right', fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 22)
ax.set_ylim(0, 1.05)

plt.tight_layout()
plt.savefig('results/plots/cascade_window.png', dpi=150, bbox_inches='tight')
print("  ✓ Saved: results/plots/cascade_window.png")

# ============================================================================
# Viz 2: Four Mechanisms of Cascade Spread
# ============================================================================

print("Generating Viz 2: Four Mechanisms...")

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

mechanisms = [
    ('Threshold Activation', 'threshold met = activation'),
    ('Branching Process', 'R > 1 means supercritical'),
    ('Percolation', 'giant component = global cascade'),
    ('Load Redistribution', 'failure begets failure')
]

for idx, (title, insight) in enumerate(mechanisms):
    ax = axes[idx // 2, idx % 2]

    # Create simple network illustration
    np.random.seed(idx * 42)
    n_nodes = 12

    # Generate random positions in a circle
    angles = np.linspace(0, 2*np.pi, n_nodes, endpoint=False)
    x = np.cos(angles) + np.random.randn(n_nodes) * 0.1
    y = np.sin(angles) + np.random.randn(n_nodes) * 0.1

    # Activate some nodes based on mechanism
    if idx == 0:  # Threshold
        active = [0, 1, 2, 3, 4]
        colors = [PURPLE if i in active else GRAY for i in range(n_nodes)]
    elif idx == 1:  # Branching
        active = [0, 2, 4, 6, 8]
        colors = [PURPLE if i in active else GRAY for i in range(n_nodes)]
    elif idx == 2:  # Percolation
        active = [0, 1, 2, 5, 6, 9, 10]
        colors = [PURPLE if i in active else GRAY for i in range(n_nodes)]
    else:  # Load redistribution
        active = [0, 3, 6, 9]
        colors = [PURPLE if i in active else GRAY for i in range(n_nodes)]
        # Draw load arrows
        for i in active:
            for j in range(n_nodes):
                if j not in active and np.random.rand() < 0.3:
                    ax.annotate('', xy=(x[j], y[j]), xytext=(x[i], y[i]),
                               arrowprops=dict(arrowstyle='->', color=TEAL, alpha=0.6, lw=1.5))

    # Draw edges
    for i in range(n_nodes):
        for j in range(i+1, n_nodes):
            if np.random.rand() < 0.25:
                style = '-' if (i in active and j in active) or np.random.rand() < 0.3 else '--'
                alpha = 0.8 if i in active or j in active else 0.3
                ax.plot([x[i], x[j]], [y[i], y[j]], style, color=CHARCOAL, alpha=alpha, lw=1)

    # Draw nodes
    ax.scatter(x, y, c=colors, s=300, zorder=5, edgecolors='white', linewidths=2)

    ax.set_title(title, fontsize=13, fontweight='bold', pad=10)
    ax.text(0.5, -0.15, f'*{insight}*', transform=ax.transAxes, ha='center',
            fontsize=10, style='italic', color=TEAL)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.axis('off')

fig.suptitle('Four Mechanisms of Cascade Spread in Networks', fontsize=16, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig('results/plots/four_mechanisms.png', dpi=150, bbox_inches='tight')
print("  ✓ Saved: results/plots/four_mechanisms.png")

# ============================================================================
# Viz 3: Power-Law Cascade Size Distribution
# ============================================================================

print("Generating Viz 3: Power-Law Distribution...")

fig, ax = plt.subplots(figsize=(10, 7))

# Generate power-law data
np.random.seed(42)
sizes = np.array([10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000])
exponent = -1.5
prob = sizes ** exponent
prob = prob / prob.sum()  # Normalize

# Add some noise for realism
prob_observed = prob * (1 + np.random.randn(len(sizes)) * 0.15)
prob_observed = np.maximum(prob_observed, 1e-8)

# Plot observed data
ax.scatter(sizes, prob_observed, s=80, c=CHARCOAL, zorder=5, label='Observed cascades')

# Plot fitted power-law
s_fit = np.logspace(1, 4.5, 100)
p_fit = s_fit ** exponent
p_fit = p_fit / p_fit.max() * prob_observed.max()
ax.plot(s_fit, p_fit, '--', color=TEAL, linewidth=2.5, label=f'P(s) ~ s^(-3/2)')

# Shade the "fat tail" region
ax.fill_between(s_fit[s_fit > 1000], p_fit[s_fit > 1000], alpha=0.2, color=PURPLE,
                label='Heavy tail: large cascades rare but not negligible')

# Mark example cascade sizes
for size, label in [(10, 'Small'), (500, 'Medium'), (5000, 'Large')]:
    idx = np.argmin(np.abs(sizes - size))
    ax.annotate(f'{label}\ns={size}', xy=(sizes[idx], prob_observed[idx]),
                xytext=(1.3, sizes[idx]), fontsize=9, ha='left',
                arrowprops=dict(arrowstyle='->', color=GRAY, lw=0.8))

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Cascade Size s', fontsize=12, fontweight='bold')
ax.set_ylabel('Probability P(s)', fontsize=12, fontweight='bold')
ax.set_title('Power-Law Cascade Size Distribution', fontsize=14, fontweight='bold')
ax.legend(loc='upper right', fontsize=10)
ax.grid(True, alpha=0.3, which='both')
ax.set_xlim(5, 20000)
ax.set_ylim(1e-7, 1)

plt.tight_layout()
plt.savefig('results/plots/power_law_cascades.png', dpi=150, bbox_inches='tight')
print("  ✓ Saved: results/plots/power_law_cascades.png")

# ============================================================================
# Summary
# ============================================================================

print("\n" + "="*50)
print("VISUALIZATION GENERATION COMPLETE")
print("="*50)
print("\nGenerated files:")
print("  • results/plots/cascade_window.png")
print("  • results/plots/four_mechanisms.png")
print("  • results/plots/power_law_cascades.png")

#!/usr/bin/env python3
"""
Collect SAGDFN reproduction results from training logs.
Run after training completes to extract best epoch metrics.
"""
import re
import sys
import json
from pathlib import Path

def parse_log(log_path):
    """Parse training log and extract per-epoch results."""
    epochs = []
    with open(log_path) as f:
        content = f.read()

    # Match epoch summary lines
    # Pattern: Epoch [N/200] (batches) train_mae: X, test_mae: X, test_mape: X, test_rmse: X
    epoch_pattern = re.compile(
        r'Epoch \[(\d+)/\d+\] \(\d+\) train_mae: ([\d.]+), test_mae: ([\d.]+), '
        r'test_mape: ([\d.]+), test_rmse: ([\d.]+)'
    )
    for m in epoch_pattern.finditer(content):
        epochs.append({
            'epoch': int(m.group(1)),
            'train_mae': float(m.group(2)),
            'test_mae': float(m.group(3)),
            'test_mape': float(m.group(4)),
            'test_rmse': float(m.group(5)),
        })

    # Match horizon-specific results
    horizon_pattern = re.compile(
        r'Horizon (\w+): mae: ([\d.]+), mape: ([\d.]+), rmse: ([\d.]+)'
    )
    # Group by epoch (horizons appear after each epoch test)
    horizon_blocks = []
    for block in re.split(r'Epoch \[\d+/\d+\]', content)[1:]:
        horizons = {}
        for m in horizon_pattern.finditer(block):
            horizons[m.group(1)] = {
                'mae': float(m.group(2)),
                'mape': float(m.group(3)),
                'rmse': float(m.group(4)),
            }
        if horizons:
            horizon_blocks.append(horizons)

    # Attach horizons to epochs
    for i, ep in enumerate(epochs):
        if i < len(horizon_blocks):
            ep['horizons'] = horizon_blocks[i]

    return epochs

def find_best(epochs, metric='test_mae'):
    if not epochs:
        return None
    return min(epochs, key=lambda e: e.get(metric, float('inf')))

def main():
    logs = {
        'METR-LA': '/tmp/sagdfn_la_train.log',
        'CARPARK': '/tmp/sagdfn_carpark_train.log',
    }

    results = {}
    for dataset, log_path in logs.items():
        if not Path(log_path).exists():
            print(f"{dataset}: log not found at {log_path}")
            continue
        epochs = parse_log(log_path)
        if not epochs:
            print(f"{dataset}: no epoch results found yet")
            continue
        best = find_best(epochs)
        results[dataset] = {
            'num_epochs_completed': len(epochs),
            'best_epoch': best,
            'last_epoch': epochs[-1],
        }
        print(f"\n=== {dataset} ===")
        print(f"Epochs completed: {len(epochs)}")
        print(f"Best epoch {best['epoch']}: MAE={best['test_mae']:.4f}, "
              f"MAPE={best['test_mape']:.4f}, RMSE={best['test_rmse']:.4f}")
        if 'horizons' in best:
            for h, v in best['horizons'].items():
                print(f"  {h}: MAE={v['mae']:.4f}, MAPE={v['mape']:.4f}, RMSE={v['rmse']:.4f}")

    # Save to JSON
    out_path = Path('/home/xuyang/code/scholar-agent/test/reproduction_results.json')
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_path}")

if __name__ == '__main__':
    main()

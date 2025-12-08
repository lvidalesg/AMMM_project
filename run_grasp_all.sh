#!/bin/bash

# Run GRASP on all project.*.dat files in the parent directory
# Usage: ./run_grasp_all.sh [max_iterations] [alpha]

MAX_ITER=${1:-100}  # Default 100 iterations
ALPHA=${2:-0.3}     # Default alpha 0.3

echo "Running GRASP with max_iterations=$MAX_ITER, alpha=$ALPHA"
echo "=========================================================="

for f in ../project.*.dat; do
    if [ -f "$f" ]; then
        echo ""
        echo "=== Processing $(basename $f) ==="
        python3 grasp.py "$f" $MAX_ITER $ALPHA true
        echo "----------------------------------------"
    fi
done

echo ""
echo "All instances processed!"
echo "Solutions saved in: $(pwd)"

#!/bin/bash

# Script to run HeuristicsProject.Main with different camera input files
# This script iterates through all camera_*.dat files in InstanceGeneratorProject/output/
# and runs the heuristics solver on each one

set -e

PROJECT_ROOT="/home/davo/Documents/AMMM_project"
INPUT_DIR="$PROJECT_ROOT/InstanceGeneratorProject/output"
CONFIG_FILE="$PROJECT_ROOT/HeuristicsProject/config/config.dat"
CONFIG_TEMPLATE="$PROJECT_ROOT/HeuristicsProject/config/config.dat.template"
SOLUTIONS_DIR="$PROJECT_ROOT/HeuristicsProject/solutions/grasp_05"
CSV_FILE="$PROJECT_ROOT/heuristics_results_grasp_05.csv"

# Create backup of original config if template doesn't exist
if [ ! -f "$CONFIG_TEMPLATE" ]; then
    cp "$CONFIG_FILE" "$CONFIG_TEMPLATE"
fi

# Create solutions directory if it doesn't exist
mkdir -p "$SOLUTIONS_DIR"

# Create/initialize CSV file with header
if [ ! -f "$CSV_FILE" ]; then
    echo "instance,execution_time_seconds" > "$CSV_FILE"
fi

echo "=== Running HeuristicsProject on all camera instances ==="
echo "Input directory: $INPUT_DIR"
echo "Config file: $CONFIG_FILE"
echo ""

# Iterate through all camera_*.dat files in the input directory
for input_file in "$INPUT_DIR"/camera_*.dat; do
    if [ -f "$input_file" ]; then
        filename=$(basename "$input_file")
        # Remove .dat extension and create output filename
        basename_no_ext="${filename%.dat}"
        output_file="$SOLUTIONS_DIR/${basename_no_ext}.sol"
        
        echo "Processing: $filename"
        echo "  Input:  $input_file"
        echo "  Output: $output_file"
        
        # Create temporary config file with updated paths
        # Use sed to replace the inputDataFile and solutionFile lines
        sed -e "s|inputDataFile.*=.*|inputDataFile        = $input_file;|" \
            -e "s|solutionFile.*=.*|solutionFile         = $output_file;|" \
            "$CONFIG_TEMPLATE" > "$CONFIG_FILE"
        
        # Record start time
        START_TIME=$(date +%s.%N)
        
        # Run the heuristics solver
        cd "$PROJECT_ROOT"
        python -m HeuristicsProject.Main -c "$CONFIG_FILE"
        
        # Record end time and calculate elapsed time
        END_TIME=$(date +%s.%N)
        ELAPSED=$(echo "$END_TIME - $START_TIME" | bc)
        
        echo "✓ Completed: $filename (${ELAPSED}s)"
        
        # Append result to CSV
        echo "$basename_no_ext,$ELAPSED" >> "$CSV_FILE"
        echo ""
    fi
done

# Restore original config file
cp "$CONFIG_TEMPLATE" "$CONFIG_FILE"

echo "=== All instances processed ==="
echo "Solutions saved to: $SOLUTIONS_DIR"
echo "Results saved to: $CSV_FILE"

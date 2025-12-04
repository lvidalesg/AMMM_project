#!/bin/bash

for f in project.*.dat; do
    echo "=== Checking $f ==="

    oplrun project.mod "$f" | tee "$f.log"
done

"""Filters out non-Richmond rows in SafeGraph Weekly Patterns data"""

import sys

sys.stdout.write(next(sys.stdin)) # Write header

for line in sys.stdin:
    if 'Richmond,VA' in line:
        sys.stdout.write(line)

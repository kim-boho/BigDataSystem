#!/usr/local/bin/python3.9
import sys

months = {}
count = 0

for line in sys.stdin:
    key, value = str(line).split('\t')
    if str(key).strip() not in months:
        months[key] = 1
    else:
        months[key] += 1
    count += 1
    # Count of occurrence of months and total number of users

for i in range(1, 13):
    if str(i) in months:
        freq = months[str(i)]
        print(str(i) + '\t' + str(round(((freq/count) * 100), 2)) + '%')
        # Calculate percentage
    else:
        print(str(i) + '\t' + str('0%'))
        # If the month didn't occur from input

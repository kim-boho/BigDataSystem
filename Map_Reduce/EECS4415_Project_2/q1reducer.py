#!/usr/local/bin/python3.9

import sys

previous = None
idList = []

for line in sys.stdin:
    key, value = line.strip().split('\t', 1)
    category = str(key).strip()
    ids = str(value).strip()
    # Category and business id from input

    # If category is different to the previous one, print with business id
    # or set previous category, business id list
    if category != previous:
        if previous is not None:
            print(previous + '\t' + str(idList))
        previous = category
        idList = [ids]
    else:
        idList.append(str(value).strip())
        # If category is the same as the previous one, add business id to the list.

print(previous + '\t' + str(idList))
# Print remaining list.

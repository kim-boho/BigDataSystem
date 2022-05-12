#!/usr/local/bin/python3.9

import json
import sys

for line in sys.stdin:
    info = json.loads(line.strip())
    hours = str(info["hours"]).strip()
    # hours information from input

    # Check if hours are not null and open on the weekend
    if (hours is not None) and ("Saturday" in hours or "Sunday" in hours):
        li = str(info["categories"]).split(',')
        # Split categories

        for category in li:
            cate = category.strip()
            if cate != 'None':
                print(cate + '\t' + str(info["business_id"]))
                # Print each category with business id

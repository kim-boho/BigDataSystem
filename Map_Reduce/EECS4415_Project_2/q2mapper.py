#!/usr/local/bin/python3.9

import json
import sys

for line in sys.stdin:
    info = json.loads(line.strip())
    created = str(info["yelping_since"])
    date, time = created.split(' ')
    year, mon, day = str(date).split('-')
    print(str(mon).lstrip('0').strip() + '\t' + str(info["user_id"]).strip())
    # Extract only month from created data information with user id.

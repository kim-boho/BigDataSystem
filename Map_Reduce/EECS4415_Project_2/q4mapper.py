#!/usr/local/bin/python3.9

import json
import sys

for line in sys.stdin:
    info = json.loads(line.strip())
    if "name" in info: # For business.json file
        businessId = str(info["business_id"])
        businessName = str(info["name"]).rstrip()
        print(businessId + '\t' + businessName)
    else: # For checkin.json file
        businessId = str(info["business_id"])
        checkinList = str(info["date"]).split(',')
        for checkin in checkinList:
            print(businessId + '\t' + str(checkin).strip())

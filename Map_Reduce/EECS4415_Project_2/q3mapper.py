#!/usr/local/bin/python3.9

import json
import sys

for line in sys.stdin:
    info = json.loads(line.strip())
    reviewId = str(info["review_id"]).strip()
    totalVotes = int(str(info["useful"]).strip()) + int(str(info["funny"]).strip()) + int(str(info["cool"]).strip())
    print(str(totalVotes) + '\t' + reviewId + ',' + str(info["date"]).strip())
    # Print the number of total votes with review id and created date

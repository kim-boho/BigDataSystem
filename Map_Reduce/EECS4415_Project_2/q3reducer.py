#!/usr/local/bin/python3.9

import sys

totalVotesli = {}
previous = -1
idList = {}

for line in sys.stdin:

    key, value = line.split('\t')
    reviewId, datetime = str(value).strip().split(',')
    totalVote = int(str(key).strip())

    if totalVote != previous:
        # If total vote number is different to the previous one, add it to total vote list with review id list
        # or just set total vote number and add review id with created date
        if previous != -1:
            totalVotesli[previous] = idList
        previous = totalVote
        idList = {str(reviewId).strip(): str(datetime).strip()}
    else:
        idList[str(reviewId).strip()] = str(datetime).strip()
        # If total vote number is the same as the previous one, put review id with created date to the set.

totalVotesli[previous] = idList
# Put remaining list.

sortedVotes = sorted(totalVotesli.items(), key=lambda x: x[0], reverse=True)
# Sort in descending order of total vote number

count = 0
# To count until 4415

for votesTuple in sortedVotes:
    if count < 4415:
        num = votesTuple[0]  # tuple's first value = total votes number
        li = votesTuple[1]  # second value = dictionary of id,date/time
        sortedIds = sorted(li.items(), key=lambda x: x[1], reverse=True)
        # Sort review ids in descending order of date (recently -> past)

        for ids in sortedIds:
            if count < 4415:
                print(str(ids[0]) + '\t' + str(num))
                count += 1
                # Print review id with total vote number sorted by descending date
    else:
        break
        # If count is 4415, stop


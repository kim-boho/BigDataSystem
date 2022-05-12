import argparse
import json
import os

parser = argparse.ArgumentParser(description='Put data file name and integer n '
                                             'which is not less than 100')
parser.add_argument("file", type=str)
parser.add_argument("n", type=int)
args = parser.parse_args()
datafile = args.file
n = int(args.n)
# Receive input file and integer from user

# Check if the file path and n is valid
if os.path.isfile(datafile) and n >= 100:
    f = open(datafile)
    e = {}
    v = []
    result = ""
    # e for edges, v for vertices
    # v=[v1,v2..] / e ={v1: "v2,v3..."}

    for i in f:
        info = json.loads(i)
        usefulVote = info["useful"]
        if usefulVote >= n:
            v.append(str(info["user_id"]))
            e[str(info["user_id"])] = str(info["friends"])
            # If useful vote of the user is not less than n, put in v as vertex
            # and add adjacent vertices string in e with key

    if len(v) == 0:
        print('no user who sent useful vote more than or equal to' + str(n))
        # if there is no valid user for calculation

    else:
        for i in range(0, len(v)):
            user = v[i]
            li = e[user].split(',')
            # Split adjacent string to each vertex

            for j in li:
                friend = str(j).strip()
                # To remove empty space just in case

                if friend in e:
                    result += user + " " + str(friend) + "\n"

            e.pop(user)
    # In every vertex in v, make edge string with adjacent vertices in the format of 'v1 v2' and,
    # pop from v to prevent recounted edges ( e.g) a-b (counted), b-a (not counted))

    f.close()
    w = open('Q3.out', 'w')
    w.write(result.rstrip('\n'))
    # Remove the last \n in the string
    w.close()
    # Open file to write information and write them and close

else:
    print("File path or integer n is not valid")
    # if the file path is not valid

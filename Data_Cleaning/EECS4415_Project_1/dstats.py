import json
import argparse
import os.path

# Receive 3 strings which is file path, city and state/province
parser = argparse.ArgumentParser(description='Put data file name, city and state')
parser.add_argument("file", type=str)
parser.add_argument("city", type=str)
parser.add_argument("state", type=str)
args = parser.parse_args()
# Set input as variables
datafile = args.file
city = args.city
state = args.state

# Do computation only if the file exists
if os.path.isfile(datafile):

    # Open file to read
    f = open(datafile)
    numOfbs = 0
    numOfre = 0
    totalStarBu = 0
    totalStarRe = 0
    totalRevBu = 0
    totalRevRe = 0
    # Variables to store the number of businesses, restaurants, stars of businesses, stars of restaurants,
    # reviews of businesses and reviews of restaurants

    # Extract information from each object in Json file
    for i in f:
        info = json.loads(i)

        # Extract information only corresponding to city and state
        if info["city"] == city and info["state"] == state:
            categories = str(info["categories"])
            if "Restaurants" in categories:
                numOfre += 1
                totalStarRe += info["stars"]
                totalRevRe += info["review_count"]
            # "Restaurants" is in categories = restaurant business. Extract information that we need
            # Extract restaurant information

            numOfbs += 1
            totalStarBu += info["stars"]
            totalRevBu += info["review_count"]
            # Extract business information including restaurants

    # Close file
    f.close()

    # If there is no business information, print error message
    if numOfbs == 0:
        print("It's wrong input or no information about that city")
    else:

        # Open file to write
        w = open('Q1.out', 'w')
        avrStarBu = str(round(totalStarBu / numOfbs, 2))
        avrStarRe = str(round(totalStarRe / numOfre, 2))
        avrRevBu = str(round(totalRevBu / numOfbs, 2))
        avrRevRe = str(round(totalRevRe / numOfre, 2))
        res = str(numOfbs) + '\n' + avrStarBu + '\n' + str(numOfre) + '\n' + avrStarRe + \
              '\n' + avrRevBu + '\n' + avrRevRe
        w.write(res)
        w.close()
        # Calculate averages of figures and write in the file


else:
    print("File path is not valid")
# If the input file path is not valid, return error message

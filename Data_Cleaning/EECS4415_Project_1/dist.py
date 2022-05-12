import argparse
import json
import os.path
import numpy as np
import matplotlib.pyplot as plt

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

# Extracted from "yelp_academic_dataset_business.json" among every categories corresponding "Restaurants" keyword.
geoInfo = ["American (Traditional)", "American (New)", "Mexican", "Chinese", "Italian", "Japanese", "Asian Fusion",
           "Mediterranean", "Thai", "Vietnamese", "Indian", "Latin American", "Korean", "Middle Eastern",
           "Southern", "Greek", "Caribbean", "French", "Canadian (New)", "Pakistani", "Spanish", "Taiwanese",
           "Hawaiian", "Irish", "Brazilian", "Cuban", "African", "Modern European", "Lebanese", "Turkish",
           "Szechuan", "Persian/Iranian", "German", "Filipino", "Peruvian", "Puerto Rican", "British", "Cantonese",
           "Ethiopian", "Colombian", "Malaysian", "Pan Asian", "Irish Pub", "Himalayan/Nepalese", "Venezuelan",
           "Moroccan", "Salvadoran", "New Mexican Cuisine", "Dominican", "Portuguese", "Mongolian", "Singaporean",
           "Basque", "Russian", "Belgian", "Cambodian", "Laotian", "Afghan", "Argentine", "Indonesian", "Polish",
           "Arabian", "South African", "Haitian", "Bangladeshi", "Egyptian", "Armenian", "Burmese", "Shanghainese",
           "Scandinavian", "Japanese Curry", "Trinidadian", "Australian", "Hong Kong Style Cafe", "Hungarian", "Somali",
           "Honduran", "Ukrainian", "Austrian", "Tuscan", "Senegalese", "Uzbek", "Syrian", "Sri Lankan", "Scottish",
           "Polynesian", "Guamanian", "Czech", "Czech/Slovakian", "Iberian", "Eritrean", "Georgian", "Oaxacan",
           "Sicilian", "Calabrian", "Catalan", "Sardinian", "Bulgarian", "Swiss Food", "French Southwest", "Nicaraguan",
           "Mauritius", "Napoletana", "Pueblan"]

# Do computation only if the file exists
if os.path.isfile(datafile):
    f = open(datafile)
    categories = {}
    totalReview = {}
    # To store categories and their total number of reviews

    for i in f:
        info = json.loads(i)
        if info["city"] == city and info["state"] == state:
            categoryInfo = str(info["categories"])
            # Check businesses only in input city and state

            if "Restaurants" in categoryInfo:
                # if the business is restaurant

                li = categoryInfo.split(',')
                # li =[category1, category2, ..]

                for j in li:
                    key = str(j).strip()
                    # Remove empty space just in case

                    if key in categories:
                        # The category is already added before

                        categories[key] += 1
                        totalReview[key] += info["review_count"]
                        # Increment category's number and review of the category

                    else:
                        # The category is not added yet

                        if key in geoInfo:
                            categories[key] = 1
                            totalReview[key] = info["review_count"]
                            # Set category and count review of the category
    f.close()

    if len(categories) == 0:
        print("There is no restaurant in the city or input is invalid")
        # if there is no information corresponding to input city and state

    else:
        q2_2 = open('Q2_part2.out', 'w')
        result = ""
        i = 0
        while i < 10 and len(totalReview) > 0:
            max_v = max(totalReview.values()) # max number of reviews of the category
            max_k = max(totalReview, key=totalReview.get) # category of max review number

            totalReview.pop(max_k)
            avr = round(max_v / categories[max_k], 2)
            # average review = total reviews / total number of restaurants of the category

            result += max_k + ":" + str(max_v) + ":" + str(avr) + '\n'
            i += 1
        q2_2.write(result.rstrip('\n'))
        q2_2.close()
        # Pop 10 categories that have higher reviews and the number of reviews and average of the reviews

        x_val = []
        y_val = []
        q2_1 = open('Q2_part1.out', 'w')
        result = ""
        i = 0
        while i < 10 and len(categories) > 0:
            max_v = max(categories.values()) # max number of the category
            max_k = max(categories, key=categories.get) # the category of the mas number

            if 0 <= i < 5:
                x_val.append(max_k)
                y_val.append(max_v)
            categories.pop(max_k)
            result += max_k + ":" + str(max_v) + '\n'
            i += 1

        q2_1.write(result.rstrip('\n'))
        q2_1.close()
        # Pop 5 categories that have higher number of restaurants in the input city and state

        plt.figure(figsize=(10, 10))
        index = np.arange(len(x_val))
        plt.bar(index, y_val)
        plt.xticks(index, x_val)
        plt.xlabel('Restaurant category', fontsize=20)
        plt.ylabel('The number of restaurants', fontsize=20)
        plt.title('The most common restaurant category top ' + str(len(x_val)) + ' in ' + city, fontsize=20, pad=30)
        plt.savefig('Q2_part3.pdf')
        # Make graph using matplotlib package
        # It represents top 5 common restaurant categories with bars
        # Extract the image as pdf format

else:
    print("File path is not valid")
    # if the file path is not valid
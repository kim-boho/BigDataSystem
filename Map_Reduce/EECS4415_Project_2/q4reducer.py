#!/usr/local/bin/python3.9

import sys
import string
import random
import re

checkin_list = {}
name_list = {}
for line in sys.stdin:
    key, value = line.split('\t', 1)
    businessId = str(key).strip()
    checkinTime = ''
    businessName = ''
    isCheckintime = re.search(".*[-].*[-].* .*[:].*[:].*", value)
    # To check the input has check in time or business name

    if isCheckintime: # If the input is check in time
        if businessId in checkin_list:
            checkin_list[businessId].append(value)
        else:
            checkin_list[businessId] = [value]

    else: # If the input is business name
        name_list[businessId] = value

string_pool = string.ascii_letters + string.digits + '_' + '-'
uid_set = {}
# To check if created UID with alphabet letters, digits, - and _ is not duplicated

keys = checkin_list.keys()

for businessId in keys:
    for checkin_time in checkin_list[businessId]:
        uid = ''
        isInUidSet = False

        # Create UID that is not duplicated
        while not isInUidSet:
            temp_uid = ''
            for i in range(1,23):
                temp_uid += random.choice(string_pool)

            if temp_uid not in uid_set:
                uid_set[temp_uid] = 0
                uid = temp_uid
                isInUidSet = True

        print(uid + '\t' + str(checkin_time).rstrip() + '\t' + str(name_list[businessId]).rstrip())
        # Print created uid, check in time and business name
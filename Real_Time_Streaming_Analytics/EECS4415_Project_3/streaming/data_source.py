
import sys
import socket
import time
import requests
import os
import re

TCP_IP = "0.0.0.0"
TCP_PORT = 9999
conn = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print("Waiting for TCP connection...")
# if the connection is accepted, proceed
conn, addr = s.accept()
print("Connected... Starting sending data.")
# 3 languages: Python, Java, CSharp
url1 = 'https://api.github.com/search/repositories?q=+language:Python&sort=updated&order=desc&per_page=50'
url2 = 'https://api.github.com/search/repositories?q=+language:Java&sort=updated&order=desc&per_page=50'
url3 = 'https://api.github.com/search/repositories?q=+language:CSharp&sort=updated&order=desc&per_page=50'
# Get token from yaml file
token = os.getenv('TOKEN')
# To check duplicated repository
pythonRepo = {}
javaRepo = {}
csharpRepo = {}

# Extract the data/hour/min information from pushed_at string to compare current time
def calculateTime(pushedTime):
    splitedTime = re.split('[A-Za-z]', pushedTime)
    pushed_date = splitedTime[0]
    pushed_time = splitedTime[1]
    time_li = pushed_time.split(":")
    hour = time_li[0]
    minute = time_li[1]
    repo_timeStamp = pushed_date+hour+minute
    # Ex) 2022-04-07T23:09:37Z ==> 2022-04-072309
    return repo_timeStamp

while True:
    try:
        # Get information from Github API
        res1 = requests.get(url1, headers={"Authorization": "token "+token})
        res2 = requests.get(url2, headers={"Authorization": "token "+token})
        res3 = requests.get(url3, headers={"Authorization": "token "+token})

        python_result = res1.json()
        java_result = res2.json()
        csharp_result = res3.json()

        # Data cleaning
            
        for i in python_result["items"]:

            # Extract pushed time without second information
            data = "PythonPushedTime,"+calculateTime(i["pushed_at"])+"\n"
            print(data)
            conn.send(data.encode())

            # Extract information of repository that is not duplicated
            if i["full_name"] not in pythonRepo:
                pythonRepo[i["full_name"]] = int(i["stargazers_count"])
                data = "Python\n"
                print(data)
                conn.send(data.encode())
                data = "PythonStar,"+str(i["stargazers_count"])+"\n"
                print(data)
                conn.send(data.encode())
                if i["description"] is not None:
                    description = i["description"]
                    words = re.sub('[^a-zA-Z ]', '', description)
                    word_li = words.split(" ")
                    for j in word_li:
                        if j != "":
                            data = "PythonWord,"+j+"\n"
                            print(data)
                            conn.send(data.encode())
            else:
                # Update star count if it's changed
                if int(pythonRepo[i["full_name"]]) != int(i["stargazers_count"]):
                    oldStarCount = int(pythonRepo[i["full_name"]]) * (-1)
                    oldData = "PythonStar," + str(oldStarCount) + "\n"
                    print(oldData)
                    conn.send(oldData.encode())
                    data = "PythonStar," + str(i["stargazers_count"]) + "\n"
                    print(data)
                    conn.send(data.encode())

        for i in java_result["items"]:
            data = "JavaPushedTime,"+calculateTime(i["pushed_at"])+"\n"
            print(data)
            conn.send(data.encode())
            if i["full_name"] not in javaRepo:
                javaRepo[i["full_name"]] = int(i["stargazers_count"])
                data = "Java\n"
                print(data)
                conn.send(data.encode())
                data = "JavaStar,"+str(i["stargazers_count"])+"\n"
                print(data)
                conn.send(data.encode())
                if i["description"] is not None:
                    description = i["description"]
                    words = re.sub('[^a-zA-Z ]', '', description)
                    word_li = words.split(" ")
                    for j in word_li:
                        if j != "":
                            data = "JavaWord,"+j+"\n"
                            print(data)
                            conn.send(data.encode())
            else:
                if int(javaRepo[i["full_name"]]) != int(i["stargazers_count"]):
                    oldStarCount = int(javaRepo[i["full_name"]]) * (-1)
                    oldData = "JavaStar," + str(oldStarCount) + "\n"
                    print(oldData)
                    conn.send(oldData.encode())
                    data = "JavaStar," + str(i["stargazers_count"]) + "\n"
                    print(data)
                    conn.send(data.encode())

        for i in csharp_result["items"]:
            data = "CSharpPushedTime,"+calculateTime(i["pushed_at"])+"\n"
            print(data)
            conn.send(data.encode())
            if i["full_name"] not in csharpRepo:
                csharpRepo[i["full_name"]] = int(i["stargazers_count"])
                data = "CSharp\n"
                print(data)
                conn.send(data.encode())
                data = "CSharpStar,"+str(i["stargazers_count"])+"\n"
                print(data)
                conn.send(data.encode())
                if i["description"] is not None:
                    description = i["description"]
                    words = re.sub('[^a-zA-Z ]', '', description)
                    word_li = words.split(" ")
                    for j in word_li:
                        if j != "":
                            data = "CSharpWord,"+j+"\n"
                            print(data)
                            conn.send(data.encode())
            else:
                if int(csharpRepo[i["full_name"]]) != int(i["stargazers_count"]):
                    oldStarCount = int(csharpRepo[i["full_name"]]) * (-1)
                    oldData = "CSharpStar," + str(oldStarCount) + "\n"
                    print(oldData)
                    conn.send(oldData.encode())
                    data = "CSharpStar," + str(i["stargazers_count"]) + "\n"
                    print(data)
                    conn.send(data.encode())
        time.sleep(15)
        # Send data per 15 sec

    except KeyboardInterrupt:
        s.shutdown(socket.SHUT_RD)

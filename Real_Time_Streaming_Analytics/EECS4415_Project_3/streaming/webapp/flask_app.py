
from flask import Flask, jsonify, request, render_template
from redis import Redis
import matplotlib.pyplot as plt
import json
import datetime

app = Flask(__name__)

pypushed_timeList = {}
japushed_timeList = {}
cspushed_timeList = {}
wordList=[["","",""],["","",""],["","",""],["","",""],["","",""],["","",""],["","",""],["","",""],["","",""],["","",""]]

def makeBargraph(pystarAve, jastarAve, csstarAve):
    x = [1, 2, 3]
    height = [pystarAve, jastarAve, csstarAve]
    tick_label = ['Python', 'Java', 'CSharp']
    plt.bar(x, height, tick_label=tick_label, width=0.3, color=['tab:orange', 'tab:blue', 'tab:red'])
    plt.ylabel('Average Number of Stars')
    plt.xlabel('Program Language')
    plt.title('Star Average')
    plt.savefig('/streaming/webapp/static/images/avechart.png')
    plt.clf()

@app.route('/updateData', methods=['POST'])
def updateData():
    data = request.get_json()
    r = Redis(host='redis', port=6379)
    r.set('data', json.dumps(data))
    return jsonify({'msg': 'success'})

@app.route('/updateData2', methods=['POST'])
def updateData2():
    data = request.get_json()
    r = Redis(host='redis', port=6379)
    r.set('data2', json.dumps(data))
    return jsonify({'msg': 'success'})

@app.route('/', methods=['GET'])
def index():
    r = Redis(host='redis', port=6379)
    data = r.get('data')
    data2 = r.get('data2')
    try:
        # Get data
        data = json.loads(data)
        data2 = json.loads(data2)
    except TypeError:
        # Wait until getting data
        return "waiting for data..."
    try:
        # Extract data for web application
        PythonIndex = data['Language'].index('Python')
        pyTotal = data['Count'][PythonIndex]
        JavaIndex = data['Language'].index('Java')
        javaTotal = data['Count'][JavaIndex]
        CSharpIndex = data['Language'].index('CSharp')
        csTotal = data['Count'][CSharpIndex]
        pystarAve = data['StarAverage'][PythonIndex]
        jastarAve = data['StarAverage'][JavaIndex]
        csstarAve = data['StarAverage'][CSharpIndex]
        pyPushedCount = data['PushedIn60secCount'][PythonIndex]
        jaPushedCount = data['PushedIn60secCount'][JavaIndex]
        csPushedCount = data['PushedIn60secCount'][CSharpIndex]

        # Top 10 words process
        for i in range(1,11):
            wordCountIndex = data2['index'].index(i)
            pyw = "( "+data2['PythonWordTop10'][wordCountIndex]+" )"
            jaw = "( "+data2['JavaWordTop10'][wordCountIndex]+" )"
            csw = "( "+data2['CSharpWordTop10'][wordCountIndex]+" )"
            wordList[i-1] = [pyw, jaw, csw]

        # Make bar graph with average stars information
        makeBargraph(pystarAve, jastarAve, csstarAve)

        currentUTCdate = str(datetime.datetime.utcnow()).split(" ")[1].split(".")[0]
        currentUTCtime = currentUTCdate[0:len(currentUTCdate) - 2] + "00"
        pypushed_timeList[currentUTCtime] = pyPushedCount
        japushed_timeList[currentUTCtime] = jaPushedCount
        cspushed_timeList[currentUTCtime] = csPushedCount

        # Make line graph with pushed time information
        x_timeLi = []
        for i in range(1, 5):
            tmp = str(datetime.datetime.utcnow() - datetime.timedelta(minutes=5-i)).split(" ")[1].split(".")[0]
            time = tmp[0:len(tmp) - 2] + "00"
            x_timeLi.append(time)
        x_timeLi.append(currentUTCtime)

        pyYlist = []
        jaYList = []
        csYList = []

        for i in range(0, 5):

            if x_timeLi[i] in pypushed_timeList:
                pyYlist.append(pypushed_timeList[x_timeLi[i]])
            else:
                pyYlist.append(0)

            if x_timeLi[i] in japushed_timeList:
                jaYList.append(japushed_timeList[x_timeLi[i]])
            else:
                jaYList.append(0)

            if x_timeLi[i] in cspushed_timeList:
                csYList.append(cspushed_timeList[x_timeLi[i]])
            else:
                csYList.append(0)

        plt.plot(x_timeLi, pyYlist)
        plt.plot(x_timeLi, jaYList)
        plt.plot(x_timeLi, csYList)
        plt.title('Number of pushed repositories in last 60 sec')
        plt.xticks(rotation=20)
        plt.legend(['Python', 'Java', 'CSharp'])
        plt.savefig('/streaming/webapp/static/images/pushedchart.png')
        plt.clf()

        # Send transformed data for html page
        return render_template('index.html', url='/static/images/pushedchart.png', url2='/static/images/avechart.png',
                               pyTotal=pyTotal, javaTotal=javaTotal, csTotal=csTotal,
                               pyw1=wordList[0][0], jaw1=wordList[0][1], csw1=wordList[0][2],
                               pyw2=wordList[1][0], jaw2=wordList[1][1], csw2=wordList[1][2],
                               pyw3=wordList[2][0], jaw3=wordList[2][1], csw3=wordList[2][2],
                               pyw4=wordList[3][0], jaw4=wordList[3][1], csw4=wordList[3][2],
                               pyw5=wordList[4][0], jaw5=wordList[4][1], csw5=wordList[4][2],
                               pyw6=wordList[5][0], jaw6=wordList[5][1], csw6=wordList[5][2],
                               pyw7=wordList[6][0], jaw7=wordList[6][1], csw7=wordList[6][2],
                               pyw8=wordList[7][0], jaw8=wordList[7][1], csw8=wordList[7][2],
                               pyw9=wordList[8][0], jaw9=wordList[8][1], csw9=wordList[8][2],
                               pyw10=wordList[9][0], jaw10=wordList[9][1], csw10=wordList[9][2])
    except ValueError:
        return "waiting for data..."

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
